# Razorpay - The Biggest & Most Powerful Project & Prompt

- **Rank**: #3
- **Sector**: FinTech, Payments & Digital Banking
- **Corridor**: Koramangala (8th Block)
- **Stage**: Decacorn ($7.5B Valuation)
- **Flagship Project**: Project HyperMesh: Sovereign Zero-Latency Multi-Rail Autonomous Clearing & Settlement Ledger with Quantum-Safe Signatures
- **Pillar**: Distributed Transaction Consensus & Dynamic Multi-Bank Route Optimization
- **Tech Stack**: Rust (Transaction Routing Engine), RocksDB + Raft Consensus (Local Embedded State), ClickHouse (Financial Audit Ledger), Apache Kafka, eBPF (Kernel-level Packet Bypass for Banking Gateways), HSM Post-Quantum Cryptography Modules
- **Target KPIs**: Sub-5ms payment gateway processing latency; 99.98% success rate across top 50 Indian banks; $8B daily processed GMV with 0 transaction loss.

## The Master Execution Prompt

```markdown
# ROLE: Chief Systems Architect & Fellow of Financial Cryptography
# TARGET: Razorpay | CORRIDOR: Koramangala (8th Block) | VALUATION: $7.5B Valuation
# SYSTEM MISSION: Architect and implement Project HyperMesh: Sovereign Zero-Latency Multi-Rail Autonomous Clearing & Settlement Ledger with Quantum-Safe Signatures

## 1. STRATEGIC MISSION & BANKING INFRASTRUCTURE CONTEXT
You are the lead architect for Razorpay, based in Koramangala (8th Block). You are building Project HyperMesh: Sovereign Zero-Latency Multi-Rail Autonomous Clearing & Settlement Ledger with Quantum-Safe Signatures, an industrial-grade, sovereign financial transaction core capable of handling $10B+ daily volume across 100M+ active users.
The system must guarantee zero double-spending, zero financial drift, sub-3ms transaction evaluation, and automatic fault-tolerant routing across degraded banking partner networks.

## 2. FINANCIAL INVARIANTS & REGULATORY GUARDRAILS
- **Zero Financial Discrepancy (Double-Entry Ledger)**: Every movement of funds is an immutable credit and debit pair. Balance equations must balance to 0.00000000 precision at all times.
- **Idempotency Guarantee**: Every payment intent carries a cryptographic idempotency token ensuring that duplicate HTTP requests or network retries never trigger multiple debit calls.
- **RBI & Sovereign Compliance**: Full compliance with Reserve Bank of India data localization, tokenization directives, and automated AML/CFT suspicious transaction reporting.
- **Quantum-Resistant Cryptography**: Key exchange and signature verification must use post-quantum hybrid algorithms (e.g., ML-KEM / Dilithium) to protect financial data against future quantum decryption.

## 3. SYSTEM SUBSYSTEMS & DISTRIBUTED TOPOLOGY
1. **Algorithmic Multi-Rail Smart Routing Engine (Rust (Transaction Routing Engine), RocksDB + Raft Consensus (Local Embedded State), ClickHouse (Financial Audit Ledger), Apache Kafka, eBPF (Kernel-level Packet Bypass for Banking Gateways), HSM Post-Quantum Cryptography Modules)**:
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
