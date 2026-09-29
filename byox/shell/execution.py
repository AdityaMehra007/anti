"""
Shell Execution Engine: Pipelines, Redirection, PATH Resolution, and REPL.
"""

import os
import sys
import subprocess
from typing import List, Optional, TextIO, Tuple, Dict
from byox.shell.tokenizer import tokenize
from byox.shell.builtins import Builtins

class ShellContext:
    def __init__(self, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None):
        self.cwd = os.path.abspath(cwd or os.getcwd())
        self.env = dict(env or os.environ)

    def resolve_executable(self, cmd: str) -> Optional[str]:
        if os.path.isabs(cmd) or "/" in cmd or "\\" in cmd:
            full = os.path.join(self.cwd, cmd)
            if os.path.isfile(full):
                return os.path.abspath(full)
            return None

        path_dirs = self.env.get("PATH", "").split(os.pathsep)
        extensions = [""]
        if sys.platform == "win32":
            pathext = self.env.get("PATHEXT", ".EXE;.CMD;.BAT").split(";")
            extensions.extend(pathext)

        for directory in path_dirs:
            for ext in extensions:
                candidate = os.path.join(directory, cmd + ext)
                if os.path.isfile(candidate):
                    return os.path.abspath(candidate)
        return None

    def execute_line(
        self,
        line: str,
        stdin: Optional[TextIO] = None,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
    ) -> int:
        tokens = tokenize(line.strip())
        if not tokens:
            return 0

        # Split tokens by pipe '|'
        stages: List[List[str]] = []
        current_stage: List[str] = []
        for t in tokens:
            if t == "|":
                stages.append(current_stage)
                current_stage = []
            else:
                current_stage.append(t)
        if current_stage:
            stages.append(current_stage)

        if not stages:
            return 0

        if len(stages) == 1:
            return self._execute_stage(stages[0], stdin=stdin, stdout=stdout, stderr=stderr)
        else:
            return self._execute_pipeline(stages, stdin=stdin, stdout=stdout, stderr=stderr)

    def _execute_stage(
        self,
        tokens: List[str],
        stdin: Optional[TextIO] = None,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
    ) -> int:
        cmd_args: List[str] = []
        redirect_out = None
        append_out = False
        redirect_err = None
        append_err = False

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == ">" and i + 1 < len(tokens):
                redirect_out = tokens[i + 1]
                append_out = False
                i += 2
            elif token == ">>" and i + 1 < len(tokens):
                redirect_out = tokens[i + 1]
                append_out = True
                i += 2
            elif token == "2>" and i + 1 < len(tokens):
                redirect_err = tokens[i + 1]
                append_err = False
                i += 2
            else:
                cmd_args.append(token)
                i += 1

        if not cmd_args:
            return 0

        out_stream = stdout or sys.stdout
        err_stream = stderr or sys.stderr

        out_file_handle = None
        err_file_handle = None

        try:
            if redirect_out:
                mode = "a" if append_out else "w"
                target_path = os.path.join(self.cwd, redirect_out)
                out_file_handle = open(target_path, mode, encoding="utf-8")
                out_stream = out_file_handle

            if redirect_err:
                mode = "a" if append_err else "w"
                target_path = os.path.join(self.cwd, redirect_err)
                err_file_handle = open(target_path, mode, encoding="utf-8")
                err_stream = err_file_handle

            cmd = cmd_args[0]
            args = cmd_args[1:]

            if cmd == "exit":
                code = int(args[0]) if args else 0
                return code

            if cmd == "echo":
                return Builtins.echo(args, stdout=out_stream)

            if cmd == "pwd":
                return Builtins.pwd(self.cwd, stdout=out_stream)

            if cmd == "cd":
                self.cwd = Builtins.cd(args, self.cwd, stderr=err_stream)
                return 0

            if cmd in ("type", "which"):
                return Builtins.type_cmd(args, self, stdout=out_stream, stderr=err_stream)

            # External command
            exe = self.resolve_executable(cmd)
            if not exe:
                err_stream.write(f"{cmd}: command not found\n")
                err_stream.flush()
                return 127

            # Run subprocess
            input_data = None
            if stdin and hasattr(stdin, "read"):
                # Read whatever input is available
                val = stdin.read()
                input_data = val.encode("utf-8") if isinstance(val, str) else val

            proc = subprocess.Popen(
                [exe] + args,
                cwd=self.cwd,
                env=self.env,
                stdin=subprocess.PIPE if input_data is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out_bytes, err_bytes = proc.communicate(input=input_data)

            if out_bytes:
                out_text = out_bytes.decode("utf-8", errors="replace")
                out_stream.write(out_text)
                out_stream.flush()

            if err_bytes:
                err_text = err_bytes.decode("utf-8", errors="replace")
                err_stream.write(err_text)
                err_stream.flush()

            return proc.returncode

        finally:
            if out_file_handle:
                out_file_handle.close()
            if err_file_handle:
                err_file_handle.close()

    def _execute_pipeline(
        self,
        stages: List[List[str]],
        stdin: Optional[TextIO] = None,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
    ) -> int:
        import io
        prev_output: Optional[str] = None
        if stdin and hasattr(stdin, "read"):
            prev_output = stdin.read()

        exit_code = 0
        for i, stage in enumerate(stages):
            is_last = (i == len(stages) - 1)
            stage_in = io.StringIO(prev_output) if prev_output is not None else None
            stage_out = stdout if is_last else io.StringIO()

            exit_code = self._execute_stage(
                stage,
                stdin=stage_in,
                stdout=stage_out,
                stderr=stderr,
            )

            if not is_last:
                prev_output = stage_out.getvalue()

        return exit_code

    def repl(self):
        print("BYOX Shell (type 'exit' to quit)")
        while True:
            try:
                prompt = f"{os.path.basename(self.cwd)} $ "
                line = input(prompt)
                if not line.strip():
                    continue
                code = self.execute_line(line)
                if line.strip() == "exit":
                    break
            except (EOFError, KeyboardInterrupt):
                print()
                break
