"""
SQL Parser and AST Definitions.
"""

from typing import List, Tuple, Any, Optional
from byox.sqlite.lexer import Token, TokenType

class Statement:
    pass

class CreateTableStatement(Statement):
    def __init__(self, table_name: str, columns: List[Tuple[str, str]]):
        self.table_name = table_name
        self.columns = columns  # List of (column_name, type)

    def __repr__(self):
        return f"CreateTableStatement({self.table_name}, {self.columns})"


class InsertStatement(Statement):
    def __init__(self, table_name: str, values: List[Any]):
        self.table_name = table_name
        self.values = values

    def __repr__(self):
        return f"InsertStatement({self.table_name}, {self.values})"


class WhereClause:
    def __init__(self, col: str, op: str, value: Any):
        self.col = col
        self.op = op
        self.value = value

    def evaluate(self, row: dict) -> bool:
        if self.col not in row:
            return False
        val = row[self.col]
        target = self.value

        # Auto-cast if comparable
        if isinstance(target, (int, float)) and isinstance(val, (int, float)):
            target = float(target)
            val = float(val)

        if self.op == "=":
            return val == target
        elif self.op == "!=":
            return val != target
        elif self.op == "<":
            return val < target
        elif self.op == ">":
            return val > target
        elif self.op == "<=":
            return val <= target
        elif self.op == ">=":
            return val >= target
        return False

    def __repr__(self):
        return f"WhereClause({self.col} {self.op} {self.value!r})"


class SelectStatement(Statement):
    def __init__(self, table_name: str, columns: List[str], where: Optional[WhereClause] = None):
        self.table_name = table_name
        self.columns = columns
        self.where = where

    def __repr__(self):
        return f"SelectStatement({self.table_name}, {self.columns}, where={self.where})"


class SQLParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def advance(self) -> Token:
        tok = self.current()
        self.pos += 1
        return tok

    def expect(self, type_: TokenType, value: Optional[Any] = None) -> Token:
        tok = self.advance()
        if tok.type != type_ or (value is not None and tok.value != value):
            raise ValueError(f"Syntax error: Expected {type_.name} {value!r}, got {tok.type.name} {tok.value!r}")
        return tok

    def parse(self) -> Statement:
        tok = self.current()
        if tok.type == TokenType.KEYWORD:
            if tok.value == "CREATE":
                return self.parse_create()
            elif tok.value == "INSERT":
                return self.parse_insert()
            elif tok.value == "SELECT":
                return self.parse_select()

        raise ValueError(f"Unsupported statement beginning with {tok.value}")

    def parse_create(self) -> CreateTableStatement:
        self.expect(TokenType.KEYWORD, "CREATE")
        self.expect(TokenType.KEYWORD, "TABLE")
        table_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SYMBOL, "(")

        columns: List[Tuple[str, str]] = []
        while True:
            col_name = self.expect(TokenType.IDENTIFIER).value
            col_type = self.expect(TokenType.KEYWORD).value
            columns.append((col_name, col_type))

            if self.current().type == TokenType.SYMBOL and self.current().value == ",":
                self.advance()
            else:
                break

        self.expect(TokenType.SYMBOL, ")")
        return CreateTableStatement(table_name, columns)

    def parse_insert(self) -> InsertStatement:
        self.expect(TokenType.KEYWORD, "INSERT")
        self.expect(TokenType.KEYWORD, "INTO")
        table_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.KEYWORD, "VALUES")
        self.expect(TokenType.SYMBOL, "(")

        values: List[Any] = []
        while True:
            tok = self.advance()
            if tok.type not in (TokenType.NUMBER, TokenType.STRING):
                raise ValueError(f"Expected literal value in INSERT, got {tok.value}")
            values.append(tok.value)

            if self.current().type == TokenType.SYMBOL and self.current().value == ",":
                self.advance()
            else:
                break

        self.expect(TokenType.SYMBOL, ")")
        return InsertStatement(table_name, values)

    def parse_select(self) -> SelectStatement:
        self.expect(TokenType.KEYWORD, "SELECT")
        columns: List[str] = []

        if self.current().type == TokenType.SYMBOL and self.current().value == "*":
            self.advance()
            columns = ["*"]
        else:
            while True:
                col_name = self.expect(TokenType.IDENTIFIER).value
                columns.append(col_name)
                if self.current().type == TokenType.SYMBOL and self.current().value == ",":
                    self.advance()
                else:
                    break

        self.expect(TokenType.KEYWORD, "FROM")
        table_name = self.expect(TokenType.IDENTIFIER).value

        where = None
        if self.current().type == TokenType.KEYWORD and self.current().value == "WHERE":
            self.advance()
            col = self.expect(TokenType.IDENTIFIER).value
            op = self.expect(TokenType.SYMBOL).value
            val_tok = self.advance()
            if val_tok.type not in (TokenType.NUMBER, TokenType.STRING):
                raise ValueError(f"Expected literal in WHERE comparison, got {val_tok.value}")
            where = WhereClause(col, op, val_tok.value)

        return SelectStatement(table_name, columns, where)
