# Specification: Build Your Own X (BYOX) — Autonomous Systems Engineering Suite

**Date**: 2026-09-29  
**Status**: Approved (Architectural Design)  
**Author**: Antigravity  
**Target Package**: `byox/`  

---

## 1. Executive Summary & Vision

The **Build Your Own X (BYOX)** suite provides a comprehensive, production-clean collection of fundamental computing systems reconstructed from first principles in pure Python (standard library only, zero external dependencies). 

Following the Richard Feynman maxim (*"What I cannot create, I do not understand"*), each system is engineered as a **Deep Module**: minimal and clean public interface, rich internal capability, zero vibe coding, and validated against formal RFCs and behavior test suites.

---

## 2. Core Architectural Principles

1. **Zero External Dependencies**: Standard library primitives only (`socket`, `struct`, `hashlib`, `zlib`, `selectors`, `math`, `sys`, `os`, `threading`, `time`). No `pip install` required; runs instantaneously on any Windows or Unix Python 3.10+ runtime.
2. **Deep Modules & Isolation**: Every system resides in its own isolated sub-package under `byox/<system>/` and can be used both as an importable library or executed via CLI.
3. **Behavioral Fidelity**: Each system adheres to the actual industry protocols and binary formats:
   - Git reads/writes real Git object format and zlib compression.
   - Redis speaks binary-safe RESP2 over TCP.
   - BitTorrent encodes/decodes bencode format and SHA-1 info_hashes.
   - Regex implements Thompson NFA evaluation in $O(M \times N)$ linear time without catastrophic backtracking.
   - Neural Net implements a full automatic differentiation computational graph (`Value` class + backprop) and trains an MLP from scratch.
4. **Unified Control Plane**: A single top-level entrypoint `python -m byox` provides an interactive shell, system selector, built-in demos, and test runner.

---

## 3. Package Structure

```
byox/
├── __init__.py
├── __main__.py               # Top-level CLI entrypoint
├── cli.py                    # Unified CLI command router & runner
│
├── git/                      # Git clone (content-addressable storage & porcelain)
│   ├── __init__.py
│   ├── objects.py            # Blobs, Trees, Commits, Tags, zlib, SHA-1
│   ├── repository.py         # .git layout, refs, HEAD, staging index
│   └── commands.py           # init, hash-object, cat-file, write-tree, commit, log, status
│
├── redis/                    # Redis clone (in-memory key-value + RESP)
│   ├── __init__.py
│   ├── protocol.py           # RESP2 serializer & deserializer
│   ├── store.py              # In-memory dict with TTL, Lists, Hashes, Sets
│   ├── server.py             # Event-driven TCP server (selectors / socket)
│   └── client.py             # Built-in lightweight RESP client
│
├── sqlite/                   # Relational database & B-Tree storage engine
│   ├── __init__.py
│   ├── lexer.py              # SQL tokenization
│   ├── parser.py             # Recursive descent parser for SQL subset
│   ├── btree.py              # Paged B-Tree / disk page manager
│   └── engine.py             # Table catalog, row serialization, query executor
│
├── shell/                    # Interactive Unix/POSIX-style shell
│   ├── __init__.py
│   ├── tokenizer.py          # Quoting (' and "), whitespace, operators
│   ├── builtins.py           # cd, pwd, echo, type, exit, export
│   └── execution.py          # PATH resolution, pipes (|), redirection (>, >>, 2>)
│
├── regex/                    # Non-backtracking Thompson NFA regex engine
│   ├── __init__.py
│   ├── ast.py                # Regex AST nodes (Char, Concat, Alt, Star, Plus, Opt)
│   ├── parser.py             # Shunting-yard / recursive descent regex parser
│   └── nfa.py                # Thompson NFA builder and state simulator
│
├── neural_net/               # Autograd engine & Multi-Layer Perceptron
│   ├── __init__.py
│   ├── engine.py             # Value node with backpropagation DAG & gradient tracking
│   ├── nn.py                 # Neuron, Layer, MLP architectures
│   └── optim.py              # SGD optimizer, Mean Squared Error, Binary Cross Entropy
│
├── web_server/               # HTTP/1.1 socket server
│   ├── __init__.py
│   ├── request.py            # HTTP request line, headers, and body parser
│   ├── response.py           # HTTP status codes, headers, chunked streaming
│   └── server.py             # Multi-threaded / keep-alive socket server & router
│
├── interpreter/              # S-Expression Lisp / Scheme interpreter
│   ├── __init__.py
│   ├── tokenizer.py          # S-expression token stream
│   ├── parser.py             # Parenthesized AST builder
│   ├── environment.py        # Nested lexical scope frames
│   └── evaluator.py          # eval/apply loop, lambdas, closures, recursion
│
├── bittorrent/               # BitTorrent protocol engine
│   ├── __init__.py
│   ├── bencode.py            # Bencode decoder and encoder (strings, ints, lists, dicts)
│   └── torrent.py            # .torrent metainfo file parser, info_hash, peer handshake
│
└── raytracer/                # 3D Software Raytracer & Renderer
    ├── __init__.py
    ├── vec3.py               # 3D Vector algebra (dot, cross, norm, unit)
    ├── geometry.py           # Ray, Sphere, Plane, Material (Lambertian, Metal)
    └── renderer.py           # Viewport camera, ray intersection loop, PPM/ASCII output
```

---

## 4. Subsystem Specifications

### 4.1 `byox.git`
- **Object Model**: Supports standard 4 object types (`blob`, `tree`, `commit`, `tag`). Format: `<type> <size>\0<content>` compressed with `zlib.compress` and keyed by 40-character hex SHA-1.
- **Repository Operations**:
  - `init`: Creates `.git/objects`, `.git/refs/heads`, and `.git/HEAD` pointing to `ref: refs/heads/main`.
  - `hash-object`: Computes SHA-1 and writes compressed object file.
  - `cat-file -p <hash>`: Uncompresses object and prints content.
  - `write-tree`: Scans working directory, writes blobs and directory trees recursively.
  - `commit-tree <tree-hash> -m <message> -p <parent-hash>`: Creates commit object with author, committer, timestamp, and GPG/parent metadata.
  - `log`: Walks commit parent pointers and renders git log.

### 4.2 `byox.redis`
- **Protocol (RESP2)**:
  - Simple Strings (`+OK\r\n`)
  - Errors (`-ERR ...\r\n`)
  - Integers (`:1000\r\n`)
  - Bulk Strings (`$6\r\nfoobar\r\n` or `$-1\r\n` for null)
  - Arrays (`*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n`)
- **Engine**:
  - In-memory key-value dictionary with monotonic millisecond TTL expiration.
  - Commands implemented: `PING`, `ECHO`, `SET` (with `PX` expiration), `GET`, `DEL`, `EXISTS`, `INCR`, `DECR`, `LPUSH`, `RPUSH`, `LPOP`, `RPOP`, `LRANGE`, `HSET`, `HGET`, `HGETALL`, `KEYS`.
  - TCP Server: Non-blocking or threaded socket server on port 6379 (configurable).

### 4.3 `byox.sqlite`
- **SQL Parser**:
  - `CREATE TABLE <name> (<col> <type>, ...)`
  - `INSERT INTO <name> VALUES (<val>, ...)`
  - `SELECT <cols> FROM <name> [WHERE <col> = <val>]`
- **Storage Engine**:
  - Page-based binary file storage (4096-byte pages) and in-memory fallback.
  - Slotted-page or B-Tree table leaf nodes with binary packing (`struct.pack`).
  - Catalog table tracking schemas and root page IDs.

### 4.4 `byox.shell`
- **REPL & Parsing**:
  - Supports quoting (`'single'` and `"double"` quotes, escaping).
  - Built-in commands: `cd`, `pwd`, `echo`, `type`, `which`, `exit`, `export`.
  - External command resolution via `PATH`.
  - I/O Redirection: `>` (overwrite), `>>` (append), `2>` (stderr).
  - Pipelines: arbitrary stages `cmd1 | cmd2 | cmd3` wired via OS pipes / subprocesses.

### 4.5 `byox.regex`
- **NFA Engine**:
  - Supports: Literals, Wildcard (`.`), Concatenation, Alternation (`|`), Zero-or-more (`*`), One-or-more (`+`), Optional (`?`), Character sets (`[a-z0-9]`), Negated sets (`[^a-z]`), Anchors (`^`, `$`).
  - Algorithm: Compiles expression into an ε-NFA (Thompson construction).
  - Evaluation: Maintains current active state set without backtracking, guaranteeing linear time matching $O(|pattern| \times |text|)$.

### 4.6 `byox.neural_net`
- **Autograd Engine (`Value`)**:
  - Scalar node tracking `data`, `grad`, `_prev` children, and `_op`.
  - Differentiable operations: `+`, `-`, `*`, `/`, `**`, `relu()`, `tanh()`, `sigmoid()`.
  - `backward()`: Topologically sorts graph and executes reverse-mode chain rule.
- **Neural Network Architecture**:
  - `Neuron`: Linear combination of inputs with weights and bias + non-linear activation.
  - `Layer`: Collection of parallel neurons.
  - `MLP`: Multi-layer perceptron mapping input dimensions to output dimensions.
  - Optimization: Mean squared error (MSE) loss and stochastic gradient descent step.

### 4.7 `byox.web_server`
- **HTTP Engine**:
  - Parser for HTTP/1.1 request line (Method, URI, HTTP version), headers dictionary, and request body.
  - Keep-Alive connection handling with timeout.
  - Chunked transfer decoding and encoding.
  - File router: Serves static files with correct MIME types (`text/html`, `application/json`, `text/plain`).
  - Programmatic router: Allows registering custom handler functions for paths.

### 4.8 `byox.interpreter`
- **Lisp / Scheme Engine**:
  - Tokenizer for numbers, symbols, strings, and parentheses.
  - Reader: Builds nested Python lists representing S-expressions.
  - Environment: Lexical frame with parent lookup for variable resolution.
  - Special forms: `define`, `set!`, `if`, `lambda`, `begin`, `quote`, `cond`.
  - Standard library: `+`, `-`, `*`, `/`, `=`, `<`, `>`, `car`, `cdr`, `cons`, `list`, `null?`, `print`.

### 4.9 `byox.bittorrent`
- **Bencode & Metainfo**:
  - Complete bencode parser (`bdecode`) and serializer (`bencode`): integers (`i...e`), byte strings (`length:...`), lists (`l...e`), dictionaries (`d...e`).
  - Torrent metadata extraction: `announce` URL, `piece length`, `pieces` SHA-1 array, `name`, `length`.
  - Info hash: SHA-1 digest of the raw bencoded `info` dictionary.
  - Peer wire protocol framing: Handshake packet construction (`\x13BitTorrent protocol...`).

### 4.10 `byox.raytracer`
- **3D Graphics Engine**:
  - Vector math module (`Vec3`): addition, scalar multiplication, dot product, cross product, normalization.
  - Ray-sphere intersection geometry solving quadratic form $t^2 d \cdot d + 2t d \cdot (o - c) + (o - c) \cdot (o - c) - R^2 = 0$.
  - Shading model: Surface normals, diffuse Lambertian shading, ambient light, and specular highlights.
  - Output: Direct PPM image format writer (viewable anywhere or convertible to PNG) and terminal ANSI ASCII renderer.

---

## 5. Unified CLI & Interactive Dashboard

The command-line interface `byox` allows interacting with any of the 10 systems:
- `python -m byox test`: Run all verification test suites across all 10 modules.
- `python -m byox git [init|add|commit|log|cat-file]`: Run the Git clone.
- `python -m byox redis [--port 6379]`: Start the Redis RESP server.
- `python -m byox sqlite [--db file.db]`: Open the interactive SQL database shell.
- `python -m byox shell`: Launch the interactive Unix/POSIX shell.
- `python -m byox regex "<pattern>" "<text>"`: Test regex match and print NFA state graph.
- `python -m byox neural-net [--demo]`: Train an MLP on binary classification with live loss logging.
- `python -m byox web-server [--port 8080]`: Launch the HTTP/1.1 server.
- `python -m byox lisp [--repl]`: Open the interactive Lisp REPL.
- `python -m byox bittorrent <file.torrent>`: Inspect and verify a torrent file.
- `python -m byox raytracer [--ascii] [--output render.ppm]`: Render a 3D scene.

---

## 6. Testing & Quality Gateways

- Every module must have a corresponding test suite in `tests/test_<module>.py`.
- 100% automated test pass rate with standard `unittest` / `pytest`.
- Zero third-party packages required for running tests or modules.
