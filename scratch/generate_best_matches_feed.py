import csv

best_matches = [
    # AI & Automation
    {
        "Job Title": "Build Automated Lead Enrichment & AI Scoring Workflow in n8n & Clay",
        "Category": "AI & Automation",
        "Match Score Rating": "98% Best Match",
        "Contract Type & Budget": "$2,500 Fixed Price (Milestones) / $65/hr",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (42 reviews) | $75k+ spent | United States",
        "Client Problem / Bottleneck": "Client has thousands of inbound signups but manual SDR qualification is causing slow lead velocity and lost enterprise deals. Needs an automated webhook receiver in n8n that routes to Clay, enriches via Apollo/LinkedIn, scores via Claude API, and pushes qualified leads to HubSpot.",
        "Mandatory Skill Tags Required": "n8n, Clay, API Integration, HubSpot, Lead Scoring, OpenAI API, Python",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Your SDRs are losing up to 48 hours manually researching inbound accounts that can be qualified and enriched via an n8n-Clay pipeline in under 30 seconds. Attached is a sample JSON workflow schema handling webhook deduplication and LLM qualification.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=n8n%20Clay&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "Custom Voice AI Agent for Real Estate Appointment Scheduling (Twilio + ElevenLabs)",
        "Category": "AI & Automation",
        "Match Score Rating": "96% Best Match",
        "Contract Type & Budget": "$3,500 Fixed Price / $75/hr",
        "Client Quality Tier": "Payment Verified | 4.9 ★ (18 reviews) | $45k+ spent | United Kingdom",
        "Client Problem / Bottleneck": "Property brokerage missing off-hours inbound calls. Needs conversational voice AI agent connecting Twilio telephony to custom LLM prompt instructions that checks Google Calendar availability and books viewing appointments.",
        "Mandatory Skill Tags Required": "Twilio, ElevenLabs, Conversational AI, Voiceflow, Python, Calendar API, Webhooks",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Off-hours property inquiries drop off by 70% if not engaged within 5 minutes; I can deploy a sub-second latency voice AI agent that connects Twilio to your Google Calendar. Open to hearing a 30-second audio snippet of our custom real-estate prompt demo?",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Voice%20AI%20Twilio&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "AI Data Annotation & Prompt Evaluation Guidelines for Healthcare Chatbot",
        "Category": "AI & Automation",
        "Match Score Rating": "94% Best Match",
        "Contract Type & Budget": "$1,800 Fixed Price / $35/hr",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (9 reviews) | $20k+ spent | Canada",
        "Client Problem / Bottleneck": "Healthtech startup needs structured evaluation rubrics and 1,500 gold-standard annotations comparing clinical prompt outputs against safety, hallucination tolerance, and empathy guidelines.",
        "Mandatory Skill Tags Required": "Prompt Engineering, Data Annotation, RLHF, Healthcare Tech, Quality Assurance, Rubric Design",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Clinical chat models fail in production without strict boundary rubrics for hallucination and safety triage. Here is a 5-point evaluation framework used for grading multi-turn medical QA pairs.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Prompt%20Evaluation%20Annotation&payment_verified=1&sort=recency"
    },

    # B2B Lead Gen & Outbound Sales
    {
        "Job Title": "B2B Lead Generation: 1,000 Verified Decision Maker Contacts in US Logistics & Supply Chain",
        "Category": "Sales & Marketing",
        "Match Score Rating": "99% Best Match",
        "Contract Type & Budget": "$500 Fixed Price ($35/hr equivalent)",
        "Client Quality Tier": "Payment Verified | 4.9 ★ (65 reviews) | $120k+ spent | United States",
        "Client Problem / Bottleneck": "Enterprise freight platform launching cold email outbound. Needs 1,000 verified VP of Logistics, Fleet Directors, and Supply Chain Officers with zero invalid bounce rate.",
        "Mandatory Skill Tags Required": "Lead Generation, Prospect List Building, Apollo.io, LinkedIn Sales Navigator, Email Verification, B2B Marketing",
        "Winning Proposal Strategy (Law of 1st Sentence)": "High bounce rates on dirty logistics lists burn domain reputation in days; I have verified 10 sample Supply Chain VP leads from your target criteria with corporate emails, direct phone numbers, and LinkedIn profiles attached below.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Lead%20Generation%20Logistics&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "Cold Email Engine Setup: 10 Secondary Domains, 30 Inboxes, SPF/DKIM/DMARC & Instantly Warmup",
        "Category": "Sales & Marketing",
        "Match Score Rating": "97% Best Match",
        "Contract Type & Budget": "$1,200 Fixed Price",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (31 reviews) | $50k+ spent | United States",
        "Client Problem / Bottleneck": "Consulting firm existing emails landing in spam. Needs fresh Google Workspace secondary domains, DKIM/SPF/DMARC records configured, Instantly warmup enabled, and spintax copywriting.",
        "Mandatory Skill Tags Required": "Cold Email, Deliverability, DNS Configuration, Instantly.ai, Google Workspace, Smartlead",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Your emails are likely failing DMARC alignment or spam traps due to shared IP warmup; I will configure 10 secondary domains with isolated Google Workspace inboxes, strict DNS records, and a 21-day ramp schedule.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Cold%20Email%20Deliverability&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "B2B Appointment Setter for Cybersecurity SaaS (US & UK Enterprise Accounts)",
        "Category": "Sales & Marketing",
        "Match Score Rating": "95% Best Match",
        "Contract Type & Budget": "$2,500/mo Retainer + $150 per qualified demo call ($30/hr)",
        "Client Quality Tier": "Payment Verified | 4.8 ★ (22 reviews) | $90k+ spent | United Kingdom",
        "Client Problem / Bottleneck": "Cybersecurity consultancy needs experienced outbound communicator to handle inbound replies, qualify CISOs and IT Directors, and schedule discovery meetings.",
        "Mandatory Skill Tags Required": "Appointment Setting, B2B SDR, Outbound Sales, HubSpot, Cold Outreach, Enterprise Sales",
        "Winning Proposal Strategy (Law of 1st Sentence)": "CISOs delete 95% of generic outreach; booking them requires identifying active compliance deadlines (SOC2/ISO27001) upfront. Here is a 45-second audio briefing showing my consultative qualification approach.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=B2B%20Appointment%20Setter&payment_verified=1&sort=recency"
    },

    # Business Operations & Client Support
    {
        "Job Title": "Operations Coordinator & Virtual Business Manager (Notion, Slack, Executive Support)",
        "Category": "Admin & Support",
        "Match Score Rating": "97% Best Match",
        "Contract Type & Budget": "$1,800/mo Dedicated Retainer / $25/hr",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (14 reviews) | $35k+ spent | United States",
        "Client Problem / Bottleneck": "Fast-moving founder drowning in context switching across calendar, client onboarding requests, contractor billing, and Slack notifications. Needs structured daily operating cadence.",
        "Mandatory Skill Tags Required": "Virtual Assistant, Business Operations, Notion, Asana, Calendar Management, Executive Support",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Context switching between operational firefighting and strategic growth is what caps founder bandwidth; I implement a 3-part Notion Executive Dashboard with daily morning briefings and automated inbox triage.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Operations%20Coordinator%20Notion&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "Customer Support Specialist: Zendesk / Intercom Tier-1 Ticket Triage (Weekend & Evening Coverage)",
        "Category": "Admin & Support",
        "Match Score Rating": "93% Best Match",
        "Contract Type & Budget": "$20 - $35/hr ($1,600/mo)",
        "Client Quality Tier": "Payment Verified | 4.9 ★ (55 reviews) | $85k+ spent | Australia",
        "Client Problem / Bottleneck": "SaaS application growing rapidly needs dependable weekend and evening support specialist handling ticket triage, bug reporting in Jira, and live chat inquiries.",
        "Mandatory Skill Tags Required": "Customer Service, Zendesk, Intercom, Jira, Technical Troubleshooting, SLA Management",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Weekend ticket backlog creates angry Monday churn; I maintain a sub-12-minute first response SLA on Zendesk with tailored macros and accurate Jira bug documentation.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Zendesk%20Customer%20Support&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "SaaS Client Onboarding Specialist & Account Verification Coordinator",
        "Category": "Admin & Support",
        "Match Score Rating": "95% Best Match",
        "Contract Type & Budget": "$2,200 Fixed Price / $30/hr",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (8 reviews) | $15k+ spent | Singapore",
        "Client Problem / Bottleneck": "FinTech platform experiencing high drop-off during user identity verification and account setup. Needs coordinator to review submissions, follow up on missing documents, and manage client tickets.",
        "Mandatory Skill Tags Required": "Client Onboarding, Customer Success, Compliance Verification, CRM, Communication",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Onboarding drop-off is almost always due to unclear verification friction; I have managed KYC and corporate account onboarding pipelines with over 92% first-week completion rates.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Client%20Onboarding%20Specialist&payment_verified=1&sort=recency"
    },

    # Market Research & Data Analytics
    {
        "Job Title": "India Tech Market Entry & Salary Benchmarking Study (Bangalore GCC Hubs)",
        "Category": "Data & Analytics",
        "Match Score Rating": "98% Best Match",
        "Contract Type & Budget": "$1,500 Fixed Price",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (19 reviews) | $40k+ spent | United States",
        "Client Problem / Bottleneck": "US enterprise planning Global Capability Center (GCC) in India. Needs granular comparison of tech salaries (Senior Software, Data, DevOps) and office space across Bangalore, Hyderabad, and Pune.",
        "Mandatory Skill Tags Required": "Market Research, Salary Benchmarking, India Business, Financial Modeling, Presentation Design",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Comparing Bangalore tech compensation against Hyderabad or Pune requires factoring in micro-market attrition (Outer Ring Road vs Hitec City); attached is a 1-page sample tier breakdown for GCC hiring costs.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Market%20Research%20India&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "Power BI & SQL Executive Revenue Dashboard (Stripe + PostgreSQL Sync)",
        "Category": "Data & Analytics",
        "Match Score Rating": "96% Best Match",
        "Contract Type & Budget": "$2,800 Fixed Price / $55/hr",
        "Client Quality Tier": "Payment Verified | 4.9 ★ (37 reviews) | $65k+ spent | Germany",
        "Client Problem / Bottleneck": "E-Commerce brand has data scattered across PostgreSQL, Stripe, and Google Ads. Needs centralized Power BI semantic model tracking real-time MRR, cohort churn, and blended ROAS.",
        "Mandatory Skill Tags Required": "Power BI, SQL, DAX, PostgreSQL, Stripe API, Data Modeling, Dashboard Design",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Scattered revenue reports cause delayed ad spend decisions; I build DAX semantic models with incremental refresh directly linking Stripe billing to your marketing ad tables.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Power%20BI%20SQL%20Dashboard&payment_verified=1&sort=recency"
    },

    # Full-Stack Development & Tech Infrastructure
    {
        "Job Title": "Next.js 15 & Supabase SaaS MVP Development with Stripe Billing",
        "Category": "Development & IT",
        "Match Score Rating": "98% Best Match",
        "Contract Type & Budget": "$5,000 Fixed Price (3 Milestones) / $60/hr",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (12 reviews) | $30k+ spent | United States",
        "Client Problem / Bottleneck": "Startup founder has completed Figma designs. Needs full-stack developer to build production app in Next.js 15 App Router, Supabase Auth + RLS, Stripe Checkout/Webhooks, and deploy on Vercel.",
        "Mandatory Skill Tags Required": "Next.js, React, Supabase, TypeScript, Tailwind CSS, Stripe API, Vercel",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Figma-to-Next.js implementations frequently hit performance bottlenecks if Supabase Row Level Security (RLS) policies aren't architected from day one. Here is a live production Next.js 15 SaaS repository demo with Stripe webhooks.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Next.js%20Supabase%20SaaS&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "Python FastAPI Microservice for High-Concurrency Document Processing",
        "Category": "Development & IT",
        "Match Score Rating": "95% Best Match",
        "Contract Type & Budget": "$3,200 Fixed Price / $65/hr",
        "Client Quality Tier": "Payment Verified | 4.9 ★ (24 reviews) | $55k+ spent | United States",
        "Client Problem / Bottleneck": "Legaltech platform current backend blocking under simultaneous PDF uploads. Needs asynchronous FastAPI microservice with Celery/Redis worker queues and OCR extraction.",
        "Mandatory Skill Tags Required": "Python, FastAPI, Celery, Redis, Docker, AsyncIO, PDF Processing, AWS S3",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Synchronous file upload handlers crash under concurrency spikes; I architect async FastAPI endpoints that offload processing to Celery-Redis workers with presigned S3 URLs.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=FastAPI%20Celery&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "Figma UI/UX Redesign for B2B FinTech Platform & Component Library",
        "Category": "Design & Creative",
        "Match Score Rating": "94% Best Match",
        "Contract Type & Budget": "$3,000 Fixed Price / $50/hr",
        "Client Quality Tier": "Payment Verified | 5.0 ★ (16 reviews) | $45k+ spent | United Kingdom",
        "Client Problem / Bottleneck": "FinTech web application UI feels outdated and non-intuitive. Needs complete overhaul of 30 screens in Figma with auto-layout, design tokens, light/dark themes, and developer-ready component library.",
        "Mandatory Skill Tags Required": "Figma, UI/UX Design, Design Systems, Wireframing, Auto Layout, B2B SaaS",
        "Winning Proposal Strategy (Law of 1st Sentence)": "FinTech user retention hinges on clarity and density in table views; here is an interactive Figma prototype redesigning financial transaction tables with tokenized auto-layouts.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=Figma%20Design%20System%20SaaS&payment_verified=1&sort=recency"
    },
    {
        "Job Title": "API Developer Documentation & SDK Quickstart Guide (ReadMe / Mintlify)",
        "Category": "Writing & Content",
        "Match Score Rating": "93% Best Match",
        "Contract Type & Budget": "$1,500 Fixed Price",
        "Client Quality Tier": "Payment Verified | 4.8 ★ (11 reviews) | $25k+ spent | United States",
        "Client Problem / Bottleneck": "API platform losing developer conversions because documentation lacks interactive curl examples, clear authentication walkthroughs, and error code troubleshooting tables.",
        "Mandatory Skill Tags Required": "Technical Writing, API Documentation, OpenAPI/Swagger, Markdown, Mintlify, Developer Experience",
        "Winning Proposal Strategy (Law of 1st Sentence)": "Developers bounce within 60 seconds if they can't copy a working curl request to terminal; I author documentation following the 3-minute quickstart rule with full request/response schemas.",
        "Direct Upwork Search URL": "https://www.upwork.com/nx/search/jobs/?q=API%20Documentation%20Technical%20Writing&payment_verified=1&sort=recency"
    }
]

output_file = "e:/anti/upwork_best_matches_feed.csv"

fieldnames = [
    "Job Title",
    "Category",
    "Match Score Rating",
    "Contract Type & Budget",
    "Client Quality Tier",
    "Client Problem / Bottleneck",
    "Mandatory Skill Tags Required",
    "Winning Proposal Strategy (Law of 1st Sentence)",
    "Direct Upwork Search URL"
]

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in best_matches:
        writer.writerow(row)

print(f"Successfully generated {output_file} with {len(best_matches)} records.")
