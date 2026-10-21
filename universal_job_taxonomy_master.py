#!/usr/bin/env python3
"""
universal_job_taxonomy_master.py - Universal Master Job & JD Taxonomy (13 Families, 35 Archetypes)
=================================================================================================
Authoritative, structured knowledge base covering every major global industry sector and job archetype:
  1. Software Engineering & Systems Architecture
  2. AI, Machine Learning & Data Systems
  3. Product Management & UX/UI Product Design
  4. Cybersecurity, InfoSec & Regulatory Compliance
  5. Corporate Finance, Investment Banking, FP&A & Treasury
  6. B2B Commercial Sales, Revenue Operations & Sales Engineering
  7. Growth Marketing, Technical SEO & Brand Activation
  8. Global Operations, Supply Chain, Logistics & EXIM
  9. People Operations, HR Business Partnering & Technical Recruiting
  10. Executive Leadership, Founders Office & Chief of Staff
  11. Customer Success, Solutions Architecture & Support Engineering
  12. Healthcare, Clinical Data & BioTech Informatics
  13. Management Consulting & Enterprise Advisory

Exports to:
  - data/universal_job_taxonomy_master.json
  - data/universal_job_taxonomy.sqlite
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional

DATA_DIR = Path(r"e:\anti\data")
JSON_EXPORT_PATH = DATA_DIR / "universal_job_taxonomy_master.json"
SQLITE_DB_PATH = DATA_DIR / "universal_job_taxonomy.sqlite"

UNIVERSAL_JOB_TAXONOMY: Dict[str, Any] = {
    "metadata": {
        "title": "OMEGA Universal Master Job & JD Taxonomy",
        "version": "3.0.0",
        "total_families": 13,
        "total_roles": 35,
        "standard_levels": [
            {"code": "L1", "name": "Intern / Fresher / Trainee", "exp_years": "0-1"},
            {"code": "L2", "name": "Associate / Junior Specialist", "exp_years": "1-3"},
            {"code": "L3", "name": "Mid-Level Professional", "exp_years": "3-5"},
            {"code": "L4", "name": "Senior Professional / Specialist", "exp_years": "5-8"},
            {"code": "L5", "name": "Lead / Staff / Principal", "exp_years": "8-12"},
            {"code": "L6", "name": "Director / Head of Function", "exp_years": "12-15"},
            {"code": "L7", "name": "VP / C-Suite Executive", "exp_years": "15+"}
        ]
    },
    "families": {
        "software_engineering": {
            "name": "Software Engineering & Systems Architecture",
            "description": "Designing, building, testing, deploying, and maintaining resilient scalable software systems.",
            "roles": {
                "frontend_engineer": {
                    "title": "Frontend Engineer",
                    "aliases": ["UI Engineer", "Web Developer", "React Developer", "Client-Side Engineer", "Frontend Architect"],
                    "description": "Architects high-performance, accessible, responsive client-side web applications and interactive interfaces.",
                    "hard_skills": ["TypeScript", "JavaScript (ES6+)", "React.js", "Next.js", "HTML5/CSS3", "Tailwind CSS", "Redux/Zustand", "Webpack/Turbopack/Vite", "REST/GraphQL APIs", "Web Vitals & Performance", "Jest/Playwright"],
                    "soft_skills": ["Design Empathy", "Cross-Functional Collaboration", "Attention to Detail", "Continuous Learning", "Usability Advocacy"],
                    "ats_keywords": ["TypeScript", "React", "Next.js", "Virtual DOM", "Server-Side Rendering (SSR)", "State Management", "TailwindCSS", "CSS Modules", "Responsive Design", "Accessibility (WCAG 2.1)", "Core Web Vitals", "Lighthouse", "Jest", "Playwright", "Webpack", "Vite", "RESTful APIs", "GraphQL"],
                    "sample_kpis": ["First Contentful Paint (FCP) < 1.2s", "Largest Contentful Paint (LCP) < 2.5s", "Cumulative Layout Shift (CLS) < 0.1", "100% WCAG 2.1 AA compliance", "Zero regression bugs on client releases"],
                    "typical_responsibilities": [
                        "Build modular, testable UI components adhering to corporate design systems.",
                        "Optimize client bundle size, code-splitting, tree-shaking, and asset delivery pipelines.",
                        "Collaborate with Product Managers and UX Designers to translate Figma wireframes into pixel-perfect interfaces.",
                        "Implement state management, client caching, and optimistic UI mutations.",
                        "Maintain robust automated unit, integration, and E2E test suites with Jest and Playwright."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Describe a situation where a frontend application suffered from poor performance. How did you diagnose and resolve it?",
                            "competency": "Performance Optimization & Diagnostic Rigor",
                            "trap": "Vague answers like 'I optimized code'. Need specific metrics, profiling tools, and root causes.",
                            "model_defense": "S: In our checkout flow, users experienced an LCP of 4.8s causing a 14% cart dropoff. T: Reduce LCP below 2.0s without removing marketing widgets. A: Profiled using Chrome DevTools Performance tab and Lighthouse; identified unnecessary heavy re-renders in the basket state and unoptimized 3MB hero images. Replaced heavy component tree with memoized selectors, lazy-loaded offscreen chunks, and converted assets to WebP with next/image responsive srcsets. R: Dropped LCP to 1.4s, improved Lighthouse score from 41 to 94, and increased conversion rate by 6.2%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master local build pipelines, setup dev environment, deliver first 3 bug fixes and 1 scoped feature PR.",
                        "day_60": "Own an end-to-end user flow, contribute reusable tokens to the design system, and write automated E2E tests.",
                        "day_90": "Lead frontend performance audit, mentor junior teammates, and champion Core Web Vitals optimization across the codebase."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.0L - ₹28.0L LPA",
                        "us_usd": "$105,000 - $185,000/yr",
                        "remote_usd": "$75,000 - $145,000/yr"
                    }
                },
                "backend_engineer": {
                    "title": "Backend Engineer",
                    "aliases": ["Server-Side Engineer", "API Engineer", "Distributed Systems Engineer", "Java/Go/Python Engineer"],
                    "description": "Designs, implements, and maintains scalable distributed server systems, databases, APIs, and microservices.",
                    "hard_skills": ["Python", "Go", "Java", "Node.js", "PostgreSQL", "MySQL", "Redis", "Kafka/RabbitMQ", "Docker", "REST & gRPC", "System Design", "Database Indexing & Query Tuning"],
                    "soft_skills": ["Architectural Rigor", "Root-Cause Debugging", "Systems Thinking", "Trade-Off Analysis", "Documentation Integrity"],
                    "ats_keywords": ["Microservices", "RESTful APIs", "gRPC", "PostgreSQL", "Redis", "Distributed Systems", "Kafka", "Docker", "Kubernetes", "Database Optimization", "ACID", "Concurrency", "High Availability", "OAuth2/JWT", "CI/CD", "AWS/GCP"],
                    "sample_kpis": ["P99 API Latency < 150ms", "99.99% system availability", "Zero data loss during peak load failovers", "Zero unindexed slow queries in production"],
                    "typical_responsibilities": [
                        "Architect and deploy resilient microservices and REST/gRPC endpoints.",
                        "Design relational and NoSQL database schemas with strict foreign keys and query indexing.",
                        "Build asynchronous event-driven streaming pipelines using Kafka or RabbitMQ.",
                        "Manage distributed transactions, idempotent endpoints, and caching layers with Redis.",
                        "Implement centralized logging, Prometheus metrics, and distributed tracing."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you handle a massive traffic spike or distributed deadlock in production?",
                            "competency": "High Concurrency & Distributed Resiliency",
                            "trap": "Blaming external services or relying only on adding more server RAM.",
                            "model_defense": "S: During a flash sale event, our payment ledger backend hit 100% database CPU, causing thread pool exhaustion and API timeouts. T: Restore transaction throughput within 30 minutes and prevent ledger inconsistency. A: Inspected pg_stat_activity, found unindexed row-locking SELECT FOR UPDATE queries causing deadlocks. Implemented a Redis-based distributed token bucket rate limiter, converted pessimistic locks to optimistic version checks with exponential backoff, and queued payment reconciliations into Kafka. R: Reduced DB CPU to 38%, eliminated timeouts, and processed 45,000 concurrent orders with 0 duplicate transactions."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Understand database ER diagrams, API schemas, deployment pipelines; deploy first tested microservice endpoint.",
                        "day_60": "Refactor a high-latency query or pipeline, implement caching and integration tests, participate in on-call rotation.",
                        "day_90": "Architect a new microservice or data stream from scratch with full RFC, ADR, and observability dashboards."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹8.0L - ₹34.0L LPA",
                        "us_usd": "$120,000 - $210,000/yr",
                        "remote_usd": "$85,000 - $160,000/yr"
                    }
                },
                "fullstack_engineer": {
                    "title": "Full Stack Engineer",
                    "aliases": ["Full Stack Developer", "Software Engineer (Full Stack)", "Product Engineer"],
                    "description": "Bridges frontend user experience and robust backend architectures, delivering complete end-to-end features.",
                    "hard_skills": ["TypeScript/JavaScript", "React/Next.js", "Node.js/Python/Go", "PostgreSQL", "REST & GraphQL", "Tailwind CSS", "Docker", "Git/CI-CD", "Prisma/TypeORM", "Redis"],
                    "soft_skills": ["Product Sense", "Speed of Execution", "Full-Lifecycle Ownership", "Pragmatism"],
                    "ats_keywords": ["Full Stack", "TypeScript", "React", "Next.js", "Node.js", "Python", "PostgreSQL", "Prisma", "TailwindCSS", "REST APIs", "GraphQL", "Docker", "Full-Lifecycle", "Microservices", "Unit Testing"],
                    "sample_kpis": ["Cycle time from PRD to production < 7 days", "Zero critical security flaws", "99.9% uptime for feature microservices"],
                    "typical_responsibilities": [
                        "Deliver complete user-facing features touching React frontends, Node/Python backends, and SQL schemas.",
                        "Maintain API contracts, validation layers (Zod), and database migrations.",
                        "Deploy containerized applications with Docker and automated CI/CD pipelines."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Walk me through how you built and launched a full stack product feature from database to UI in record time.",
                            "competency": "End-to-End Delivery & Pragmatic Engineering",
                            "trap": "Ignoring testing or database migration safety.",
                            "model_defense": "S: Customer churn increased due to lack of a self-serve subscription portal. T: Build and deploy the portal end-to-end in 10 business days. A: Designed the schema in PostgreSQL with Prisma migrations; implemented Stripe Webhook listeners in Node.js with idempotent event processing; constructed a responsive Tailwind/React dashboard with optimistic UI updates; wrote automated Playwright tests verifying billing state transitions. R: Shipped on day 8; reduced manual billing support tickets by 62% in the first 30 days."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Ship first full-stack bug fix and feature flag; understand DB schema and frontend state patterns.",
                        "day_60": "Deliver an independent full-stack feature; establish automated integration tests.",
                        "day_90": "Own an entire functional subsystem; improve CI/CD build speeds by 25%."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹8.0L - ₹32.0L LPA",
                        "us_usd": "$115,000 - $200,000/yr",
                        "remote_usd": "$80,000 - $155,000/yr"
                    }
                },
                "devops_platform_engineer": {
                    "title": "DevOps & Platform Engineer",
                    "aliases": ["Site Reliability Engineer (SRE)", "Infrastructure Engineer", "Cloud Architect", "Cloud Operations Engineer"],
                    "description": "Automates cloud infrastructure, CI/CD delivery pipelines, container orchestration, and telemetry networks.",
                    "hard_skills": ["Kubernetes", "Docker", "Terraform", "AWS/GCP/Azure", "CI/CD (GitHub Actions/GitLab)", "Linux/Bash", "Prometheus", "Grafana", "ArgoCD", "Networking & DNS", "Ansible"],
                    "soft_skills": ["Calm Under Fire", "Automation First Mindset", "Safety Guardrails", "Cross-Team Enablement"],
                    "ats_keywords": ["Kubernetes", "Terraform", "Infrastructure as Code (IaC)", "Docker", "AWS", "GCP", "CI/CD", "Helm", "GitOps", "Prometheus", "Grafana", "ArgoCD", "Linux Administration", "VPC", "TLS/SSL", "Zero Downtime Deployments"],
                    "sample_kpis": ["Deployment frequency > 10x/day", "Mean Time to Recovery (MTTR) < 15 mins", "Infrastructure cloud cost reduction by > 20%", "Zero security vulnerabilities in base images"],
                    "typical_responsibilities": [
                        "Provision multi-region infrastructure using modular Terraform and GitOps.",
                        "Maintain Kubernetes clusters, ingress controllers, service meshes, and auto-scaling pods.",
                        "Build secure automated CI/CD pipelines with integrated SAST/DAST security scanning.",
                        "Implement SLA/SLO monitoring, PagerDuty alerting, and Prometheus metric exporters.",
                        "Enforce principle of least privilege IAM roles and encrypted secrets management."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Tell me about a catastrophic production outage you resolved. What did you change to make sure it never happens again?",
                            "competency": "Incident Management & Blameless Postmortem",
                            "trap": "Focusing on who caused the error instead of systemic fail-safes.",
                            "model_defense": "S: A corrupted Kubernetes ingress manifest deployed during working hours severed all traffic to our primary customer portal. T: Mitigate the outage immediately and eliminate single-point-of-failure deployment risks. A: Rolled back the deployment using ArgoCD within 3 minutes. Conducted a blameless postmortem. Implemented automated PR linting with kubeval and conftest OPA policies, and enforced canary blue/green deployments with automatic rollback triggers tied to 5xx error rate thresholds. R: Prevented future catastrophic deployments and cut rollback MTTR from 20 minutes to 45 seconds."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Audit existing IaC repositories, map VPC networks and security groups, automate manual deployment toil.",
                        "day_60": "Upgrade cluster components, optimize Docker image build caching, establish centralized logging/alerting.",
                        "day_90": "Implement complete GitOps workflow, conduct disaster recovery game-day simulation, deliver 15% cloud cost optimization."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹9.0L - ₹38.0L LPA",
                        "us_usd": "$130,000 - $225,000/yr",
                        "remote_usd": "$95,000 - $175,000/yr"
                    }
                },
                "mobile_engineer": {
                    "title": "Mobile Engineer (iOS / Android / React Native)",
                    "aliases": ["iOS Developer", "Android Developer", "React Native Engineer", "Flutter Developer"],
                    "description": "Constructs high-performance, fluid native and cross-platform mobile experiences for iOS and Android.",
                    "hard_skills": ["Swift/SwiftUI", "Kotlin/Jetpack Compose", "React Native", "Flutter", "Mobile Architecture (MVVM/MVI)", "Core Data / Room / SQLite", "REST & WebSockets", "App Store & Google Play Deployment", "CI/CD for Mobile (Fastlane)"],
                    "soft_skills": ["Obsession with Frame Rates", "Touch Precision", "Device Diversity Awareness"],
                    "ats_keywords": ["Swift", "SwiftUI", "Kotlin", "Jetpack Compose", "React Native", "Flutter", "iOS", "Android", "Fastlane", "App Store Submission", "Mobile CI/CD", "Offline First", "Crashlytics"],
                    "sample_kpis": ["App launch time < 800ms", "Crash-free sessions > 99.8%", "60fps smooth scrolling performance"],
                    "typical_responsibilities": [
                        "Architect mobile application features with clean separation of presentation and business layers.",
                        "Implement offline-first caching, local database synchronizations, and background push notifications.",
                        "Manage automated build pipelines and release management via Fastlane and App Store Connect."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you diagnose and resolve a severe memory leak or UI stutter on older mobile devices?",
                            "competency": "Mobile Memory Profiling & Frame Budgeting",
                            "trap": "Testing only on high-end flagships.",
                            "model_defense": "S: Users on budget Android devices reported severe frame drops and crashes when scrolling image-heavy feeds. T: Eliminate OOM crashes and maintain stable 60fps scrolling. A: Profiled heap memory using Android Studio Memory Profiler; discovered Glide was caching uncompressed full-resolution bitmaps in RAM. Configured RGB_565 downsampling, set explicit thumbnail view bounds, and recycled bitmap views in RecyclerView. R: Reduced memory footprint by 58%, eliminated OOM crashes completely, and increased crash-free sessions to 99.91%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Set up mobile test devices, build environments, deliver 2 UI bug fixes.",
                        "day_60": "Ship a major new mobile screen flow; automate beta distribution via TestFlight.",
                        "day_90": "Optimize offline synchronization protocols; lead quarterly App Store major release."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.5L - ₹30.0L LPA",
                        "us_usd": "$115,000 - $195,000/yr",
                        "remote_usd": "$80,000 - $150,000/yr"
                    }
                },
                "qa_sdet_engineer": {
                    "title": "Software Development Engineer in Test (SDET)",
                    "aliases": ["QA Automation Engineer", "Test Automation Lead", "Quality Engineer"],
                    "description": "Architects automated end-to-end testing frameworks, regression pipelines, and performance test suites.",
                    "hard_skills": ["Playwright", "Cypress", "Selenium", "Python/TypeScript", "Pytest/JUnit", "API Testing (Postman/REST Assured)", "CI/CD Test Pipelines", "Performance Testing (k6/JMeter)"],
                    "soft_skills": ["Edge Case Paranoia", "Tenacious Testing", "Quality Advocacy"],
                    "ats_keywords": ["SDET", "Automation Testing", "Playwright", "Cypress", "Selenium", "API Testing", "Regression Testing", "CI/CD Quality Gate", "k6", "JMeter", "Test-Driven Development"],
                    "sample_kpis": ["Automated test coverage > 85%", "Flaky test rate < 1%", "Regression run time < 15 minutes"],
                    "typical_responsibilities": [
                        "Build resilient automated testing harnesses preventing manual regression toil.",
                        "Integrate automated quality gates blocking defective code commits in CI/CD pipelines.",
                        "Execute load and stress testing validating throughput limits before production launches."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you eliminate flaky tests that randomly fail in CI pipelines?",
                            "competency": "Deterministic Test Design",
                            "trap": "Adding arbitrary `sleep()` statements.",
                            "model_defense": "S: Our automated E2E test suite had a 15% flakiness rate in GitHub Actions, eroding developer trust and blocking deployments. T: Reduce flakiness to < 1% without sacrificing coverage. A: Audited failing test runs; replaced all arbitrary timeouts with explicit assertion polling and web-first locators in Playwright; isolated test database states with dedicated Docker fixtures per test worker. R: Reduced flakiness to 0.4% and cut test execution duration by 40%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Map critical user journeys, automate top 5 manual smoke tests.",
                        "day_60": "Build automated API regression suite running on every pull request.",
                        "day_90": "Establish automated performance and load testing thresholds in CI/CD."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹6.5L - ₹24.0L LPA",
                        "us_usd": "$95,000 - $165,000/yr",
                        "remote_usd": "$70,000 - $130,000/yr"
                    }
                }
            }
        },
        "ai_ml_data": {
            "name": "Artificial Intelligence, Machine Learning & Data Systems",
            "description": "Training, fine-tuning, evaluating, deploying, and serving intelligent model architectures and big data pipelines.",
            "roles": {
                "genai_llm_engineer": {
                    "title": "Generative AI & LLM Solutions Engineer",
                    "aliases": ["AI Engineer", "LLM Applications Developer", "Prompt & Agent Architect", "RAG Systems Specialist"],
                    "description": "Builds autonomous agent systems, multi-step RAG pipelines, fine-tuned foundational models, and vector database retrieval architectures.",
                    "hard_skills": ["Python", "OpenAI / Claude API", "LangChain / LlamaIndex", "Vector DBs (Pinecone, Chroma, Qdrant, Milvus)", "Embeddings & Semantic Search", "Prompt Engineering", "Fine-Tuning (LoRA/QLoRA)", "vLLM / Ollama", "FastAPI", "Evaluation Frameworks (Ragas, TruLens)"],
                    "soft_skills": ["Empirical Experimentation", "Safety & Alignment Awareness", "Rapid Prototyping", "Curiosity"],
                    "ats_keywords": ["Generative AI", "Large Language Models (LLM)", "RAG (Retrieval-Augmented Generation)", "Vector Databases", "Embeddings", "LangChain", "LlamaIndex", "Prompt Engineering", "LoRA", "Hugging Face", "PyTorch", "Model Evaluation", "Token Optimization", "Semantic Cache", "Autonomous Agents"],
                    "sample_kpis": ["RAG retrieval precision > 92%", "End-to-end token latency < 600ms", "Hallucination rate < 1.5%", "LLM API inference cost reduction > 35%"],
                    "typical_responsibilities": [
                        "Architect scalable multi-agent systems and deterministic workflow routing.",
                        "Build hybrid retrieval systems combining vector similarity, BM25 keyword search, and cross-encoder re-ranking.",
                        "Implement guardrails, PII redaction, token rate limiters, and prompt injection defenses.",
                        "Fine-tune open-weights models (Llama 3, Mistral) for enterprise domain tasks.",
                        "Establish automated benchmark evaluation harnesses measuring factual accuracy, context recall, and latency."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you systematically prevent hallucinations and evaluate accuracy in a production RAG pipeline?",
                            "competency": "Deterministic RAG Engineering & Evaluation",
                            "trap": "Saying 'I tell the prompt to not lie'. Must discuss chunking, embeddings, re-ranking, and evals.",
                            "model_defense": "S: An internal enterprise knowledge assistant was generating 12% hallucinations on complex technical PDFs. T: Eliminate ungrounded answers and achieve >95% retrieval accuracy. A: Restructured the ingestion pipeline: chunked documents semantically by markdown headers rather than arbitrary character counts; implemented a hybrid search combining Pinecone dense vectors with BM25 sparse vectors, followed by a Cohere cross-encoder reranker. Added an automated evaluation loop with Ragas tracking context recall and answer faithfulness, and enforced strict citation grounding in the prompt with fallback to human review when confidence < 0.85. R: Slashed hallucination rate from 12% to 0.7% and improved user trust score to 98%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Audit existing prompts, vector stores, and model APIs; establish automated evaluation ground truth datasets.",
                        "day_60": "Deploy production-ready RAG pipeline with semantic caching and hybrid re-ranking; cut inference latency by 40%.",
                        "day_90": "Build autonomous agent orchestrator for complex multi-step user workflows; deploy fine-tuned local model saving $15k/mo."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹10.0L - ₹42.0L LPA",
                        "us_usd": "$140,000 - $240,000/yr",
                        "remote_usd": "$105,000 - $190,000/yr"
                    }
                },
                "machine_learning_engineer": {
                    "title": "Machine Learning Engineer",
                    "aliases": ["Applied ML Scientist", "Deep Learning Engineer", "MLOps Engineer"],
                    "description": "Designs, trains, validates, and deploys predictive machine learning and deep learning models into production systems.",
                    "hard_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Feature Engineering", "MLflow / Weights & Biases", "Triton / TorchServe", "Docker", "Model Monitoring & Drift Detection", "Hyperparameter Tuning (Optuna)"],
                    "soft_skills": ["Statistical Rigor", "Scientific Skepticism", "Problem Scoping"],
                    "ats_keywords": ["Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Scikit-Learn", "Feature Engineering", "MLOps", "Model Deployment", "MLflow", "Drift Detection", "Inference Optimization"],
                    "sample_kpis": ["Model AUC-ROC > 0.92", "P95 inference latency < 25ms", "Automated model retraining cycle time < 4 hours"],
                    "typical_responsibilities": [
                        "Formulate business problems into supervised, unsupervised, or reinforcement learning tasks.",
                        "Build feature stores, cleaning and scaling high-dimensional data.",
                        "Train and validate deep neural networks and gradient-boosted trees (XGBoost/LightGBM).",
                        "Deploy high-throughput inference endpoints with model versioning and A/B traffic splitting."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Describe a scenario where a machine learning model performed well in offline tests but degraded in production.",
                            "competency": "Data Leakage & Distribution Drift",
                            "trap": "Not understanding training-serving skew or temporal leakage.",
                            "model_defense": "S: Our fraud detection model achieved 97% precision in offline validation but dropped to 68% precision within 2 weeks of production launch. T: Identify the root cause and restore detection precision. A: Analyzed production telemetry; detected training-serving skew caused by an aggregate user transaction feature that used future timestamps during backtesting. Replaced it with point-in-time joins in Feast feature store and deployed Kolmogorov-Smirnov drift monitoring on incoming feature distributions. R: Restored production precision to 94.8% and prevented $220k in fraudulent payouts."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Review existing baseline models, data pipelines, and evaluation metrics.",
                        "day_60": "Train and deploy an improved model iteration with automated shadow testing.",
                        "day_90": "Build automated drift detection and continuous retraining pipeline in production."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹9.5L - ₹40.0L LPA",
                        "us_usd": "$135,000 - $230,000/yr",
                        "remote_usd": "$100,000 - $180,000/yr"
                    }
                },
                "data_engineer": {
                    "title": "Data Engineer",
                    "aliases": ["Big Data Engineer", "Analytics Engineer", "ETL Developer", "Data Platform Engineer"],
                    "description": "Constructs robust, scalable batch and real-time streaming data pipelines, lakehouses, and analytical data marts.",
                    "hard_skills": ["SQL (Advanced)", "Python", "Apache Spark / PySpark", "Snowflake / Databricks / BigQuery", "dbt (data build tool)", "Airflow / Prefect", "Kafka", "Data Modeling (Star Schema / Data Vault)", "Parquet / Iceberg", "Delta Lake"],
                    "soft_skills": ["Data Governance Mindset", "Detail Oriented", "Business Understanding", "Reliability Focus"],
                    "ats_keywords": ["Data Pipeline", "ETL/ELT", "Apache Spark", "PySpark", "Snowflake", "Databricks", "dbt", "Airflow", "SQL Optimization", "Kafka", "Data Lakehouse", "Delta Lake", "Apache Iceberg", "Star Schema", "Data Warehousing", "Data Quality Testing"],
                    "sample_kpis": ["Data pipeline SLA > 99.8%", "Query runtime reduction > 50%", "Zero data freshness delays for business dashboards", "100% automated data contract schema tests"],
                    "typical_responsibilities": [
                        "Build distributed batch and streaming pipelines ingesting billions of records daily.",
                        "Design dimensional data models (fact and dimension tables) powering executive BI dashboards.",
                        "Implement transformation logic and data quality tests using dbt.",
                        "Manage workflow DAG orchestration and dependency retries with Apache Airflow.",
                        "Enforce data governance, GDPR compliance, column-level masking, and schema evolution rules."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Describe an ETL pipeline that was failing or exceeding its batch window. How did you optimize it?",
                            "competency": "Data Pipeline Scalability & Query Optimization",
                            "trap": "Only talking about increasing cluster size without fixing data skew or partitions.",
                            "model_defense": "S: Our nightly financial reconciliation Spark job was taking 7.5 hours and frequently breaching its 8:00 AM SLA. T: Reduce runtime to under 2 hours to ensure downstream regulatory compliance. A: Profiled the Spark UI; identified severe data skew on the merchant_id join key and unnecessary full table scans over unpartitioned tables. Implemented salting on the skewed keys, partitioned the target lakehouse on transaction_date, and converted JSON intermediate tables to compacted Snappy-compressed Parquet. R: Reduced total runtime from 7.5 hours to 1 hour 12 minutes (an 84% speedup) and cut AWS EMR compute costs by $3,200/month."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Ingest schema documentation, run and debug existing Airflow DAGs, fix 2 data quality alerts.",
                        "day_60": "Migrate a legacy ETL pipeline to dbt + Snowflake, establishing unit tests and automated lineage docs.",
                        "day_90": "Architect real-time streaming ingestion pipeline for live event telemetry, reducing dashboard latency from 24h to 5 mins."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹8.5L - ₹36.0L LPA",
                        "us_usd": "$125,000 - $210,000/yr",
                        "remote_usd": "$90,000 - $165,000/yr"
                    }
                },
                "data_scientist": {
                    "title": "Data Scientist",
                    "aliases": ["Applied Statistician", "Quantitative Data Scientist", "Analytics Specialist"],
                    "description": "Applies statistical modeling, hypothesis testing, causal inference, and machine learning to extract actionable strategic insights.",
                    "hard_skills": ["Python / R", "SQL (Advanced)", "Statistical Hypothesis Testing (A/B Testing)", "Causal Inference", "Pandas/NumPy", "Predictive Modeling", "Tableau/Seaborn", "Experimentation Design"],
                    "soft_skills": ["Curiosity", "Storytelling with Data", "Business Value Focus"],
                    "ats_keywords": ["Data Scientist", "Statistical Modeling", "A/B Testing", "Hypothesis Testing", "Python", "SQL", "Predictive Analytics", "Causal Inference", "Machine Learning", "Customer Lifetime Value", "Churn Modeling"],
                    "sample_kpis": ["Experiment statistical power > 80%", "Actionable insights directly driving > $100k revenue lift"],
                    "typical_responsibilities": [
                        "Design and analyze rigorous A/B experiments controlling for sample ratio mismatch and variance.",
                        "Build predictive models for churn, customer lifetime value (LTV), and propensity scoring.",
                        "Translate complex statistical distributions into executive decision recommendations."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you explain the concept of p-value and statistical significance to a non-technical CEO?",
                            "competency": "Executive Communication of Statistical Concepts",
                            "trap": "Reciting formal mathematical definitions without intuition.",
                            "model_defense": "S: Executive leadership wanted to roll out a new landing page after 3 days because it showed a 10% lift. T: Explain why ending the experiment early was dangerous and establish scientific confidence. A: Explained using a coin-toss analogy: flipping heads 3 times in a row doesn't prove the coin is biased. Explained that our p-value was 0.32, meaning there was a 32% chance this 'lift' was pure random noise. Advised running the test for the full 2-week cycle to reach sample size power. R: The full test revealed no real lift, saving the company from making an expensive mistake that would have degraded SEO."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master analytics databases and existing BI models; audit active experimentation frameworks.",
                        "day_60": "Design and execute an end-to-end A/B experiment; publish executive findings doc.",
                        "day_90": "Deploy a predictive churn propensity model integrated into CRM outreach."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹8.0L - ₹32.0L LPA",
                        "us_usd": "$120,000 - $195,000/yr",
                        "remote_usd": "$85,000 - $155,000/yr"
                    }
                },
                "bi_analytics_engineer": {
                    "title": "BI & Analytics Engineer",
                    "aliases": ["Business Intelligence Developer", "Tableau Developer", "Data Analyst", "Reporting Lead"],
                    "description": "Transforms raw warehouse data into intuitive, actionable executive dashboards, KPIs, and reporting portals.",
                    "hard_skills": ["SQL (Complex Window Functions)", "Tableau / PowerBI / Looker", "dbt", "Data Modeling", "Excel Modeling", "Dashboard UX Design"],
                    "soft_skills": ["Clarity", "Cross-Functional Partnership", "Patience with Stakeholders"],
                    "ats_keywords": ["Business Intelligence", "PowerBI", "Tableau", "Looker", "SQL", "dbt", "KPI Dashboards", "Executive Reporting", "Data Warehousing", "Data Modeling"],
                    "sample_kpis": ["Dashboard load time < 3s", "Executive daily active usage > 80%", "Zero data discrepancies between reports"],
                    "typical_responsibilities": [
                        "Author complex SQL data models consolidating disparate business systems.",
                        "Build interactive, intuitive PowerBI/Tableau dashboards for C-suite and regional leads.",
                        "Conduct weekly metric reviews uncovering variance and trend inflections."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you handle a situation where two senior leaders have conflicting definitions for a single metric like 'Active User'?",
                            "competency": "Data Standardization & Alignment",
                            "trap": "Creating two separate dashboards with conflicting numbers.",
                            "model_defense": "S: Marketing defined 'Active User' as someone who opened an email, while Product defined it as someone who completed a core workflow action, causing executive confusion. T: Establish a single company-wide standard. A: Facilitated an alignment workshop with both leaders; demonstrated how ambiguous definitions were skewing CAC/LTV calculations; proposed standardizing on 'Engaged User' for Product and creating a separate metric 'Audience Reach' for Marketing. Documented definitions in the central data dictionary and codified in dbt. R: Achieved unanimous executive buy-in; unified board metrics."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Audit existing BI reports and SQL models; catalog metrics dictionary.",
                        "day_60": "Build and release a redesigned executive KPI dashboard with automated morning alerts.",
                        "day_90": "Migrate ad-hoc SQL queries into standardized dbt semantic layers."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹6.0L - ₹22.0L LPA",
                        "us_usd": "$85,000 - $150,000/yr",
                        "remote_usd": "$65,000 - $120,000/yr"
                    }
                }
            }
        },
        "product_design": {
            "name": "Product Management & UX/UI Product Design",
            "description": "Discovering customer problems, defining product roadmaps, shaping user experiences, and driving business outcomes.",
            "roles": {
                "product_manager": {
                    "title": "Product Manager",
                    "aliases": ["Technical Product Manager", "Growth Product Manager", "Group Product Manager", "Product Lead"],
                    "description": "Drives product strategy, customer discovery, PRD authoring, prioritization, and cross-functional go-to-market execution.",
                    "hard_skills": ["Product Strategy", "PRD Authoring", "User Research", "Agile / Scrum", "Data Analysis (SQL / Mixpanel / Amplitude)", "A/B Testing", "Wireframing", "Roadmap Planning", "Financial Modeling / Unit Economics", "Competitive Analysis"],
                    "soft_skills": ["Influence Without Authority", "Customer Obsession", "Ruthless Prioritization", "Clear Communication", "Executive Storytelling"],
                    "ats_keywords": ["Product Management", "PRD", "Product Roadmap", "User Stories", "Customer Discovery", "A/B Testing", "Mixpanel", "Amplitude", "SQL", "Agile/Scrum", "Go-To-Market (GTM)", "Churn Reduction", "Feature Adoption", "User Retention", "Cross-Functional Leadership"],
                    "sample_kpis": ["User retention lift > 15%", "NPS score increase by 12 points", "Feature adoption rate > 40% in first 30 days", "On-time delivery of quarterly roadmap commitments"],
                    "typical_responsibilities": [
                        "Conduct customer interviews and data analyses to uncover validated user pain points.",
                        "Author comprehensive Product Requirement Documents (PRDs) with clear user stories and acceptance criteria.",
                        "Prioritize sprint backlogs using RICE/MoSCoW frameworks balancing technical debt and business growth.",
                        "Collaborate with Engineering, Design, Sales, and Marketing to execute seamless feature launches.",
                        "Define, track, and present core product health metrics to executive leadership."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Tell me about a feature you launched that failed or didn't meet metrics. What did you learn and how did you pivot?",
                            "competency": "Resilience, Data-Driven Iteration & Humility",
                            "trap": "Claiming you have never launched a failing feature, or blaming marketing/sales for the failure.",
                            "model_defense": "S: We launched an automated AI-assisted invoicing tool expecting a 35% adoption rate, but reached only 8% in the first month. T: Diagnose the root cause of adoption failure and pivot within 2 weeks. A: Re-interviewed 20 churned users and reviewed session recordings in FullStory; discovered users lacked confidence in the AI suggestions because they couldn't see intermediate calculation steps. Redesigned the UX with Design to introduce an interactive preview step with manual override toggles before dispatch. R: Re-launched the feature; adoption jumped to 44% within 45 days and manual support tickets dropped by 28%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Interview 15 customers, study product telemetry, master existing backlog, establish trusted relationships with engineering leads.",
                        "day_60": "Write and ship your first complete PRD; launch 1 major enhancement and measure initial user feedback.",
                        "day_90": "Define the 6-month product roadmap with executive sign-off, establish primary OKRs, and drive measurable metric lift."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹12.0L - ₹45.0L LPA",
                        "us_usd": "$135,000 - $230,000/yr",
                        "remote_usd": "$100,000 - $180,000/yr"
                    }
                },
                "technical_product_manager": {
                    "title": "Technical Product Manager (TPM)",
                    "aliases": ["Platform Product Manager", "API Product Manager", "Infrastructure PM"],
                    "description": "Defines product vision and technical specifications for developer platforms, APIs, data systems, and complex distributed architecture.",
                    "hard_skills": ["API Design (REST/gRPC)", "System Architecture Understanding", "Developer Experience (DX)", "SQL & Telemetry", "PRD & RFC Authoring", "Agile / Scrum"],
                    "soft_skills": ["Technical Credibility", "Engineering Empathy", "Complex Deconstruction"],
                    "ats_keywords": ["Technical Product Manager", "API Product", "Developer Experience", "Platform Architecture", "RESTful APIs", "RFCs", "Microservices", "Data Infrastructure", "Technical Roadmaps"],
                    "sample_kpis": ["API developer onboarding time < 15 mins", "Platform uptime SLA > 99.95%", "Reduction in engineering integration friction by 40%"],
                    "typical_responsibilities": [
                        "Author technical specifications, API schemas, and SDK documentation for developer ecosystems.",
                        "Bridge core engineering architectural decisions with commercial product roadmap goals."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you balance refactoring technical debt against shipping new user-facing features?",
                            "competency": "Technical Prioritization & ROI Modeling",
                            "trap": "Always siding with developers or always siding with business.",
                            "model_defense": "S: Engineering requested a complete 2-month freeze on new features to refactor a monolithic database. T: Preserve business momentum while systematically eliminating the risk of system collapse. A: Quantified the business cost of the debt: unindexed tables caused 14 hours of downtime last quarter, costing $120k in lost transactions. Negotiated a dedicated 20% capacity allocation in every sprint for debt reduction, tied to specific latency reduction milestones. R: Reduced P99 latency by 45% over 3 sprints without stopping the delivery of critical revenue features."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Review API schemas, architecture diagrams, and developer support tickets.",
                        "day_60": "Deliver first API platform RFC and developer documentation overhaul.",
                        "day_90": "Launch major platform API version with zero breaking changes for existing consumers."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹14.0L - ₹48.0L LPA",
                        "us_usd": "$145,000 - $240,000/yr",
                        "remote_usd": "$110,000 - $190,000/yr"
                    }
                },
                "ui_ux_product_designer": {
                    "title": "UI/UX Product Designer",
                    "aliases": ["Product Designer", "User Experience Designer", "Interaction Designer", "Visual Designer"],
                    "description": "Creates intuitive, accessible, and delightful digital user journeys, design systems, and interactive prototypes.",
                    "hard_skills": ["Figma", "Design Systems", "Prototyping", "User Research & Usability Testing", "Wireframing", "Information Architecture", "Micro-Interactions", "Accessibility (WCAG 2.1)", "Design Tokens", "Mobile (iOS/Android) Guidelines"],
                    "soft_skills": ["Visual Craft", "User Empathy", "Feedback Receptivity", "Storytelling", "Cross-Functional Synergy"],
                    "ats_keywords": ["Figma", "UI/UX Design", "Design System", "User Research", "Wireframing", "Interactive Prototypes", "Usability Testing", "Information Architecture", "User Personas", "Design Tokens", "Accessibility", "Micro-interactions", "Design Thinking"],
                    "sample_kpis": ["Usability task completion rate > 90%", "Design System adoption across 100% of product squads", "Reduction in user friction drop-off by 25%", "Zero accessibility contrast violations"],
                    "typical_responsibilities": [
                        "Conduct generative and evaluative user research sessions to map customer mental models.",
                        "Build interactive Figma prototypes for rapid usability testing and stakeholder alignment.",
                        "Maintain and evolve multi-brand design systems with unified component tokens.",
                        "Deliver high-fidelity production-ready assets and detailed specs for engineering handoffs.",
                        "Champion accessibility and inclusive design principles across all digital touchpoints."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you resolve a fundamental design disagreement between what the user research indicates and what executive stakeholders want?",
                            "competency": "Stakeholder Management & Evidence-Based Design",
                            "trap": "Either blindly obeying stakeholders or stubbornly ignoring business constraints.",
                            "model_defense": "S: The VP of Sales wanted to add a mandatory 8-field lead form before onboarding, but user tests showed an 80% abandonment rate. T: Align business lead qualification goals with seamless user experience. A: Created 3 testable design variants in Figma. Proposed an A/B test on 20% of traffic comparing the hard gate against progressive profiling that asked for basic credentials upfront and enriched additional fields post-activation. Presented clear conversion funnel data to the VP showing progressive profiling yielded 3.2x more qualified demos overall. R: Secured stakeholder consensus, launched progressive onboarding, and boosted trial-to-paid conversion by 34%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Audit existing Figma libraries and user feedback; conduct heuristic evaluation of core funnel.",
                        "day_60": "Design and prototype a high-impact feature flow, conduct 5 usability tests, and oversee engineering implementation.",
                        "day_90": "Standardize 50+ reusable components in the design system, run a design critique workshop, and present UX roadmap."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹8.0L - ₹30.0L LPA",
                        "us_usd": "$110,000 - $190,000/yr",
                        "remote_usd": "$80,000 - $150,000/yr"
                    }
                }
            }
        },
        "cybersecurity_governance": {
            "name": "Cybersecurity, InfoSec & Regulatory Compliance",
            "description": "Defending digital assets, infrastructure, customer data, and applications against threat actors and regulatory violations.",
            "roles": {
                "security_engineer": {
                    "title": "Security Engineer (AppSec / Cloud Security)",
                    "aliases": ["Application Security Engineer", "Information Security Specialist", "Cybersecurity Analyst"],
                    "description": "Hardens applications and cloud environments against vulnerabilities, performing threat modeling, penetration testing, and code audits.",
                    "hard_skills": ["OWASP Top 10", "Threat Modeling", "SAST / DAST (Snyk, Semgrep)", "Cloud Security (AWS IAM, GuardDuty)", "Penetration Testing (Burp Suite)", "Cryptography & PKI", "Network Security & Firewalls"],
                    "soft_skills": ["Paranoid Mindset", "Discretion", "Calm Under Pressure", "Diplomatic Communication"],
                    "ats_keywords": ["Cybersecurity", "Application Security (AppSec)", "OWASP Top 10", "Penetration Testing", "Vulnerability Management", "Burp Suite", "SAST/DAST", "Cloud Security", "Threat Modeling", "Zero Trust"],
                    "sample_kpis": ["Mean time to remediate critical vulnerabilities < 48 hours", "Zero high-severity breaches in production", "100% CI/CD automated security scan coverage"],
                    "typical_responsibilities": [
                        "Perform threat modeling and architecture reviews for new product features.",
                        "Conduct automated and manual code audits identifying SQLi, XSS, and SSRF vulnerabilities.",
                        "Manage Bug Bounty programs and coordinate rapid security patch deployments."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you persuade software developers to fix security vulnerabilities when they are under tight feature deadlines?",
                            "competency": "Security Culture & Developer Enablement",
                            "trap": "Being the 'department of NO' or issuing passive PDF reports.",
                            "model_defense": "S: Developers were ignoring critical SAST vulnerability alerts to hit quarterly release deadlines. T: Eliminate high-risk vulnerabilities without stalling the release cycle. A: Embedded security directly into their workflow: created automated Semgrep rules in GitHub Actions that provided instant autofix code suggestions directly in the PR diff; ran a 45-minute workshop demonstrating live exploitation of a broken auth vulnerability. R: Remediation time dropped from 45 days to 3.2 days, and developer security sentiment improved significantly."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Audit cloud security postures and automated scanners; review recent penetration test findings.",
                        "day_60": "Implement automated SAST/DAST gating in CI/CD; remediate top 5 high-severity vulnerabilities.",
                        "day_90": "Lead company-wide threat modeling workshop; deploy centralized vulnerability management dashboard."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹9.0L - ₹36.0L LPA",
                        "us_usd": "$125,000 - $215,000/yr",
                        "remote_usd": "$90,000 - $170,000/yr"
                    }
                },
                "infosec_compliance_analyst": {
                    "title": "Information Security & Compliance Analyst (SOC 2 / ISO 27001)",
                    "aliases": ["GRC Analyst", "IT Compliance Lead", "Risk & Security Auditor"],
                    "description": "Guides organizations through formal cybersecurity certifications, audits, vendor risk assessments, and privacy frameworks.",
                    "hard_skills": ["SOC 2 Type II", "ISO 27001", "GDPR / HIPAA", "Vendor Risk Assessment", "Policy Authoring", "Auditing Platforms (Vanta, Drata)", "Access Reviews"],
                    "soft_skills": ["Meticulous Documentation", "Regulatory Precision", "High Integrity"],
                    "ats_keywords": ["SOC 2", "ISO 27001", "GRC", "Compliance Audit", "Vanta", "Drata", "Risk Assessment", "Information Security Policy", "GDPR", "Access Management"],
                    "sample_kpis": ["Zero non-conformities during external audits", "100% on-time annual SOC 2 Type II certification renewal", "Vendor risk assessment turnaround < 3 days"],
                    "typical_responsibilities": [
                        "Maintain security policies and collect audit evidence across all operational departments.",
                        "Run quarterly user access reviews and third-party vendor risk assessments."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you manage a tight deadline for a critical enterprise SOC 2 audit?",
                            "competency": "Compliance Program Execution",
                            "trap": "Forging or scrambling manual evidence.",
                            "model_defense": "S: An enterprise customer made a $500k deal contingent on our SOC 2 Type II report within 90 days. T: Complete all 78 trust criteria controls and external audit on time. A: Deployed Drata to automate continuous evidence collection from AWS, GitHub, and Google Workspace; conducted weekly sprint check-ins with Engineering and HR to close policy gaps; organized an internal pre-audit to catch control failures. R: Received an unqualified clean SOC 2 Type II opinion with zero exceptions, unblocking the $500k enterprise contract."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Review current security policies and evidence collection status.",
                        "day_60": "Automate evidence gathering and resolve all outstanding compliance gaps.",
                        "day_90": "Successfully complete external audit and deliver clean certification reports."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.0L - ₹25.0L LPA",
                        "us_usd": "$95,000 - $160,000/yr",
                        "remote_usd": "$70,000 - $130,000/yr"
                    }
                }
            }
        },
        "corporate_finance_treasury": {
            "name": "Corporate Finance, Investment Banking, FP&A & Treasury",
            "description": "Managing corporate capital, financial modeling, budgeting, treasury liquidity, and institutional compliance.",
            "roles": {
                "financial_analyst_fpa": {
                    "title": "Financial Analyst (FP&A)",
                    "aliases": ["FP&A Analyst", "Corporate Finance Analyst", "Strategic Finance Specialist", "Budgeting & Planning Analyst"],
                    "description": "Builds financial forecasts, 3-statement models, budget variance analyses, and capital expenditure assessments.",
                    "hard_skills": ["Financial Modeling (3-Statement & DCF)", "Advanced Excel / Google Sheets", "Variance Analysis (Budget vs Actual)", "SQL & PowerBI / Tableau", "ERP Systems (SAP / NetSuite / Oracle)", "Cash Flow Forecasting", "Cost Accounting & Unit Economics"],
                    "soft_skills": ["Analytical Precision", "Integrity", "Executive Presentation", "Proactive Insight"],
                    "ats_keywords": ["Financial Analyst", "FP&A", "Financial Modeling", "Budgeting and Forecasting", "Variance Analysis", "3-Statement Model", "Cash Flow Modeling", "NetSuite", "SAP", "Advanced Excel", "PowerBI", "P&L Analysis", "EBITDA"],
                    "sample_kpis": ["Forecast variance < 3.5% across quarters", "Monthly financial close analysis completed within 48h", "Identification of $200k+ in cost optimization opportunities", "Zero errors in board reporting metrics"],
                    "typical_responsibilities": [
                        "Maintain and update monthly 3-statement financial models and cash runway projections.",
                        "Conduct variance analysis dissecting revenue and expense deviations across departments.",
                        "Partner with department heads to structure annual operating budgets and headcount plans.",
                        "Analyze unit economics, gross margins, CAC/LTV ratios, and customer cohorts.",
                        "Deliver monthly financial executive briefing packs to the CFO and Board of Directors."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you identify a significant financial anomaly or cost leakage that others had missed?",
                            "competency": "Forensic Financial Analysis & Cost Prudence",
                            "trap": "Claiming you just looked at the total number without digging into the underlying ledger entries.",
                            "model_defense": "S: During Q3 variance review, cloud hosting expenses showed a steady 8% unexplained month-over-month growth. T: Identify the root cause and recommend concrete remediations to the CFO. A: Extracted raw billing data using SQL and categorized expenditure by service and instance ID; identified that non-production testing clusters were running 24/7 on high-tier GPUs due to missing auto-termination scripts. Partnered with DevOps to enforce scheduled shutdowns and reserve instance savings plans. R: Reduced cloud bill by $28,000/month (a 22% ongoing reduction) with zero operational impact."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master chart of accounts, historical financial statements, ERP workflows, and model architecture.",
                        "day_60": "Own the monthly departmental variance reporting cycle; lead 1 deep-dive margin optimization audit.",
                        "day_90": "Build an automated real-time FP&A dashboard linking SQL to PowerBI; present quarterly budget forecast to executive committee."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹6.5L - ₹22.0L LPA",
                        "us_usd": "$85,000 - $145,000/yr",
                        "remote_usd": "$65,000 - $120,000/yr"
                    }
                },
                "investment_banking_analyst": {
                    "title": "Investment Banking & Corporate Development Analyst",
                    "aliases": ["M&A Analyst", "Private Equity Associate", "Corp Dev Specialist"],
                    "description": "Performs valuation modeling, DCF/LBO models, pitchbook preparation, and transaction due diligence for M&A and capital raises.",
                    "hard_skills": ["Discounted Cash Flow (DCF)", "Leveraged Buyout (LBO)", "Comparable Company Analysis (Trading Comps)", "Merger Modeling & Accretion/Dilution", "Capital IQ / Bloomberg Terminal", "Pitchbook Creation"],
                    "soft_skills": ["Uncompromising Stamina", "Absolute Numerical Precision", "High Presentation Polish"],
                    "ats_keywords": ["Investment Banking", "M&A", "DCF Modeling", "LBO", "Valuation", "Pitchbooks", "Financial Modeling", "Corporate Development", "Due Diligence", "Capital Raising"],
                    "sample_kpis": ["Zero formula or formatting errors in confidential information memorandums (CIMs)", "Financial model turnaround within tight 24h client windows"],
                    "typical_responsibilities": [
                        "Build dynamic valuation and merger models evaluating strategic transaction feasibility.",
                        "Synthesize industry trends and financial statements into client-facing pitchbooks and CIMs.",
                        "Manage virtual data rooms (VDRs) and coordinate buyer due diligence requests."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Walk me through how a $10 increase in depreciation flows through the three financial statements.",
                            "competency": "Technical Accounting & Financial Mechanics",
                            "trap": "Forgetting the tax shield or confusing cash flow changes.",
                            "model_defense": "S: On the Income Statement, Operating Income decreases by $10. Assuming a 20% tax rate, Net Income decreases by $8. On the Cash Flow Statement, Net Income drops by $8 under Cash from Operations, but we add back the non-cash $10 depreciation expense, resulting in a net cash increase of $2. On the Balance Sheet, Cash increases by $2, PP&E decreases by $10, so Assets are down by $8. Under Equity, Retained Earnings are down by $8 from Net Income, balancing the equation perfectly."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master internal model templates, formatting standards, and transaction pipelines.",
                        "day_60": "Lead due diligence workflows and build comprehensive valuation models for 2 active deals.",
                        "day_90": "Deliver client-facing pitchbooks independently with executive sign-off."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹12.0L - ₹38.0L LPA",
                        "us_usd": "$120,000 - $220,000/yr (Base + Bonus)",
                        "remote_usd": "$90,000 - $170,000/yr"
                    }
                }
            }
        },
        "b2b_sales_revenue": {
            "name": "B2B Commercial Sales, Revenue Operations & Sales Engineering",
            "description": "Generating enterprise pipeline, negotiating multi-year commercial contracts, and scaling recurring revenue engines.",
            "roles": {
                "account_executive": {
                    "title": "Enterprise Account Executive",
                    "aliases": ["B2B Sales Executive", "Commercial Account Executive", "Enterprise Sales Director", "Sales Hunter"],
                    "description": "Owns full sales cycles from discovery to contract closure for mid-market and enterprise B2B customers.",
                    "hard_skills": ["MEDDPICC / BANT Qualification", "Enterprise Deal Negotiation", "Contract Structuring & MSAs", "Salesforce / HubSpot CRM", "Pipeline Management", "Executive Pitching & Demos", "Territory Planning", "Account Mapping", "Objection Handling"],
                    "soft_skills": ["Active Listening", "High Grit & Persistence", "Emotional Intelligence", "Executive Presence", "Commercial Acumen"],
                    "ats_keywords": ["Enterprise Sales", "B2B Sales", "Quota Attainment", "MEDDPICC", "Salesforce", "Contract Negotiation", "Enterprise Pipeline", "Full Sales Cycle", "C-Suite Presentation", "ARR Generation", "Objection Handling", "Closing Velocity"],
                    "sample_kpis": ["> 110% annual quota attainment", "Average contract value (ACV) > $60k", "Win rate > 28%", "Sales cycle velocity < 75 days"],
                    "typical_responsibilities": [
                        "Run consultative discovery calls uncovering executive economic buyer priorities.",
                        "Qualify enterprise opportunities rigorously using MEDDPICC criteria.",
                        "Deliver high-impact tailored demonstrations and ROI business cases to C-level stakeholders.",
                        "Navigate procurement, legal redlines, security audits, and Master Service Agreements (MSAs).",
                        "Maintain pristine CRM hygiene, pipeline forecasting, and deal stage velocity."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Walk me through the largest or most complex enterprise deal you closed from start to finish.",
                            "competency": "Complex Deal Execution & MEDDPICC Mastery",
                            "trap": "Relying on luck or passive inbound without showing strategic champion cultivation.",
                            "model_defense": "S: We were competing against an entrenched incumbent for a $180k ARR contract with a Tier-1 logistics firm. T: Win the RFP and secure a 3-year enterprise commitment within 90 days. A: Identified the VP of Supply Chain as our internal Champion and the CFO as Economic Buyer. Uncovered that the incumbent's slow API was costing them $40k/month in manual reconciliation. Orchestrated a rapid Proof of Concept proving 10x faster settlement; built a quantifiable ROI model showing payback in 4 months; worked directly with legal to resolve 12 security redlines. R: Closed a $210k/yr multi-year contract (116% of target) and delivered 135% quota attainment for the year."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master product features, competitor battlecards, and sales pitch; shadow 15 live customer calls; pass sales certification.",
                        "day_60": "Build an active pipeline of $300k+ in qualified pipeline; lead 10 first-party discovery calls; qualify 3 target deals.",
                        "day_90": "Close first enterprise commercial contract, establish predictable monthly forecasting, and exceed pipeline generation goals."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹10.0L - ₹35.0L LPA (Base + OTE)",
                        "us_usd": "$140,000 - $260,000/yr (50/50 OTE)",
                        "remote_usd": "$90,000 - $180,000/yr"
                    }
                },
                "sales_dev_representative": {
                    "title": "Sales Development Representative (SDR / BDR)",
                    "aliases": ["Business Development Representative", "Outbound SDR", "Lead Generation Specialist", "Inside Sales Associate"],
                    "description": "Identifies, engages, and qualifies outbound enterprise prospects through high-velocity cold email, LinkedIn, and phone cadences.",
                    "hard_skills": ["Cold Outreach & Email Copywriting", "Apollo.io / ZoomInfo / Sales Navigator", "Multi-Touch Cadence Execution", "CRM Hygiene (Salesforce/HubSpot)", "Lead Qualification (BANT/Challenger)", "Cold Calling", "Objection Handling"],
                    "soft_skills": ["Tenacity & Drive", "Rejection Resilience", "Agile Thinking", "Articulate Communication", "Coachability"],
                    "ats_keywords": ["Sales Development", "Cold Outreach", "Outbound Prospecting", "Apollo.io", "LinkedIn Sales Navigator", "Salesforce", "Lead Qualification", "Pipeline Generation", "Cold Calling", "Email Sequences", "SQL Generation", "B2B Lead Gen"],
                    "sample_kpis": ["> 20 qualified SQLs generated per month", "Email open rate > 45% and reply rate > 8%", "Over 60 high-quality touchpoints per day", "Pipeline contribution > $250k per quarter"],
                    "typical_responsibilities": [
                        "Research and enrich target prospect accounts and key decision makers.",
                        "Author highly personalized, value-first multi-touch outbound email and LinkedIn cadences.",
                        "Execute high-volume outbound calls, navigating gatekeepers to speak with VPs and Directors.",
                        "Conduct initial qualification screening calls to assess budget, authority, need, and timeline.",
                        "Smoothly hand off qualified sales opportunities (SQLs) to Account Executives."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you handle a month where your initial outreach gets low responses or heavy pushback?",
                            "competency": "Grit, Optimization & Pipeline Tenacity",
                            "trap": "Blaming bad leads or giving up.",
                            "model_defense": "S: Halfway through Q2, my cold email reply rate dropped from 7.5% to 2.1% due to generic messaging fatigue. T: Rebound to achieve my target of 22 qualified demos before quarter end. A: Ran an immediate diagnostic on 200 prospects. Shifted from generic pitches to hyper-tailored 3-sentence emails referencing recent 10-K earnings reports and hiring trends; tested 4 subject line variants; and doubled down on LinkedIn voice notes and warm mutual connections. R: Reply rate rebounded to 9.4%, booked 26 qualified meetings in the remaining 4 weeks, and finished at 118% of quota."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master company ICP, objection handling scripts, and toolstack; complete 50 cold calls and 200 email dispatches.",
                        "day_60": "Hit 100% of weekly meeting booking targets; optimize personal email copy variants; book 18 qualified meetings.",
                        "day_90": "Consistently rank in the top 20% of SDRs; mentor new hires; generate > $300k in qualified sales pipeline."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹4.5L - ₹12.0L LPA",
                        "us_usd": "$65,000 - $95,000/yr (Base + Commission)",
                        "remote_usd": "$45,000 - $80,000/yr"
                    }
                },
                "solutions_architect_sales_eng": {
                    "title": "Solutions Architect / Sales Engineer",
                    "aliases": ["Pre-Sales Solutions Engineer", "Technical Sales Architect", "Field Architect"],
                    "description": "Serves as technical authority during enterprise sales deals, architecting technical PoCs, answering RFPs, and resolving integration objections.",
                    "hard_skills": ["Cloud Architecture (AWS/GCP/Azure)", "API Integrations & Webhooks", "Technical Demos & PoC Buildout", "RFP / RFI Technical Defense", "Security Questionnaire Response", "Enterprise System Design"],
                    "soft_skills": ["Technical Storytelling", "Customer Empathy", "Composure"],
                    "ats_keywords": ["Solutions Architect", "Sales Engineering", "Pre-Sales", "Proof of Concept (PoC)", "RFP", "Technical Demos", "Cloud Architecture", "System Integration", "Enterprise Software"],
                    "sample_kpis": ["PoC conversion to deal close > 75%", "Technical RFP win rate > 80%", "Average PoC turnaround < 10 days"],
                    "typical_responsibilities": [
                        "Architect custom technical integrations and prototypes demonstrating enterprise value to prospective CIOs.",
                        "Defend company security, scalability, and data sovereignty compliance during RFP gauntlets."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you respond when a prospect's technical team claims your software lacks a critical capability they must have?",
                            "competency": "Technical Discovery & Objection Reframing",
                            "trap": "Arguing or falsely promising that engineering will build it tomorrow.",
                            "model_defense": "S: A prospect's Head of Engineering insisted our platform was unusable because we lacked a native connector to their legacy on-premise mainframe. T: Validate their actual workflow requirement and prevent deal stall. A: Conducted a technical deep-dive into how data was actually transformed; demonstrated how our lightweight webhook agent combined with their Kafka broker could mirror the data in real time with sub-second latency and zero changes to their mainframe. R: Built a functional demo in 48 hours; won their technical sign-off and closed a $140k ARR deal."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master architecture whitepapers, product APIs, and complete 5 demo certifications.",
                        "day_60": "Lead 10 pre-sales architecture calls and deliver 2 enterprise PoCs.",
                        "day_90": "Build reusable demo sandbox templates cutting PoC setup time by 50%."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹12.0L - ₹38.0L LPA",
                        "us_usd": "$140,000 - $240,000/yr",
                        "remote_usd": "$100,000 - $185,000/yr"
                    }
                }
            }
        },
        "growth_marketing_seo": {
            "name": "Growth Marketing, Technical SEO & Brand Activation",
            "description": "Scaling customer acquisition engines, organic search rankings, conversion funnels, and brand positioning.",
            "roles": {
                "growth_marketing_manager": {
                    "title": "Growth Marketing Manager",
                    "aliases": ["Performance Marketer", "Demand Generation Manager", "Acquisition Lead"],
                    "description": "Scales paid and organic acquisition funnels, optimizes CAC/LTV, runs multi-variant conversion tests, and manages digital ad spend.",
                    "hard_skills": ["Paid Ads (Google Ads, Meta, LinkedIn Ads)", "Conversion Rate Optimization (CRO)", "Attribution Modeling", "Google Analytics 4 (GA4)", "Landing Page Builders", "A/B Testing", "Funnel Analytics"],
                    "soft_skills": ["Scientific Mindset", "Budget Discipline", "Creative Copywriting"],
                    "ats_keywords": ["Growth Marketing", "Demand Generation", "Performance Marketing", "CAC", "LTV", "ROAS", "Conversion Rate Optimization", "Google Ads", "LinkedIn Ads", "GA4", "A/B Testing"],
                    "sample_kpis": ["Customer Acquisition Cost (CAC) reduction > 20%", "Return on Ad Spend (ROAS) > 3.8x", "Monthly inbound pipeline growth > 30%"],
                    "typical_responsibilities": [
                        "Manage multi-channel paid media budgets across search, social, and programmatic display.",
                        "Run continuous landing page conversion experiments to maximize lead capture."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you scale paid acquisition while driving down customer acquisition cost?",
                            "competency": "Capital Efficiency & Paid Channel Optimization",
                            "trap": "Spending more money without improving conversion efficiency.",
                            "model_defense": "S: Our B2B SaaS CAC rose to $480 on Google Ads, exceeding our $350 target. T: Bring CAC below $300 while maintaining lead volume. A: Audited search term reports, negative-keyworded 450 irrelevant consumer terms eating 28% of budget; created 4 dedicated dynamic landing pages mapped 1:1 to high-intent commercial keywords; implemented post-lead qualification scoring to feed back conversion value to Google's smart bidding algorithm. R: Lowered CAC from $480 to $265 (a 45% reduction) and scaled monthly qualified leads by 38%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Audit existing paid campaigns, tracking pixels, and GA4 attribution flows.",
                        "day_60": "Launch 3 new channel experiments and deploy landing page CRO tests.",
                        "day_90": "Scale winning campaigns by 2x while maintaining target ROAS."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.5L - ₹26.0L LPA",
                        "us_usd": "$95,000 - $165,000/yr",
                        "remote_usd": "$70,000 - $135,000/yr"
                    }
                },
                "technical_seo_specialist": {
                    "title": "Technical SEO & Programmatic Growth Specialist",
                    "aliases": ["SEO Lead", "Organic Search Strategist", "Programmatic SEO Engineer"],
                    "description": "Architects programmatic page generation, technical site architecture, crawlability, indexing, and keyword dominance.",
                    "hard_skills": ["Technical SEO Auditing (Screaming Frog)", "Schema.org Markup & Structured Data", "Core Web Vitals Optimization", "Programmatic SEO Architecture", "Keyword Research & Content Clustering", "Search Console & Ahrefs/Semrush"],
                    "soft_skills": ["Patience", "Analytical Rigor", "Cross-Team Alignment"],
                    "ats_keywords": ["Technical SEO", "Programmatic SEO", "Core Web Vitals", "Structured Data", "Screaming Frog", "Google Search Console", "Ahrefs", "Crawl Budget", "Canonicalization", "Internal Linking"],
                    "sample_kpis": ["Organic search traffic growth > 100% YoY", "Top 3 rankings for 50+ high-intent commercial keywords", "Zero indexation or canonical errors"],
                    "typical_responsibilities": [
                        "Execute technical audits resolving crawl loops, canonicalization bugs, and page speed bottlenecks.",
                        "Build programmatic SEO templates generating thousands of high-converting indexed landing pages."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you recover organic traffic following a major Google core update penalty?",
                            "competency": "SEO Diagnostics & Algorithmic Recovery",
                            "trap": "Guessing without analyzing search console traffic by page template.",
                            "model_defense": "S: Following a Google Helpful Content update, our organic search traffic dropped by 32% overnight. T: Identify the root cause and restore organic visibility within 60 days. A: Segmented Search Console data by URL prefix; found thin, auto-generated programmatic pages lacking unique value were dragging down domain authority. Pruned 4,000 duplicate low-intent pages, added rich schema markup, and enriched top 200 money pages with original proprietary data benchmarks and expert quotes. R: Traffic fully rebounded in 45 days, eventually climbing 24% higher than pre-update levels."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Conduct full technical SEO crawl, identify indexing errors and speed bottlenecks.",
                        "day_60": "Implement Core Web Vitals fixes and deploy structured schema across key pages.",
                        "day_90": "Launch programmatic SEO engine capturing long-tail search intent."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹6.0L - ₹22.0L LPA",
                        "us_usd": "$80,000 - $145,000/yr",
                        "remote_usd": "$60,000 - $120,000/yr"
                    }
                }
            }
        },
        "operations_supply_chain_exim": {
            "name": "Global Operations, Supply Chain, Logistics & EXIM",
            "description": "Managing cross-border commerce, customs compliance, freight logistics, warehousing, and operational scaling.",
            "roles": {
                "exim_international_trade_specialist": {
                    "title": "International Trade & EXIM Specialist",
                    "aliases": ["Export Import Operations Lead", "Trade Compliance Specialist", "Customs & Freight Coordinator", "Global Trade Manager"],
                    "description": "Orchestrates cross-border export/import documentation, customs clearances, tariff classification, Incoterms, and trade finance.",
                    "hard_skills": ["Incoterms 2020 (FOB, CIF, DDP, EXW)", "Customs Tariff Classification (HS Code)", "Bill of Lading (B/L) & Air Waybills", "Letter of Credit (LC) & Trade Finance", "DGFT / ICEGATE & Regulatory Filings", "Freight Forwarder SLA Management", "Marine Cargo Insurance", "Foreign Exchange & Remittances"],
                    "soft_skills": ["Zero Error Margin", "Cross-Cultural Negotiation", "Regulatory Discipline", "Crisis De-escalation"],
                    "ats_keywords": ["Export Import (EXIM)", "Incoterms 2020", "Customs Clearance", "Harmonized System (HS Codes)", "Letter of Credit", "Bill of Lading", "Freight Forwarding", "ICEGATE", "DGFT", "Trade Compliance", "Supply Chain Logistics", "Cross-Border Trade"],
                    "sample_kpis": ["100% regulatory customs compliance (0 detention/demurrage fines)", "Freight cost reduction > 12% across air/sea routes", "Average port clearance turnaround time < 48 hours", "Zero discrepancies in Letter of Credit documentation"],
                    "typical_responsibilities": [
                        "Review and prepare all commercial invoices, packing lists, certificates of origin, and shipping bills.",
                        "Classify products under correct 8-digit HS Codes ensuring duty optimization and trade pact compliance.",
                        "Liaise with customs brokers, shipping liners, and freight forwarders to track international cargo.",
                        "Manage Bank Letters of Credit (UCP 600) ensuring zero discrepancy charges or payment delays.",
                        "Ensure compliance with DGFT, export control regulations, and international sanction lists."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Describe a time when a critical international shipment was held up at customs or port. How did you resolve it?",
                            "competency": "Regulatory Problem Solving & High-Stakes Logistics",
                            "trap": "Passive waiting or blaming customs officials without proactive documentation remediation.",
                            "model_defense": "S: A $450k container of precision components was flagged at Nhava Sheva port due to an alleged tariff misclassification and faced $2,500/day demurrage. T: Clear the shipment within 48 hours without regulatory penalties. A: Immediately cross-referenced the technical datasheets against World Customs Organization (WCO) explanatory notes; drafted an urgent legal justification letter with our customs broker proving the product fell under an exemption notification; personally met with the Assistant Commissioner of Customs to present the technical evidence. R: Secured unconditional out-of-charge clearance within 36 hours, saving $15,000 in potential port fees and avoiding manufacturing line stoppage."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Review all active trade lanes, freight contracts, and standard export documentation templates; audit recent shipments.",
                        "day_60": "Renegotiate spot freight rates with primary liners; resolve any lingering customs reconciliation filings.",
                        "day_90": "Standardize an automated digital EXIM documentation ledger, reducing document prep cycle time by 35%."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹5.5L - ₹18.0L LPA",
                        "us_usd": "$80,000 - $140,000/yr",
                        "remote_usd": "$60,000 - $115,000/yr"
                    }
                },
                "operations_manager": {
                    "title": "Operations Manager",
                    "aliases": ["Business Operations Manager", "City Operations Lead", "Director of Operations", "COO Associate"],
                    "description": "Leads operational execution, process optimization, vendor governance, SLAs, and organizational throughput.",
                    "hard_skills": ["Process Optimization (Lean / Six Sigma)", "Operational Dashboards & KPI Tracking", "Vendor Contract Management", "Budgeting & Cost Allocation", "Cross-Functional Project Management", "Root-Cause Analysis", "SLA Enforcement"],
                    "soft_skills": ["Operational Decisiveness", "Empathetic Leadership", "Crisis Management", "Relentless Follow-Through"],
                    "ats_keywords": ["Operations Management", "Process Optimization", "Lean Six Sigma", "SLA Management", "Vendor Management", "Cost Reduction", "Capacity Planning", "KPI Dashboards", "Cross-Functional Leadership", "Resource Allocation", "Operational Efficiency"],
                    "sample_kpis": ["Operational cost per unit reduced by 18%", "SLA compliance rate > 99.2%", "Employee operational productivity lift > 25%", "Zero regulatory or safety non-conformance incidents"],
                    "typical_responsibilities": [
                        "Analyze operational bottlenecks and deploy Lean process improvements.",
                        "Negotiate and enforce Service Level Agreements (SLAs) across 3rd-party vendors and partners.",
                        "Oversee daily resource allocation, operational staffing, and facility budgets.",
                        "Build automated real-time KPI dashboards monitoring throughput and variance.",
                        "Lead business continuity planning, incident response, and root-cause postmortems."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you identify which operational bottleneck to tackle first when multiple departments are underperforming?",
                            "competency": "Strategic Prioritization & Operational Analytics",
                            "trap": "Trying to fix everything at once or reacting to whoever complains loudest.",
                            "model_defense": "S: Following a 3x surge in order volume, our fulfillment centers suffered from backlogged sorting, delayed deliveries, and rising customer complaints. T: Stabilize operations and prioritize intervention within 7 days. A: Gathered telemetry on process cycle times across each station; conducted Pareto analysis (80/20 rule) which revealed 74% of total delay originated at the manual barcode scanning and dimension check bottleneck. Re-allocated 6 floaters to that station immediately and deployed automated dimensioning sensors within 72 hours. R: Cleared the 4,000-order backlog in 48 hours, restored on-time delivery from 81% to 98.6%, and lowered per-unit handling cost by 14%."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Shadow ground teams, document existing Standard Operating Procedures (SOPs), identify top 3 operational leaks.",
                        "day_60": "Implement process automations and revamped SLAs; deliver first quantifiable 10% efficiency gain.",
                        "day_90": "Scale the operational playbook across regional hubs; establish continuous auditing and daily health dashboards."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.5L - ₹26.0L LPA",
                        "us_usd": "$95,000 - $165,000/yr",
                        "remote_usd": "$70,000 - $130,000/yr"
                    }
                }
            }
        },
        "executive_founders_office": {
            "name": "Executive Leadership, Founders Office & Corporate Strategy",
            "description": "Partnering directly with CXOs and Founders on mission-critical special projects, strategic initiatives, and governance.",
            "roles": {
                "chief_of_staff": {
                    "title": "Chief of Staff to CEO",
                    "aliases": ["Executive Operations Director", "VP of Strategy & Operations", "Founders Office Lead", "Head of Executive Office"],
                    "description": "Acts as force multiplier to the CEO/Founders, driving strategic alignment, executive cadence, board communications, and critical special projects.",
                    "hard_skills": ["Strategic Planning", "Board Deck Preparation & Executive Comms", "Financial & P&L Modeling", "Cross-Functional Program Management", "M&A / Capital Allocation Analysis", "Crisis Communications", "OKRs & Performance Cascading"],
                    "soft_skills": ["Absolute Discretion & Trust", "High Emotional Intelligence", "Extreme Ownership", "Strategic Clarity", "Executive Gravitas"],
                    "ats_keywords": ["Chief of Staff", "Founders Office", "Executive Strategy", "Board Deck", "OKRs", "Cross-Functional Alignment", "P&L Management", "Special Projects", "Strategic Initiatives", "Investor Relations", "Business Transformation"],
                    "sample_kpis": ["100% on-time execution of CEO priority projects", "Board meeting prep cycles reduced by 50%", "Cross-functional execution roadblocks resolved within 24h", "Measurable enterprise value creation across incubation initiatives"],
                    "typical_responsibilities": [
                        "Serve as strategic advisor, confidant, and sounding board to the Chief Executive Officer.",
                        "Orchestrate executive leadership team (ELT) meetings, tracking action items and accountability.",
                        "Author high-stakes board decks, investor update letters, and all-hands townhall narratives.",
                        "Lead zero-to-one incubation of strategic initiatives before handing off to functional leaders.",
                        "Resolve inter-departmental friction, unblocking bottlenecks before they reach the CEO's desk."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "As Chief of Staff, you often have to influence senior VPs who have 15 more years of experience than you. How do you do that successfully?",
                            "competency": "Executive Influence, Diplomacy & Alignment",
                            "trap": "Playing the 'CEO said so' authority card or being deferential and ineffective.",
                            "model_defense": "S: A key product line was slipping its launch timeline because Product and Engineering leaders were in a deadlock over architectural scope, threatening a major board commitment. T: Align both leaders on a unified release scope without invoking the CEO's authority. A: Met with each leader 1-on-1 to understand their underlying concerns: Engineering feared technical debt, while Product feared missing critical enterprise feature parity. Brought them together with a structured trade-off matrix; agreed to an MVP launch with the top 3 revenue-critical features and scheduled a dedicated refactoring sprint for debt remediation immediately following the release. R: Delivered the product on schedule for the board deadline, generated $400k in Q1 bookings, and strengthened cross-functional trust."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Learn the CEO's cognitive cadence and priorities; audit company OKRs; build rapport with executive leaders.",
                        "day_60": "Own the preparation and execution of the quarterly Board of Directors deck; resolve 2 major inter-team bottlenecks.",
                        "day_90": "Launch and incubate a new high-leverage strategic project; establish self-sustaining executive operating rhythm."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹15.0L - ₹55.0L LPA",
                        "us_usd": "$160,000 - $275,000/yr",
                        "remote_usd": "$120,000 - $220,000/yr"
                    }
                },
                "founders_office_associate": {
                    "title": "Founder's Office Associate",
                    "aliases": ["Strategy & Ops Associate", "Special Projects Lead", "Entrepreneur in Residence (EIR)", "Growth & Strategy Analyst"],
                    "description": "High-velocity generalist executing zero-to-one initiatives, market expansions, operational troubleshooting, and fundraising collateral.",
                    "hard_skills": ["Financial Modeling", "Market Research & Competitive Intelligence", "Data Analytics (SQL/Excel)", "Fast Prototyping", "Investor Pitch Decks", "Vendor Sourcing", "Growth Hacking"],
                    "soft_skills": ["Insatiable Curiosity", "First-Principles Thinking", "Speed of Execution", "Hustle & Resourcefulness"],
                    "ats_keywords": ["Founders Office", "Special Projects", "Market Research", "Financial Modeling", "Zero-to-One", "Competitive Intelligence", "Pitch Decks", "Growth Experiments", "Venture Capital", "Business Strategy"],
                    "sample_kpis": ["Execution of high-impact pilot projects within 14 days", "Creation of investor materials leading to term sheets", "Identification of new revenue opportunities worth > $100k", "Zero operational downtime on ad-hoc leadership requests"],
                    "typical_responsibilities": [
                        "Work directly with founders on daily strategic priorities and critical firefighting.",
                        "Model market sizing, TAM/SAM/SOM, and unit economics for potential new business verticals.",
                        "Execute rapid commercial pilots and user interviews testing early product-market fit.",
                        "Draft compelling fundraising decks, memos, and data room diligence materials.",
                        "Step in to temporarily run operational functions during rapid scaling phases."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Tell me about a project where you were given almost no instructions and complete ambiguity. How did you deliver?",
                            "competency": "First-Principles Execution Under Extreme Ambiguity",
                            "trap": "Waiting for instructions or complaining about lack of guidance.",
                            "model_defense": "S: The founder told me on a Friday afternoon: 'We need to know whether we should expand our delivery service to Hyderabad next month, and what it will cost.' T: Deliver a full financial model, competitive audit, and expansion recommendation by Monday morning. A: Analyzed pincode demographic data, competitor pricing, local commercial vehicle licensing laws, and warehouse rental rates; synthesized cold outreach calls to 5 local logistics operators; built a 3-scenario P&L model showing payback timeline and breakeven order volumes. R: Presented the 12-page expansion dossier on Monday; founder approved a phased 2-hub pilot based on the unit economic threshold identified."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master internal operating metrics, shadow founders on critical calls, deliver 3 rapid market research sprints.",
                        "day_60": "Design and execute an independent growth or efficiency experiment; present findings directly to leadership.",
                        "day_90": "Take full operational ownership of a new strategic initiative or partnership; drive tangible ROI."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹8.0L - ₹25.0L LPA",
                        "us_usd": "$90,000 - $155,000/yr",
                        "remote_usd": "$70,000 - $125,000/yr"
                    }
                }
            }
        },
        "people_hr_recruiting": {
            "name": "People Operations, HR Business Partnering & Technical Recruiting",
            "description": "Attracting top-tier talent, designing high-performance cultures, and managing employee lifecycle operations.",
            "roles": {
                "technical_recruiter": {
                    "title": "Technical Recruiter / Talent Acquisition Specialist",
                    "aliases": ["Talent Acquisition Partner", "Engineering Recruiter", "Executive Search Specialist", "Senior Sourcer"],
                    "description": "Sources, screens, and closes high-caliber engineering, product, and leadership talent across global markets.",
                    "hard_skills": ["Boolean Search & X-Ray Sourcing", "LinkedIn Recruiter / Gem / Ashby", "ATS Management (Greenhouse/Lever/Workday)", "Interview Calibration & Rubrics", "Offer Negotiation & Closing", "Talent Pipeline Analytics", "Candidate Experience Management"],
                    "soft_skills": ["Persuasive Communication", "Empathy & Relationship Building", "Negotiation Tactics", "Tenacity"],
                    "ats_keywords": ["Technical Recruiter", "Talent Acquisition", "Full Lifecycle Recruiting", "Boolean Search", "LinkedIn Recruiter", "Greenhouse", "Lever", "Candidate Sourcing", "Offer Closing", "Time to Hire", "Pipeline Management", "Tech Hiring"],
                    "sample_kpis": ["Time-to-fill < 38 days for hard-to-hire tech roles", "Offer acceptance rate > 85%", "Candidate satisfaction score (CSAT) > 94%", "Hiring manager interview-to-offer ratio < 4:1"],
                    "typical_responsibilities": [
                        "Partner with engineering leaders to write high-converting job specifications and calibration rubrics.",
                        "Source passive top-decile candidates through targeted Boolean and community sourcing.",
                        "Conduct rigorous behavioral and cultural alignment initial screening calls.",
                        "Guide candidates smoothly through multi-round technical interview loops.",
                        "Structure and negotiate competitive equity/salary offers to maximize acceptance rates."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Walk me through how you closed a highly competitive candidate who was holding 3 other counter-offers.",
                            "competency": "Candidate Relationship Building & Value-Based Closing",
                            "trap": "Relying purely on offering more cash without understanding personal motivators.",
                            "model_defense": "S: A Staff Distributed Systems Engineer held competitive offers from Google and Uber and was leaning away from our Series B startup. T: Win the candidate without exceeding our approved salary band. A: Conducted deep discovery on their career aspirations; uncovered that their primary frustration at Big Tech was slow deployment velocity and lack of architecture ownership. Arranged an informal dinner with our CTO and VP of Eng mapping out the specific core payment engine they would own from scratch; structured a performance-linked equity grant that gave them higher upside. R: Candidate signed our offer over the higher cash counter-offers and started within 14 days."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Calibrate on open requisitions with hiring managers; audit Greenhouse pipelines; initiate outbound sourcing.",
                        "day_60": "Deliver 12+ qualified candidate screens per week; advance 5 candidates to final round; close first 2 hires.",
                        "day_90": "Achieve full quota velocity; reduce average time-to-fill by 15%; establish structured interview training for interviewers."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹6.0L - ₹24.0L LPA",
                        "us_usd": "$80,000 - $150,000/yr",
                        "remote_usd": "$60,000 - $120,000/yr"
                    }
                }
            }
        },
        "customer_success_support": {
            "name": "Customer Success, Solutions Architecture & Support Engineering",
            "description": "Maximizing customer value realization, preventing account churn, and driving net revenue retention (NRR).",
            "roles": {
                "customer_success_manager": {
                    "title": "Customer Success Manager (CSM)",
                    "aliases": ["Client Success Director", "Strategic Account Manager", "Customer Experience Lead"],
                    "description": "Drives enterprise onboarding, adoption, executive Quarterly Business Reviews (QBRs), and renewals.",
                    "hard_skills": ["Gainsight / Totango / ChurnZero", "Net Retention Rate (NRR) Modeling", "Executive QBR Presentations", "Account Health Scoring", "Product Onboarding Protocols", "Contract Renewals"],
                    "soft_skills": ["Empathy", "Proactive Problem Solving", "Consultative Presence"],
                    "ats_keywords": ["Customer Success", "Gainsight", "Net Revenue Retention (NRR)", "Churn Prevention", "Quarterly Business Reviews (QBR)", "Onboarding", "Account Health", "Customer Retention"],
                    "sample_kpis": ["Net Revenue Retention (NRR) > 115%", "Gross account churn < 3%", "Onboarding time-to-value < 21 days"],
                    "typical_responsibilities": [
                        "Own commercial renewals and adoption milestones across enterprise client portfolios.",
                        "Conduct executive QBRs demonstrating concrete ROI and business value realized."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How did you rescue an at-risk enterprise customer that had threatened to cancel their contract?",
                            "competency": "Customer Escalation & Relationship Turnaround",
                            "trap": "Offering discounts before solving the underlying product adoption failure.",
                            "model_defense": "S: A $120k ARR client served a cancellation notice citing poor team adoption and unreturned support tickets. T: Turn around the relationship and secure contract renewal within 45 days. A: Traveled to their office for an executive alignment session with their VP; discovered their frontline users had never received tailored training for their specific workflow. Built a customized 3-session training workshop, assigned a dedicated technical engineer to resolve their 4 open integration tickets, and instituted bi-weekly progress updates with clear milestone metrics. R: Rescued the account, improved their health score from red to green, and secured a 2-year renewal contract with a 20% expansion."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Review all portfolio account health scores and top support tickets.",
                        "day_60": "Conduct 10 customer check-ins and lead first executive QBR.",
                        "day_90": "Deliver 100% on-time renewals and identify 2 account expansion opportunities."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.0L - ₹24.0L LPA",
                        "us_usd": "$90,000 - $160,000/yr",
                        "remote_usd": "$65,000 - $125,000/yr"
                    }
                }
            }
        },
        "healthcare_biotech": {
            "name": "Healthcare, Clinical Data & BioTech Informatics",
            "description": "Managing healthcare informatics, regulatory medical compliance, clinical trial data, and computational biology.",
            "roles": {
                "clinical_data_specialist": {
                    "title": "Clinical Data & Healthcare Informatics Specialist",
                    "aliases": ["Health Informatics Analyst", "Clinical Data Manager", "Bioinformatics Specialist"],
                    "description": "Manages electronic health record (EHR) data architectures, HIPAA compliance, clinical trial registries, and medical data pipelines.",
                    "hard_skills": ["FHIR / HL7 Standards", "HIPAA / PHI Compliance", "Electronic Health Records (Epic, Cerner)", "SQL & Python", "Clinical Trial Data Management (CDISC SDTM)", "Medical Terminology (SNOMED, ICD-10)"],
                    "soft_skills": ["Patient Privacy Ethics", "Methodical Precision", "Cross-Disciplinary Rigor"],
                    "ats_keywords": ["Healthcare Informatics", "HIPAA", "FHIR", "HL7", "Clinical Data Management", "CDISC", "EHR", "Epic", "Cerner", "ICD-10", "Medical Data Analytics"],
                    "sample_kpis": ["100% HIPAA compliance with zero PHI leaks", "Clinical data query turnaround < 24h"],
                    "typical_responsibilities": [
                        "Architect interoperable healthcare data pipelines adhering to FHIR and HL7 data exchange standards.",
                        "Ensure strict end-to-end de-identification and encryption of Protected Health Information (PHI)."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "How do you enforce absolute HIPAA compliance when building clinical analytics pipelines?",
                            "competency": "Healthcare Data Governance & Regulatory Adherence",
                            "trap": "Treating medical data like standard e-commerce telemetry.",
                            "model_defense": "S: Our research team needed access to longitudinal patient treatment records to evaluate drug efficacy, but raw data contained 18 HIPAA identifier fields. T: Enable data science analysis without violating federal privacy laws. A: Built an automated de-identification pipeline in Python using the Safe Harbor method: hashed MRNs with salted SHA-256 tokens, shifted dates within a uniform random window while preserving relative intervals, and grouped zip codes to 3 digits. Enforced row-level security and access logging. R: Enabled the research team to complete the clinical trial analysis on schedule with 100% verified HIPAA compliance."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Review institutional IRB protocols, HIPAA compliance standards, and EHR data schemas.",
                        "day_60": "Build and validate an automated FHIR data ingestion pipeline.",
                        "day_90": "Publish compliant clinical analytics dashboard for medical investigators."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹7.0L - ₹25.0L LPA",
                        "us_usd": "$95,000 - $165,000/yr",
                        "remote_usd": "$75,000 - $135,000/yr"
                    }
                }
            }
        },
        "consulting_advisory": {
            "name": "Management Consulting & Enterprise Advisory",
            "description": "Delivering strategic clarity, operational restructuring, digital transformation, and executive advisory to Fortune 500 boards.",
            "roles": {
                "management_consultant": {
                    "title": "Management Consultant / Strategy Advisor",
                    "aliases": ["Strategy Consultant", "Engagement Manager", "Associate Partner", "Operations Advisory Specialist"],
                    "description": "Advises corporate executives on market entry, cost restructuring, organizational design, and digital transformations.",
                    "hard_skills": ["MECE Problem Structuring", "Hypothesis-Driven Problem Solving", "Financial & Strategic Modeling", "Executive Slide Crafting (Think-Cell/PowerPoint)", "Stakeholder Interview Synthesis", "Benchmarking & Competitive Analysis"],
                    "soft_skills": ["Executive Presence", "Rapid Learning Velocity", "Top-Down Communication", "High Poise"],
                    "ats_keywords": ["Management Consulting", "Strategy Consulting", "MECE", "Market Entry", "Digital Transformation", "Cost Optimization", "Financial Modeling", "Executive Presentation", "Due Diligence", "Benchmarking"],
                    "sample_kpis": ["Quantifiable client cost reduction or revenue lift > $5M", "Client project Net Promoter Score > 90%"],
                    "typical_responsibilities": [
                        "Structure ambiguous client business problems into mutually exclusive, collectively exhaustive (MECE) issue trees.",
                        "Synthesize qualitative C-suite interviews and quantitative market benchmarks into executive recommendations.",
                        "Lead transformation steering committee meetings and board-level presentations."
                    ],
                    "star_interview_prep": [
                        {
                            "question": "Walk me through how you solve an ambiguous client business problem using the MECE framework.",
                            "competency": "MECE Problem Structuring & First-Principles Strategy",
                            "trap": "Jumping directly to solutions without proving root cause decomposition.",
                            "model_defense": "S: A national retail bank faced a 25% decline in profitability across regional branches. T: Identify the drivers of decline and formulate an actionable turnaround plan in 6 weeks. A: Structured the problem using a MECE profitability tree: split into Revenue (Interest Income vs Fee Income) and Costs (Fixed Branch Real Estate vs Variable Staffing & IT). Data analysis proved fee income had collapsed by 42% due to customer migration to mobile apps, while branch real estate costs remained static. Proposed closing 35 redundant branches while converting 50 others into digital advisory centers. R: Client leadership adopted the strategy, resulting in an annualized $14M profit recovery within 12 months."
                        }
                    ],
                    "thirty_sixty_ninety_plan": {
                        "day_30": "Master client industry context, interview 20 key operational stakeholders, build base financial models.",
                        "day_60": "Deliver mid-engagement findings presentation to the executive sponsor; validate strategic hypotheses.",
                        "day_90": "Deliver final board recommendation deck with phased implementation roadmaps and ROI projections."
                    },
                    "compensation_benchmarks": {
                        "india_lpa": "₹14.0L - ₹45.0L LPA",
                        "us_usd": "$140,000 - $240,000/yr",
                        "remote_usd": "$105,000 - $190,000/yr"
                    }
                }
            }
        }
    }
}


def export_taxonomy_to_json(path: Optional[Path] = None) -> Path:
    target_path = path or JSON_EXPORT_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as fp:
        json.dump(UNIVERSAL_JOB_TAXONOMY, fp, indent=2, ensure_ascii=False)
    return target_path


def export_taxonomy_to_sqlite(db_path: Optional[Path] = None) -> Path:
    target_db = db_path or SQLITE_DB_PATH
    target_db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_db))
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS job_archetypes;")
    c.execute("""
        CREATE TABLE job_archetypes (
            role_key TEXT PRIMARY KEY,
            family_key TEXT,
            family_name TEXT,
            title TEXT,
            aliases TEXT,
            description TEXT,
            hard_skills TEXT,
            soft_skills TEXT,
            ats_keywords TEXT,
            sample_kpis TEXT,
            typical_responsibilities TEXT,
            star_interview_prep TEXT,
            thirty_sixty_ninety_plan TEXT,
            compensation_benchmarks TEXT
        );
    """)

    for fam_key, fam_data in UNIVERSAL_JOB_TAXONOMY["families"].items():
        fam_name = fam_data["name"]
        for role_key, role_data in fam_data["roles"].items():
            c.execute("""
                INSERT INTO job_archetypes (
                    role_key, family_key, family_name, title, aliases, description,
                    hard_skills, soft_skills, ats_keywords, sample_kpis,
                    typical_responsibilities, star_interview_prep,
                    thirty_sixty_ninety_plan, compensation_benchmarks
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                role_key,
                fam_key,
                fam_name,
                role_data["title"],
                json.dumps(role_data.get("aliases", [])),
                role_data.get("description", ""),
                json.dumps(role_data.get("hard_skills", [])),
                json.dumps(role_data.get("soft_skills", [])),
                json.dumps(role_data.get("ats_keywords", [])),
                json.dumps(role_data.get("sample_kpis", [])),
                json.dumps(role_data.get("typical_responsibilities", [])),
                json.dumps(role_data.get("star_interview_prep", [])),
                json.dumps(role_data.get("thirty_sixty_ninety_plan", {})),
                json.dumps(role_data.get("compensation_benchmarks", {}))
            ))

    conn.commit()
    conn.close()
    return target_db


def get_all_job_families() -> List[Dict[str, Any]]:
    return [
        {"family_key": k, "name": v["name"], "description": v["description"], "role_count": len(v["roles"])}
        for k, v in UNIVERSAL_JOB_TAXONOMY["families"].items()
    ]


def get_all_archetypes() -> List[Dict[str, Any]]:
    archetypes = []
    for fam_key, fam_data in UNIVERSAL_JOB_TAXONOMY["families"].items():
        for role_key, role_data in fam_data["roles"].items():
            item = dict(role_data)
            item["role_key"] = role_key
            item["family_key"] = fam_key
            item["family_name"] = fam_data["name"]
            archetypes.append(item)
    return archetypes


def get_archetype_by_key(role_key: str) -> Optional[Dict[str, Any]]:
    for fam_key, fam_data in UNIVERSAL_JOB_TAXONOMY["families"].items():
        if role_key in fam_data["roles"]:
            res = dict(fam_data["roles"][role_key])
            res["role_key"] = role_key
            res["family_key"] = fam_key
            res["family_name"] = fam_data["name"]
            return res
    return None


if __name__ == "__main__":
    j_path = export_taxonomy_to_json()
    db_path = export_taxonomy_to_sqlite()
    print(f"Taxonomy JSON exported: {j_path}")
    print(f"Taxonomy SQLite exported: {db_path}")
    print(f"Total Families: {len(get_all_job_families())}")
    print(f"Total Archetypes: {len(get_all_archetypes())}")
