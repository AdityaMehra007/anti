"""
Shell Command Tokenizer supporting single/double quotes, escapes, and operators.
"""

from typing import List

OPERATORS = ["|", ">>", ">", "2>", "<"]

def tokenize(cmd_line: str) -> List[str]:
    tokens: List[str] = []
    current: List[str] = []
    in_single = False
    in_double = False
    escaped = False
    i = 0
    n = len(cmd_line)

    while i < n:
        ch = cmd_line[i]

        if escaped:
            current.append(ch)
            escaped = False
            i += 1
            continue

        if ch == "\\" and not in_single:
            if in_double:
                # In double quotes, backslash only escapes ", \, $, ` or newline
                if i + 1 < n and cmd_line[i + 1] in ('"', '\\', '$', '`', '\n'):
                    escaped = True
                    i += 1
                    continue
                else:
                    current.append(ch)
                    i += 1
                    continue
            else:
                escaped = True
                i += 1
                continue

        if ch == "'" and not in_double:
            in_single = not in_single
            i += 1
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            i += 1
            continue

        if not in_single and not in_double:
            # Check multi-char operator
            if i + 1 < n and cmd_line[i : i + 2] in (">>", "2>"):
                if current:
                    tokens.append("".join(current))
                    current = []
                tokens.append(cmd_line[i : i + 2])
                i += 2
                continue
            elif ch in ("|", ">", "<"):
                if current:
                    tokens.append("".join(current))
                    current = []
                tokens.append(ch)
                i += 1
                continue
            elif ch.isspace():
                if current:
                    tokens.append("".join(current))
                    current = []
                i += 1
                continue

        current.append(ch)
        i += 1

    if current:
        tokens.append("".join(current))

    return tokens
