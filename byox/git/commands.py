"""
Git Porcelain and Plumbing Commands.
"""

import os
from typing import List, Optional, Tuple, Dict, Any
from byox.git.objects import Blob, Tree, TreeEntry, Commit
from byox.git.repository import Repository

def cmd_init(path: str = ".") -> str:
    repo = Repository(path)
    return repo.init()

def cmd_hash_object(path_or_data: str, write: bool = True, obj_type: str = "blob") -> str:
    if os.path.exists(path_or_data):
        with open(path_or_data, "rb") as f:
            data = f.read()
    else:
        data = path_or_data.encode("utf-8") if isinstance(path_or_data, str) else path_or_data

    if obj_type == "blob":
        obj = Blob(data)
    else:
        raise ValueError(f"Unsupported object type for hash-object: {obj_type}")

    if write:
        repo = Repository.find(".")
        return repo.write_object(obj)
    else:
        sha, _ = obj.compute_hash_and_payload()
        return sha

def cmd_cat_file(sha: str) -> Tuple[str, int, bytes]:
    repo = Repository.find(".")
    obj = repo.read_object(sha)
    payload = obj.serialize()
    fmt = obj.fmt.decode("ascii")
    return fmt, len(payload), payload

def cmd_write_tree(path: str = ".") -> str:
    repo = Repository.find(path)
    root_dir = os.path.abspath(path)

    def build_tree_recursive(current_dir: str) -> str:
        entries: List[TreeEntry] = []
        for item in sorted(os.listdir(current_dir)):
            if item == ".git":
                continue
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                sub_sha = build_tree_recursive(item_path)
                entries.append(TreeEntry(mode="40000", name=item, sha=sub_sha))
            elif os.path.isfile(item_path):
                with open(item_path, "rb") as f:
                    data = f.read()
                blob = Blob(data)
                blob_sha = repo.write_object(blob)
                mode = "100755" if os.access(item_path, os.X_OK) else "100644"
                entries.append(TreeEntry(mode=mode, name=item, sha=blob_sha))

        tree = Tree(entries)
        return repo.write_object(tree)

    return build_tree_recursive(root_dir)

def cmd_commit_tree(
    tree_sha: str,
    message: str,
    parent: Optional[str] = None,
    author: str = "BYOX Developer <developer@byox.org>",
) -> str:
    repo = Repository.find(".")
    parents = [parent] if parent else []
    commit = Commit(tree_sha=tree_sha, parents=parents, author=author, message=message)
    return repo.write_object(commit)

def cmd_commit(
    message: str,
    author: str = "BYOX Developer <developer@byox.org>",
) -> str:
    repo = Repository.find(".")
    tree_sha = cmd_write_tree(repo.worktree)
    parent_sha = repo.resolve_ref("HEAD")
    commit_sha = cmd_commit_tree(tree_sha=tree_sha, message=message, parent=parent_sha, author=author)
    repo.update_ref("HEAD", commit_sha)
    return commit_sha

def cmd_log(sha: Optional[str] = None, max_count: int = 50) -> List[Dict[str, Any]]:
    repo = Repository.find(".")
    current_sha = sha or repo.resolve_ref("HEAD")
    history = []
    visited = set()

    while current_sha and current_sha not in visited and len(history) < max_count:
        visited.add(current_sha)
        try:
            obj = repo.read_object(current_sha)
        except FileNotFoundError:
            break
        if not isinstance(obj, Commit):
            break

        history.append({
            "sha": current_sha,
            "tree": obj.tree_sha,
            "parents": obj.parents,
            "author": obj.author,
            "timestamp": obj.author_time,
            "message": obj.message,
        })
        current_sha = obj.parents[0] if obj.parents else None

    return history
