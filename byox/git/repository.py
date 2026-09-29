"""
Git Repository Layout, Object Storage, and Reference Resolution.
"""

import os
from typing import Optional, Tuple
from byox.git.objects import GitObject

class Repository:
    def __init__(self, worktree: str = "."):
        self.worktree = os.path.abspath(worktree)
        self.gitdir = os.path.join(self.worktree, ".git")

    @classmethod
    def find(cls, path: str = ".") -> "Repository":
        current = os.path.abspath(path)
        while True:
            candidate = os.path.join(current, ".git")
            if os.path.isdir(candidate):
                return cls(current)
            parent = os.path.dirname(current)
            if parent == current:
                raise FileNotFoundError(f"Not a git repository (or any of the parent directories): {path}")
            current = parent

    def init(self) -> str:
        os.makedirs(os.path.join(self.gitdir, "objects"), exist_ok=True)
        os.makedirs(os.path.join(self.gitdir, "refs", "heads"), exist_ok=True)
        head_path = os.path.join(self.gitdir, "HEAD")
        if not os.path.exists(head_path):
            with open(head_path, "w", encoding="utf-8") as f:
                f.write("ref: refs/heads/main\n")
        return self.gitdir

    def object_path(self, sha: str) -> str:
        sha = sha.lower()
        return os.path.join(self.gitdir, "objects", sha[:2], sha[2:])

    def write_object(self, obj: GitObject) -> str:
        sha, _ = obj.compute_hash_and_payload()
        compressed = obj.compress()
        path = self.object_path(sha)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(compressed)
        return sha

    def read_object(self, sha: str) -> GitObject:
        path = self.object_path(sha)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Git object not found: {sha}")
        with open(path, "rb") as f:
            compressed = f.read()
        _, obj = GitObject.decompress_and_parse(compressed)
        return obj

    def resolve_ref(self, ref_name: str = "HEAD") -> Optional[str]:
        ref_file = os.path.join(self.gitdir, ref_name)
        if not os.path.exists(ref_file):
            return None
        with open(ref_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content.startswith("ref: "):
            target = content[5:].strip()
            return self.resolve_ref(target)
        return content if len(content) == 40 else None

    def get_current_branch(self) -> Optional[str]:
        head_file = os.path.join(self.gitdir, "HEAD")
        if not os.path.exists(head_file):
            return None
        with open(head_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content.startswith("ref: refs/heads/"):
            return content[16:].strip()
        return None

    def update_ref(self, ref_name: str, sha: str):
        head_file = os.path.join(self.gitdir, "HEAD")
        target_file = os.path.join(self.gitdir, ref_name)
        if ref_name == "HEAD" and os.path.exists(head_file):
            with open(head_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content.startswith("ref: "):
                target_file = os.path.join(self.gitdir, content[5:].strip())

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(sha + "\n")
