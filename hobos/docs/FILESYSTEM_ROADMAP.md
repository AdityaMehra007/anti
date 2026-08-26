# 📁 HobOS Filesystem Roadmap (Phase 10)

## VFS Layer
- Supports standard POSIX operations: `open()`, `close()`, `read()`, `write()`, `lookup()`.
- File Descriptor table per process (0=stdin, 1=stdout, 2=stderr, 3..31=files).

## Implementation Progression
1. **Stage 1 (Current)**: In-Memory RamFS for static files and MOTD.
2. **Stage 2 (Short-Term)**: InitRAMFS CPIO archive loading.
3. **Stage 3 (Long-Term)**: VirtIO-Block driver with ext2 filesystem.

