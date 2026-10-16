# ARCHITECTURAL DECISION RECORDS (ADRs)

**System:** Google Antigravity Workstation Command Center  
**Status:** Adopted & Active  

---

## ADR-001: Execution & Data Placement on `E:\` Drive
- **Status:** Accepted
- **Context:** System drive `C:\` has 26.13 GB free, whereas `E:\` has 314.63 GB free. Writing large caches, node modules, virtual environments, or model checkpoints to `C:\` risks OS disk starvation.
- **Decision:** All new development repositories, virtual environments, databases, and model weights must reside strictly within `E:\anti\` and `E:\anti\AI-Command-Center\`. Environment variables (`HF_HOME`, `OLLAMA_MODELS`) redirect any cache directory to `E:\`.
- **Consequences:** Eliminates risk of OS slowdowns or crashes on `C:\`. Maximizes available storage runway.

---

## ADR-002: Cloud-First Analytical Reasoning with Lean Local AI Fallback
- **Status:** Accepted
- **Context:** The machine is powered by an Intel i7-6700HQ with 16 GB RAM (3.67 GB available under standard desktop load) and an NVIDIA GTX 960M (4 GB VRAM, Maxwell architecture). Heavy local models (7B, 13B+) cannot fit into 4 GB VRAM and will spill into RAM, creating extreme thermal throttling, latency, or out-of-memory crashes.
- **Decision:** Utilize Google Antigravity and Gemini cloud endpoints for primary reasoning, complex code generation, and multi-agent workflows. Limit local Ollama inference to compact, quantized models ($\le 3$B parameters, such as Llama 3.2 1B/3B Q4) strictly for offline parsing and PII redaction.
- **Consequences:** Zero laptop thermal strain during heavy coding sessions. Preserves system responsiveness while maintaining private offline fallback capability.

---

## ADR-003: SQLite Embedded Database for Data & Job State
- **Status:** Accepted
- **Context:** Managing hundreds of job openings, corporate target matrices, recruiter logs, and application events requires relational integrity, rapid querying, and deduplication.
- **Decision:** Implement an embedded SQLite database (`career_vault.db`) with strict UNIQUE indexes on `(job_id)` and `(normalized_url)`.
- **Consequences:** Zero external daemon processes (unlike PostgreSQL or MySQL). Zero memory footprint when idle. Single-file portability and instant ACID transaction safety.

---

## ADR-004: Six-Factor Job Scoring Rubric with Hard Disqualification Gates
- **Status:** Accepted
- **Context:** Traditional job scrapers flood candidates with hundreds of low-relevance leads or sales roles disguised as business operations.
- **Decision:** Implement a deterministic 100-point scoring algorithm evaluating:
  1. *Eligibility & Fresher Suitability (25 pts)*
  2. *Education & Experience Alignment (25 pts)*
  3. *Non-Sales Role Fidelity (15 pts)*
  4. *Technical & Operational Skill Match (15 pts)*
  5. *Long-Term Career Growth Potential (10 pts)*
  6. *Location / Bangalore Hub Alignment (10 pts)*
  In addition, any role requiring mandatory 3+ years experience or cold-calling quota is flagged with an explicit Disqualification Warning, preventing misleading overall scores.
- **Consequences:** Guarantees that high-scoring opportunities represent actionable, high-probability applications for Aditya Mehra's profile.

---

## ADR-005: Strict Ground-Truth Evidence Integrity (Zero Hallucination)
- **Status:** Accepted
- **Context:** AI career generators often invent fake metrics, inflated past titles, or unverified technical skills, damaging candidate credibility in executive background checks.
- **Decision:** All resume bullets, portfolio summaries, and outreach communications must strictly derive from the verified evidence ledger (`CAREER_PROFILE_MASTER.md`), grounded in concrete documented achievements (Dayananda Sagar University BBA, 300+ events delivered, AERO India 2025, Instawork AI Data Ops, Pencil Mark BD commendation).
- **Consequences:** 100% auditable career assets. Absolute consistency across LinkedIn, portfolio, and submitted resumes.
