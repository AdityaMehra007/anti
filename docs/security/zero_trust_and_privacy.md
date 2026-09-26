# Security Baseline & Zero-Trust Architecture
**Directory:** `docs/security/`  
**Directives:** 38, 40, 77, 79, 125, 126 (ADI OMNI CODEX)  

## Key Security Mandates
1. **No Secret Leakage:** Never commit API keys, private tokens, or sensitive credentials to code or git repositories.
2. **Untrusted External Data:** All scraped job descriptions, external recruiter websites, and user uploads are treated as untrusted text.
3. **Prompt Injection Defense:** External JD text must never override system prompts or constitution directives.
4. **Human-in-the-Loop:** External submissions and messaging require human authorization.
