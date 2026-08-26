# 🗺️ HobOS — Master Roadmap

## LEVEL 0: Current Foundation (Completed)
- Functional AArch64 boot, EL drop, MMU page tables, Buddy + Slab allocators, GICv2, PL011 UART, Preemptive Scheduler, VFS.

## LEVEL 1: Reliability & Process Isolation (Months 1–2)
- Copy-On-Write (COW) fork mechanics.
- Kernel heap guard pages to detect stack overflow.
- Per-process separate page tables loaded into `TTBR0_EL1`.

## LEVEL 2: Persistent Storage & Filesystem (Months 3–4)
- VirtIO-Block PCI driver implementation.
- Read/Write ext2 or FAT32 filesystem support.
- Standard CPIO initramfs loader.

## LEVEL 3: Rich Userspace & Shell (Months 5–6)
- ELF64 binary dynamic / static loader.
- Interactive user command line shell with line editing.
- Standard POSIX utility toolset (`cat`, `ls`, `ps`, `kill`, `echo`).

## LEVEL 4: Networking Stack (Months 7–9)
- VirtIO-Net network card driver.
- Lightweight TCP/IP stack with BSD socket API.
