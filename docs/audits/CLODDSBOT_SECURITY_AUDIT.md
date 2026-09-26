# CloddsBot Codebase & Security Audit Report

**Audit Date**: September 12, 2026  
**Target Repository**: [`alsk1992/CloddsBot`](https://github.com/alsk1992/CloddsBot)  
**Local Staging Path**: [`external/CloddsBot`](file:///e:/anti/external/CloddsBot)  
**Auditor**: Antigravity Autonomous Security Engineer  

---

## 1. Executive Summary

CloddsBot is a multi-chain autonomous AI trading terminal supporting prediction markets (Polymarket, Kalshi, etc.), Solana DeFi, EVM DEXs, and perpetual futures. A static and architectural analysis of the codebase confirms that:
- **No Malicious Backdoors**: There are no hidden remote drainers, obfuscated key-stealing payloads, or suspicious unauthorized exfiltration endpoints. Outbound traffic is restricted to user-configured APIs (Anthropic, RPC endpoints, and public exchange APIs).
- **Modern Encryption for Credentials**: Secrets are encrypted at rest using `AES-256-GCM` with `scrypt` key derivation and random salts/IVs (`src/credentials/index.ts`).
- **Comprehensive Pre-Trade Risk Controls**: Trade execution is strictly guarded by a unified risk engine (`src/risk/engine.ts`) enforcing circuit breakers, daily loss limits, Kelly sizing, and global kill switches.
- **Platform Consideration**: The package `@drift-labs/sdk` references `helius-laserstream`, which targets `darwin` and `linux`. Windows users require `--force` or platform override flags during npm installation.

---

## 2. Secrets & Key Management Audit

### 2.1 Encryption at Rest (`src/credentials/index.ts`)
- **Algorithm**: `AES-256-GCM` (Version `v2` payload with 16-byte random salt, 12-byte IV, and 16-byte authentication tag).
- **Key Derivation**: `crypto.scryptSync(encKey, salt, 32)`.
- **Environment Key**: `CLODDS_CREDENTIAL_KEY`. If unset, attempts to encrypt credentials throw an error rather than falling back to an unencrypted or static key.
- **Isolation**: Tools and AI agents receive a constrained `TradingContext` rather than raw private keys, preventing accidental prompt injection leaks into LLM outputs.

### 2.2 Memory Hygiene & Hot Wallets
- **Finding**: Private keys (`SOLANA_PRIVATE_KEY`, EVM keys) are decrypted at runtime to sign transactions. While typical for non-custodial trading bots, operators should use dedicated sub-wallets with strictly limited balances rather than master treasury accounts.
- **Recommendation**:
  1. Never configure production primary wallets with significant reserves.
  2. Implement hardware signer support or MPC for high-value operations.

---

## 3. Network Communication & Outbound Telemetry Audit

### 3.1 Domain Whitelist & Telemetry Check
- **Grep Pattern Analyzed**: All instances of `cloddsbot.com`, `http://`, and `https://` across `src/`.
- **Findings**:
  - `compute.cloddsbot.com`: Listed in `src/gateway/server.ts` host redirection whitelist (safe).
  - `cloddsbot.com/logo.png`: Referenced as static asset image in WebChat UI (safe).
  - No background analytics or telemetry pingbacks were found collecting user IPs or keystrokes.
  - LLM calls strictly route to the provider configured in `DEFAULT_CONFIG` / `.env` (`@anthropic-ai/sdk`, OpenAI, Ollama, etc.).

---

## 4. Pre-Trade Risk Engine & Execution Safety

### 4.1 Unified Risk Engine (`src/risk/engine.ts`)
Every trade must pass ten distinct validation gates before dispatching to an exchange adapter:
1. **Kill Switch Check**: Instantly blocks all execution if manual or automated emergency stop is triggered (`src/trading/safety.ts`).
2. **Circuit Breaker**: Trips on volatility spikes, consecutive trade failures, or liquidity collapses (`src/risk/circuit-breaker.ts`).
3. **Max Order Size**: Enforces hard caps in USD notional value per trade.
4. **Exposure Limits**: Prevents concentration beyond a defined percentage of portfolio value.
5. **Daily Loss Limit**: Halts trading if daily realized or unrealized losses exceed predefined thresholds.
6. **Max Drawdown Protection**: Halts trading if the portfolio drops beyond maximum allowed drawdown from peak value.
7. **Concentration Limits**: Limits simultaneous exposure to identical outcomes.
8. **Value-at-Risk (VaR)**: Checks 95% and 99% parametric/historical VaR limits (`src/risk/var.ts`).
9. **Volatility Regime Adjustment**: Scales down position sizes in high-volatility environments (`src/risk/volatility.ts`).
10. **Kelly Criterion Sizing**: Suggests fractional Kelly sizing (half/quarter Kelly) calibrated by confidence scores (`src/trading/kelly.ts`).

### 4.2 Dry-Run Default Configuration
- In `src/config/index.ts`, safety-critical flags default to dry-run or disabled:
  ```typescript
  signalRouter: { enabled: false, dryRun: true },
  mlPipeline: { enabled: false },
  bittensor: { enabled: false },
  feeds: { drift: { enabled: false }, news: { enabled: false } }
  ```
- Command-line handlers default to checking `process.env.DRY_RUN === 'true'`.

---

## 5. Build, Platform & Dependency Constraints

1. **Node.js Engine**: Requires Node.js $\ge$ 22.0.0. (Verified running on Node.js `v26.4.0`).
2. **Platform Dependency Note**:
   - Dependency `@drift-labs/sdk` pulls `helius-laserstream@0.1.8`, which specifies `os: ["darwin", "linux"]`.
   - On Windows, standard `npm install` halts on `EBADPLATFORM`.
   - Solution: Use `npm install --force` or patch the optional dependency tree for non-POSIX platforms.
3. **CJS / ESM Interop Fixes**:
   - The repository ships verified post-install scripts (`scripts/fix-native-bindings.js` for `bigint-buffer` and `scripts/fix-anchor-bn-export.js` for Anchor BN exports) to resolve native module loading issues.

---

## 6. Audit Verdict

| Category | Assessment | Status |
| :--- | :--- | :---: |
| **Supply Chain & Malware** | No malicious dependencies, backdoors, or token drainers found | **PASS** |
| **Secrets Protection** | AES-256-GCM encrypted database storage with scrypt KDF | **PASS** |
| **Risk Guards** | 10-point pre-trade validation with hard loss limits and circuit breakers | **PASS** |
| **Network Safety** | No unauthorized telemetry; strictly explicit endpoints | **PASS** |
| **Cross-Platform Readiness** | Requires platform flag bypass on Windows due to Drift SDK helper | **PASS WITH NOTE** |

**Conclusion**: The repository is safe for local staging, development, and dry-run execution. Operators must adhere to standard crypto security hygiene by using dedicated paper-trading or low-balance test wallets.
