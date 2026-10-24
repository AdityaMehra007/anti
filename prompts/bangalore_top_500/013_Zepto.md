# Zepto - The Biggest & Most Powerful Project & Prompt

- **Rank**: #13
- **Sector**: Quick Commerce, FoodTech & Consumer Internet
- **Corridor**: HSR Layout & Koramangala
- **Stage**: Unicorn ($5.0B Valuation)
- **Flagship Project**: Project Chronos-10: Predictive Micro-Depot Ingestion, Computer-Vision Darkstore Automated Picking & 300-Second Dispatch Pipeline
- **Pillar**: Ultra-Fast Micro-Depot Robotics & Automated Pick-Pack-Dispatch Pipeline
- **Tech Stack**: Go (Dispatch Core), OpenCV / PyTorch (Dark-store Shelf Vision), Redis Cluster (Inventory Reservation), Redpanda, PostgreSQL with Timescale, Kubernetes Edge on Darkstore Minis
- **Target KPIs**: Average pick-and-pack time reduced to 54 seconds; 99.4% on-time delivery rate under 10 minutes; darkstore stock shrinkage reduced by 70%.

## The Master Execution Prompt

```markdown
# ROLE: Principal Software Architect & Head of Enterprise Engineering
# TARGET: Zepto | CORRIDOR: HSR Layout & Koramangala | VALUATION: $5.0B Valuation
# SYSTEM MISSION: Design, architect, and deliver Project Chronos-10: Predictive Micro-Depot Ingestion, Computer-Vision Darkstore Automated Picking & 300-Second Dispatch Pipeline

## 1. STRATEGIC MISSION & HIGH-GROWTH CONTEXT
You are the Principal Enterprise Architect for Zepto, a premier tech startup in HSR Layout & Koramangala (Quick Commerce, FoodTech & Consumer Internet). You have been tasked with building Project Chronos-10: Predictive Micro-Depot Ingestion, Computer-Vision Darkstore Automated Picking & 300-Second Dispatch Pipeline, designed to establish market leadership and unassailable technological advantage.
The project directly solves Zepto's strategic bottleneck: Zepto's unit economics require pick-and-pack times inside dark stores to drop under 90 seconds. Chronos-10 combines computer vision overhead item tracking, automated pick-path optimization on handheld terminals, and live telemetry dispatch that pairs riders before packing completes..

## 2. ARCHITECTURAL INVARIANTS & SYSTEM PRINCIPLES
- **Deep Modules & Clear Boundaries**: Simple public interfaces concealing rich, battle-tested operational capability.
- **Zero Vibe Coding**: Concrete specifications, verified types, deterministic error handling, and complete test suites.
- **High Concurrency & Fault Tolerance**: Scalable distributed architecture built on Go (Dispatch Core), OpenCV / PyTorch (Dark-store Shelf Vision), Redis Cluster (Inventory Reservation), Redpanda, PostgreSQL with Timescale, Kubernetes Edge on Darkstore Minis, achieving Average pick-and-pack time reduced to 54 seconds; 99.4% on-time delivery rate under 10 minutes; darkstore stock shrinkage reduced by 70%..
- **Enterprise-Grade Observability**: Structured logging, OpenTelemetry tracing, and automated health checks across all components.

## 3. COMPONENT SUBSYSTEM ARCHITECTURE
1. **Core Processing & Business Logic Engine**:
   - High-throughput asynchronous service layer handling domain transactions with strong consistency guarantees.
2. **Data Persistence & Cache Matrix**:
   - Optimized relational and time-series/columnar storage with sub-millisecond in-memory caching.
3. **Integration & API Gateway Layer**:
   - Secure mTLS REST, gRPC, and GraphQL endpoints with rate limiting, JWT authentication, and schema validation.
4. **Resilience, Chaos & Disaster Recovery**:
   - Circuit breakers, exponential backoff retries with jitter, and automated state reconciliation.

## 4. STEP-BY-STEP IMPLEMENTATION GUIDE
- Provide production-grade data models and interface definitions in the primary system language.
- Implement the core business logic handlers, transaction coordinators, and event publishers.
- Produce comprehensive test suites covering happy paths, edge cases, and high-concurrency race conditions.
- Specify deployment manifests (Docker, Kubernetes, Terraform) with resource limits and scaling policies.

## 5. DELIVERABLES
Deliver a complete, high-quality, production-ready architectural implementation document with clean code, schemas, and verification instructions.
```
