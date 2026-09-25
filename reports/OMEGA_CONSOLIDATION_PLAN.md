# ANTIGRAVITY OMEGA ULTRA — CONSOLIDATION PLAN

**Document ID:** OMEGA-CONSOLIDATE-2026-FINAL  
**Standard:** Codebase Rationalization, Directory Unification, & Architectural Pruning  

---

## 🏛️ 1. CONSOLIDATION BLUEPRINT

To ensure maximum operational focus, runtime efficiency, and zero confusion between legacy stubs and live production systems, the ecosystem will follow this consolidation mapping:

### 1. Canonical Core Unification
- **Master Platform**: `e:/anti/omnivanta/` is designated as the **Single Source of Truth** for the enterprise operating system.
- **Relational Stores**: All active relational entities reside in `e:/anti/omnivanta/data/omnivanta.db`.
- **Presentation Layer**: All user-facing web portals are consolidated into `omnivanta/applications/` and served on `http://localhost:3000/`.

### 2. Career Intelligence Unification
- Merge raw datasets from `e:/anti/linkedin_export/` directly into the `career-intelligence` tables in `omnivanta.db`.
- Archive standalone single-file career scripts into `e:/anti/archive/legacy_scripts/` once their core logic is integrated into `omnivanta/`.

### 3. Skill & Agent Catalog Harmonization
- Preserve verified skill execution markdown SOPs in `e:/anti/.agents/skills/`.
- Ensure agent definitions in `omnivanta.db` reference corresponding skill SOPs.
