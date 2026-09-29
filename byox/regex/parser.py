"""
Regex Parser using Recursive Descent.
"""

from typing import Set
from byox.regex.ast import (
    RegexNode, Empty, Literal, Wildcard, CharClass,
    Concat, Alt, Star, Plus, OptionalNode, AnchorStart, AnchorEnd
)

class RegexParser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0
        self.n = len(pattern)

    def current(self) -> str:
        return self.pattern[self.pos] if self.pos < self.n else ""

    def advance(self) -> str:
        ch = self.current()
        self.pos += 1
        return ch

    def parse(self) -> RegexNode:
        if not self.pattern:
            return Empty()
        node = self.parse_expr()
        if self.pos < self.n:
            raise ValueError(f"Unexpected trailing token at position {self.pos}: '{self.pattern[self.pos]}'")
        return node

    def parse_expr(self) -> RegexNode:
        left = self.parse_concat()
        while self.current() == "|":
            self.advance()  # consume '|'
            right = self.parse_concat()
            left = Alt(left, right)
        return left

    def parse_concat(self) -> RegexNode:
        nodes = []
        while self.pos < self.n and self.current() not in ("|", ")"):
            nodes.append(self.parse_piece())
        if not nodes:
            return Empty()
        res = nodes[0]
        for node in nodes[1:]:
            res = Concat(res, node)
        return res

    def parse_piece(self) -> RegexNode:
        atom = self.parse_atom()
        while self.pos < self.n:
            ch = self.current()
            if ch == "*":
                self.advance()
                atom = Star(atom)
            elif ch == "+":
                self.advance()
                atom = Plus(atom)
            elif ch == "?":
                self.advance()
                atom = OptionalNode(atom)
            else:
                break
        return atom

    def parse_atom(self) -> RegexNode:
        ch = self.current()
        if ch == "":
            return Empty()

        if ch == "(":
            self.advance()
            node = self.parse_expr()
            if self.current() != ")":
                raise ValueError(f"Unmatched '(' at position {self.pos}")
            self.advance()  # consume ')'
            return node

        elif ch == "[":
            return self.parse_char_class()

        elif ch == ".":
            self.advance()
            return Wildcard()

        elif ch == "^":
            self.advance()
            return AnchorStart()

        elif ch == "$":
            self.advance()
            return AnchorEnd()

        elif ch == "\\":
            self.advance()
            if self.pos >= self.n:
                raise ValueError("Trailing backslash in regex pattern")
            escaped_ch = self.advance()
            return Literal(escaped_ch)

        else:
            self.advance()
            return Literal(ch)

    def parse_char_class(self) -> RegexNode:
        self.advance()  # consume '['
        negated = False
        if self.current() == "^":
            negated = True
            self.advance()

        chars: Set[str] = set()
        while self.pos < self.n and self.current() != "]":
            ch = self.advance()
            if ch == "\\" and self.pos < self.n:
                chars.add(self.advance())
            elif self.current() == "-" and self.pos + 1 < self.n and self.pattern[self.pos + 1] != "]":
                self.advance()  # consume '-'
                end_ch = self.advance()
                for code in range(ord(ch), ord(end_ch) + 1):
                    chars.add(chr(code))
            else:
                chars.add(ch)

        if self.current() != "]":
            raise ValueError("Unclosed character class '['")
        self.advance()  # consume ']'
        return CharClass(chars, negated=negated)
