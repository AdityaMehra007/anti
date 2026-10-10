import csv

contracts = [
    {
        "Project Title": "India Market Research & Benchmarking Deck (Bangalore, Hyderabad, Pune)",
        "Category": "Market Research & Strategy",
        "Contract Type": "Fixed-Price",
        "Target Location": "Bengaluru / India",
        "Budget / Rate": "$500 - $1,500 Fixed Price",
        "Client Origin": "United States (Enterprise)",
        "Scope & Deliverables": "City-level salary benchmarking, tech talent availability, commercial real estate cost comparison for Bangalore vs Hyderabad/Pune/Chennai",
        "Proposal Win Angle": "Attach 2-page sample executive compensation index for Bengaluru tech corridors (Whitefield vs Outer Ring Road vs Koramangala)",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/market-research-bangalore/"
    },
    {
        "Project Title": "Part-Time B2B SDR / Appointment Setter based in India",
        "Category": "Sales & Business Development",
        "Contract Type": "Hourly",
        "Target Location": "India (English Fluent)",
        "Budget / Rate": "$18 - $35/hr USD (₹1,500 - ₹2,900/hr)",
        "Client Origin": "United Kingdom (SaaS)",
        "Scope & Deliverables": "Outbound prospecting into US/UK mid-market accounts, cold email follow-up, booking discovery calls with Head of Engineering/Operations",
        "Proposal Win Angle": "Include 45-second audio Loom introduction demonstrating fluent consultative English and previous cold email response rates (>8%)",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/b2b-sdr-india/"
    },
    {
        "Project Title": "India Business Decision Maker Contact List (CXO / Director Lead Gen)",
        "Category": "Lead Generation & Data Mining",
        "Contract Type": "Fixed-Price",
        "Target Location": "Bengaluru / India",
        "Budget / Rate": "$350 - $800 Fixed Price",
        "Client Origin": "Singapore (B2B Services)",
        "Scope & Deliverables": "Scraping and verifying 750 verified corporate emails and direct phone numbers for Managing Directors in manufacturing and logistics across India",
        "Proposal Win Angle": "Attach 10-prospect verified sample dataset with 0% bounce guarantee and LinkedIn profile URLs",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/lead-generation-india/"
    },
    {
        "Project Title": "Virtual Operations Assistant & Vendor Coordinator (Bengaluru Hub)",
        "Category": "Admin & Customer Support",
        "Contract Type": "Hourly / Monthly Retainer",
        "Target Location": "Bengaluru, India",
        "Budget / Rate": "$15 - $25/hr USD (₹1,250 - ₹2,100/hr)",
        "Client Origin": "Australia (Event & Hospitality)",
        "Scope & Deliverables": "Local vendor negotiations in Bengaluru, hospitality partner inquiries, expense logging, calendar scheduling across IST and AEST",
        "Proposal Win Angle": "Highlight on-the-ground knowledge of Bengaluru commercial hubs (Indiranagar, MG Road, Whitefield) and rapid vendor turnaround",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/virtual-assistant-bengaluru/"
    },
    {
        "Project Title": "Performance Marketing & Google Ads Optimization (Bangalore Business)",
        "Category": "Digital Marketing & PPC",
        "Contract Type": "Fixed-Price / Monthly Retainer",
        "Target Location": "Bengaluru, India",
        "Budget / Rate": "$600 - $1,800/mo",
        "Client Origin": "India / UAE (Commercial Real Estate)",
        "Scope & Deliverables": "Google Search & Local Services Ads management, negative keyword pruning, conversion tracking via GA4, landing page A/B testing",
        "Proposal Win Angle": "Provide 1-page breakdown of local Bangalore high-intent search keywords and estimated CPL benchmarks",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/google-ads-bangalore/"
    },
    {
        "Project Title": "Full-Stack Next.js 15 & Supabase SaaS MVP Development",
        "Category": "Web Development",
        "Contract Type": "Fixed-Price Milestones",
        "Target Location": "India (Bengaluru Tech Preferred)",
        "Budget / Rate": "$3,000 - $8,000 Fixed Price",
        "Client Origin": "United States (Startup Founder)",
        "Scope & Deliverables": "Build responsive multi-tenant SaaS frontend in Next.js/Tailwind, PostgreSQL backend on Supabase, Stripe subscriptions, and Vercel CI/CD",
        "Proposal Win Angle": "Share live URL of a deployed Next.js/Supabase production app with interactive credentials",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/nextjs-supabase/"
    },
    {
        "Project Title": "n8n & Voice AI Customer Support Automation Engine",
        "Category": "AI & Workflow Automation",
        "Contract Type": "Fixed-Price Milestones",
        "Target Location": "Worldwide / India",
        "Budget / Rate": "$2,000 - $5,500 Fixed Price",
        "Client Origin": "United States (Healthcare / E-Com)",
        "Scope & Deliverables": "Connect Twilio voice calls, ElevenLabs speech synthesis, and OpenAI Assistant to automatically triage and resolve appointment inquiries",
        "Proposal Win Angle": "Share exportable n8n workflow JSON snippet and 60-second video demo showing webhook trigger latency",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/n8n-automation/"
    },
    {
        "Project Title": "Figma UI/UX Design System for B2B FinTech Platform",
        "Category": "UI/UX Design",
        "Contract Type": "Hourly",
        "Target Location": "Worldwide / India",
        "Budget / Rate": "$35 - $65/hr USD (₹2,900 - ₹5,400/hr)",
        "Client Origin": "Canada (Fintech)",
        "Scope & Deliverables": "Design 25+ responsive screens in Figma with auto-layout, interactive prototype, dark/light mode tokens, and mobile viewports",
        "Proposal Win Angle": "Send Figma Community link or video walkthrough of design token architecture and typography hierarchy",
        "Upwork Job URL": "https://www.upwork.com/freelance-jobs/q/figma-ui-ux/"
    }
]

output_file = "e:/anti/upwork_bengaluru_contracts.csv"

fieldnames = [
    "Project Title",
    "Category",
    "Contract Type",
    "Target Location",
    "Budget / Rate",
    "Client Origin",
    "Scope & Deliverables",
    "Proposal Win Angle",
    "Upwork Job URL"
]

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for c in contracts:
        writer.writerow(c)

print(f"Successfully generated {output_file} with {len(contracts)} contracts.")
