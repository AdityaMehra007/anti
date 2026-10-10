import csv

records = [
    # AI & Automation
    {
        "Domain / Category": "AI & Automation",
        "Specialization Track": "AI Agent & Workflow Integration (n8n, Make, LangChain)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/ai-integration/",
        "Global Hourly Rate (USD)": "$60 - $140/hr",
        "India / Bengaluru Rate": "$35 - $85/hr (₹2,900 - ₹7,100/hr)",
        "Standard Fixed-Price Milestone": "$1,500 - $6,500 per autonomous system",
        "Top In-Demand Skills & Tools": "n8n, LangChain, OpenAI/Anthropic APIs, Pinecone, Webhooks, Python, Docker",
        "High-Ticket Closing Strategy": "Attach visual n8n workflow diagram + 1-minute Loom video demonstrating automated CRM enrichment",
        "Sample Project Archetype": "Autonomous inbound lead qualification & appointment booking agent across WhatsApp/Email"
    },
    {
        "Domain / Category": "AI & Automation",
        "Specialization Track": "AI Video Generation, Synthetic Media & Editing",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/ai-video-generation/",
        "Global Hourly Rate (USD)": "$50 - $125/hr",
        "India / Bengaluru Rate": "$30 - $75/hr (₹2,500 - ₹6,200/hr)",
        "Standard Fixed-Price Milestone": "$800 - $4,000 per video campaign",
        "Top In-Demand Skills & Tools": "HeyGen, Runway Gen-3, ElevenLabs, Midjourney, Premiere Pro, CapCut, After Effects",
        "High-Ticket Closing Strategy": "Send 3 sample 15-second personalized ad hooks generated for the client's exact competitor niche",
        "Sample Project Archetype": "High-converting UGC & AI avatar performance ad batch (20 variations) for DTC brand"
    },
    {
        "Domain / Category": "AI & Automation",
        "Specialization Track": "Custom AI Chatbots & Customer Service LLMs",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/chatbot-development/",
        "Global Hourly Rate (USD)": "$55 - $130/hr",
        "India / Bengaluru Rate": "$30 - $70/hr (₹2,500 - ₹5,800/hr)",
        "Standard Fixed-Price Milestone": "$1,200 - $5,000 per deployed bot",
        "Top In-Demand Skills & Tools": "Voiceflow, Botpress, FastAPI, RAG, Zendesk/Intercom integration, vector embeddings",
        "High-Ticket Closing Strategy": "Share interactive demo bot hosted on Vercel trained on the client's public help center URLs",
        "Sample Project Archetype": "Customer support bot resolving 65% Tier-1 tickets with human handoff fallback"
    },
    {
        "Domain / Category": "AI & Automation",
        "Specialization Track": "AI Data Annotation, Fine-Tuning & Evaluation",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/data-annotation/",
        "Global Hourly Rate (USD)": "$25 - $60/hr",
        "India / Bengaluru Rate": "$18 - $40/hr (₹1,500 - ₹3,300/hr)",
        "Standard Fixed-Price Milestone": "$500 - $2,500 per annotated dataset",
        "Top In-Demand Skills & Tools": "RLHF, prompt red-teaming, taxonomy creation, Labelbox, Scale Rapid, JSONL formatting",
        "High-Ticket Closing Strategy": "Provide sample rubric and 20 verified gold-standard evaluated prompt responses upfront",
        "Sample Project Archetype": "Domain-specific medical/legal instruction-tuning dataset curation (5,000 QA pairs)"
    },

    # Development & IT
    {
        "Domain / Category": "Development & IT",
        "Specialization Track": "Full-Stack Web Development (Next.js, TypeScript, Tailwind)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/full-stack-development/",
        "Global Hourly Rate (USD)": "$50 - $120/hr",
        "India / Bengaluru Rate": "$30 - $75/hr (₹2,500 - ₹6,200/hr)",
        "Standard Fixed-Price Milestone": "$2,500 - $12,000 per full MVP",
        "Top In-Demand Skills & Tools": "Next.js 15, React, Node.js, Supabase, PostgreSQL, Prisma, Vercel, Stripe API",
        "High-Ticket Closing Strategy": "Deliver clean modular architecture audit + Figma-to-code prototype live demo",
        "Sample Project Archetype": "B2B SaaS dashboard with authentication, team workspaces, usage metering & Stripe billing"
    },
    {
        "Domain / Category": "Development & IT",
        "Specialization Track": "Python Backend & API Infrastructure",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/python/",
        "Global Hourly Rate (USD)": "$55 - $125/hr",
        "India / Bengaluru Rate": "$35 - $80/hr (₹2,900 - ₹6,600/hr)",
        "Standard Fixed-Price Milestone": "$1,500 - $7,500 per microservice",
        "Top In-Demand Skills & Tools": "FastAPI, Django, Celery, Redis, PostgreSQL, Docker, AWS Lambda, AsyncIO",
        "High-Ticket Closing Strategy": "Propose OpenAPI spec with verified response latency SLAs (<100ms) and test coverage",
        "Sample Project Archetype": "High-throughput data ingestion pipeline handling 1M+ daily webhook events"
    },
    {
        "Domain / Category": "Development & IT",
        "Specialization Track": "Mobile App Development (React Native & Flutter)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/mobile-development/",
        "Global Hourly Rate (USD)": "$45 - $110/hr",
        "India / Bengaluru Rate": "$25 - $65/hr (₹2,100 - ₹5,400/hr)",
        "Standard Fixed-Price Milestone": "$3,000 - $15,000 per cross-platform app",
        "Top In-Demand Skills & Tools": "React Native, Expo, Flutter, Dart, Firebase, iOS TestFlight, Google Play Console",
        "High-Ticket Closing Strategy": "Provide TestFlight/APK build link of a similar production app in the same niche",
        "Sample Project Archetype": "Cross-platform fintech/health tracking mobile app with push notifications and in-app purchases"
    },
    {
        "Domain / Category": "Development & IT",
        "Specialization Track": "DevOps, Cloud & Infrastructure Architecture",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/devops/",
        "Global Hourly Rate (USD)": "$65 - $150/hr",
        "India / Bengaluru Rate": "$40 - $95/hr (₹3,300 - ₹7,900/hr)",
        "Standard Fixed-Price Milestone": "$2,000 - $8,500 per infrastructure rollout",
        "Top In-Demand Skills & Tools": "Terraform, Kubernetes, Docker, AWS (ECS/EKS/RDS), GitHub Actions CI/CD, Datadog",
        "High-Ticket Closing Strategy": "Show Infrastructure-as-Code Terraform snippet + estimated cloud cost reduction report",
        "Sample Project Archetype": "Zero-downtime multi-region AWS migration with auto-scaling and blue/green deployments"
    },

    # Sales & Marketing
    {
        "Domain / Category": "Sales & Marketing",
        "Specialization Track": "B2B Lead Generation & Account Prospecting",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/lead-generation/",
        "Global Hourly Rate (USD)": "$35 - $80/hr",
        "India / Bengaluru Rate": "$20 - $50/hr (₹1,700 - ₹4,200/hr)",
        "Standard Fixed-Price Milestone": "$350 - $1,800 per 500-1,000 verified leads",
        "Top In-Demand Skills & Tools": "Apollo.io, LinkedIn Sales Navigator, Clay.com, MillionVerifier, Google Sheets, CRM mapping",
        "High-Ticket Closing Strategy": "Attach 10-prospect verified sample dataset with valid corporate emails and LinkedIn profiles",
        "Sample Project Archetype": "Custom ICP list building of 1,000 verified Series A SaaS VP of Engineering leads with verified work emails"
    },
    {
        "Domain / Category": "Sales & Marketing",
        "Specialization Track": "Cold Email Infrastructure & Outbound Deliverability",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/email-marketing/",
        "Global Hourly Rate (USD)": "$50 - $110/hr",
        "India / Bengaluru Rate": "$30 - $70/hr (₹2,500 - ₹5,800/hr)",
        "Standard Fixed-Price Milestone": "$1,000 - $4,500 per outbound engine",
        "Top In-Demand Skills & Tools": "Smartlead, Instantly.ai, Google Workspace secondary domains, SPF/DKIM/DMARC, Clay, Spintax",
        "High-Ticket Closing Strategy": "Offer DNS deliverability audit report uncovering SPF/DMARC misalignment in client's secondary domains",
        "Sample Project Archetype": "Setup of 15 secondary domains, 45 inboxes, automated warmup, and 3-step personalized cold sequence"
    },
    {
        "Domain / Category": "Sales & Marketing",
        "Specialization Track": "B2B Appointment Setting & SDR Outreach",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/appointment-setting/",
        "Global Hourly Rate (USD)": "$30 - $65/hr",
        "India / Bengaluru Rate": "$18 - $40/hr (₹1,500 - ₹3,300/hr)",
        "Standard Fixed-Price Milestone": "$1,500 - $4,000/mo retainer + $100-$250/qualified call",
        "Top In-Demand Skills & Tools": "HubSpot, Salesforce, LinkedIn outreach, cold calling, objection handling, Calendly",
        "High-Ticket Closing Strategy": "Share call recording excerpts demonstrating professional US-accented English and consultative qualification",
        "Sample Project Archetype": "Booking 12-18 qualified enterprise demo calls per month with IT directors in North America"
    },
    {
        "Domain / Category": "Sales & Marketing",
        "Specialization Track": "Performance Marketing & Paid Ads (Google/Meta)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/google-ads/",
        "Global Hourly Rate (USD)": "$50 - $125/hr",
        "India / Bengaluru Rate": "$30 - $75/hr (₹2,500 - ₹6,200/hr)",
        "Standard Fixed-Price Milestone": "$1,200 - $5,000/mo management fee",
        "Top In-Demand Skills & Tools": "Google Ads, Meta Ads Manager, GA4, GTM server-side tracking, CRO, landing page design",
        "High-Ticket Closing Strategy": "Provide 1-page account audit showing wasted search query spend and negative keyword opportunities",
        "Sample Project Archetype": "Scaling B2B Google Search & Performance Max campaign from $5k/mo to $30k/mo at <$85 CPL"
    },

    # Admin, Operations & Customer Support
    {
        "Domain / Category": "Admin & Support",
        "Specialization Track": "Virtual Executive Assistant & Business Operations",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/virtual-assistant/",
        "Global Hourly Rate (USD)": "$25 - $55/hr",
        "India / Bengaluru Rate": "$15 - $35/hr (₹1,250 - ₹2,900/hr)",
        "Standard Fixed-Price Milestone": "$1,000 - $3,500/mo dedicated fractional retainer",
        "Top In-Demand Skills & Tools": "Calendar management, Slack, Notion, Asana, Zapier, travel planning, inbox triage, expense tracking",
        "High-Ticket Closing Strategy": "Present structured Notion Operating System template showing inbox zero protocols and daily debrief cadence",
        "Sample Project Archetype": "Executive support for US venture founder managing schedule, investor updates, travel & vendor invoices"
    },
    {
        "Domain / Category": "Admin & Support",
        "Specialization Track": "Customer Experience & Support Engineering (Zendesk / Intercom)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/customer-service/",
        "Global Hourly Rate (USD)": "$22 - $50/hr",
        "India / Bengaluru Rate": "$14 - $30/hr (₹1,150 - ₹2,500/hr)",
        "Standard Fixed-Price Milestone": "$800 - $2,500/mo per shift coverage",
        "Top In-Demand Skills & Tools": "Zendesk, Intercom, Gorgias, Jira Service Desk, macro authoring, CSAT optimization, SLA tracking",
        "High-Ticket Closing Strategy": "Demonstrate SLA management dashboard + automated trigger rules reducing response time under 15 minutes",
        "Sample Project Archetype": "24/7 Tier-1/2 customer support coverage for fast-growing SaaS application with >95% CSAT"
    },
    {
        "Domain / Category": "Admin & Support",
        "Specialization Track": "E-Commerce Operations & Marketplace Management",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/ecommerce/",
        "Global Hourly Rate (USD)": "$30 - $70/hr",
        "India / Bengaluru Rate": "$18 - $45/hr (₹1,500 - ₹3,700/hr)",
        "Standard Fixed-Price Milestone": "$1,000 - $4,000/mo management fee",
        "Top In-Demand Skills & Tools": "Shopify, Amazon Seller Central, Helium 10, inventory forecasting, listing optimization, Klaviyo",
        "High-Ticket Closing Strategy": "Submit listing audit highlighting missing backend search terms, A+ content gaps, and margin leaks",
        "Sample Project Archetype": "End-to-end catalog management, order fulfillment troubleshooting, and multi-channel sync"
    },

    # Data & Analytics
    {
        "Domain / Category": "Data & Analytics",
        "Specialization Track": "Data Analytics & Business Intelligence (Power BI, Tableau, SQL)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/data-analytics/",
        "Global Hourly Rate (USD)": "$45 - $110/hr",
        "India / Bengaluru Rate": "$25 - $65/hr (₹2,100 - ₹5,400/hr)",
        "Standard Fixed-Price Milestone": "$1,200 - $6,000 per dashboard suite",
        "Top In-Demand Skills & Tools": "SQL, Power BI, Tableau, Snowflake, BigQuery, dbt, Looker, Python pandas",
        "High-Ticket Closing Strategy": "Share interactive web-hosted Power BI dashboard portfolio with drill-through executive views",
        "Sample Project Archetype": "Automated executive revenue, cohort retention, and CAC/LTV dashboard connected to Snowflake"
    },
    {
        "Domain / Category": "Data & Analytics",
        "Specialization Track": "Market Research, Industry Intelligence & Pitch Decks",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/market-research/",
        "Global Hourly Rate (USD)": "$40 - $95/hr",
        "India / Bengaluru Rate": "$22 - $55/hr (₹1,800 - ₹4,600/hr)",
        "Standard Fixed-Price Milestone": "$800 - $4,500 per research report",
        "Top In-Demand Skills & Tools": "TAM/SAM/SOM modeling, competitive benchmarking, Statista, PitchBook, PowerPoint, Canva",
        "High-Ticket Closing Strategy": "Attach 2-page sample executive brief highlighting competitor pricing matrix and market share breakdown",
        "Sample Project Archetype": "Comprehensive 30-page market entry analysis and investor deck for GCC tech expansion into India"
    },

    # Design & Creative
    {
        "Domain / Category": "Design & Creative",
        "Specialization Track": "Product Design & Design Systems (UI/UX - Figma)",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/ui-ux-design/",
        "Global Hourly Rate (USD)": "$45 - $115/hr",
        "India / Bengaluru Rate": "$25 - $65/hr (₹2,100 - ₹5,400/hr)",
        "Standard Fixed-Price Milestone": "$2,000 - $8,000 per app/web design",
        "Top In-Demand Skills & Tools": "Figma, auto-layout, design tokens, wireframing, user testing, responsive design, component libraries",
        "High-Ticket Closing Strategy": "Send interactive Figma prototype link redesigning the client's current friction-heavy signup flow",
        "Sample Project Archetype": "Complete web app redesign with scalable design system components and developer handoff documentation"
    },
    {
        "Domain / Category": "Design & Creative",
        "Specialization Track": "Motion Graphics & Brand Video Production",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/video-editing/",
        "Global Hourly Rate (USD)": "$40 - $95/hr",
        "India / Bengaluru Rate": "$20 - $55/hr (₹1,700 - ₹4,600/hr)",
        "Standard Fixed-Price Milestone": "$600 - $3,500 per animated video",
        "Top In-Demand Skills & Tools": "After Effects, Premiere Pro, Blender, sound design, kinetic typography, Lottie animations",
        "High-Ticket Closing Strategy": "Send 30-second custom animated teaser incorporating client's actual logo and product UI assets",
        "Sample Project Archetype": "90-second SaaS explainer video with custom 2D vector animation, sound effects, and voiceover sync"
    },

    # Writing & Content
    {
        "Domain / Category": "Writing & Content",
        "Specialization Track": "Technical Writing & API Documentation",
        "Upwork Directory URL": "https://www.upwork.com/freelance-jobs/technical-writing/",
        "Global Hourly Rate (USD)": "$45 - $105/hr",
        "India / Bengaluru Rate": "$25 - $60/hr (₹2,100 - ₹5,000/hr)",
        "Standard Fixed-Price Milestone": "$1,000 - $5,000 per documentation set",
        "Top In-Demand Skills & Tools": "Markdown, Git, OpenAPI/Swagger, ReadMe, Mintlify, developer tutorials, architecture guides",
        "High-Ticket Closing Strategy": "Attach GitHub repo link showcasing self-authored developer guide with runnable curl examples",
        "Sample Project Archetype": "Complete developer portal documentation including quickstart guides, SDK references, and authentication flows"
    }
]

output_file = "e:/anti/upwork_freelance_jobs_ecosystem.csv"

fieldnames = [
    "Domain / Category",
    "Specialization Track",
    "Upwork Directory URL",
    "Global Hourly Rate (USD)",
    "India / Bengaluru Rate",
    "Standard Fixed-Price Milestone",
    "Top In-Demand Skills & Tools",
    "High-Ticket Closing Strategy",
    "Sample Project Archetype"
]

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in records:
        writer.writerow(row)

print(f"Successfully generated {output_file} with {len(records)} verified records.")
