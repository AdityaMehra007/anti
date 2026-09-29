"""
Regex Abstract Syntax Tree Nodes.
"""

from typing import Set

class RegexNode:
    pass

class Empty(RegexNode):
    def __repr__(self):
        return "Empty()"

class Literal(RegexNode):
    def __init__(self, char: str):
        self.char = char

    def __repr__(self):
        return f"Literal({self.char!r})"

class Wildcard(RegexNode):
    def __repr__(self):
        return "Wildcard()"

class CharClass(RegexNode):
    def __init__(self, chars: Set[str], negated: bool = False):
        self.chars = chars
        self.negated = negated

    def matches(self, ch: str) -> bool:
        matched = ch in self.chars
        return not matched if self.negated else matched

    def __repr__(self):
        return f"CharClass(negated={self.negated})"

class Concat(RegexNode):
    def __init__(self, left: RegexNode, right: RegexNode):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Concat({self.left}, {self.right})"

class Alt(RegexNode):
    def __init__(self, left: RegexNode, right: RegexNode):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Alt({self.left}, {self.right})"

class Star(RegexNode):
    def __init__(self, child: RegexNode):
        self.child = child

    def __repr__(self):
        return f"Star({self.child})"

class Plus(RegexNode):
    def __init__(self, child: RegexNode):
        self.child = child

    def __repr__(self):
        return f"Plus({self.child})"

class OptionalNode(RegexNode):
    def __init__(self, child: RegexNode):
        self.child = child

    def __repr__(self):
        return f"OptionalNode({self.child})"

class AnchorStart(RegexNode):
    def __repr__(self):
        return "AnchorStart()"

class AnchorEnd(RegexNode):
    def __repr__(self):
        return "AnchorEnd()"
