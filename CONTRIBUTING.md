# Contributing to OMEGA Platform & Autonomous Engines

Thank you for your interest in contributing to the **OMEGA Autonomous Engineering Ecosystem**!

This project adheres to a strict standard of **Zero Vibe Sloppiness**: we embrace high-speed AI-assisted development ("Vibe Coding"), but we enforce uncompromising engineering rigor, deterministic schemas, and hermetic automated testing.

---

## 🛠️ Contribution Workflow

1. **Fork the Repository:** Create a feature branch (`git checkout -b feature/your-feature-name`).
2. **Implement with Clear Specifications:**
   * Write deep modules with simple, robust interfaces.
   * Do not add unnecessary dependencies or speculative abstractions.
   * Adhere to existing coding conventions across Python, SQL, and Markdown.
3. **Run the Hermetic Test Suite:**
   All 16 core tests must pass with zero regressions:
   ```bash
   pytest tests/test_auto_apply_pipeline.py tests/test_recruiter_dispatcher.py tests/test_interview_cockpit.py -v
   ```
4. **Commit with Conventional Messages:**
   * `feat(...)`: New autonomous capabilities, dispatchers, or parsers.
   * `fix(...)`: Bug fixes or cross-platform compatibility patches.
   * `docs(...)`: Documentation and architectural diagrams.
   * `test(...)`: New unit or integration test cases.
5. **Open a Pull Request:** Provide a clear description of the problem solved and test results.

---

## 🔒 Security Standards

* **No Secrets:** Never commit `.env` files, API tokens, bearer keys, or sensitive recruiter correspondence.
* **Hermetic Tests:** Tests should run offline without requiring external network access or live API calls.
* **Cross-Platform:** Ensure code runs seamlessly on both Windows and Linux environments.

Thank you for building high-leverage autonomous systems with us!
