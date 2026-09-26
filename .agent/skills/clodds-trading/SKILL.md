---
name: clodds-trading
description: Autonomous operation, market scanning, dry-run simulation, and risk analysis using the CloddsBot trading engine across Polymarket, Kalshi, Solana DEXs, and perpetual futures.
metadata:
  origin: Antigravity
---

# Clodds Trading Terminal & Market Intelligence Skill

Use this skill when interacting with the CloddsBot autonomous trading framework staged at [`external/CloddsBot`](file:///e:/anti/external/CloddsBot).

## Operational Safety Principles

1. **Mandatory Dry-Run Mode**:
   Always ensure `DRY_RUN=true` or use `--dry-run` flag unless the user explicitly provides signed execution orders and live wallet credentials.
2. **Never Log Secrets**:
   Private keys, API secrets, and seed phrases must never be printed to stdout, logged to files, or stored in git.
3. **Pre-Trade Risk Verification**:
   All trade candidates must be validated against the Unified Risk Engine (`src/risk/engine.ts`) — checking VaR, concentration limits, daily loss limits, and Kelly sizing.

---

## Core Capabilities & Commands

### 1. Fast-Round Prediction Market Discovery (Polymarket)
Polymarket BTC/ETH/SOL 5m/15m/1h binary options are indexed by round slots:
```typescript
import { createMarketScanner } from 'external/CloddsBot/src/strategies/crypto-hft/market-scanner.js';

const scanner = createMarketScanner({
  assets: ['BTC', 'ETH', 'SOL'],
  roundDurationSec: 900, // 15-min rounds
  minRoundAgeSec: 60,
  minTimeLeftSec: 60,
});

const markets = await scanner.refresh();
```

### 2. Arbitrage Detection Engine
Scan for pricing discrepancies across Polymarket, Kalshi, Manifold, and Drift:
- Spread calculation: $P_{\text{sell}} - P_{\text{buy}}$
- Kelly position sizing: $\frac{p - q}{1 - q} \times \text{Confidence} \times 0.25$

### 3. CLI Invocations
From `external/CloddsBot`:
```bash
# Check system diagnostics & dependencies
npx tsx src/cli/index.ts doctor

# Start local gateway in dry-run mode
DRY_RUN=true npx tsx src/index.ts

# Inspect trade ledger statistics
npx tsx src/cli/index.ts ledger stats
```

---

## Architecture References
- Audit: [`docs/audits/CLODDSBOT_SECURITY_AUDIT.md`](file:///e:/anti/docs/audits/CLODDSBOT_SECURITY_AUDIT.md)
- Strategy Specs: [`docs/architecture/CLODDSBOT_STRATEGY_EXTRACTION.md`](file:///e:/anti/docs/architecture/CLODDSBOT_STRATEGY_EXTRACTION.md)
