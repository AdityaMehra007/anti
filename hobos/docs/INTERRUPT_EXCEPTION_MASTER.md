# 📡 HobOS Interrupt & Exception Architecture (Phase 7)

## Exception Vector Table (VBAR_EL1)
Aligned to a 2048-byte boundary (`.align 11`). 16 dedicated entries (128 bytes each, `.align 7`):

| Exception Class | Source | Vector Offset | Handler Routine |
| :--- | :--- | :---: | :--- |
| **Sync** | Current EL with SP0 | `+0x000` | `unhandled_exception` |
| **IRQ** | Current EL with SP0 | `+0x080` | `unhandled_exception` |
| **Sync** | Current EL with SPx | `+0x200` | `handle_kernel_sync_exception` |
| **IRQ** | Current EL with SPx | `+0x280` | `gic_handle_irq` (Timer/UART) |
| **Sync (SVC)** | Lower EL (AArch64 EL0)| `+0x400` | `handle_syscall` (EC=0x15) |
| **IRQ** | Lower EL (AArch64 EL0)| `+0x480` | `gic_handle_irq` |

