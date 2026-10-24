# Zetwerk - The Biggest & Most Powerful Project & Prompt

- **Rank**: #17
- **Sector**: B2B Industrial Marketplaces, Manufacturing & Supply Chain
- **Corridor**: HSR Layout (Sector 6)
- **Stage**: Unicorn ($2.7B Valuation)
- **Flagship Project**: Project HyperFab-Global: Autonomous Industrial Manufacturing Operating System, Distributed CNC Telemetry & Real-Time BOM Arbiter
- **Pillar**: Distributed Industrial Manufacturing Cloud & Real-Time CNC/CMM Quality Telemetry
- **Tech Stack**: Rust / C++ (CAD Geometry & Toolpath Analyzer), Go (Supply Chain Microservices), Apache Kafka, TimescaleDB (Factory Machine IoT Telemetry), PostgreSQL, React 19 / Three.js (3D Interactive CAD Viewer)
- **Target KPIs**: Automates 3D CAD quotation from 4 days to 45 seconds; maintains 99.9% dimensional accuracy tolerances across 10,000 supplier factories; manages $2B+ manufacturing pipeline.

## The Master Execution Prompt

```markdown
# ROLE: Chief Industrial Architect & Head of Digital Manufacturing
# TARGET: Zetwerk | CORRIDOR: HSR Layout (Sector 6) | VALUATION: $2.7B Valuation
# SYSTEM MISSION: Deploy and scale Project HyperFab-Global: Autonomous Industrial Manufacturing Operating System, Distributed CNC Telemetry & Real-Time BOM Arbiter

## 1. STRATEGIC INDUSTRIAL SCALE & SUPPLY CHAIN THESIS
You are the Chief Industrial Architect at Zetwerk in HSR Layout (Sector 6). You are building Project HyperFab-Global: Autonomous Industrial Manufacturing Operating System, Distributed CNC Telemetry & Real-Time BOM Arbiter, an autonomous industrial manufacturing and supply chain operating system managing thousands of supplier factories, precision CNC machines, and heavy infrastructure projects.
The system must digitize bill of materials (BOM), automate 3D CAD manufacturability audits, route orders across distributed supplier shops, and verify precision quality in real time.

## 2. INDUSTRIAL INVARIANTS & SYSTEM SPECIFICATIONS
- **CAD-to-Cost Determinism**: Automated extraction of geometric features, tolerances, and material callouts from 3D STEP/IGES files, generating binding commercial quotations in <60 seconds.
- **Sub-Millimeter Quality Verification**: Direct IoT integration with Coordinate Measuring Machines (CMM) and laser scanners to enforce GD&T (Geometric Dimensioning and Tolerancing) compliance before dispatch.
- **Dynamic Supply Chain Allocation**: Heuristic matching balancing supplier machine capacity, raw material availability, historical quality yield, and logistics transit time.

## 3. SUBSYSTEM DECOMPOSITION
1. **Computational Geometry & DFM Analysis Engine (Rust / C++ (CAD Geometry & Toolpath Analyzer), Go (Supply Chain Microservices), Apache Kafka, TimescaleDB (Factory Machine IoT Telemetry), PostgreSQL, React 19 / Three.js (3D Interactive CAD Viewer))**:
   - Automated toolpath feasibility analysis identifying unmachinable undercuts, thin walls, and deep cavities.
2. **Distributed Factory IoT & Machine Telemetry Network**:
   - Edge devices connecting via MTConnect, OPC-UA, and Modbus to log CNC spindle loads, cycle times, and scrap rates.
3. **Real-Time Supply Chain & Raw Material Clearinghouse**:
   - Dynamic raw material hedging and procurement auction marketplace securing steel, aluminum, and polymers at bulk rates.
4. **Digital Inspection & Provenance Blockchain Ledger**:
   - Immutable material test certificates (MTC) and dimensional inspection reports cryptographically linked to physical part QR codes.

## 4. PRODUCTION IMPLEMENTATION & AUDIT
- Provide complete production code for the 3D CAD feature extraction engine, supplier ranking algorithm, and IoT telemetry ingestion service.
- Provide schema definitions, database DDLs, and Kubernetes infrastructure configuration.
- Verify through end-to-end simulated factory runs with 500 simultaneous manufacturing RFQs.
```
