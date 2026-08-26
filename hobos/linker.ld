/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * linker.ld - Linker script for QEMU virt board (RAM at 0x40000000)
 */

ENTRY(_start)

SECTIONS
{
    /* QEMU virt loads kernel image at 0x40080000 */
    . = 0x40080000;

    .text.boot : {
        *(.text.boot)
    }

    . = ALIGN(4096);
    .text : {
        *(.text*)
    }

    . = ALIGN(4096);
    .rodata : {
        *(.rodata*)
    }

    . = ALIGN(4096);
    .data : {
        *(.data*)
    }

    . = ALIGN(4096);
    __bss_start = .;
    .bss : {
        *(.bss.boot)
        *(.bss*)
        *(COMMON)
    }
    . = ALIGN(4096);
    __bss_end = .;

    _kernel_end = .;
}
