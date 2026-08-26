# HobOS Makefile for ARM64 (AArch64)

CROSS_COMPILE ?= aarch64-linux-gnu-
CC      := $(CROSS_COMPILE)gcc
AS      := $(CROSS_COMPILE)as
LD      := $(CROSS_COMPILE)ld
OBJCOPY := $(CROSS_COMPILE)objcopy

CFLAGS  := -Wall -Wextra -nostdlib -nostartfiles -ffreestanding -Iinclude -mcpu=cortex-a53 -O2 -g
LDFLAGS := -T linker.ld

ASM_SRCS := arch/aarch64/boot.S arch/aarch64/vectors.S arch/aarch64/context.S
C_SRCS   := kernel/main.c kernel/printk.c kernel/panic.c kernel/task.c kernel/sched.c kernel/syscall.c kernel/sync.c \
            arch/aarch64/mmu.c arch/aarch64/gic.c arch/aarch64/timer.c \
            mm/buddy.c mm/slab.c \
            drivers/uart_pl011.c \
            fs/vfs.c

OBJS     := $(ASM_SRCS:.S=.o) $(C_SRCS:.c=.o)

all: hobos.elf hobos.bin

%.o: %.S
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

hobos.elf: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) $(OBJS) -o $@

hobos.bin: hobos.elf
	$(OBJCOPY) -O binary $< $@

qemu: hobos.elf
	qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1024 -nographic -kernel hobos.elf

clean:
	rm -f $(OBJS) hobos.elf hobos.bin

.PHONY: all qemu clean
