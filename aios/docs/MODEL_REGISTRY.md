# ANTIGRAVITY OMEGA :: MODEL REGISTRY

**Version**: 1.0.0  
**Last Updated**: 2026-10-01  
**Authority**: Supreme Constitution Directives & AI Architect  
**Status**: ACTIVE & VERIFIED  

---

## 1. Executive Summary

This registry governs all local and cloud AI models permitted to operate within the ANTIGRAVITY OMEGA ecosystem. In strict adherence to the **Hardware Profile (GTX 960M 4GB VRAM, 16GB DDR4 RAM)** and **Ponytail Minimalism**, models are divided into operational safety zones:

- **🟢 GREEN (Safe Routine Execution)**: 1B–3.8B parameters. 100% offload to NVIDIA Maxwell GM107 GPU. Sub-2GB VRAM footprint.
- **🟡 YELLOW (On-Demand / Staged)**: 7B–8B parameters. Partial GPU offload with CPU spillover. High RAM pressure.
- **🔴 RED (Prohibited on Hardware)**: > 14B local parameters. Exceeds host capacity; routed to Cloud Adapters.

---

## 2. Active Model Registry Matrix

| Model Identifier | Parameter Count | Quantization | Download Size | VRAM (Allocated) | Offload Layers | Speed (TPS) | TTFT | Safety Zone | Primary Purpose | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:3b`** | 3.09B | Q4_K_M | 1.93 GB | 1,834 MB | **37 / 37 (100%)** | **10.53** | 1,790 ms | 🟢 GREEN | Coding, API design, Refactor, TDD | **ACTIVE** |
| **`fable5:latest`** | 8.03B | Q4_0 | 4.66 GB | ~2,800 MB | 16 / 33 (48%) | ~3.80 | 4,200 ms | 🟡 YELLOW | Conversational prose, storytelling | **STANDBY** |
| **`llama3:latest`** | 8.03B | Q4_0 | 4.66 GB | ~2,800 MB | 16 / 33 (48%) | ~3.50 | 4,500 ms | 🟡 YELLOW | Broad instruction following, summarization | **STANDBY** |
| **`gemini-2.0-flash`** | Frontier | Cloud API | 0 MB Local | 0 MB | Cloud | > 80.0 | ~350 ms | 🟢 CLOUD | High-speed multi-step synthesis, RAG | **ROUTED** |
| **`claude-3-5-sonnet`**| Frontier | Cloud API | 0 MB Local | 0 MB | Cloud | > 50.0 | ~600 ms | 🟢 CLOUD | Deep architecture, complex refactors | **ROUTED** |

---

## 3. Detailed Model Specifications

### 3.1 `qwen2.5-coder:3b` (Primary Local Engine)
- **Provider**: Alibaba Cloud / Qwen Team
- **Architecture**: Qwen2 Causal LM (GGUF format)
- **Base Digest**: `f72c60cabf6237b07f6e632b2c48d533cef25eda2efbd34bed21c5e9c01e6225`
- **Context Length**: 32,768 tokens (configured to 8,192 default context to conserve VRAM)
- **Hardware Footprint**:
  - Model Buffer: 1,834 MB in GTX 960M GDDR5 VRAM
  - Compute Buffer: 556 MB
  - Total VRAM: 2,390 MB (leaving 1.7 GB free VRAM headroom)
- **Benchmarked Performance**:
  - Throughput: **10.53 tokens/second**
  - Time To First Token (TTFT): **1,790.5 milliseconds**
  - Prompt Processing Velocity: **59.2 tokens/second**
- **License**: Apache 2.0 (Permissive for commercial and private local deployment)
- **Verified Capabilities**: Unit test generation, Python 3.13 stdlib scripts, bug triage, JSON schema validation.

### 3.2 `fable5:latest` & `llama3:latest` (Yellow Zone Assistive Models)
- **Provider**: Meta AI / Community fine-tunes
- **Architecture**: Llama-3 8B
- **Context Length**: 8,192 tokens
- **Hardware Footprint**: Exceeds single-GPU 4GB physical buffer. Ollama splits layers between GPU and CPU host RAM via OpenBLAS/cuBLAS fallback.
- **Operating Policy**: Keep unloaded during standard system operation. Load only when specific 8B instruction nuances are required, and unload immediately afterwards (`keep_alive=0`).
- **License**: Meta Llama 3 Community License.

---

## 4. Planned Capabilities & Embedding Tier

| Capability | Target Model / Engine | Footprint | Evaluation Rationale |
| :--- | :--- | :--- | :--- |
| **Local Vector Embeddings** | `bge-small-en-v1.5` / `nomic-embed-text` | ~274 MB | Fast, dense embedding for local documentation RAG. Fits entirely in VRAM alongside Qwen Coder. |
| **Speech-to-Text (STT)** | `whisper.cpp` (Base/Small) | ~140 MB | Local transcription with minimal CPU overhead. |
| **Text-to-Speech (TTS)** | `piper-tts` (en_US-lessac) | ~60 MB | Fast, zero-dependency neural TTS running purely on CPU. |
| **Vision Analysis** | Cloud Routed (`gemini-2.0-flash`) | 0 MB Local | Visual tokens require extensive memory. Routing to cloud maintains local system responsiveness. |

---

## 5. Model Lifecycle & Hygiene Rules

1. **VRAM Preservation**: `OLLAMA_MAX_LOADED_MODELS=1` is enforced across all configurations. Never load two models simultaneously into VRAM.
2. **Idle Unload**: `OLLAMA_KEEP_ALIVE=15m` unloads inactive models to return VRAM to the operating system and GPU desktop renderer.
3. **Restricted Storage**: Storage location is permanently set to `E:\anti gravity\OllamaData\models` on Drive E:. No weights may reside on Drive C:.
4. **Verification Gate**: Any new model must pass `scripts/benchmark_ai.py` and achieve at least 8.0 TPS before being certified for routine automation.
