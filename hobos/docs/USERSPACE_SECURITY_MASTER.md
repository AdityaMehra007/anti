# 🛡️ HobOS Syscall & Userspace Security (Phase 8)

## Syscall ABI
- **Instruction**: `SVC #0` from EL0.
- **Syscall Number**: Passed in register `x8`.
- **Arguments**: Passed in `x0` through `x5`.
- **Return Value**: Returned in `x0` (`-1` on error).

## Pointer Sanitization (`copy_from_user` / `copy_to_user`)
- **Boundary Verification**: Checks that user pointer `uaddr < 0xFFFF000000000000ULL` and `uaddr + size >= uaddr` (prevents integer overflow into kernel space).
- **Page Fault Protection**: Accessing unmapped addresses triggers user synchronous fault and terminates offending task without crashing kernel.

