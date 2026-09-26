# AI Architecture & Prompt Standards
**Directory:** `docs/ai/`  
**Directives:** 32, 33, 34, 35, 213, 214 (ADI OMNI CODEX)  

## Model Routing Principles
1. **Task-Appropriate Sizing:** Use smaller/faster models for text sanitization, classification, and formatting; reserve high-reasoning models for multi-factor scoring and strategic analysis.
2. **Deterministic Schema Enforcement:** All LLM outputs generating career data or recruiter messages must adhere to strict JSON schemas or markdown templates.
3. **Zero Vibe Coding:** Prompts must specify exact input contexts and output constraints.
