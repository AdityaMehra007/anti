# Groww — Project WealthEngine: AI-Autonomous Retail Portfolio Rebalancer, Global Direct Market Access & Sovereign Multi-Asset Custody Core

## Executive Overview
- **Enterprise**: Groww (Rank #7 in Bangalore)
- **Sector**: FinTech, Payments & Digital Banking
- **Corridor**: Outer Ring Road (Marathahalli)
- **Stage**: Unicorn ($3.0B Valuation)
- **Engineering Pillar**: Automated Multi-Asset Wealth Optimization & Distributed Portfolio Ledger
- **Tech Stack**: `Go (High-Concurrency Trading Microservices), Java (Spring Boot Core Banking/Demats), Apache Cassandra (High-Write Portfolio History), Redpanda (Event Stream), ClickHouse, Kubernetes on Bare Metal`
- **Target Scale KPIs**: Real-time execution of 10M concurrent automated portfolio tax-harvesting runs; 99.995% execution reliability on NSE/BSE colocation; $25B+ assets under tracking.

---

## Strategic Thesis
Groww manages India's largest retail active client base in stock broking. WealthEngine implements an autonomous real-time quantitative portfolio rebalancer that continuously monitors tax-harvesting opportunities, ETF arbitrage, and automated SIP capital deployment for 40M+ retail portfolios simultaneously.

---

## Architectural Invariants & Non-Negotiables
1. **Zero Vibe Coding**: Strict typing, contract verification, and mathematical consistency.
2. **Linearizable State Synchronization**: Zero data loss across active-active micro-hubs.
3. **Continuous Chaos Resilience**: Automatic circuit breaking and zero-downtime failover.
4. **P99 Latency Guarantee**: Sub-5ms to sub-15ms execution envelope under peak loads.

---

## Microservices Topology
- **`ingestion-gateway`**: High-concurrency edge entrypoint terminating mTLS 1.3.
- **`core-consensus-engine`**: High-throughput distributed state machine.
- **`telemetry-sentinel`**: Real-time OpenTelemetry & forensic audit trail.

---

## Deployment & Verification
```bash
# Run local microservice simulation
python service_blueprint.py

# Launch multi-container stack
docker-compose up -d
```
