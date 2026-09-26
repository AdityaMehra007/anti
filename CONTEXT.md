# Ubiquitous Language & Project Context (CONTEXT.md)

This document standardizes the domain vocabulary across the workspace. Agents and developers must use these terms consistently without inventing synonyms.

---

## 1. Core System Architecture

- **Career OS / Omega Platform**: The centralized autonomous career intelligence and execution operating system that manages candidate positioning, job matching, recruiter discovery, and application delivery.
- **Truth Layer**: The tamper-evident evidence registry verifying all experience claims (`EXP-001` through `EXP-009`) against concrete historical artifacts, preventing hallucination or false claims.
- **Omega Dispatcher**: The deterministic orchestrator dispatching tailored CVs, cover letters, and outreach sequences according to rate limits and verification gates.
- **Sovereign Engine**: The background daemon and autopilot continuous loop executing scheduled search, enrichment, and pipeline updates.

---

## 2. Data Structures & Pipelines

- **Target Matrix**: The deduplicated database of corporate targets (e.g. `Master_4500_Unique_Companies_Deduplicated.csv` and Fortune 500 subsets) enriched with industry, location, and HR contacts.
- **HR Directory Master**: Verified recruiter, talent acquisition, and hiring manager contact records across Bangalore, India, and global hubs.
- **Referral Map**: Graph mapping candidate alumni connections and mutual LinkedIn networks to verified target opportunities.
- **Tracer-Bullet Ticket**: A minimal vertical slice ticket with explicit dependency edges (`Blocked by:`) that delivers observable end-to-end functionality.

---

## 3. Skills & Agent Taxonomy

- **Master Skill Matrix**: The normalized taxonomy of 300+ primary professional competencies spanning 5 key tracks:
  1. *Business Development & B2B Sales*
  2. *International Trade, EXIM & Global Logistics*
  3. *AI & Agent Infrastructure Operations*
  4. *Software Engineering, Cloud & DevOps*
  5. *Brand Activation & Growth Marketing*
- **Matt Pocock Engineering Skills**: Standardized agent capabilities for grilling, architecture design, TDD, code review, and issue tracking installed in `.agents/skills/`.
- **Model-Invoked Skill**: An autonomous discipline skill (e.g. `tdd`, `diagnosing-bugs`) triggered automatically by the agent when conditions are met.
- **User-Invoked Skill**: An orchestration skill (e.g. `/grill-me`, `/wayfinder`, `/triage`) triggered explicitly by user command.

---

## 4. Engineering Disciplines & Boundaries

- **Deep Module**: A software module that provides extensive functionality behind a small, simple, and stable interface (minimizing surface complexity).
- **Seam**: A clean boundary between two components where behavior can be observed, mocked, or tested without modifying implementation internals.
- **Grilling Frontier**: The active set of open design decisions whose prerequisites are settled and can be questioned immediately without guesswork.
- **Red-Green-Refactor Loop**: The strict test-driven development loop: write a failing test first $\rightarrow$ write minimal code to pass $\rightarrow$ refactor while green.
