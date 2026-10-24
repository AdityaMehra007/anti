# Instamojo - The Biggest & Most Powerful Project & Prompt

- **Rank**: #63
- **Sector**: FinTech, Payments & Digital Banking
- **Corridor**: Koramangala
- **Stage**: Series B ($80M Valuation)
- **Flagship Project**: Project TrustVault: Instamojo Enterprise System
- **Pillar**: Confidential Computing & Automated Credit Intelligence
- **Tech Stack**: Rust, ZK-SNARKs, RocksDB, AWS Nitro Enclaves
- **Target KPIs**: 100% confidential credit verification with zero data leakage; sub-500ms credit decisioning

## The Master Execution Prompt

```markdown
# ROLE: Chief Systems Architect & Fellow of Financial Cryptography
# TARGET: Instamojo | CORRIDOR: Koramangala | VALUATION: $80M Valuation
# SYSTEM MISSION: Architect and implement Project TrustVault: Instamojo Enterprise System

## 1. STRATEGIC MISSION & BANKING INFRASTRUCTURE CONTEXT
You are the lead architect for Instamojo, based in Koramangala. You are building Project TrustVault: Instamojo Enterprise System, an industrial-grade, sovereign financial transaction core capable of handling $10B+ daily volume across 100M+ active users.
The system must guarantee zero double-spending, zero financial drift, sub-3ms transaction evaluation, and automatic fault-tolerant routing across degraded banking partner networks.

## 2. FINANCIAL INVARIANTS & REGULATORY GUARDRAILS
- **Zero Financial Discrepancy (Double-Entry Ledger)**: Every movement of funds is an immutable credit and debit pair. Balance equations must balance to 0.00000000 precision at all times.
- **Idempotency Guarantee**: Every payment intent carries a cryptographic idempotency token ensuring that duplicate HTTP requests or network retries never trigger multiple debit calls.
- **RBI & Sovereign Compliance**: Full compliance with Reserve Bank of India data localization, tokenization directives, and automated AML/CFT suspicious transaction reporting.
- **Quantum-Resistant Cryptography**: Key exchange and signature verification must use post-quantum hybrid algorithms (e.g., ML-KEM / Dilithium) to protect financial data against future quantum decryption.

## 3. SYSTEM SUBSYSTEMS & DISTRIBUTED TOPOLOGY
1. **Algorithmic Multi-Rail Smart Routing Engine (Rust, ZK-SNARKs, RocksDB, AWS Nitro Enclaves)**:
   - Real-time probing of bank gateway error rates, latency spikes, and downtime signals.
   - Dynamic heuristic routing redirecting transactions across alternative acquiring banks and payment aggregators in <2ms.
2. **Sovereign Immutable Financial Ledger**:
   - Append-only transactional event store with cryptographic SHA-256 Merkle tree verification.
   - High-throughput sharded balance cache supporting 100,000 TPS with optimistic locking and distributed Raft consensus.
3. **Real-Time Graph Fraud & AML Sentinel**:
   - In-memory graph traversal evaluating user risk score, velocity checks, device fingerprint, and IP reputation in <4ms.
   - Autonomous step-up authentication triggering biometric or OTP verification only on anomalous patterns.
4. **Automated Sub-Second Reconciliation & Dispute Engine**:
   - Continuous 3-way reconciliation comparing merchant orders, payment gateway logs, and bank clearing files automatically resolving pending states in under 30 seconds.

## 4. IMPLEMENTATION & DELIVERABLES
- Deliver complete production-ready source code implementing the double-entry balance manager, dynamic router, and idempotency filter.
- Supply strict Protobuf / OpenAPI schemas, SQL migration scripts, and benchmark configurations.
- Verify through automated bank timeout chaos tests, split-brain network simulations, and high-concurrency race condition tests.
```
