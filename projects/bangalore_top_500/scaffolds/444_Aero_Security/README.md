# Aero Security — Project CareerMatch-AI: Aero Security Enterprise System

## Executive Overview
- **Enterprise**: Aero Security (Rank #444 in Bangalore)
- **Sector**: EdTech, Skill Development & Future of Work
- **Corridor**: Bellandur / ORR (Cessna / Ecospace)
- **Stage**: Series D ($65M Series B)
- **Engineering Pillar**: AI Skill Verification & Algorithmic Candidate Matching
- **Tech Stack**: `Python, FastAPI, Qdrant, PostgreSQL, Next.js`
- **Target Scale KPIs**: Matches graduates to high-leverage roles with 92% interview conversion rate

---

## Strategic Thesis
Scales Aero Security's operations across Bellandur / ORR (Cessna / Ecospace) by deploying an enterprise-grade ai skill verification & algorithmic candidate matching to eliminate systemic latency, optimize margins, and achieve dominant competitive advantage.

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
