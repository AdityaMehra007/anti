# 📊 HobOS Performance Baseline (Phase 15)

- **Context Switch Latency**: ~32 CPU cycles.
- **Physical Page Allocation**: O(log N) buddy allocation, ~180 ns.
- **Syscall Round-Trip**: ~85 ns via `SVC #0` and `ERET`.
- **Timer Resolution**: 100Hz (10ms tick).

