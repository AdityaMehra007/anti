# 🌍 HobOS Global Benchmark & Comparison (Phase 20)

| OS Project | Architecture | Memory Management | Scheduling | Syscall Safety |
| :--- | :---: | :---: | :---: | :---: |
| **HobOS** | **ARM64 (AArch64)** | **Buddy + Slab + 4-Level MMU** | **Preemptive Priority** | **Full user-pointer sanitization** |
| **xv6-aarch64** | ARM64 | Free-list allocator | Round-robin | Basic boundary check |
| **Minix 3** | x86 / ARM | Microkernel server | Multi-level feedback | IPC message passing |
| **SerenityOS** | x86_64 | Full VMM + kmalloc | Multi-priority | POSIX syscall layer |

