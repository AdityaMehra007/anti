"""
SQL Lexer and Token Definitions.
"""

from enum import Enum, auto
from typing import List, Any

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    SYMBOL = auto()
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: Any, pos: int = 0):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


KEYWORDS = {
    "CREATE", "TABLE", "INSERT", "INTO", "VALUES",
    "SELECT", "FROM", "WHERE", "AND", "OR",
    "INT", "TEXT", "FLOAT"
}

SYMBOLS = {"*", ",", "(", ")", "=", "!=", "<", ">", "<=", ">="}

class SQLLexer:
    def __init__(self, sql: str):
        self.sql = sql
        self.pos = 0
        self.n = len(sql)

    def current(self) -> str:
        return self.sql[self.pos] if self.pos < self.n else ""

    def advance(self) -> str:
        ch = self.current()
        self.pos += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.n:
            ch = self.current()

            if ch.isspace():
                self.advance()
                continue

            # Strings '...' or "..."
            if ch in ("'", '"'):
                quote = self.advance()
                start = self.pos
                chars = []
                while self.pos < self.n and self.current() != quote:
                    if self.current() == "\\" and self.pos + 1 < self.n:
                        self.advance()
                    chars.append(self.advance())
                if self.current() != quote:
                    raise ValueError(f"Unclosed string quote starting at {start}")
                self.advance()  # consume quote
                tokens.append(Token(TokenType.STRING, "".join(chars), start))
                continue

            # Numbers
            if ch.isdigit() or (ch == "-" and self.pos + 1 < self.n and self.sql[self.pos + 1].isdigit()):
                start = self.pos
                num_str = [self.advance()]
                has_dot = False
                while self.pos < self.n and (self.current().isdigit() or self.current() == "."):
                    if self.current() == ".":
                        if has_dot:
                            break
                        has_dot = True
                    num_str.append(self.advance())
                s = "".join(num_str)
                val = float(s) if has_dot else int(s)
                tokens.append(Token(TokenType.NUMBER, val, start))
                continue

            # Multi-character symbols !=, <=, >=
            if self.pos + 1 < self.n and self.sql[self.pos : self.pos + 2] in ("!=", "<=", ">="):
                sym = self.sql[self.pos : self.pos + 2]
                start = self.pos
                self.pos += 2
                tokens.append(Token(TokenType.SYMBOL, sym, start))
                continue

            # Single-character symbols
            if ch in ("*", ",", "(", ")", "=", "<", ">"):
                start = self.pos
                self.advance()
                tokens.append(Token(TokenType.SYMBOL, ch, start))
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == "_":
                start = self.pos
                ident = [self.advance()]
                while self.pos < self.n and (self.current().isalnum() or self.current() == "_"):
                    ident.append(self.advance())
                word = "".join(ident)
                if word.upper() in KEYWORDS:
                    tokens.append(Token(TokenType.KEYWORD, word.upper(), start))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word, start))
                continue

            raise ValueError(f"Unexpected character in SQL at pos {self.pos}: '{ch}'")

        tokens.append(Token(TokenType.EOF, None, self.pos))
        return tokens
