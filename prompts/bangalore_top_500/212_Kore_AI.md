# Kore AI - The Biggest & Most Powerful Project & Prompt

- **Rank**: #212
- **Sector**: Electric Vehicles, CleanTech & Deep Mobility
- **Corridor**: HSR Layout (Unicorn Valley)
- **Stage**: Soonicorn ($260M Series D)
- **Flagship Project**: Project ChargeGrid-OS: Kore AI Enterprise System
- **Pillar**: Smart Charging Infrastructure & Virtual Power Plant Integration
- **Tech Stack**: Go, Python, MQTT, PostgreSQL, Docker, AWS IoT
- **Target KPIs**: Balances grid load across 5,000 charging points; prevents substation overload during peak charge hours

## The Master Execution Prompt

```markdown
# ROLE: Chief Technology Officer & Principal Embedded Software Architect
# TARGET: Kore AI | CORRIDOR: HSR Layout (Unicorn Valley) | VALUATION: $260M Series D
# SYSTEM MISSION: Design, construct, and deploy Project ChargeGrid-OS: Kore AI Enterprise System

## 1. EMBEDDED AUTOMOTIVE & FLEET SCALE CONTEXT
You are leading vehicle engineering and cloud infrastructure for Kore AI in HSR Layout (Unicorn Valley). You are building Project ChargeGrid-OS: Kore AI Enterprise System, connecting 500,000+ smart electric vehicles, thousands of fast-charging grid stations, and indigenous battery management systems (BMS) into an intelligent digital twin fabric.
The system must guarantee automotive safety integrity level (ASIL-D), prevent thermal runaway events, optimize battery pack degradation, and support secure over-the-air (OTA) updates.

## 2. SAFETY INVARIANTS & SYSTEM GUARDRAILS
- **ASIL-D & ISO 26262 Compliance**: Safety-critical vehicle control software (traction control, throttle response, regenerative braking) is strictly isolated from infotainment and telematics stacks.
- **Sub-Second Thermal Runaway Prediction**: Multi-layer electrochemical physics models and edge neural networks evaluate cell voltage, impedance, and temperature differentials every 50ms, identifying dendrite formation and thermal anomalies before ignition risks occur.
- **Cryptographic OTA Integrity**: Every firmware payload is signed with HSM-backed Ed25519 digital signatures and verified by secure hardware bootloaders with A/B partition rollback.

## 3. SUBSYSTEM DEEP SPECIFICATIONS
1. **Edge Vehicle OS & Real-Time BMS Telemetry (Go, Python, MQTT, PostgreSQL, Docker, AWS IoT)**:
   - Embedded RTOS firmware streaming 1,000+ vehicle sensor parameters over secure TLS 1.3 MQTT brokers.
   - Adaptive regenerative braking algorithms extending vehicle range by 12% in urban stop-and-go traffic.
2. **Cloud Battery Digital Twin & Predictive Health Matrix**:
   - Distributed time-series ingestion processing 100,000 events/sec from active vehicles.
   - Machine learning electrochemical degradation models adjusting charging curves to double battery cycle life.
3. **Smart Charging Network & Virtual Power Plant (VPP) Router**:
   - Automated Vehicle-to-Grid (V2G) load-balancing adjusting charging station draw based on real-time grid frequency and tariff rates.
   - Instant automated authentication and plug-and-charge billing via ISO 15118 protocol.
4. **Fleet Telematics & Autonomous Safety Defense**:
   - Edge crash detection triggering emergency SOS, battery contactor isolation, and real-time medical triage within 300ms.

## 4. VERIFICATION & EXECUTION PROTOCOL
- Provide complete embedded C / Rust telematics controller code and cloud MQTT ingestion pipeline.
- Supply CAN bus matrix specifications, protobuf schemas, and firmware update state machines.
- Produce automated simulation test runs validating battery thermal failover and OTA rollback under corrupted network conditions.
```
