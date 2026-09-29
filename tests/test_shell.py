import io
import os
import shutil
import tempfile
import unittest
from byox.shell.tokenizer import tokenize
from byox.shell.execution import ShellContext

class TestShell(unittest.TestCase):
    def test_tokenizer_basic_and_quotes(self):
        # Basic whitespace
        self.assertEqual(tokenize("echo hello world"), ["echo", "hello", "world"])
        
        # Single quotes
        self.assertEqual(tokenize("echo 'hello   world'"), ["echo", "hello   world"])
        
        # Double quotes with escapes
        self.assertEqual(tokenize('echo "hello \\"world\\""'), ["echo", 'hello "world"'])
        
        # Mixed quotes
        self.assertEqual(tokenize("cat 'file 1.txt' \"file 2.txt\""), ["cat", "file 1.txt", "file 2.txt"])

        # Redirection and pipe operators
        self.assertEqual(
            tokenize("cat file.txt | grep error > out.txt"),
            ["cat", "file.txt", "|", "grep", "error", ">", "out.txt"]
        )

    def test_builtins_echo_and_pwd(self):
        ctx = ShellContext()
        out = io.StringIO()
        err = io.StringIO()
        
        code = ctx.execute_line("echo hello from shell", stdout=out, stderr=err)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "hello from shell")

        out = io.StringIO()
        code = ctx.execute_line("pwd", stdout=out, stderr=err)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), os.getcwd())

    def test_builtins_cd(self):
        temp_dir = tempfile.mkdtemp(prefix="byox_shell_cd_")
        try:
            ctx = ShellContext()
            ctx.execute_line(f"cd '{temp_dir}'")
            self.assertEqual(os.path.realpath(ctx.cwd), os.path.realpath(temp_dir))
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_redirection(self):
        temp_dir = tempfile.mkdtemp(prefix="byox_shell_redir_")
        try:
            ctx = ShellContext(cwd=temp_dir)
            out_file = os.path.join(temp_dir, "output.txt")
            
            # Overwrite >
            ctx.execute_line(f"echo first line > output.txt")
            with open(out_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.assertEqual(content, "first line")

            # Append >>
            ctx.execute_line(f"echo second line >> output.txt")
            with open(out_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.assertEqual(content, "first line\nsecond line")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_pipeline_execution(self):
        ctx = ShellContext()
        out = io.StringIO()
        err = io.StringIO()
        
        # Pipeline: echo piped into python stdin reader
        code = ctx.execute_line(
            'echo "line1\\nline2" | python -c "import sys; print(len(sys.stdin.read().split()))"',
            stdout=out,
            stderr=err
        )
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "2")

if __name__ == "__main__":
    unittest.main()
