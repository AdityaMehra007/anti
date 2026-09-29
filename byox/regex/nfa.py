"""
Thompson NFA Construction and Simulation Engine.
"""

from typing import Set, List, Optional, Tuple, Callable, Any
from byox.regex.ast import (
    RegexNode, Empty, Literal, Wildcard, CharClass,
    Concat, Alt, Star, Plus, OptionalNode, AnchorStart, AnchorEnd
)
from byox.regex.parser import RegexParser

class State:
    _id_counter = 0

    def __init__(self):
        State._id_counter += 1
        self.id = State._id_counter
        self.transitions: List[Tuple[Optional[Any], "State"]] = []

    def add_epsilon(self, target: "State"):
        self.transitions.append((None, target))

    def add_transition(self, matcher: Any, target: "State"):
        self.transitions.append((matcher, target))

    def __repr__(self):
        return f"State({self.id})"


class NFAFragment:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept


class NFA:
    def __init__(self, start: State, accept: State, has_start_anchor: bool = False, has_end_anchor: bool = False):
        self.start = start
        self.accept = accept
        self.has_start_anchor = has_start_anchor
        self.has_end_anchor = has_end_anchor

    @classmethod
    def compile_node(cls, node: RegexNode) -> NFAFragment:
        if isinstance(node, Empty):
            s = State()
            a = State()
            s.add_epsilon(a)
            return NFAFragment(s, a)

        elif isinstance(node, Literal):
            s = State()
            a = State()
            s.add_transition(node.char, a)
            return NFAFragment(s, a)

        elif isinstance(node, Wildcard):
            s = State()
            a = State()
            s.add_transition(lambda ch: ch != "\n", a)
            return NFAFragment(s, a)

        elif isinstance(node, CharClass):
            s = State()
            a = State()
            s.add_transition(node.matches, a)
            return NFAFragment(s, a)

        elif isinstance(node, (AnchorStart, AnchorEnd)):
            # Anchors are handled at boundary checks
            s = State()
            a = State()
            s.add_epsilon(a)
            return NFAFragment(s, a)

        elif isinstance(node, Concat):
            left = cls.compile_node(node.left)
            right = cls.compile_node(node.right)
            left.accept.add_epsilon(right.start)
            return NFAFragment(left.start, right.accept)

        elif isinstance(node, Alt):
            s = State()
            a = State()
            left = cls.compile_node(node.left)
            right = cls.compile_node(node.right)
            s.add_epsilon(left.start)
            s.add_epsilon(right.start)
            left.accept.add_epsilon(a)
            right.accept.add_epsilon(a)
            return NFAFragment(s, a)

        elif isinstance(node, Star):
            s = State()
            a = State()
            child = cls.compile_node(node.child)
            s.add_epsilon(child.start)
            s.add_epsilon(a)
            child.accept.add_epsilon(child.start)
            child.accept.add_epsilon(a)
            return NFAFragment(s, a)

        elif isinstance(node, Plus):
            s = State()
            a = State()
            child = cls.compile_node(node.child)
            s.add_epsilon(child.start)
            child.accept.add_epsilon(child.start)
            child.accept.add_epsilon(a)
            return NFAFragment(s, a)

        elif isinstance(node, OptionalNode):
            s = State()
            a = State()
            child = cls.compile_node(node.child)
            s.add_epsilon(child.start)
            s.add_epsilon(a)
            child.accept.add_epsilon(a)
            return NFAFragment(s, a)

        else:
            raise TypeError(f"Unknown AST node type: {type(node)}")

    @classmethod
    def compile(cls, pattern: str) -> "NFA":
        has_start_anchor = pattern.startswith("^")
        has_end_anchor = pattern.endswith("$") and not pattern.endswith("\\$")

        clean_pattern = pattern
        if has_start_anchor:
            clean_pattern = clean_pattern[1:]
        if has_end_anchor and clean_pattern:
            clean_pattern = clean_pattern[:-1]

        ast = RegexParser(clean_pattern).parse()
        frag = cls.compile_node(ast)
        return cls(frag.start, frag.accept, has_start_anchor, has_end_anchor)

    @staticmethod
    def epsilon_closure(states: Set[State]) -> Set[State]:
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for matcher, target in state.transitions:
                if matcher is None and target not in closure:
                    closure.add(target)
                    stack.append(target)
        return closure

    def step(self, current_states: Set[State], ch: str) -> Set[State]:
        next_states: Set[State] = set()
        for state in current_states:
            for matcher, target in state.transitions:
                if matcher is None:
                    continue
                matched = False
                if isinstance(matcher, str):
                    matched = (matcher == ch)
                elif callable(matcher):
                    matched = matcher(ch)
                if matched:
                    next_states.add(target)
        return self.epsilon_closure(next_states)

    def match_from(self, text: str, start_pos: int, exact_length: bool) -> bool:
        current = self.epsilon_closure({self.start})
        n = len(text)
        i = start_pos

        if exact_length:
            while i < n and current:
                current = self.step(current, text[i])
                i += 1
            return i == n and self.accept in current
        else:
            if self.accept in current:
                return True
            while i < n and current:
                current = self.step(current, text[i])
                if self.accept in current and not self.has_end_anchor:
                    return True
                i += 1
            return self.accept in current


def match(pattern: str, text: str) -> bool:
    """Full string match (equivalent to ^pattern$) unless pattern has anchors."""
    nfa = NFA.compile(pattern)
    return nfa.match_from(text, 0, exact_length=True)

def search(pattern: str, text: str) -> bool:
    """Scan through text looking for the first location where pattern matches."""
    nfa = NFA.compile(pattern)
    if nfa.has_start_anchor:
        return nfa.match_from(text, 0, exact_length=nfa.has_end_anchor)
    for start_pos in range(len(text) + 1):
        if nfa.match_from(text, start_pos, exact_length=nfa.has_end_anchor):
            return True
    return False
