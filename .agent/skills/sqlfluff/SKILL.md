---
name: sqlfluff
description: SQL linting, formatting, syntax checking, dialect validation, and schema hygiene using SQLFluff. Use when authoring, reviewing, refactoring, or auto-fixing SQL schemas, queries, or database migrations across SQLite, PostgreSQL, MySQL, DuckDB, Snowflake, and BigQuery.
metadata:
  origin: OMEGA
---

# SQLFluff Skill & SQL Quality Gateway

Use this skill when authoring, formatting, linting, auditing, or refactoring SQL schemas, queries, or database migrations across the repository.

---

## 1. Activation Scenarios

- Adding or modifying database schemas (`.sql` files) in `aios/databases/`, `REVENUE_OS/database/`, `supabase/`, etc.
- Reviewing SQL queries or schema definitions in PRs.
- Auto-fixing syntax, indentation, and casing inconsistencies across SQL files.
- Validating dialect-specific features (SQLite WAL mode, PostgreSQL extensions, vector datatypes).
- Investigating SQL syntax parsing errors or Jinja/dbt templating issues.

---

## 2. Core Execution CLI

In this repository, use the automated wrapper `scripts/sqlfluff_runner.py` (which automatically uses `sqlfluff` or falls back to `uv tool run sqlfluff`):

```bash
# 1. Lint default project schemas
python scripts/sqlfluff_runner.py lint

# 2. Lint a specific file or directory
python scripts/sqlfluff_runner.py lint aios/databases/init_schema.sql
python scripts/sqlfluff_runner.py lint REVENUE_OS/database/schema.sql
python scripts/sqlfluff_runner.py lint supabase/migrations/ --dialect postgres

# 3. Auto-fix violations
python scripts/sqlfluff_runner.py fix aios/databases/init_schema.sql
python scripts/sqlfluff_runner.py fix REVENUE_OS/database/schema.sql

# 4. View parsed AST (syntax debugging)
uv tool run sqlfluff parse path/to/query.sql --dialect sqlite

# 5. List available rules and supported dialects
python scripts/sqlfluff_runner.py rules
python scripts/sqlfluff_runner.py dialects
```

---

## 3. Repository Configuration Standards

### Dialect Support
- **Default (Root)**: SQLite (`dialect = sqlite` in `.sqlfluff`).
- **Supabase**: PostgreSQL (`dialect = postgres` in `supabase/.sqlfluff`).

### Style & Casing Directives
- **Keywords**: `UPPER` (`SELECT`, `INSERT`, `CREATE TABLE`, `WHERE`)
- **Identifiers**: `lower` (`user_id`, `created_at`, `status`)
- **Functions**: `UPPER` (`COUNT()`, `COALESCE()`, `NOW()`, `DATETIME()`)
- **Literals**: `UPPER` (`NULL`, `TRUE`, `FALSE`)
- **Indentation**: 4 spaces (SQLite/Root), 2 spaces (Supabase/PostgreSQL).
- **Line Length**: 120 columns.

---

## 4. Key Rule Reference

| Rule Code | Category | Description | Auto-Fixable |
| :--- | :--- | :--- | :---: |
| **LT01** | Spacing | Expected single whitespace around keywords, commas, brackets | Yes |
| **LT02** | Indentation | Indentation must match tab/space policy | Yes |
| **LT05** | Line Length | Line exceeds maximum configured width (120 chars) | Yes / Manual |
| **CP01** | Casing | Keywords must match upper/lower casing policy | Yes |
| **CP03** | Casing | Function names must be consistently uppercase | Yes |
| **CP04** | Casing | Literals (`NULL`, `TRUE`) must match casing policy | Yes |
| **CP05** | Casing | Datatypes (`TEXT`, `INTEGER`, `TIMESTAMPTZ`) casing policy | Yes |
| **RF04** | References | Keywords should not be used as identifiers (e.g. `order`) | Manual |
| **RF05** | References | Disallow special characters in unquoted identifiers | Manual |
| **RF06** | References | Disallow unnecessary quoted identifiers | Yes |

---

## 5. Verification Checklist

Before completing any task involving SQL files:
1. Run `python scripts/sqlfluff_runner.py lint <target-files>`.
2. If violations are reported, run `python scripts/sqlfluff_runner.py fix <target-files>`.
3. Verify remaining unfixable violations manually.
4. Execute unit tests: `python -m pytest tests/test_sqlfluff_runner.py -v`.
