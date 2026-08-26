# 🔄 HobOS SMP & Concurrency Architecture (Phase 6)

## Multicore Architecture
- **Primary Core (Core 0)**: Executes boot sequence, memory init, driver setup.
- **Secondary Cores (Cores 1..3)**: Parked via `wfe` (Wait For Event) in `boot.S`. Woken via PSCI (Power State Coordination Interface) on multicore boot.

## Synchronization Primitives
1. **Spinlocks (`spinlock_t`)**: Implemented using AArch64 Exclusive Load/Store instructions:
   ```arm64
   1: ldaxr w0, [x1]
      cbnz  w0, 1b
      stxr  w0, w2, [x1]
      cbnz  w0, 1b
   ```
2. **Mutexes (`mutex_t`)**: Sleep locks built on top of spinlocks with voluntary scheduler yielding on contention.

