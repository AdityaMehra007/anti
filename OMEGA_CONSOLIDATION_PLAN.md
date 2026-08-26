# OMEGA CONSOLIDATION PLAN

1. **Retire Legacy Scripts**:
   - Move old Generation 1-2 scripts (`run_omnivanta_*.js`, `v20_*`, `v22_*`) into `E:\anti\archive\legacy_omni\`.
2. **Unify Under `omega` Namespace**:
   - All production logic is canonicalized under `E:\anti\omega\`:
     - `omega/career_war_room/`
     - `omega/model_router/`
     - `omega/engines/`
     - `omega/control_tower/`
     - `omega/data/`
3. **Single Master Database**:
   - Canonical database: `E:\anti\omega\data\omega_master.db` (18 Tables).
