# Build Your Own X (BYOX) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construct a production-grade, zero-dependency suite of 10 fundamental systems from scratch in pure Python standard library with 100% automated test coverage and a unified CLI runner.

**Architecture:** Monolithic multi-module architecture with deep modules (`byox.<system>`), shared zero-dependency standards, cross-platform Windows compatibility, and unified CLI command dispatch.

**Tech Stack:** Python 3.10+ standard library (`socket`, `struct`, `hashlib`, `zlib`, `selectors`, `math`, `sys`, `os`, `threading`, `time`, `unittest`).

**Spec:** [`docs/superpowers/specs/2026-09-29-build-your-own-x-suite-design.md`](file:///e:/anti/docs/superpowers/specs/2026-09-29-build-your-own-x-suite-design.md)

## Global Constraints
- Zero external dependencies: stdlib only (no pip dependencies required).
- 100% test pass rate across all modules using `python -m unittest discover tests`.
- Cross-platform Windows & Unix compatibility (handle CRLF/LF, paths with `pathlib.Path` or `os.path`).
- Clean separation of concerns with deep modules and single-responsibility source files.

---

### Task 1: Package Scaffolding & Unified CLI Router

**Files:**
- Create: `byox/__init__.py`
- Create: `byox/__main__.py`
- Create: `byox/cli.py`
- Create: `tests/__init__.py`
- Create: `tests/test_scaffolding.py`

**Interfaces:**
- Produces: `byox.cli.main(argv=None) -> int`, `byox.cli.run_all_tests() -> int`

- [ ] **Step 1: Write test for package scaffolding and CLI entrypoint**
```python
# tests/test_scaffolding.py
import unittest
from byox.cli import main

class TestScaffolding(unittest.TestCase):
    def test_cli_help(self):
        code = main(["--help"])
        self.assertEqual(code, 0)
        
    def test_cli_version(self):
        code = main(["--version"])
        self.assertEqual(code, 0)
```

- [ ] **Step 2: Run test to verify it fails**
Run: `python -m unittest tests/test_scaffolding.py`
Expected: FAIL (No module named 'byox')

- [ ] **Step 3: Implement package initialization and CLI dispatcher**
Implement `byox/__init__.py`, `byox/__main__.py`, and `byox/cli.py` supporting `test`, `help`, `version`, and system subcommands.

- [ ] **Step 4: Run test to verify it passes**
Run: `python -m unittest tests/test_scaffolding.py`
Expected: PASS

- [ ] **Step 5: Commit**
`git add byox tests; git commit -m "feat(byox): initialize package scaffolding and unified CLI"`

---

### Task 2: Git from Scratch (`byox.git`)

**Files:**
- Create: `byox/git/__init__.py`
- Create: `byox/git/objects.py`
- Create: `byox/git/repository.py`
- Create: `byox/git/commands.py`
- Create: `tests/test_git.py`

**Interfaces:**
- Produces:
  - `GitObject`: `serialize() -> bytes`, `deserialize(data: bytes)`
  - `Blob(GitObject)`, `Tree(GitObject)`, `Commit(GitObject)`
  - `Repository(path)`: `init()`, `hash_object(data, write=True) -> str`, `cat_file(sha) -> tuple[str, bytes]`, `write_tree() -> str`, `commit(tree_sha, message, parent=None) -> str`, `log() -> list[dict]`

- [ ] **Step 1: Write test for Git object storage and repository operations**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement Git objects, compression, hashing, repository layout, and porcelain commands**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 3: Redis from Scratch (`byox.redis`)

**Files:**
- Create: `byox/redis/__init__.py`
- Create: `byox/redis/protocol.py`
- Create: `byox/redis/store.py`
- Create: `byox/redis/server.py`
- Create: `byox/redis/client.py`
- Create: `tests/test_redis.py`

**Interfaces:**
- Produces:
  - `RESPParser.parse(buffer: bytes) -> tuple[Any, int]`
  - `RESPSerializer.encode(value: Any) -> bytes`
  - `DataStore`: `get(key)`, `set(key, val, px=None)`, `delete(key)`, `incr(key)`, `lpush/rpush/lrange`, `hset/hget/hgetall`
  - `RedisServer(host, port)`: `start()`, `stop()`
  - `RedisClient(host, port)`: `execute(*args)`

- [ ] **Step 1: Write unit tests for RESP protocol encoding/decoding and in-memory store**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement RESP serializer/deserializer, data store with TTL, socket server and client**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 4: Shell from Scratch (`byox.shell`)

**Files:**
- Create: `byox/shell/__init__.py`
- Create: `byox/shell/tokenizer.py`
- Create: `byox/shell/builtins.py`
- Create: `byox/shell/execution.py`
- Create: `tests/test_shell.py`

**Interfaces:**
- Produces:
  - `tokenize(cmd: str) -> list[str]`
  - `ShellContext`: `execute_line(line: str) -> int`, `cd(path)`, `pwd()`, `echo(*args)`
  - Pipeline & redirection evaluator: `execute_pipeline(stages)`

- [ ] **Step 1: Write test for shell tokenization (quotes, escapes), builtins, and redirection**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement tokenizer, builtins, PATH resolution, redirection, and pipeline execution**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 5: Regex Engine from Scratch (`byox.regex`)

**Files:**
- Create: `byox/regex/__init__.py`
- Create: `byox/regex/ast.py`
- Create: `byox/regex/parser.py`
- Create: `byox/regex/nfa.py`
- Create: `tests/test_regex.py`

**Interfaces:**
- Produces:
  - `RegexParser.parse(pattern: str) -> RegexNode`
  - `NFA.compile(ast: RegexNode) -> NFA`
  - `match(pattern: str, text: str) -> bool`
  - `find(pattern: str, text: str) -> Optional[tuple[int, int]]`

- [ ] **Step 1: Write test for regex patterns (literals, `.`, `*`, `+`, `?`, `|`, `[a-z]`, `^`, `$`)**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement regex AST, parser with operator precedence, Thompson NFA and state set step simulator**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 6: Neural Network & Autograd from Scratch (`byox.neural_net`)

**Files:**
- Create: `byox/neural_net/__init__.py`
- Create: `byox/neural_net/engine.py`
- Create: `byox/neural_net/nn.py`
- Create: `byox/neural_net/optim.py`
- Create: `tests/test_neural_net.py`

**Interfaces:**
- Produces:
  - `Value(data: float)`: `+`, `-`, `*`, `/`, `**`, `relu()`, `tanh()`, `backward()`
  - `Neuron(nin)`, `Layer(nin, nout)`, `MLP(nin, nouts)`
  - `SGD(parameters, lr)`: `step()`, `zero_grad()`
  - `mse_loss(predictions, targets) -> Value`

- [ ] **Step 1: Write test for automatic differentiation graph, backpropagation, and MLP parameter update**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement scalar autograd engine, neurons/layers/MLP, and optimizer**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 7: SQLite / Relational DB from Scratch (`byox.sqlite`)

**Files:**
- Create: `byox/sqlite/__init__.py`
- Create: `byox/sqlite/lexer.py`
- Create: `byox/sqlite/parser.py`
- Create: `byox/sqlite/btree.py`
- Create: `byox/sqlite/engine.py`
- Create: `tests/test_sqlite.py`

**Interfaces:**
- Produces:
  - `SQLLexer.tokenize(sql: str) -> list[Token]`
  - `SQLParser.parse(tokens) -> Statement`
  - `BTreeEngine(filepath)`: `insert(key, value)`, `search(key)`
  - `Database(filepath=None)`: `execute(sql: str) -> list[dict]`

- [ ] **Step 1: Write test for SQL tokenization, AST parsing, and execute CREATE/INSERT/SELECT**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement SQL lexer, recursive parser, paged B-Tree / table storage, and query execution engine**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 8: HTTP/1.1 Web Server from Scratch (`byox.web_server`)

**Files:**
- Create: `byox/web_server/__init__.py`
- Create: `byox/web_server/request.py`
- Create: `byox/web_server/response.py`
- Create: `byox/web_server/server.py`
- Create: `tests/test_web_server.py`

**Interfaces:**
- Produces:
  - `HTTPRequest`: `method`, `path`, `query_params`, `headers`, `body`
  - `HTTPResponse`: `status_code`, `headers`, `body`, `to_bytes()`
  - `HTTPServer(host, port)`: `route(path, methods)` decorator, `serve_static(dir)`, `start()`, `stop()`

- [ ] **Step 1: Write test for HTTP request parsing, routing, response serialization, and static file serving**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement request/response parser, router, socket server with keep-alive support**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 9: Lisp / Scheme Interpreter from Scratch (`byox.interpreter`)

**Files:**
- Create: `byox/interpreter/__init__.py`
- Create: `byox/interpreter/tokenizer.py`
- Create: `byox/interpreter/parser.py`
- Create: `byox/interpreter/environment.py`
- Create: `byox/interpreter/evaluator.py`
- Create: `tests/test_interpreter.py`

**Interfaces:**
- Produces:
  - `tokenize(chars: str) -> list[str]`
  - `parse(program: str) -> Any`
  - `Environment(params, args, outer)`
  - `eval_lisp(x: Any, env: Environment) -> Any`
  - `run(program: str) -> Any`

- [ ] **Step 1: Write test for Lisp parsing, arithmetic, variable definitions, lambdas, and recursion**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement tokenizer, S-expression parser, lexical environment, evaluator, and REPL**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 10: BitTorrent Protocol from Scratch (`byox.bittorrent`)

**Files:**
- Create: `byox/bittorrent/__init__.py`
- Create: `byox/bittorrent/bencode.py`
- Create: `byox/bittorrent/torrent.py`
- Create: `tests/test_bittorrent.py`

**Interfaces:**
- Produces:
  - `bdecode(data: bytes) -> tuple[Any, int]`
  - `bencode(obj: Any) -> bytes`
  - `Torrent(path_or_bytes)`: `announce`, `piece_length`, `pieces`, `info_hash_bytes`, `info_hash_hex`, `create_handshake(peer_id) -> bytes`

- [ ] **Step 1: Write test for Bencode decoding/encoding (int, string, list, dict) and torrent info_hash computation**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement Bencode parser, serializer, and Torrent metainfo parser**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 11: 3D Raytracer from Scratch (`byox.raytracer`)

**Files:**
- Create: `byox/raytracer/__init__.py`
- Create: `byox/raytracer/vec3.py`
- Create: `byox/raytracer/geometry.py`
- Create: `byox/raytracer/renderer.py`
- Create: `tests/test_raytracer.py`

**Interfaces:**
- Produces:
  - `Vec3(x, y, z)`: vector operations (+, -, *, dot, cross, length, unit)
  - `Ray(origin, direction)`
  - `Sphere(center, radius, color, specular)`
  - `Scene`: `add(object)`, `render_ppm(width, height) -> str`, `render_ascii(width, height) -> str`

- [ ] **Step 1: Write test for 3D vector algebra, ray-sphere intersection, and image rendering output**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement vector mathematics, geometric primitives, lighting calculations, PPM, and ASCII renderers**
- [ ] **Step 4: Run test to verify passing**
- [ ] **Step 5: Commit**

---

### Task 12: Unified CLI Commands, Interactive Demos, and Verification

**Files:**
- Modify: `byox/cli.py`
- Create: `tests/test_cli.py`
- Create: `README_BYOX.md`

**Interfaces:**
- Produces: Complete interactive CLI support for all 10 systems + full test suite passing

- [ ] **Step 1: Write end-to-end CLI command tests**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Wire all 10 systems into CLI subcommands, add rich interactive demos, and compile comprehensive documentation**
- [ ] **Step 4: Run full test suite (`python -m byox test` and `python -m unittest discover tests`)**
- [ ] **Step 5: Commit**
