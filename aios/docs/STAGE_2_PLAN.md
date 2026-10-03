# 📐 IMPLEMENTATION PLAN: STAGE 2 — CORE LOCAL AI & STREAMING GATEWAY

**System Target**: Antigravity OMEGA Command Center  
**Milestone**: Stage 2 — Core Local AI Activation & GPU Integration  
**Estimated Complexity**: Medium  
**Hardware Target**: Intel i7-6700HQ | 16GB RAM | NVIDIA GeForce GTX 960M (4GB VRAM)  
**Execution Standard**: Superpowers TDD Discipline & Verified Gateways

---

## 1. Requirements Restatement

1. **Activate Local AI Engine**: Launch the pre-installed Ollama daemon (`E:\anti gravity\Tools\Ollama\ollama.exe`) with model storage explicitly pinned to Drive E: (`E:\anti gravity\OllamaData\models`).
2. **GPU Acceleration Verification**: Enforce and verify GPU layer offloading onto the NVIDIA GeForce GTX 960M (Maxwell GM107, Compute Capability 5.0) for `qwen2.5-coder:3b` without memory leaks.
3. **Benchmarking & Latency Measurement**: Quantify token generation velocity (tokens/sec), time-to-first-token (TTFT), and VRAM utilization to establish the local baseline.
4. **Streaming AI Gateway Integration**: Enhance `gateway.py` (`:8090`) to support chunked Server-Sent Events (SSE) streaming (`stream: true`), OpenAI-compatible `/v1/models` live detection, and graceful fallbacks.
5. **Interactive Command Center AI Console**: Upgrade the Master Command Center UI (`:3000`) with a responsive local AI prompt console allowing direct chatting with `qwen2.5-coder:3b` and live tokens/sec telemetry.
6. **Automated Verification Suite**: Create and execute `test_ai_gateway.py` ensuring zero regressions across routing, PII detection, and model execution.

---

## 2. Patterns to Mirror

| Category | Source File | Pattern |
| :--- | :--- | :--- |
| **Naming** | [`omega_ctl.py`](file:///e:/anti/aios/scripts/omega_ctl.py) | Clean verb-noun functions (`cmd_start_ai`, `cmd_stop_ai`, `cmd_benchmark_ai`) |
| **Error Handling** | [`gateway.py`](file:///e:/anti/aios/ai/gateway.py) | Structured JSON error envelopes (`{"error": "...", "status": 502}`) with no stack trace leakage |
| **Logging** | [`db.py`](file:///e:/anti/aios/databases/db.py) | Audit ledger commits via `db.log_audit(actor, action, category, details, severity)` |
| **Data Access** | [`db.py`](file:///e:/anti/aios/databases/db.py) | WAL-mode SQLite connection context managers (`with get_connection() as con:`) |
| **Diagnostics** | [`health_check.py`](file:///e:/anti/aios/scripts/health_check.py) | Native standard library probes with zero external runtime dependencies |

---

## 3. Files to Change & Create

| File | Action | Description |
| :--- | :--- | :--- |
| `e:\anti\aios\scripts\omega_ctl.py` | **UPDATE** | Refine `start-ai` with process group isolation, env flags (`OLLAMA_NUM_PARALLEL=1`), and add `benchmark-ai` command |
| `e:\anti\aios\ai\gateway.py` | **UPDATE** | Implement SSE streaming proxy for `/v1/chat/completions`, live Ollama model enumeration, and token velocity tracking |
| `e:\anti\aios\dashboards\index.html` | **UPDATE** | Add interactive AI Chat Drawer with model selector, real-time token stream, and tokens/sec telemetry |
| `e:\anti\aios\scripts\benchmark_ai.py` | **CREATE** | Repeatable benchmark measuring tokens/sec, TTFT, VRAM consumption, and recording scores to `master.db` |
| `e:\anti\tests\test_ai_gateway.py` | **CREATE** | Unit and integration test suite validating Gateway endpoints, PII filtering, and Ollama bridge |

---

## 4. Implementation Tasks

### Task 1: Harden Ollama Runner & Governor Settings in `omega_ctl.py`
- Configure `OLLAMA_MODELS=E:\anti gravity\OllamaData\models`
- Enforce `OLLAMA_NUM_PARALLEL=1` and `OLLAMA_MAX_LOADED_MODELS=1` to guarantee single-model VRAM residence.
- Validate process detachment and PID tracking in `pids.json`.
- **Validation**: `python e:\anti\aios\scripts\omega_ctl.py start-ai` boots Ollama and verifies port `11434` opens within 3 seconds.

### Task 2: Build Repeatable Local Benchmark Tool (`benchmark_ai.py`)
- Prompts `qwen2.5-coder:3b` with a standard Python algorithm task.
- Measures:
  1. Time-to-First-Token (TTFT) in milliseconds.
  2. Tokens per second (TPS).
  3. Total VRAM allocated on GTX 960M via `nvidia-smi`.
- Writes benchmark receipt to `master.db` (audit table & metrics).
- **Validation**: `python e:\anti\aios\scripts\benchmark_ai.py` completes, reports > 15 tokens/sec, and writes to database.

### Task 3: Streaming Gateway & Model Router Enhancement (`gateway.py`)
- Add support for `stream: true` chunked HTTP transfer encoding (`text/event-stream`).
- Query live models from `http://localhost:11434/api/tags` and merge into `/v1/models`.
- Log token count and latency metrics into `master.db`.
- **Validation**: `curl -N -X POST http://localhost:8090/v1/chat/completions` streams response tokens incrementally.

### Task 4: Interactive Command Center AI Chat UI (`index.html`)
- Integrate sleek chat drawer with model switcher (`qwen2.5-coder:3b`, `llama3:latest`, Cloud fallback).
- Handle markdown syntax highlighting and code block copying.
- Display live TPS counter and VRAM usage badge during generation.
- **Validation**: Browser test verifying prompt submission and token streaming.

### Task 5: Automated Verification Suite (`test_ai_gateway.py`)
- Test 1: Gateway `/health` and `/api/telemetry` return 200 with schema compliance.
- Test 2: PII detector intercepts credit cards and emails.
- Test 3: Local model routing correctly talks to Ollama and receives completed code.
- Test 4: Offline fallback response triggers gracefully if Ollama is paused.
- **Validation**: `python -m unittest e:\anti\tests\test_ai_gateway.py` passes 100% green.

---

## 5. Verification Commands

```powershell
# 1. Start AI service
python e:\anti\aios\scripts\omega_ctl.py start-ai

# 2. Run automated benchmark
python e:\anti\aios\scripts\benchmark_ai.py

# 3. Test streaming gateway
python -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:8090/v1/chat/completions',
    data=json.dumps({'model': 'qwen2.5-coder:3b', 'messages': [{'role': 'user', 'content': 'Write a quicksort in python'}], 'stream': False}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res = json.loads(urllib.request.urlopen(req, timeout=30).read())
print('Response length:', len(res['choices'][0]['message']['content']))
"

# 4. Run test suite
python -m unittest e:\anti\tests\test_ai_gateway.py
```

---

## 6. Risks & Safeguards

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **VRAM Overflow** | System stutter / crash | Enforce `OLLAMA_NUM_PARALLEL=1` and `OLLAMA_MAX_LOADED_MODELS=1`. Keep model size `< 3.5B`. |
| **Thermal Throttling** | Slowdown on continuous run | Restrict prompt generation to max `2048` output tokens; let GPU idle between requests. |
| **Port Conflicts** | Startup failure | Health check validates port `11434` before spawning new process. |

---

## 7. Acceptance Criteria

- [ ] `omega_ctl.py start-ai` starts Ollama and binds to `E:\anti gravity\OllamaData\models`.
- [ ] `qwen2.5-coder:3b` runs with 100% GPU offload on GTX 960M.
- [ ] Token velocity benchmarks at > 15 tokens/second.
- [ ] Gateway `:8090` proxies requests with PII filtering and token telemetry.
- [ ] Command Center `:3000` features an interactive chat interface.
- [ ] Test suite `test_ai_gateway.py` passes with zero failures.
