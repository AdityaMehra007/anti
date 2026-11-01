# HIRING WITHOUT WHITEBOARDS — MASTER STRATEGY & PLAYBOOK
## Canonical Practical Engineering Hiring Intelligence (761 Employers Analyzed)

**Repository Origin**: [`poteto/hiring-without-whiteboards`](https://github.com/poteto/hiring-without-whiteboards)  
**Curator**: Lauren Tan ([@poteto](https://github.com/poteto))  
**Analysis & Automation Engine**: `hiring_without_whiteboards_engine.py`  
**Mission Control Cockpit**: `hiring_without_whiteboards_cockpit.html` (`http://localhost:8780`)  
**Data Exports**: `data/hiring_without_whiteboards.json`, `data/hiring_without_whiteboards.csv`, `data/hiring_without_whiteboards.sqlite`  

---

## 1. Executive Summary & Philosophy

For over a decade, traditional tech hiring has been dominated by algorithmic gatekeeping: dynamic programming puzzles on dry-erase boards, memorizing LeetCode tricks, and inverting binary trees in high-stress interrogations.

### Why Whiteboard Hazing Fails
1. **Zero Predictive Validity**: Inverting a binary tree or memorizing Dijkstra's algorithm bears virtually zero correlation with building distributed web APIs, handling database deadlocks, refactoring legacy components, or diagnosing production latency.
2. **Massive False Negatives**: Highly skilled senior engineers who spend their careers shipping resilient systems routinely fail trivia interviews because they haven't spent 6 months grinding competitive programming platforms.
3. **Selection for Test-Prep Over Craftsmanship**: Whiteboards select for candidates who have excess leisure time to memorize algorithm patterns rather than engineers who write clean, testable, maintainable code.

### The Non-Whiteboard Paradigm
The 761 companies documented in this registry evaluate candidates on **work that mirrors daily production reality**:
- Writing code in their **own IDE** with normal tools (linters, documentation, search engines).
- Designing systems by evaluating **concrete trade-offs** (latency, cost, maintainability) rather than puzzles.
- Collaborating with future teammates on **actual bug fixes or feature refactors**.
- Paid trials where candidates are compensated for their time and evaluated on real output.

---

## 2. Empirical Statistics (761 Companies Analyzed)

```
Total Vetted Employers Cataloged:    761 (100.0%)
------------------------------------------------------------------
📦 Take-Home Practical Projects:     522 (68.6%)
👥 Live Collaborative Pairing:       193 (25.4%)
🌐 Remote-Friendly Pipelines:        290 (38.1%)
🏛️ Architecture & Systems Design:    89 (11.7%)
🔍 Past-Work / Code Walkthroughs:    41 (5.4%)
💰 Paid Trials / Micro-Sprints:      32 (4.2%)
```

### Geographic Distribution
- **North America**: ~380 employers (SF Bay Area, New York, Austin, Seattle, Boston, Chicago, Denver, Toronto, Montreal).
- **Europe & UK**: ~260 employers (London, Berlin, Amsterdam, Paris, Warsaw, Stockholm, Zurich, Dublin).
- **India & APAC**: ~85 employers (Bengaluru, Mumbai, Delhi-NCR, Singapore, Tokyo, Sydney).
- **Latin America & Global Remote**: ~36 employers (São Paulo, Bogotá, Mexico City, distributed worldwide).

---

## 3. The 5 Practical Assessment Archetypes & How to Ace Them

### Archetype 1: The Take-Home Assignment (68.6% of companies)
*Examples: Airtable, Algolia, Adyen, BrowserStack, Zerodha, Deliveroo, Docker teams.*

In a take-home, interviewers do not care if your code uses clever one-liners. They evaluate **production hygiene**, maintainability, and clarity.

#### The Take-Home Gold Standard Checklist:
1. **Self-Documenting Architecture (`README.md`)**:
   - Provide clear setup instructions: `make start` or `docker-compose up`.
   - Explicitly list dependencies and minimum runtime versions.
   - **Trade-Offs & Decisions Section**: Explain *why* you chose a given database, framework, or architectural pattern.
   - **Scaling Section**: Detail how you would scale the service from 100 QPS to 100,000 QPS (caching layers, read-replicas, partitioning, message queues).
2. **Comprehensive Test Suite**:
   - Include unit tests for core domain logic.
   - Include integration tests verifying HTTP endpoints and database transactions.
   - Include test fixtures / mock data.
3. **Environment & Containerization**:
   - Include a clean `Dockerfile` and `docker-compose.yml`.
   - Include `.env.example` with sensible defaults.
4. **Timebox Discipline**:
   - Never spend 40 hours on an unpaid 4-hour take-home.
   - Deliver a rock-solid core feature with tests, and document bonus features in a `FUTURE_IMPROVEMENTS.md` file.

---

### Archetype 2: Live Collaborative Pair Programming (25.4% of companies)
*Examples: CircleCI, Avant, Bocoup, Bustle, Cultivate, Echobind.*

Pair programming is **not** a live exam; it is an audition for a co-worker. The interviewer wants to know what it feels like to sit next to you on a Wednesday afternoon when an edge case breaks.

#### Pairing Rules of Engagement:
1. **Verbalize Your Mental Model Continuously**:
   - *"I'm going to start by writing a failing test for the zero-length input edge case."*
   - *"I'm choosing a hash map here to keep lookups O(1), but let's verify if memory overhead is a concern."*
2. **Treat the Interviewer as a Teammate**:
   - Ask clarifying questions: *"Does our API contract require returning a 404 or an empty array when no records match?"*
   - Solicit input: *"What do you think of this schema layout?"*
3. **Search Documentation Naturally**:
   - If you forget an API method or library syntax, don't panic. Open browser tabs, search official MDN or Python docs, and explain what you are checking.
4. **Clean Git Commits**:
   - Commit logically as you progress (`feat: implement token parser`, `test: add invalid header cases`).

---

### Archetype 3: Paid Working Trials & Micro-Sprints (4.2% of companies)
*Examples: Automattic, Buffer, DuckDuckGo, Development Seed, Elvie, Culture Foundry.*

These companies hire by paying you an hourly or project rate to work on actual tasks for 1 to 45 days.

#### How to Excel in Paid Trials:
- **Async Communication Cadence**: Post morning standup notes and end-of-day summaries outlining what was shipped, blockers, and next steps.
- **Micro-PRs**: Break large tasks into small, easily reviewable PRs (under 300 lines).
- **Respect Repository Conventions**: Mirror existing code formatting, naming patterns, and test frameworks strictly.

---

### Archetype 4: Past Project & Code Walkthroughs (5.4% of companies)
*Examples: Basecamp, Botika, Double Nines, Crownstone, DataMade.*

You bring code you have written in the past (an open-source project, a side hustle, or anonymized production code) and walk through its anatomy.

#### The STAR-Architecture Framework:
- **Situation**: What business problem or technical constraint did this system solve?
- **Task / Responsibility**: What specific modules or architecture did you own?
- **Action & Trade-Offs**: Why did you choose PostgreSQL over MongoDB? Why gRPC over REST? What alternatives were discarded?
- **Result & Production Failures**: What failed in production? How did you debug the issue? What would you redesign today?

---

### Archetype 5: Practical System Architecture Discussions (11.7% of companies)
*Examples: Checkr, ASOS, Able, Capgemini, Clarisights.*

Unlike standard whiteboard trivia, practical system design focuses on real business models (e.g. designing a ride-sharing dispatch queue, webhook ingestion pipeline, or subscription billing reconciliation engine).

#### The 5-Step System Design Flow:
1. **Scope Requirements**: Read vs Write ratio, SLA targets (99.99%), latency thresholds, data retention policies.
2. **High-Level Data Flow**: Clients -> CDN/Load Balancer -> API Gateway -> Microservices -> Data Stores -> Async Message Brokers.
3. **Data Schema & Storage Choices**: Relational consistency vs Key-Value throughput.
4. **Failure Domains & Resilience**: Circuit breakers, retry policies with exponential backoff, dead-letter queues (DLQs), idempotency keys.
5. **Observability & Alerting**: Distributed tracing (OpenTelemetry), Prometheus metrics, P95/P99 latency monitors.

---

## 4. Tailored Cold Outreach & InMail Playbook

When contacting engineering managers or recruiters at companies that don't whiteboard, highlight this shared philosophy. It immediately differentiates you from generic applicants.

### Template 1: Direct to Engineering Manager / Tech Lead
```
Subject: Practical engineering & [Company Name]'s architecture

Hi [First Name],

I noticed that [Company Name]'s engineering team has discarded whiteboard hazing in favor of practical, real-world engineering evaluations. That respect for software craftsmanship and day-to-day reality strongly resonates with my background.

Over the past [X] years, I've focused on building resilient [Backend / Full-Stack / Cloud] systems in [Python / Go / TypeScript / Rust]. Rather than spending months memorizing LeetCode puzzles, I prioritize what actually moves production forward: clean system boundaries, automated test coverage, sensible database modeling, and high team velocity.

I've been following [Company Name]'s work on [specific product/feature], and I'd love to learn more about the challenges your team is solving this quarter.

Are you open to a brief 15-minute chat next week?

Best regards,

[Your Name]
[GitHub URL] | [LinkedIn URL] | [Portfolio URL]
```

### Template 2: Direct to Talent Acquisition / Technical Recruiter
```
Subject: [Your Name] <> [Target Role] at [Company Name]

Hi [Recruiter Name],

I came across [Company Name]'s open [Senior/Staff Software Engineer] role and was thrilled to see your practical, work-simulated interview loop. It's refreshing to see teams evaluate engineers on actual day-to-day code rather than whiteboard trivia.

A brief snapshot of what I bring:
• [Achievement 1: e.g., Scaled microservices handling 25k req/sec with 99.99% uptime]
• [Achievement 2: e.g., Led migration to Kubernetes & Terraform reducing deploy times by 65%]
• [Achievement 3: e.g., Deep expertise in Python, Go, PostgreSQL, and distributed systems]

I would love to be considered for the role and participate in your practical assessment process.

Resume attached. Let me know if you have availability for an introductory call.

Best,

[Your Name]
```

---

## 5. Master Directory: Top 40 Practical Employers by Category

### Top Remote-First SaaS Pioneers
1. **Airtable**: Practical take-home + collaborative architecture onsite.
2. **Automattic**: Short code challenge + paid production trial project.
3. **Basecamp**: Past work & portfolio review.
4. **Buffer**: Code walkthrough + 45-day paid contract trial.
5. **CircleCI**: Take-home + pairing on real CircleCI bug fixes.
6. **DuckDuckGo**: Up to two paid projects + technical video calls.
7. **GitLab**: Asynchronous technical assessments and team calls.
8. **Doist**: Team interviews + real-world take-home programming assignment.
9. **Buildkite**: Anonymized writing assessment + live pairing on daily work.
10. **ConvertKit**: Short coding/writing task + technical discussion.

### Top European & UK Tech Leaders
1. **Adyen** (Amsterdam): Take-home assignment + design discussion.
2. **Algolia** (Paris): Take-home project + onsite presentation.
3. **Contentful** (Berlin): Real-world coding challenge with open internet access.
4. **DICE** (Stockholm): Practical take-home + code review.
5. **ASOS** (London): Refactoring exercise + software craftsmanship walkthrough.
6. **Allegro** (Warsaw): Take-home project + real-world architecture problem solving.
7. **Doctolib** (Paris/Berlin): Take-home + half-day working with feature team.
8. **Bitpanda** (Vienna/Krakow): Take-home assignment + deep technical chat.
9. **Auto1** (Berlin): Skype technical discussion + take-home challenge.
10. **Dare** (London): Pair programming and real architecture discussion.

### Top India & APAC Practical Employers
1. **Zerodha** (Bengaluru): Technical conversation + practical take-home task.
2. **BrowserStack** (Mumbai/Dublin): Two 2-hour practical assignments (open internet allowed).
3. **Acko** (Mumbai): Phone interview + take-home + live pairing session.
4. **Atlan** (New Delhi): 8-day mini-project + team discussion + founder call.
5. **Devfolio** (Bangalore): Small take-home problem + pair programming session.
6. **Adaface** (Bangalore/Singapore): On-the-job conversational technical assessment.
7. **Clarisights** (Bangalore): System design & low-level design based on real data flows.
8. **AMAGI** (Makati/Tokyo): GitHub profile review + real-world problem solving discussion.
9. **Cookpad** (Tokyo/Bristol): Discussion of technical experience + remote pairing.
10. **EFishery** (Bandung): Take-home challenge + architecture presentation.

---

## 6. Local Systems & Tools in This Repository

1. **Mission Control Cockpit**:
   - File: `hiring_without_whiteboards_cockpit.html`
   - Run: `START_HIRING_WITHOUT_WHITEBOARDS_COCKPIT.bat` or `python hiring_without_whiteboards_engine.py --serve 8780`
   - Opens at: `http://localhost:8780`
2. **CLI Engine**:
   - `python hiring_without_whiteboards_engine.py --search "Airtable"`
   - `python hiring_without_whiteboards_engine.py --stats`
   - `python hiring_without_whiteboards_engine.py --build`
3. **Database & Structured Files**:
   - SQLite DB: `data/hiring_without_whiteboards.sqlite` (with FTS5 search index)
   - JSON Catalog: `data/hiring_without_whiteboards.json` (761 records)
   - CSV Dataset: `data/hiring_without_whiteboards.csv`
