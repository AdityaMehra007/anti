# 🛡️ OMEGA CONTROL PLANE ARCHITECTURE
**Version:** `v26.0-SOVEREIGN`  
**Core Principle:** *Zero-Trust Partitioning between Local Execution and External Reality*  

---

## 1. Five Core Subsystems

```
┌───────────────────────────────────────────────────────────┐
│                   OMEGA CONTROL TOWER                     │
│    (Truthful UI Badges & Natural Language Query Console)  │
└──────────────┬────────────────────────────┬───────────────┘
               │                            │
┌──────────────▼─────────────┐ ┌────────────▼──────────────┐
│     OMEGA TRUTH ENGINE     │ │ IMMUTABLE TRANSACTION     │
│ (Anti-Delusion Validator)  │ │          LEDGER           │
│                            │ │ (SHA-256 State Machine)   │
└──────────────┬─────────────┘ └────────────┬──────────────┘
               │                            │
┌──────────────▼────────────────────────────▼──────────────┐
│                    MASTER DATA CORE                      │
│     (18 Normalized Entities in SQLite data/omega.db)     │
└──────────────┬────────────────────────────┬──────────────┘
               │                            │
┌──────────────▼─────────────┐ ┌────────────▼──────────────┐
│  RECONCILIATION & INCIDENT │ │     APPROVAL & GATING     │
│           ENGINE           │ │          ENGINE           │
└────────────────────────────┘ └───────────────────────────┘
```

---

## 2. Gateway States Taxonomy
1. `LOCAL`: Works purely inside the local environment.
2. `SIMULATED`: Represents external logic without external connectivity.
3. `SANDBOX`: Connected to an official test/mock environment.
4. `CONNECTED`: Authenticated connection exists; end-to-end reconciliation incomplete.
5. `LIVE`: Production credentials configured.
6. `LIVE_VERIFIED`: Real production operation executed and independently verified.
7. `FAILED` / `EXPIRED` / `REAUTH_REQUIRED` / `BLOCKED`.
