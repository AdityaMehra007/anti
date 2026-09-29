"""
Paged B-Tree Storage Architecture: Fixed Page Size, Binary Serialization, and Page Manager.
"""

import os
import json
import struct
from typing import Optional, Dict, Any, List

PAGE_SIZE = 4096
MAGIC_HEADER = b"BYOXSQL1"  # 8 bytes

class PagedStorage:
    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath
        self._file = None
        self._memory_pages: Dict[int, bytearray] = {}
        self.catalog: Dict[str, Any] = {}

        if self.filepath:
            mode = "r+b" if os.path.exists(self.filepath) else "w+b"
            self._file = open(self.filepath, mode)
            if mode == "w+b" or os.path.getsize(self.filepath) == 0:
                self._init_disk_storage()
            else:
                self._load_disk_storage()
        else:
            self._init_memory_storage()

    def _init_disk_storage(self):
        page0 = bytearray(PAGE_SIZE)
        page0[:8] = MAGIC_HEADER
        self.catalog = {"tables": {}}
        meta_bytes = json.dumps(self.catalog).encode("utf-8")
        struct.pack_into(">H", page0, 8, len(meta_bytes))
        page0[10 : 10 + len(meta_bytes)] = meta_bytes
        self._file.seek(0)
        self._file.write(page0)
        self._file.flush()

    def _load_disk_storage(self):
        self._file.seek(0)
        page0 = self._file.read(PAGE_SIZE)
        if page0[:8] != MAGIC_HEADER:
            raise ValueError("Corrupt or invalid BYOX database file")
        meta_len = struct.unpack_from(">H", page0, 8)[0]
        meta_bytes = page0[10 : 10 + meta_len]
        self.catalog = json.loads(meta_bytes.decode("utf-8"))

    def _init_memory_storage(self):
        page0 = bytearray(PAGE_SIZE)
        page0[:8] = MAGIC_HEADER
        self.catalog = {"tables": {}}
        self._memory_pages[0] = page0

    def sync_catalog(self):
        meta_bytes = json.dumps(self.catalog).encode("utf-8")
        if self._file:
            self._file.seek(0)
            page0 = bytearray(self._file.read(PAGE_SIZE))
            struct.pack_into(">H", page0, 8, len(meta_bytes))
            page0[10 : 10 + len(meta_bytes)] = meta_bytes
            self._file.seek(0)
            self._file.write(page0)
            self._file.flush()
        else:
            page0 = self._memory_pages[0]
            struct.pack_into(">H", page0, 8, len(meta_bytes))
            page0[10 : 10 + len(meta_bytes)] = meta_bytes

    def read_page(self, page_id: int) -> bytearray:
        if self._file:
            self._file.seek(page_id * PAGE_SIZE)
            data = self._file.read(PAGE_SIZE)
            if len(data) < PAGE_SIZE:
                data = data + b"\x00" * (PAGE_SIZE - len(data))
            return bytearray(data)
        else:
            return self._memory_pages.setdefault(page_id, bytearray(PAGE_SIZE))

    def write_page(self, page_id: int, page_data: bytearray):
        if len(page_data) != PAGE_SIZE:
            raise ValueError(f"Page data size must be {PAGE_SIZE}")
        if self._file:
            self._file.seek(page_id * PAGE_SIZE)
            self._file.write(page_data)
            self._file.flush()
        else:
            self._memory_pages[page_id] = page_data

    def allocate_page(self) -> int:
        if self._file:
            self._file.seek(0, os.SEEK_END)
            size = self._file.tell()
            new_page_id = size // PAGE_SIZE
            empty_page = bytearray(PAGE_SIZE)
            self._file.write(empty_page)
            self._file.flush()
            return new_page_id
        else:
            new_page_id = len(self._memory_pages)
            self._memory_pages[new_page_id] = bytearray(PAGE_SIZE)
            return new_page_id

    def close(self):
        if self._file:
            self._file.flush()
            self._file.close()
            self._file = None
