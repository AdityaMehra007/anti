import os
import shutil
import tempfile
import unittest
from byox.sqlite.lexer import SQLLexer
from byox.sqlite.parser import SQLParser, CreateTableStatement, InsertStatement, SelectStatement
from byox.sqlite.engine import Database

class TestSQLite(unittest.TestCase):
    def test_lexer_and_parser(self):
        sql = "CREATE TABLE users (id INT, name TEXT, score FLOAT)"
        tokens = SQLLexer(sql).tokenize()
        stmt = SQLParser(tokens).parse()
        self.assertIsInstance(stmt, CreateTableStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(stmt.columns, [("id", "INT"), ("name", "TEXT"), ("score", "FLOAT")])

        sql_insert = "INSERT INTO users VALUES (1, 'Alice', 98.5)"
        tokens = SQLLexer(sql_insert).tokenize()
        stmt = SQLParser(tokens).parse()
        self.assertIsInstance(stmt, InsertStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(stmt.values, [1, "Alice", 98.5])

        sql_select = "SELECT id, name FROM users WHERE score > 90"
        tokens = SQLLexer(sql_select).tokenize()
        stmt = SQLParser(tokens).parse()
        self.assertIsInstance(stmt, SelectStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(stmt.columns, ["id", "name"])
        self.assertIsNotNone(stmt.where)

    def test_in_memory_database_crud(self):
        db = Database()
        db.execute("CREATE TABLE students (id INT, name TEXT, grade TEXT)")
        db.execute("INSERT INTO students VALUES (101, 'Ada', 'A')")
        db.execute("INSERT INTO students VALUES (102, 'Bob', 'B')")
        db.execute("INSERT INTO students VALUES (103, 'Charlie', 'A')")

        # Select all
        rows = db.execute("SELECT * FROM students")
        self.assertEqual(len(rows), 3)

        # Select with WHERE filter
        a_students = db.execute("SELECT name FROM students WHERE grade = 'A'")
        self.assertEqual(len(a_students), 2)
        self.assertEqual([r["name"] for r in a_students], ["Ada", "Charlie"])

        # Numerical condition
        db.execute("CREATE TABLE products (sku INT, price FLOAT)")
        db.execute("INSERT INTO products VALUES (1, 19.99)")
        db.execute("INSERT INTO products VALUES (2, 49.99)")
        db.execute("INSERT INTO products VALUES (3, 5.00)")
        expensive = db.execute("SELECT sku, price FROM products WHERE price >= 20.0")
        self.assertEqual(len(expensive), 1)
        self.assertEqual(expensive[0]["sku"], 2)

    def test_disk_persistence_and_reload(self):
        temp_dir = tempfile.mkdtemp(prefix="byox_sqlite_test_")
        db_path = os.path.join(temp_dir, "test.db")
        try:
            # Create and populate database
            db1 = Database(db_path)
            db1.execute("CREATE TABLE employees (id INT, title TEXT)")
            db1.execute("INSERT INTO employees VALUES (1, 'Architect')")
            db1.execute("INSERT INTO employees VALUES (2, 'Lead Developer')")
            db1.close()

            # Re-open database from disk file
            db2 = Database(db_path)
            rows = db2.execute("SELECT id, title FROM employees WHERE id = 2")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["title"], "Lead Developer")
            db2.close()
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()
