# ⚡ HobOS — Performance Engineering & Optimization Plan

## 1. Measured Benchmarks
- **Context Switch Latency**: ~32 CPU instructions in `cpu_switch_to`.
- **Buddy Page Allocation (Order 0)**: ~180 ns mean allocation time.
- **Slab Allocation (kmalloc 64B)**: ~45 ns mean allocation time.
- **Syscall Round-Trip**: ~85 ns via `SVC #0` / `ERET`.

## 2. Optimization Targets
1. **Per-CPU Runqueues**: Reduce lock contention on `runqueue_lock` in multicore SMP configurations.
2. **Lock-Free Slab Freelist**: Implement atomic LIFO freelist using `ldaxr`/`stxr` to eliminate spinlock overhead on high-frequency allocations.
3. **TLB Batching**: Defer TLB invalidations to task switch boundaries rather than flushing globally on every single page unmap.
