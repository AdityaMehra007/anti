# SQLFluff Integration & SQL Quality Gateway

This guide details the **SQLFluff** setup, configuration standards, automation scripts, and CI/CD integration across the repository.

---

## 1. Overview

[SQLFluff](https://github.com/sqlfluff/sqlfluff) is an extensible, modular SQL linter and auto-formatter designed to handle multiple SQL dialects and templating engines.

In this repository, SQLFluff is configured to maintain consistency, casing rules, indentation, and idiomatic correctness across relational database schemas.

---

## 2. Configuration Files

### `.sqlfluff`
The root configuration file defines:
- **Dialect**: `sqlite` (with ANSI/Postgres/MySQL overrides available via `--dialect`).
- **Templater**: `jinja`
- **Max line length**: `120`
- **Casing policies**:
  - Keywords: `UPPER`
  - Identifiers: `lower`
  - Functions: `UPPER`
  - Literals: `UPPER`
- **Indentation**: 4 spaces, trailing commas.

### `.sqlfluffignore`
Specifies patterns excluded from SQL linting:
- `.git/`, `.venv/`, `node_modules/`, `build/`, `dist/`
- `external/` (third-party submodules & vendored checkouts)

---

## 3. Usage & CLI Automation

A centralized runner script is available at `scripts/sqlfluff_runner.py`. It automatically detects installed `sqlfluff` or falls back transparently to `uv tool run sqlfluff`.

### Linting
```bash
# Lint default project schemas (aios/databases/)
python scripts/sqlfluff_runner.py lint

# Lint specific file or directory
python scripts/sqlfluff_runner.py lint path/to/query.sql

# Lint with a custom dialect
python scripts/sqlfluff_runner.py lint path/to/schema.sql --dialect postgres
```

### Auto-Fixing
Automatically corrects formatting and layout violations:
```bash
python scripts/sqlfluff_runner.py fix aios/databases/
```

### Inspecting Rules & Dialects
```bash
python scripts/sqlfluff_runner.py rules
python scripts/sqlfluff_runner.py dialects
```

---

## 4. Pre-commit Hooks

Pre-commit hooks are configured in `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.3.1
    hooks:
      - id: sqlfluff-lint
        args: [--dialect, sqlite]
        files: ^aios/databases/.*\.sql$
      - id: sqlfluff-fix
        args: [--dialect, sqlite, --force]
        files: ^aios/databases/.*\.sql$
```

To install and run:
```bash
pre-commit install
pre-commit run --all-files
```

---

## 5. Continuous Integration (CI)

A GitHub Actions workflow is defined at `.github/workflows/sqlfluff.yml`. It triggers whenever SQL files or configuration files change:
- Uses `astral-sh/setup-uv` for fast dependency management.
- Runs `uv tool run sqlfluff lint aios/databases/ --dialect sqlite`.
- Blocks regressions from merging into `main`.

---

## 6. Verification & Tests

Unit tests are located in `tests/test_sqlfluff_runner.py`:
```bash
python -m pytest tests/test_sqlfluff_runner.py -v
```
