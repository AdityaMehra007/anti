import os
import shutil
import tempfile
import unittest
from byox.git.repository import Repository
from byox.git.objects import Blob, Tree, Commit
from byox.git.commands import (
    cmd_init,
    cmd_hash_object,
    cmd_cat_file,
    cmd_write_tree,
    cmd_commit_tree,
    cmd_commit,
    cmd_log,
)

class TestGit(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="byox_git_test_")
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_repository(self):
        repo_path = cmd_init(self.test_dir)
        git_dir = os.path.join(self.test_dir, ".git")
        self.assertTrue(os.path.exists(git_dir))
        self.assertTrue(os.path.exists(os.path.join(git_dir, "objects")))
        self.assertTrue(os.path.exists(os.path.join(git_dir, "refs", "heads")))
        with open(os.path.join(git_dir, "HEAD"), "r", encoding="utf-8") as f:
            head_content = f.read().strip()
        self.assertEqual(head_content, "ref: refs/heads/main")

    def test_blob_hash_and_cat_file(self):
        cmd_init(self.test_dir)
        file_path = os.path.join(self.test_dir, "hello.txt")
        with open(file_path, "wb") as f:
            f.write(b"hello world\n")
            
        sha = cmd_hash_object(file_path, write=True)
        # Git standard SHA-1 for "hello world\n" blob is 3b18e512dba79e4c8300dd08aeb37f8e728b8dad
        self.assertEqual(sha, "3b18e512dba79e4c8300dd08aeb37f8e728b8dad")
        
        obj_type, size, content = cmd_cat_file(sha)
        self.assertEqual(obj_type, "blob")
        self.assertEqual(size, 12)
        self.assertEqual(content, b"hello world\n")

    def test_write_tree_and_commit(self):
        cmd_init(self.test_dir)
        # Create a file structure
        with open(os.path.join(self.test_dir, "file1.txt"), "w", encoding="utf-8") as f:
            f.write("first file")
            
        sub_dir = os.path.join(self.test_dir, "src")
        os.makedirs(sub_dir)
        with open(os.path.join(sub_dir, "app.py"), "w", encoding="utf-8") as f:
            f.write("print('hello')")
            
        tree_sha = cmd_write_tree(self.test_dir)
        self.assertIsNotNone(tree_sha)
        self.assertEqual(len(tree_sha), 40)
        
        # Create first commit
        commit_sha1 = cmd_commit_tree(tree_sha, message="Initial commit")
        self.assertEqual(len(commit_sha1), 40)
        
        # Verify commit reading
        repo = Repository(self.test_dir)
        commit_obj = repo.read_object(commit_sha1)
        self.assertIsInstance(commit_obj, Commit)
        self.assertEqual(commit_obj.tree_sha, tree_sha)
        self.assertEqual(commit_obj.message, "Initial commit")
        self.assertEqual(len(commit_obj.parents), 0)
        
        # Second commit with parent
        commit_sha2 = cmd_commit_tree(tree_sha, message="Second commit", parent=commit_sha1)
        commit2 = repo.read_object(commit_sha2)
        self.assertEqual(commit2.parents, [commit_sha1])

    def test_high_level_commit_and_log(self):
        cmd_init(self.test_dir)
        with open(os.path.join(self.test_dir, "code.py"), "w", encoding="utf-8") as f:
            f.write("x = 42")
            
        c1 = cmd_commit("Root commit")
        with open(os.path.join(self.test_dir, "code.py"), "a", encoding="utf-8") as f:
            f.write("\ny = 100")
            
        c2 = cmd_commit("Update code")
        
        history = cmd_log()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["sha"], c2)
        self.assertEqual(history[0]["message"], "Update code")
        self.assertEqual(history[1]["sha"], c1)
        self.assertEqual(history[1]["message"], "Root commit")

if __name__ == "__main__":
    unittest.main()
