"""
Git Object Model: Blobs, Trees, and Commits with SHA-1 and zlib compression.
"""

import hashlib
import zlib
import time
from typing import List, Optional, Tuple

class GitObject:
    fmt: bytes = b""

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, data: bytes):
        raise NotImplementedError

    def compute_hash_and_payload(self) -> Tuple[str, bytes]:
        payload = self.serialize()
        header = f"{self.fmt.decode('ascii')} {len(payload)}\x00".encode("ascii")
        full_store = header + payload
        sha = hashlib.sha1(full_store).hexdigest()
        return sha, full_store

    def compress(self) -> bytes:
        _, full_store = self.compute_hash_and_payload()
        return zlib.compress(full_store)

    @classmethod
    def decompress_and_parse(cls, compressed_data: bytes) -> Tuple[str, "GitObject"]:
        raw = zlib.decompress(compressed_data)
        null_idx = raw.find(b"\x00")
        if null_idx == -1:
            raise ValueError("Malformed git object: missing null byte header")
        header = raw[:null_idx].decode("ascii")
        fmt, size_str = header.split(" ")
        data = raw[null_idx + 1 :]
        if len(data) != int(size_str):
            raise ValueError("Size mismatch in git object")

        if fmt == "blob":
            obj = Blob()
        elif fmt == "tree":
            obj = Tree()
        elif fmt == "commit":
            obj = Commit()
        else:
            raise ValueError(f"Unknown git object type: {fmt}")

        obj.deserialize(data)
        return fmt, obj


class Blob(GitObject):
    fmt = b"blob"

    def __init__(self, data: bytes = b""):
        self.data = data

    def serialize(self) -> bytes:
        return self.data

    def deserialize(self, data: bytes):
        self.data = data


class TreeEntry:
    def __init__(self, mode: str, name: str, sha: str):
        self.mode = mode
        self.name = name
        self.sha = sha.lower()

    def serialize(self) -> bytes:
        return f"{self.mode} {self.name}\x00".encode("utf-8") + bytes.fromhex(self.sha)


class Tree(GitObject):
    fmt = b"tree"

    def __init__(self, entries: Optional[List[TreeEntry]] = None):
        self.entries: List[TreeEntry] = entries or []

    def serialize(self) -> bytes:
        # Standard git sorts tree entries by name (directories sorted with trailing slash)
        self.entries.sort(key=lambda e: e.name + ("/" if e.mode.startswith("040000") or e.mode == "40000" else ""))
        return b"".join(entry.serialize() for entry in self.entries)

    def deserialize(self, data: bytes):
        self.entries = []
        idx = 0
        length = len(data)
        while idx < length:
            space_idx = data.find(b" ", idx)
            if space_idx == -1:
                break
            mode = data[idx:space_idx].decode("ascii")
            null_idx = data.find(b"\x00", space_idx)
            if null_idx == -1:
                break
            name = data[space_idx + 1 : null_idx].decode("utf-8")
            raw_sha = data[null_idx + 1 : null_idx + 21]
            sha = raw_sha.hex()
            self.entries.append(TreeEntry(mode=mode, name=name, sha=sha))
            idx = null_idx + 21


class Commit(GitObject):
    fmt = b"commit"

    def __init__(
        self,
        tree_sha: str = "",
        parents: Optional[List[str]] = None,
        author: str = "BYOX Developer <developer@byox.org>",
        author_time: Optional[int] = None,
        committer: Optional[str] = None,
        committer_time: Optional[int] = None,
        tz: str = "+0000",
        message: str = "",
    ):
        self.tree_sha = tree_sha
        self.parents = parents or []
        self.author = author
        self.author_time = int(time.time()) if author_time is None else author_time
        self.committer = committer or author
        self.committer_time = self.author_time if committer_time is None else committer_time
        self.tz = tz
        self.message = message.strip()

    def serialize(self) -> bytes:
        lines = [f"tree {self.tree_sha}"]
        for p in self.parents:
            lines.append(f"parent {p}")
        lines.append(f"author {self.author} {self.author_time} {self.tz}")
        lines.append(f"committer {self.committer} {self.committer_time} {self.tz}")
        lines.append("")
        lines.append(self.message + "\n")
        return "\n".join(lines).encode("utf-8")

    def deserialize(self, data: bytes):
        text = data.decode("utf-8")
        lines = text.split("\n")
        self.parents = []
        msg_lines = []
        in_message = False

        for line in lines:
            if in_message:
                msg_lines.append(line)
            elif line.startswith("tree "):
                self.tree_sha = line[5:].strip()
            elif line.startswith("parent "):
                self.parents.append(line[7:].strip())
            elif line.startswith("author "):
                parts = line[7:].rsplit(" ", 2)
                if len(parts) == 3:
                    self.author, ts, self.tz = parts
                    self.author_time = int(ts)
                else:
                    self.author = line[7:]
            elif line.startswith("committer "):
                parts = line[10:].rsplit(" ", 2)
                if len(parts) == 3:
                    self.committer, ts, _ = parts
                    self.committer_time = int(ts)
                else:
                    self.committer = line[10:]
            elif line == "":
                in_message = True

        self.message = "\n".join(msg_lines).strip()
