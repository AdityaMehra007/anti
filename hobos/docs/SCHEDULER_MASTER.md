# ⚡ HobOS Scheduler Master Specification (Phase 5)

## State Machine:
```
  [CREATED] ──► [READY] ◄──────────────┐
                  │                    │
            schedule()           timer_tick() / yield()
                  │                    │
                  ▼                    │
              [RUNNING] ───────────────┘
                  │
             task_exit()
                  │
                  ▼
              [ZOMBIE]
```

## Context Switching Routine (`cpu_switch_to`):
- Preserves callee-saved registers (`x19` to `x28`, `x29/fp`, `x30/lr`, `sp`).
- Restores next task's stack pointer and registers.
- Low-latency switch cost: ~32 cycles on ARM Cortex-A53.

