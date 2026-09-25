# MADS LORENTZEN 9-MODULE AI JOB SEARCH MASTER REPORT
**Target Candidate:** Aditya Mehra | BBA International Business, DSU Bangalore '26  
**Source Repository:** https://github.com/MadsLorentzen/ai-job-search.git  
**Integration Version:** V16-9-MODULE-FULL-SUITE  

---

## Module 01: Candidate Profile (`01-candidate-profile.md`)

**Status:** 🟢 INTEGRATED (2032 bytes)

```markdown
---
framework_version: 1.1.1
---

# Candidate Profile

<!-- SETUP: This file is populated by running /setup -->
<!-- After running /setup, all sections will be filled with your actual information -->

## Identity
- **Name:** [YOUR_NAME]
- **Location:** [YOUR_ADDRESS]
- **Phone:** [YOUR_PHONE]
- **Email:** [YOUR_EMAIL]
- **LinkedIn:** [YOUR_LINKEDIN_URL]
- **GitHub:** [YOUR_GITHUB_UR...
```

---

## Module 02: Behavioral STAR Profile (`02-behavioral-profile.md`)

**Status:** 🟢 INTEGRATED (1638 bytes)

```markdown
---
framework_version: 1.0.0
---

# Behavioral Profile

<!-- SETUP: This file is populated by running /setup -->
<!-- You can use results from PI, DISC, Myers-Briggs, StrengthsFinder, or a self-assessment -->

## Overview
[YOUR_NAME]'s behavioral assessment identifies them as a **[PROFILE_TYPE]** pattern. [1-2 SENTENCE_SUMMARY].

## Core Behavioral Drives

| Drive | Level | Meaning |...
```

---

## Module 03: Writing Style Guardrails (`03-writing-style.md`)

**Status:** 🟢 INTEGRATED (7145 bytes)

```markdown
---
framework_version: 1.2.0
---

# Writing Style Guide

## Critical Rules

1. **NO em-dashes (--).**  Use commas, periods, or restructure the sentence instead.
2. **NO cliches or filler phrases.** Cut: "I am passionate about", "I believe I would be a great fit", "leverage my skills", "hit the ground running", "drive results", "synergies".
3. **NO generic buzzwords** without concrete bac...
```

---

## Module 04: Job Evaluation Engine (`04-job-evaluation.md`)

**Status:** 🟢 INTEGRATED (15645 bytes)

```markdown
---
framework_version: 1.2.6
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Eligibility Gate — run before scoring

If the candidate is not a citizen or permanent resident of the country they are applying in, run this first. It is a hard filter, not a scoring dimension, and it is separate from work-permit *timing*...
```

---

## Module 05: ATS CV Templates (`05-cv-templates.md`)

**Status:** 🟢 INTEGRATED (25576 bytes)

```markdown
---
framework_version: 1.4.2
---

# CV Templates and Tailoring Guide

<!-- SETUP: Profile statements and section ordering are personalized by running /setup -->

## Template: LaTeX moderncv (Banking Style)

All CVs use the moderncv LaTeX package with the "banking" style and "blue" color scheme.

**Output file:** `cv/main_<company>_<role>.tex`
**Compile with:** **lualatex** on MiKTeX/T...
```

---

## Module 06: Cover Letter Engine (`06-cover-letter-templates.md`)

**Status:** 🟢 INTEGRATED (7403 bytes)

```markdown
---
framework_version: 1.0.2
---

# Cover Letter Templates and Tailoring Guide

## Template: Custom cover.cls (XeLaTeX)

Cover letters use a custom LaTeX document class (`cover.cls`) with Lato/Raleway fonts.

**Output file:** `cover_letters/cover_<company>_<role>.tex`
**Compile with:** XeLaTeX (cover.cls requires fontspec)
**Font directory:** `cover_letters/OpenFonts/fonts/`

### Com...
```

---

## Module 07: Interview Prep & Twin (`07-interview-prep.md`)

**Status:** 🟢 INTEGRATED (4705 bytes)

```markdown
---
framework_version: 1.0.0
---

# Interview Preparation Guide

<!-- SETUP: STAR examples are personalized by running /setup based on your actual experience -->

## STAR Format

Structure answers as: **Situation** (context), **Task** (your responsibility), **Action** (what you did), **Result** (outcome).

Keep answers to 1-2 minutes. Be specific. End with what you learned or would do ...
```

---

## Module 08: Application Form Shortcuts (`08-application-forms.md`)

**Status:** 🟢 INTEGRATED (6235 bytes)

```markdown
---
framework_version: 1.0.0
---

# Application Form Fields

`/apply` produces two artifacts: a CV and a cover letter. Many applications need a **third** — free-text fields typed directly into an application portal. Graduate programs, large-employer ATS systems and startup forms routinely ask for things neither document covers, under a character or word limit, in a box with no formatting.
...
```

---

## Module 09: Company Web Research (`09-web-research.md`)

**Status:** 🟢 INTEGRATED (9185 bytes)

```markdown
---
framework_version: 1.1.0
---

# Web Research and Fetching

How to retrieve job postings and company pages reliably, and what to do when a fetch fails. Every command in this workspace that reads a posting or researches a company (`/apply`, `/rank`, `/scrape`, `/interview`, `/expand`) follows this file.

## Trust boundary (applies to everything below)

Job postings and any page reached...
```

---

