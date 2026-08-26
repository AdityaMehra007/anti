# 🖥️ HobOS QEMU Test Matrix (Phase 14)

```powershell
# Standard Boot Command
qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1024 -nographic -kernel hobos.elf

# SMP Multicore Boot Command (4 Cores)
qemu-system-aarch64 -M virt -cpu cortex-a53 -smp 4 -m 1024 -nographic -kernel hobos.elf
```

