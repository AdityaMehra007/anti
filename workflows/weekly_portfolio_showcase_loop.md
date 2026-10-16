# WORKFLOW SPECIFICATION: Weekly Portfolio & LinkedIn Showcase Loop
**File**: `workflows/weekly_portfolio_showcase_loop.md`  
**Domain**: Portfolio Governance, Technical Showcase & Public Proof  
**Status**: APPROVED & SPECIFIED (Definition of Done Met)  
**Implementation Seam**: `e:/anti/AI-Command-Center/reports/PORTFOLIO_AUDIT.md` & `e:/anti/AI-Command-Center/automation/portfolio_showcase_generator.py`

---

## 1. Loop Profile & Overview
- **Objective**: Conduct a weekly automated audit of Aditya Mehra's code repositories (`github.com/AdityaMehra007`) and live web portfolio (`adi-digital-universe.ai.studio`), extract verifiable engineering and operational milestones, and formulate a high-credibility, non-sales LinkedIn update targeting Bengaluru corporate hiring managers.
- **Duration**: Total weekly human interaction $< 5$ minutes.
- **Ground Truth**: Zero buzzwords, zero inflated claims; 100% grounded in code commits, passing test suites, and empirical business metrics.
- **Output Brief**: `reports/WEEKLY_SHOWCASE_BRIEF.md` containing repository health scores, live link latency, and a formatted, ready-to-publish LinkedIn post.

---

## 2. Trigger
- **Mechanism**: Weekly Scheduled Trigger + On-Demand Command.
- **Schedule**: Fires every Friday at 05:00 PM IST (aligning with recruiter peak passive browsing hours).
- **On-Demand Command**: `python automation/portfolio_showcase_generator.py`.
- **Pre-Conditions**:
  - Git repository accessible.
  - Test report `tests/TEST_REPORT.md` present.

---

## 3. Autonomous Execution Pipeline (Pre-Checkpoint)

1. **Repository Health & Git Audit**:
   - Query git commit log for the preceding 7 days across the workspace.
   - Count files created, tests executed, and lines optimized.
   - Verify pinned repositories on GitHub profile: `anti`, `Aditya-Mehra`, `flagship-career-engine`, `Eventos-Omega`.
2. **Test Suite Telemetry Ingestion**:
   - Parse `tests/TEST_REPORT.md` to extract latest test pass rates and latency benchmarks.
3. **Career Pipeline Velocity Metrics**:
   - Query `career_vault.db` to extract:
     - Total jobs tracked and scored.
     - New applications submitted this week.
     - Active interview stages.
4. **Content Formulation (Humanized Technical Voice)**:
   - Formulate an executive LinkedIn update following the *Humanizer* discipline (eliminating AI clichés like "tapestry", "game-changer", "unravel", "delve").
   - Focus on concrete systems engineering applied to real-world operations (e.g. *building a deterministic 6-factor scoring engine for supply chain roles*, *automating vendor rate audits to recover 20% margin*).
5. **Brief Compilation**:
   - Write output to `reports/WEEKLY_SHOWCASE_BRIEF.md`.

---

## 4. Checkpoint (Push-Right)

The checkpoint is placed at the final publishing decision. The human does not draft text, calculate metrics, or format emojis.

### The Decision-Ready Brief
- **Surface**: `reports/WEEKLY_SHOWCASE_BRIEF.md` and console output.
- **Brief Contents**:
  - **Weekly Velocity Snapshot**: Commits pushed, test pass rate (12/12), total jobs indexed (110).
  - **Portfolio Health Status**: Live URL accessibility, ATS PDF resume download link check.
  - **Ready-to-Publish Post**: Complete LinkedIn post text with hashtags (`#OperationsResearch`, `#SupplyChain`, `#BengaluruJobs`, `#AIInOperations`).
  - **One-Click Action Link**: Direct link to LinkedIn post composer with text ready to paste.

### Human Action
1. Review brief and post draft (2 minutes).
2. Copy post text and publish on LinkedIn.
3. Check off weekly showcase milestone in `ROADMAP.md`.

---

## 5. Failure Modes & Edge Case Recovery

| Failure Mode | Autonomous Handling | Fallback |
| :--- | :--- | :--- |
| **No Git Commits This Week** | Shift post focus to an operational deep-dive case study (e.g. AERO India 2025 protocol logistics or Instawork CV labeling QA). | Generate educational operational teardown rather than build log. |
| **Test Suite Failing** | Flag regression in brief; suppress public showcase post until tests pass. | Output warning: *"Showcase halted: Fix failing tests in test_career_engine.py before public posting."* |

---

## 6. Definition of Done & Verification Criteria
- [x] Clear specification: Source, trigger, autonomous pipeline, checkpoint brief, and failure modes fully defined.
- [x] Generator implemented: `automation/portfolio_showcase_generator.py` produces clean briefs.
- [x] Audit report linked: `reports/PORTFOLIO_AUDIT.md` recommendations embedded.
- [x] Ready for hands-off execution: Implementer agent can run and maintain this cycle without questions.
