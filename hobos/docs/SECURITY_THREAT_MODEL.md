# 🔒 HobOS Security Threat Model (Phase 12)

## Classified Threat Vectors
| Threat Class | Severity | Mitigation in HobOS |
| :--- | :---: | :--- |
| **Kernel Memory Disclosure** | `CRITICAL` | `copy_to_user` bounds check rejecting addresses >= 0xFFFF000000000000. |
| **Arbitrary Code Execution** | `CRITICAL` | `PTE_PXN` / `PTE_UXN` execution permission bits set in page tables. |
| **Stack Smashing** | `HIGH` | Isolated 16KB kernel stacks per task. |
| **Interrupt Starvation** | `MEDIUM` | Interrupt prioritization in GICv2 with preemption threshold. |

