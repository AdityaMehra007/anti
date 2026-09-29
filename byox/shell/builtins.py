"""
Shell Built-in Commands.
"""

import os
import sys
from typing import List, Optional, TextIO, Any

class Builtins:
    NAMES = {"cd", "pwd", "echo", "type", "which", "exit", "export"}

    @classmethod
    def is_builtin(cls, cmd: str) -> bool:
        return cmd in cls.NAMES

    @classmethod
    def echo(cls, args: List[str], stdout: TextIO) -> int:
        # Interpret basic escape sequences if needed, or print space-separated
        text = " ".join(args)
        # Unescape \n and \t if present in raw string
        text = text.replace("\\n", "\n").replace("\\t", "\t")
        stdout.write(text + "\n")
        stdout.flush()
        return 0

    @classmethod
    def pwd(cls, cwd: str, stdout: TextIO) -> int:
        stdout.write(cwd + "\n")
        stdout.flush()
        return 0

    @classmethod
    def cd(cls, args: List[str], current_cwd: str, stderr: TextIO) -> str:
        target = args[0] if args else os.path.expanduser("~")
        if target.startswith("~"):
            target = os.path.expanduser(target)
        if not os.path.isabs(target):
            target = os.path.join(current_cwd, target)
        target = os.path.abspath(target)

        if not os.path.exists(target):
            stderr.write(f"cd: no such file or directory: {args[0] if args else ''}\n")
            stderr.flush()
            return current_cwd
        if not os.path.isdir(target):
            stderr.write(f"cd: not a directory: {args[0] if args else ''}\n")
            stderr.flush()
            return current_cwd
        return target

    @classmethod
    def type_cmd(cls, args: List[str], context: Any, stdout: TextIO, stderr: TextIO) -> int:
        if not args:
            return 1
        cmd = args[0]
        if cls.is_builtin(cmd):
            stdout.write(f"{cmd} is a shell builtin\n")
            stdout.flush()
            return 0
        path = context.resolve_executable(cmd)
        if path:
            stdout.write(f"{cmd} is {path}\n")
            stdout.flush()
            return 0
        stderr.write(f"{cmd}: not found\n")
        stderr.flush()
        return 1
