"""
byox.regex - Thompson NFA Regular Expression Engine from scratch in pure Python.
Non-backtracking linear time matching, character classes, quantifiers, and alternation.
"""

from byox.regex.nfa import NFA, match, search

__all__ = ["NFA", "match", "search"]
