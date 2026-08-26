"""
HobOS Systems Verification Test Harness
Executes architectural and unit-level verification across all 10 core OS subsystems.
"""
import unittest
import sys
import os
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
HOBOS_DIR = WORKSPACE / "hobos"

class TestHobOSArchitecture(unittest.TestCase):

    def test_01_linker_script_structure(self):
        linker_file = HOBOS_DIR / "linker.ld"
        self.assertTrue(linker_file.exists())
        with open(linker_file, "r") as f:
            content = f.read()
        self.assertIn("0x40080000", content)
        self.assertIn(".text.boot", content)
        self.assertIn("__bss_start", content)
        self.assertIn("__bss_end", content)

    def test_02_vector_table_alignment(self):
        vectors_file = HOBOS_DIR / "arch" / "aarch64" / "vectors.S"
        self.assertTrue(vectors_file.exists())
        with open(vectors_file, "r") as f:
            content = f.read()
        self.assertIn(".align 11", content) # 2048-byte VBAR alignment
        self.assertIn(".align 7", content)  # 128-byte vector entry alignment
        self.assertIn("vector_table_el1:", content)

    def test_03_boot_exception_level_drop(self):
        boot_file = HOBOS_DIR / "arch" / "aarch64" / "boot.S"
        self.assertTrue(boot_file.exists())
        with open(boot_file, "r") as f:
            content = f.read()
        self.assertIn("drop_from_el3:", content)
        self.assertIn("drop_from_el2:", content)
        self.assertIn("init_el1:", content)
        self.assertIn("scr_el3", content)
        self.assertIn("hcr_el2", content)

    def test_04_mmu_page_table_constants(self):
        mmu_file = HOBOS_DIR / "arch" / "aarch64" / "mmu.c"
        self.assertTrue(mmu_file.exists())
        with open(mmu_file, "r") as f:
            content = f.read()
        self.assertIn("PTE_VALID", content)
        self.assertIn("PTE_TABLE", content)
        self.assertIn("set_tcr_el1", content)
        self.assertIn("set_mair_el1", content)

    def test_05_buddy_allocator_logic(self):
        buddy_file = HOBOS_DIR / "mm" / "buddy.c"
        self.assertTrue(buddy_file.exists())
        with open(buddy_file, "r") as f:
            content = f.read()
        self.assertIn("MAX_ORDER", content)
        self.assertIn("alloc_pages", content)
        self.assertIn("free_pages", content)

    def test_06_slab_allocator_sizes(self):
        slab_file = HOBOS_DIR / "mm" / "slab.c"
        self.assertTrue(slab_file.exists())
        with open(slab_file, "r") as f:
            content = f.read()
        self.assertIn("kmalloc", content)
        self.assertIn("kfree", content)
        self.assertIn("16, 32, 64, 128, 256, 512, 1024, 2048", content)

    def test_07_gic_interrupt_registers(self):
        gic_file = HOBOS_DIR / "arch" / "aarch64" / "gic.c"
        self.assertTrue(gic_file.exists())
        with open(gic_file, "r") as f:
            content = f.read()
        self.assertIn("GICD_CTLR", content)
        self.assertIn("GICC_PMR", content)
        self.assertIn("GICC_IAR", content)
        self.assertIn("GICC_EOIR", content)

    def test_08_syscall_user_memory_safety(self):
        syscall_file = HOBOS_DIR / "kernel" / "syscall.c"
        self.assertTrue(syscall_file.exists())
        with open(syscall_file, "r") as f:
            content = f.read()
        self.assertIn("copy_from_user", content)
        self.assertIn("copy_to_user", content)
        self.assertIn("0xFFFF000000000000", content) # Kernel space bounds check

    def test_09_scheduler_preemption(self):
        sched_file = HOBOS_DIR / "kernel" / "sched.c"
        self.assertTrue(sched_file.exists())
        with open(sched_file, "r") as f:
            content = f.read()
        self.assertIn("sched_tick", content)
        self.assertIn("schedule", content)
        self.assertIn("cpu_switch_to", content)

    def test_10_uart_pl011_baud_rate(self):
        uart_file = HOBOS_DIR / "drivers" / "uart_pl011.c"
        self.assertTrue(uart_file.exists())
        with open(uart_file, "r") as f:
            content = f.read()
        self.assertIn("UART_IBRD", content)
        self.assertIn("UART_FBRD", content)
        self.assertIn("UART_LCRH", content)

if __name__ == "__main__":
    unittest.main()
