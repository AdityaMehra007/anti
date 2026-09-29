"""
Relational Database Query Engine and Table Manager.
"""

import json
from typing import Optional, List, Dict, Any
from byox.sqlite.lexer import SQLLexer
from byox.sqlite.parser import (
    SQLParser,
    CreateTableStatement,
    InsertStatement,
    SelectStatement,
)
from byox.sqlite.btree import PagedStorage

class Database:
    def __init__(self, filepath: Optional[str] = None):
        self.storage = PagedStorage(filepath)

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        tokens = SQLLexer(sql).tokenize()
        stmt = SQLParser(tokens).parse()

        if isinstance(stmt, CreateTableStatement):
            return self._exec_create(stmt)
        elif isinstance(stmt, InsertStatement):
            return self._exec_insert(stmt)
        elif isinstance(stmt, SelectStatement):
            return self._exec_select(stmt)
        else:
            raise NotImplementedError(f"Statement not implemented: {type(stmt)}")

    def _exec_create(self, stmt: CreateTableStatement) -> List[Dict[str, Any]]:
        name = stmt.table_name.lower()
        if name in self.storage.catalog["tables"]:
            raise ValueError(f"Table '{stmt.table_name}' already exists")

        page_id = self.storage.allocate_page()
        # Initialize page header
        page = self.storage.read_page(page_id)
        # Store an empty json list of rows in page
        initial_data = json.dumps([]).encode("utf-8")
        page[: len(initial_data)] = initial_data
        self.storage.write_page(page_id, page)

        self.storage.catalog["tables"][name] = {
            "name": stmt.table_name,
            "columns": stmt.columns,
            "pages": [page_id],
        }
        self.storage.sync_catalog()
        return []

    def _exec_insert(self, stmt: InsertStatement) -> List[Dict[str, Any]]:
        name = stmt.table_name.lower()
        if name not in self.storage.catalog["tables"]:
            raise ValueError(f"Table '{stmt.table_name}' does not exist")

        meta = self.storage.catalog["tables"][name]
        cols = meta["columns"]
        if len(stmt.values) != len(cols):
            raise ValueError(f"Column count mismatch: table has {len(cols)}, got {len(stmt.values)}")

        # Construct row dict with types
        row = {}
        for (col_name, col_type), val in zip(cols, stmt.values):
            if col_type == "INT":
                row[col_name] = int(val)
            elif col_type == "FLOAT":
                row[col_name] = float(val)
            elif col_type == "TEXT":
                row[col_name] = str(val)
            else:
                row[col_name] = val

        # Append row to last page
        page_id = meta["pages"][-1]
        page = self.storage.read_page(page_id)
        null_term = page.find(b"\x00")
        raw_text = page[:null_term].decode("utf-8") if null_term > 0 else "[]"
        try:
            rows = json.loads(raw_text)
        except json.JSONDecodeError:
            rows = []

        rows.append(row)
        new_bytes = json.dumps(rows).encode("utf-8")

        if len(new_bytes) > 4000:
            # Need new page
            new_page_id = self.storage.allocate_page()
            meta["pages"].append(new_page_id)
            new_page = bytearray(4096)
            new_rows_bytes = json.dumps([row]).encode("utf-8")
            new_page[: len(new_rows_bytes)] = new_rows_bytes
            self.storage.write_page(new_page_id, new_page)
        else:
            page[: len(new_bytes)] = new_bytes
            page[len(new_bytes) :] = b"\x00" * (4096 - len(new_bytes))
            self.storage.write_page(page_id, page)

        self.storage.sync_catalog()
        return []

    def _exec_select(self, stmt: SelectStatement) -> List[Dict[str, Any]]:
        name = stmt.table_name.lower()
        if name not in self.storage.catalog["tables"]:
            raise ValueError(f"Table '{stmt.table_name}' does not exist")

        meta = self.storage.catalog["tables"][name]
        results = []

        for page_id in meta["pages"]:
            page = self.storage.read_page(page_id)
            null_term = page.find(b"\x00")
            raw_text = page[:null_term].decode("utf-8") if null_term > 0 else "[]"
            try:
                rows = json.loads(raw_text)
            except json.JSONDecodeError:
                rows = []

            for r in rows:
                if stmt.where is None or stmt.where.evaluate(r):
                    if stmt.columns == ["*"]:
                        results.append(dict(r))
                    else:
                        projected = {c: r.get(c) for c in stmt.columns if c in r}
                        results.append(projected)

        return results

    def close(self):
        self.storage.close()
