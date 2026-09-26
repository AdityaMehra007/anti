#!/usr/bin/env python3
"""
========================================================================================
WORLD BILLIONAIRES GLOBAL MASTER DATABASE & COMPREHENSIVE COMPENDIUM BUILDER
========================================================================================
Compiles exhaustive data on the world's top billionaires, their enterprise empires,
market capitalizations, operating models, Bengaluru/India presence, family offices,
and strategic operational career gateways for Aditya Mehra (BBA International Business).
Outputs:
  - e:\anti\WORLD_BILLIONAIRES_GLOBAL_MASTER_DATABASE.csv
  - e:\anti\WORLD_BILLIONAIRES_GLOBAL_ENCYCLOPEDIA.md
  - SQLite table 'world_billionaires_mega_master' in BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import csv
import json
import sqlite3
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
CSV_PATH = ROOT_DIR / "WORLD_BILLIONAIRES_GLOBAL_MASTER_DATABASE.csv"
MD_PATH = ROOT_DIR / "WORLD_BILLIONAIRES_GLOBAL_ENCYCLOPEDIA.md"
DB_PATH = ROOT_DIR / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"

BILLIONAIRES_DATA = [
    # Top Global Titans
    {
        "rank": 1,
        "name": "Elon Musk",
        "net_worth": "$250 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Tesla, SpaceX, xAI, Neuralink, The Boring Company, X",
        "family_office": "Excession LLC",
        "industry": "Automotive, Aerospace, Artificial Intelligence, Energy",
        "market_cap_valuation": "$1.2 Trillion (Combined)",
        "how_company_works": "Vertical integration of manufacturing and software. Tesla controls battery chemistry, Gigafactory robotics, and autonomous FSD compute. SpaceX operates reusable rocketry (Falcon 9/Starship) and global satellite internet constellation (Starlink). xAI builds frontier LLMs (Grok) powered by massive 100k+ GPU clusters.",
        "bengaluru_india_footprint": "Tesla India Motors & Energy Pvt Ltd (Lavelle Road / Whitefield R&D hub), Starlink India licensing, and Indian aerospace vendor partnerships.",
        "target_operational_role": "Supply Chain & Regulatory Operations Coordinator / Gigafactory Logistics Lead",
        "ctc_lpa": "₹14.0L - ₹22.0L LPA",
        "executive_contact": "careers@tesla.com / Elon Musk Founder's Office",
        "pitch_trigger": "Complex component import tariff mitigation, customs clearance, and EV supply chain logistics."
    },
    {
        "rank": 2,
        "name": "Jeff Bezos",
        "net_worth": "$210 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Amazon.com Inc., Blue Origin, The Washington Post",
        "family_office": "Bezos Expeditions",
        "industry": "E-Commerce, Hyperscale Cloud Infrastructure, Aerospace",
        "market_cap_valuation": "$1.95 Trillion",
        "how_company_works": "Flywheel effect: Low cost structure leads to lower prices, attracting more customers, driving seller density and scale. Amazon Web Services (AWS) powers the modern internet with high-margin enterprise cloud compute. Blue Origin develops heavy-lift reusable rockets (New Glenn) and lunar landers.",
        "bengaluru_india_footprint": "Amazon Development Centre India (World Trade Center Rajajinagar & Bagmane Constellation ORR) - largest campus outside Seattle, hosting AWS core teams and global operations.",
        "target_operational_role": "Operations Program Manager / AWS Global Data Center BizOps Analyst",
        "ctc_lpa": "₹11.0L - ₹17.5L LPA",
        "executive_contact": "operations-in-jobs@amazon.com / Bezos Expeditions",
        "pitch_trigger": "Vendor SLA management, multi-tier fulfillment warehouse logistics, and global GCC delivery coordination."
    },
    {
        "rank": 3,
        "name": "Bernard Arnault & Family",
        "net_worth": "$195 Billion",
        "citizenship": "France",
        "primary_enterprise": "LVMH Moët Hennessy Louis Vuitton (75 luxury Maisons)",
        "family_office": "Financière Agache / Groupe Arnault",
        "industry": "Luxury Goods, Fashion, Cosmetics, Fine Wines & Spirits",
        "market_cap_valuation": "$420 Billion",
        "how_company_works": "Extreme pricing power and brand heritage management. Acquires historical luxury houses (Louis Vuitton, Dior, Tiffany & Co., Bulgari, Dom Pérignon) and maintains decentralized creative autonomy while centralizing global retail real estate, supply chain distribution, and VIP experiential marketing.",
        "bengaluru_india_footprint": "Luxury retail flagships at UB City, Bengaluru; Sephora supply chain; LVMH luxury retail operations in India.",
        "target_operational_role": "Luxury Brand Supply Chain Governance & Retail Operations Lead",
        "ctc_lpa": "₹10.0L - ₹16.0L LPA",
        "executive_contact": "contact@financiere-agache.com / LVMH India Operations",
        "pitch_trigger": "High-value asset tracking, import customs duty compliance for luxury leather/jewelry, and VIP launch operations (Puma/Tata Comm experience)."
    },
    {
        "rank": 4,
        "name": "Mark Zuckerberg",
        "net_worth": "$185 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Meta Platforms Inc. (Facebook, Instagram, WhatsApp, Reality Labs)",
        "family_office": "Chan Zuckerberg Initiative (CZI) / West Street Capital",
        "industry": "Social Media, Digital Advertising, AI, Virtual Reality",
        "market_cap_valuation": "$1.4 Trillion",
        "how_company_works": "Network effect monopoly: Over 3.2 billion daily active people across apps. Monetizes through AI-driven auction ad ranking engines. Massively invests in open-source AI infrastructure (Llama foundational models) and custom silicon to eliminate dependency on third-party hardware.",
        "bengaluru_india_footprint": "Meta India Operations (Central Business District, Bengaluru), WhatsApp India payment operations, and enterprise partner engineering.",
        "target_operational_role": "Strategic Partner Operations Analyst / AI Infrastructure Governance Specialist",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "careers@meta.com / CZI Family Office",
        "pitch_trigger": "Vendor SLA auditing, trust & safety data operations, and cross-border commercial partner triage."
    },
    {
        "rank": 5,
        "name": "Larry Ellison",
        "net_worth": "$175 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Oracle Corporation",
        "family_office": "Lawrence Investments LLC",
        "industry": "Enterprise Database Software, Cloud Infrastructure, Healthcare",
        "market_cap_valuation": "$470 Billion",
        "how_company_works": "Mission-critical relational database enterprise lock-in. Powers banking systems, airlines, and Fortune 500 ERPs. Transitioned to Oracle Cloud Infrastructure (OCI), securing massive multi-billion-dollar hyperscale GPU compute contracts with Microsoft, OpenAI, and governments.",
        "bengaluru_india_footprint": "Oracle Technology Park (Kalyani Magnum, JP Nagar & Whitefield) - massive global software and cloud operations hub.",
        "target_operational_role": "Global Cloud Commercial Contracts & Operations Analyst",
        "ctc_lpa": "₹10.0L - ₹16.0L LPA",
        "executive_contact": "india_careers@oracle.com / Lawrence Investments",
        "pitch_trigger": "Enterprise software license compliance, cloud hardware logistics, and vendor contract audits."
    },
    {
        "rank": 6,
        "name": "Warren Buffett",
        "net_worth": "$145 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Berkshire Hathaway Inc.",
        "family_office": "Berkshire Hathaway Corporate Headquarters",
        "industry": "Conglomerate, Insurance, Rail Transportation, Energy",
        "market_cap_valuation": "$1.0 Trillion",
        "how_company_works": "Insurance float compounding machine: Uses non-debt insurance float from GEICO and General Re to acquire entire enduring businesses (BNSF Railway, Berkshire Hathaway Energy, Precision Castparts) and multi-billion-dollar public equity stakes (Apple, American Express, Coca-Cola) with extreme decentralization.",
        "bengaluru_india_footprint": "Berkshire subsidiaries (Marmon Group, Precision Castparts aerospace manufacturing in Bengaluru, Lubrizol).",
        "target_operational_role": "Operations & Internal Governance Analyst / Industrial Supply Chain Lead",
        "ctc_lpa": "₹10.0L - ₹15.5L LPA",
        "executive_contact": "berkshire@berkshirehathaway.com / Marmon India",
        "pitch_trigger": "Rigorous capital discipline, lean operational oversight, and zero-bullshit supply chain inventory auditing."
    },
    {
        "rank": 7,
        "name": "Bill Gates",
        "net_worth": "$135 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Microsoft Corporation, Breakthrough Energy, Gates Foundation",
        "family_office": "Cascade Investment LLC",
        "industry": "Software, Clean Tech, Venture Philanthropy, Asset Management",
        "market_cap_valuation": "$3.1 Trillion (Microsoft)",
        "how_company_works": "Diversified asset allocation: Cascade Investment allocates across private equity, sustainable agriculture, nuclear energy (TerraPower), and enterprise rail. Bill & Melinda Gates Foundation deploys \$7B+ annually for global health and digital public infrastructure.",
        "bengaluru_india_footprint": "Bill & Melinda Gates Foundation India Country Office (Bengaluru partner initiatives), Microsoft India Global Technical Center.",
        "target_operational_role": "Program Operations Analyst / DPI & Energy Transition Operations Lead",
        "ctc_lpa": "₹11.0L - ₹17.0L LPA",
        "executive_contact": "info@cascadeinv.com / Gates Foundation Operations",
        "pitch_trigger": "Public-private health logistics, cross-border grant compliance, and vendor operational governance."
    },
    {
        "rank": 8,
        "name": "Larry Page & Sergey Brin",
        "net_worth": "$280 Billion (Combined)",
        "citizenship": "United States",
        "primary_enterprise": "Alphabet Inc. (Google, DeepMind, Waymo, Verily)",
        "family_office": "Kopec Family Office / Bayshore Global Management",
        "industry": "Search, Artificial Intelligence, Autonomous Vehicles, Cloud",
        "market_cap_valuation": "$2.2 Trillion",
        "how_company_works": "Alphabet acts as an umbrella holding company. The Google core engine generates massive cash flows from Search, YouTube, and Google Cloud, which subsidizes 'Other Bets'—Waymo (autonomous robotaxis), DeepMind (frontier AGI and scientific discovery like AlphaFold), and life sciences.",
        "bengaluru_india_footprint": "Google India (Bagmane Constellation & RMZ Infinity, Old Madras Road) and Google Research India (Bengaluru).",
        "target_operational_role": "Global Business Operations Analyst / AI Research Program Operations Associate",
        "ctc_lpa": "₹11.0L - ₹16.5L LPA",
        "executive_contact": "in-recruitment@google.com / Bayshore Global",
        "pitch_trigger": "AI research operations triage, vendor SLA audit scorecards, and multi-timezone project coordination."
    },
    {
        "rank": 9,
        "name": "Steve Ballmer",
        "net_worth": "$130 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Microsoft (Major Shareholder), LA Clippers, Ballmer Group",
        "family_office": "Ballmer Group",
        "industry": "Technology Holdings, Sports Entertainment, Civic Philanthropy",
        "market_cap_valuation": "$3.1 Trillion (Underlying Microsoft)",
        "how_company_works": "Holds massive 333M+ shares of Microsoft, yielding hundreds of millions annually in pure dividend cash flow. Funds the revolutionary Intuit Dome arena and deploys systematic data-driven philanthropy tracking US economic mobility via USAFacts.",
        "bengaluru_india_footprint": "USAFacts data engineering partners and Microsoft India enterprise ecosystem.",
        "target_operational_role": "Strategic Data Operations Associate / Philanthropic Portfolio Governance Analyst",
        "ctc_lpa": "₹10.5L - ₹16.0L LPA",
        "executive_contact": "contact@ballmergroup.org",
        "pitch_trigger": "Data integrity audits, statistical operational dashboards, and high-impact project execution."
    },
    {
        "rank": 10,
        "name": "Jensen Huang",
        "net_worth": "$115 Billion",
        "citizenship": "United States",
        "primary_enterprise": "NVIDIA Corporation",
        "family_office": "Huang Family Foundation / Jen-Hsun & Lori Huang Office",
        "industry": "Semiconductors, GPU Compute, Accelerated Computing, AI",
        "market_cap_valuation": "$3.0 Trillion",
        "how_company_works": "Full-stack accelerated computing monopoly: Designs the world's most advanced AI training GPUs (Hopper H100, Blackwell B200) coupled with the CUDA software ecosystem and NVLink networking, creating insurmountable competitive moats across AI data centers worldwide.",
        "bengaluru_india_footprint": "NVIDIA Graphics India Pvt Ltd (Manyata Tech Park & Whitefield) - one of NVIDIA's largest engineering and hardware verification centers globally.",
        "target_operational_role": "Global Compute Operations & Hardware Logistics Analyst",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "india-recruitment@nvidia.com / Jensen Huang Executive Office",
        "pitch_trigger": "GPU cluster delivery logistics, customs clearance of sensitive hardware, and automated LLM prompt eval testing (Instawork grounding)."
    },

    # Indian Mega-Titans & Conglomerates
    {
        "rank": 11,
        "name": "Mukesh Ambani & Family",
        "net_worth": "$114 Billion",
        "citizenship": "India",
        "primary_enterprise": "Reliance Industries Limited (Jio Platforms, Reliance Retail, O2C)",
        "family_office": "Reliance Strategic Office / Ambani Family Office (Singapore/Mumbai)",
        "industry": "Telecom, Retail, Petrochemicals, Renewable Energy",
        "market_cap_valuation": "$220 Billion (₹18.5 Lakh Crore)",
        "how_company_works": "Dominates India's digital and retail infrastructure. Jio has 470M+ subscribers; Reliance Retail operates 18,000+ stores across grocery, electronics, and fashion. Massive oil-to-chemicals (O2C) refining in Jamnagar produces steady cash to fund 5G network rollout and gigawatt-scale clean energy gigafactories.",
        "bengaluru_india_footprint": "Jio Bengaluru Tech Hub (Kadubeesanahalli / Electronic City), Reliance Retail regional distribution centers, and JioCinema/Viacom18 tech teams.",
        "target_operational_role": "Strategic Business Operations Associate / Retail Supply Chain Lead",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "careers.retail@ril.com / Mukesh Ambani Office",
        "pitch_trigger": "Hyperlocal dark store logistics, retail vendor SLA governance, and telecom infrastructure operations."
    },
    {
        "rank": 12,
        "name": "Gautam Adani & Family",
        "net_worth": "$84 Billion",
        "citizenship": "India",
        "primary_enterprise": "Adani Group (Adani Ports, Adani Green Energy, Adani Power, Adani Airports)",
        "family_office": "Adani Family Office",
        "industry": "Ports, Logistics, Renewable Energy, Infrastructure, Airports",
        "market_cap_valuation": "$175 Billion",
        "how_company_works": "Controls India's critical transport and energy infrastructure. Adani Ports manages ~25% of India's total port cargo capacity (Mundra, Krishnapatnam, Karaikal) and operates integrated multimodal logistics corridors (dry ports, container trains, warehouses).",
        "bengaluru_india_footprint": "Adani Logistics inland container depots (ICD), Adani Airport Holding cargo initiatives, and green energy power purchase agreements in Karnataka.",
        "target_operational_role": "EXIM Logistics & Port Turnaround Associate / Trade Corridor Governance Analyst",
        "ctc_lpa": "₹10.0L - ₹15.0L LPA",
        "executive_contact": "careers@adani.com / Adani Ports Leadership",
        "pitch_trigger": "Port demurrage reduction, ICEGATE customs tariff audit, and multimodal freight turnaround management."
    },
    {
        "rank": 13,
        "name": "Azim Premji & Rishad Premji",
        "net_worth": "$25 Billion",
        "citizenship": "India",
        "primary_enterprise": "Wipro Limited / PremjiInvest",
        "family_office": "PremjiInvest (India's largest family investment office, $10B+ AUM)",
        "industry": "IT Services, Growth Equity, Venture Capital, FMCG",
        "market_cap_valuation": "$35 Billion (Wipro) + $10B AUM (PremjiInvest)",
        "how_company_works": "PremjiInvest operates as a world-class perpetual evergreen institutional fund. Deploys capital into pre-IPO tech leaders (Lenskart, PolicyBazaar, Meesho, FirstCry) and public markets, returning all investment profits directly to fund the Azim Premji Foundation for rural public education.",
        "bengaluru_india_footprint": "PremjiInvest Headquarters (Manyata Tech Park / Sarjapur Road) and Wipro Corporate Campus (Sarjapur Road, Bengaluru).",
        "target_operational_role": "Family Office Operations & Investment Portfolio Associate",
        "ctc_lpa": "₹14.0L - ₹20.0L LPA",
        "executive_contact": "info@premjiinvest.com / Azim Premji Family Office",
        "pitch_trigger": "Zero-leakage vendor contract auditing, portfolio company governance memos, and uncompromising ethical financial reporting."
    },
    {
        "rank": 14,
        "name": "N. R. Narayana Murthy & Sudha Murty",
        "net_worth": "$5.0 Billion",
        "citizenship": "India",
        "primary_enterprise": "Infosys Limited / Catamaran Ventures",
        "family_office": "Catamaran Ventures",
        "industry": "Technology Services, Venture Capital, Growth Equity",
        "market_cap_valuation": "$85 Billion (Infosys)",
        "how_company_works": "Catamaran is a multi-stage private family office investing proprietary family capital across technology, healthcare, manufacturing, and consumer sectors with a philosophy of ethical value creation, long-term capital stewardship, and corporate governance.",
        "bengaluru_india_footprint": "Catamaran Ventures Headquarters (Jayanagar / MG Road, Bengaluru) and Infosys Global HQ (Electronic City, Bengaluru).",
        "target_operational_role": "Founder's Office Associate / Venture Operations Analyst",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "info@catamaran.com / Narayana Murthy Office",
        "pitch_trigger": "Rigorous corporate governance reporting, portfolio company audit sheets, and institutional operational analysis."
    },
    {
        "rank": 15,
        "name": "Nandan Nilekani",
        "net_worth": "$4.0 Billion",
        "citizenship": "India",
        "primary_enterprise": "Infosys (Chairman), Fundamentum Partnership, EkStep",
        "family_office": "Nilekani Family Office / Fundamentum",
        "industry": "Tech Scale-ups, Digital Public Infrastructure, Venture Capital",
        "market_cap_valuation": "$85 Billion (Infosys)",
        "how_company_works": "Architect of Aadhaar (IndiaStack) and UPI. Nilekani invests in scale-up Indian tech ventures via Fundamentum ($250M growth fund) and builds philanthropic public goods via EkStep Foundation for national education and open digital networks (ONDC).",
        "bengaluru_india_footprint": "Fundamentum Headquarters (Koramangala, Bengaluru) and EkStep Foundation (Sadashivanagar, Bengaluru).",
        "target_operational_role": "Strategic Operations & Portfolio Governance Associate",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "contact@fundamentum.co.in / Nandan Nilekani Office",
        "pitch_trigger": "Digital platform scalability, cross-border technology operations, and ecosystem governance."
    },
    {
        "rank": 16,
        "name": "Nithin Kamath & Nikhil Kamath",
        "net_worth": "$4.8 Billion (Combined)",
        "citizenship": "India",
        "primary_enterprise": "Zerodha Broking Ltd, Rainmatter Capital, Gruhas Proptech",
        "family_office": "Rainmatter / Gruhas / Kamath Family Office",
        "industry": "FinTech, Discount Brokerage, Venture Incubator, Consumer Brands",
        "market_cap_valuation": "$3.5 Billion (Bootstrapped, Zero Debt)",
        "how_company_works": "100% bootstrapped fin-tech empire. Zerodha processes ~15% of daily Indian retail trading volume with zero customer acquisition ad spend. Profits are deployed through Rainmatter to back health, climate, and fin-tech founders with patient, non-controlling capital.",
        "bengaluru_india_footprint": "Zerodha Headquarters (JP Nagar 4th Phase, Bengaluru) - central operations hub.",
        "target_operational_role": "Founder's Office / Rainmatter Operations Associate",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "nithin@zerodha.com / rainmatter@zerodha.com",
        "pitch_trigger": "Zero-bloat operational autonomy, crisis triage backed by ground coordination at Aero India 2025, and vendor SLA control."
    },
    {
        "rank": 17,
        "name": "Shiv Nadar & Roshni Nadar Malhotra",
        "net_worth": "$38 Billion",
        "citizenship": "India",
        "primary_enterprise": "HCL Technologies, Shiv Nadar Foundation",
        "family_office": "HCL Corporation",
        "industry": "IT Services, Engineering R&D, Semiconductor Fab, Philanthropy",
        "market_cap_valuation": "$52 Billion",
        "how_company_works": "Pioneer of Indian hardware and IT services. Focuses on deep Engineering and R&D services (ERS) for global aerospace, medical devices, and telecom giants. Expanding into display and semiconductor manufacturing.",
        "bengaluru_india_footprint": "HCL Tech campuses across Electronic City, Whitefield, and Manyata Tech Park.",
        "target_operational_role": "Global Business Operations Trainee / Aerospace ERS Governance Lead",
        "ctc_lpa": "₹9.0L - ₹14.0L LPA",
        "executive_contact": "careers@hcl.com / Shiv Nadar Office",
        "pitch_trigger": "Global engineering contract audits, cross-border milestone tracking, and client operational continuity."
    },
    {
        "rank": 18,
        "name": "Kumar Mangalam Birla",
        "net_worth": "$22 Billion",
        "citizenship": "India",
        "primary_enterprise": "Aditya Birla Group (Grasim, Hindalco, UltraTech, Novelis)",
        "family_office": "Birla Family Office",
        "industry": "Metals & Mining, Cement, Financial Services, Telecom, Retail",
        "market_cap_valuation": "$75 Billion (Group)",
        "how_company_works": "Global commodities and manufacturing titan. World's largest aluminum rolling company (Novelis), India's largest cement producer (UltraTech Cement), and major viscose staple fiber manufacturer with operations in 36 countries.",
        "bengaluru_india_footprint": "Madura Fashion & Lifestyle Corporate Office (Aditya Birla Fashion & Retail, Regent Gateway, Bengaluru).",
        "target_operational_role": "Group Business Operations Associate / Retail Supply Chain Analyst",
        "ctc_lpa": "₹10.0L - ₹15.0L LPA",
        "executive_contact": "careers@adityabirla.com / Birla Chairman's Office",
        "pitch_trigger": "Cross-border metal supply chain logistics, port customs clearance, and multi-tier apparel retail distribution."
    },
    {
        "rank": 19,
        "name": "Uday Kotak",
        "net_worth": "$14 Billion",
        "citizenship": "India",
        "primary_enterprise": "Kotak Mahindra Bank, Kotak Alternate Asset Management",
        "family_office": "Kotak Family Office",
        "industry": "Commercial Banking, Investment Banking, Private Equity, Wealth",
        "market_cap_valuation": "$45 Billion",
        "how_company_works": "Conservative financial powerhouse. Built India's premier integrated private bank with strict underwriting discipline, high net interest margins (NIM), and leadership in corporate investment banking and alternate asset management.",
        "bengaluru_india_footprint": "Kotak Mahindra Bank regional headquarters (MG Road, Bengaluru) and Kotak Securities operations.",
        "target_operational_role": "Treasury Operations Analyst / Trade Finance & Collateral Associate",
        "ctc_lpa": "₹10.0L - ₹15.0L LPA",
        "executive_contact": "careers@kotak.com / Kotak Executive Office",
        "pitch_trigger": "UCP 600 Letter of Credit audits, foreign exchange settlements, and institutional middle-office reconciliation."
    },
    {
        "rank": 20,
        "name": "Radhakishan Damani",
        "net_worth": "$17 Billion",
        "citizenship": "India",
        "primary_enterprise": "Avenue Supermarts Limited (DMart)",
        "family_office": "Damani Family Office",
        "industry": "Discount Retail, Warehousing, Real Estate",
        "market_cap_valuation": "$35 Billion",
        "how_company_works": "Unbeatable lowest-price retail model. DMart owns its store properties (zero rent drag), procures directly from manufacturers with fast 10-day supplier cash payments for massive discounts, and maximizes sales per square foot.",
        "bengaluru_india_footprint": "DMart central distribution centers (Bommasandra / Nelamangala) and 35+ retail stores across Bengaluru.",
        "target_operational_role": "Central Warehouse Operations Trainee / Inventory Logistics Lead",
        "ctc_lpa": "₹8.5L - ₹12.5L LPA",
        "executive_contact": "careers@dmartindia.com / DMart Corporate",
        "pitch_trigger": "Inventory shrink elimination, supplier loading dock audit, and turnaround SLA management."
    },

    # Global Consumer & Fashion Titans
    {
        "rank": 21,
        "name": "Amancio Ortega",
        "net_worth": "$110 Billion",
        "citizenship": "Spain",
        "primary_enterprise": "Inditex S.A. (Zara, Massimo Dutti, Bershka, Pull&Bear)",
        "family_office": "Pontegadea Inversiones SL",
        "industry": "Fast Fashion Retail, Global Commercial Real Estate",
        "market_cap_valuation": "$150 Billion",
        "how_company_works": "Pioneered fast-fashion agility. Designs, manufactures, and places new garment collections into 5,000+ global stores within 15 days via air freight from Spain. Reinvests retail profits through Pontegadea to buy trophy commercial office towers leased to Amazon, Apple, and Google.",
        "bengaluru_india_footprint": "Zara India retail stores and Inditex India sourcing and commercial offices.",
        "target_operational_role": "Fashion SCM Logistics Coordinator / Real Estate Operations Specialist",
        "ctc_lpa": "₹9.0L - ₹14.0L LPA",
        "executive_contact": "contact@pontegadea.com / Zara India",
        "pitch_trigger": "Air freight customs clearance, fast replenishment logistics, and retail store inventory triage."
    },
    {
        "rank": 22,
        "name": "Jim, Rob & Alice Walton",
        "net_worth": "$260 Billion (Combined)",
        "citizenship": "United States",
        "primary_enterprise": "Walmart Inc., Flipkart Group, PhonePe",
        "family_office": "Walton Enterprises LLC",
        "industry": "Retail, Supercenters, Supply Chain, FinTech",
        "market_cap_valuation": "$550 Billion",
        "how_company_works": "World's largest company by revenue ($650B+). Dominates brick-and-mortar retail in the US and international e-commerce through its Indian subsidiary Flipkart and digital payments giant PhonePe.",
        "bengaluru_india_footprint": "Walmart Global Tech India (RMZ Ecospace, Bellandur, Bengaluru) and Flipkart Global HQ (Embassy TechVillage, Bengaluru).",
        "target_operational_role": "Global SCM Operations Analyst / Dark Store Inventory Governance Lead",
        "ctc_lpa": "₹9.5L - ₹15.0L LPA",
        "executive_contact": "indiacareers@walmart.com / Walton Enterprises",
        "pitch_trigger": "Cross-border supplier contract governance, warehouse automation, and landed cost analytics."
    },
    {
        "rank": 23,
        "name": "Michael Dell",
        "net_worth": "$105 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Dell Technologies Inc.",
        "family_office": "DFO Management LLC (Dell Family Office)",
        "industry": "Enterprise IT, Cloud Servers, AI Compute Infrastructure, PC Hardware",
        "market_cap_valuation": "$90 Billion",
        "how_company_works": "Pioneered direct-to-consumer PC build-to-order models. Transformed into an enterprise AI hardware powerhouse, manufacturing custom liquid-cooled PowerEdge AI server racks powering Elon Musk's xAI Colossus supercluster.",
        "bengaluru_india_footprint": "Dell Technologies India (Embassy GolfLinks Business Park, Domlur, Bengaluru) - major R&D and global supply chain hub.",
        "target_operational_role": "Global Server Hardware Logistics Analyst / Vendor SLA Governance Specialist",
        "ctc_lpa": "₹9.0L - ₹14.5L LPA",
        "executive_contact": "india.careers@dell.com / DFO Management",
        "pitch_trigger": "Server assembly logistics, customs duty reconciliation, and cross-border vendor SLA audits."
    },
    {
        "rank": 24,
        "name": "Masayoshi Son",
        "net_worth": "$32 Billion",
        "citizenship": "Japan",
        "primary_enterprise": "SoftBank Group Corp., Vision Fund, Arm Holdings",
        "family_office": "SoftBank Group Executive Office",
        "industry": "Venture Capital, Telecom, AI Infrastructure, Semiconductor IP",
        "market_cap_valuation": "$95 Billion",
        "how_company_works": "Visionary aggressive venture capitalist. Raised the historic $100B Vision Fund to back AI, ride-sharing, and tech disruption (Uber, ByteDance, DoorDash). Holds 90% of Arm Holdings, the essential semiconductor architecture powering 99% of global smartphones.",
        "bengaluru_india_footprint": "SoftBank India Investments Office and Arm India Design Center (Bagmane Tech Park, Bengaluru).",
        "target_operational_role": "Portfolio Operations Associate / Semiconductor IP Logistics Analyst",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "contact@softbank.com / Arm India",
        "pitch_trigger": "Portfolio burn multiple analysis, cross-border tech licensing, and corporate governance triage."
    },
    {
        "rank": 25,
        "name": "Kunal Shah",
        "net_worth": "$800 Million+ (Unicorn Promoter)",
        "citizenship": "India",
        "primary_enterprise": "CRED (Dreamplug Technologies Pvt Ltd)",
        "family_office": "Kunal Shah Founder's Office / QED Innovations",
        "industry": "FinTech, Premium Commerce, Credit Rewards, Vehicle Management",
        "market_cap_valuation": "$6.4 Billion",
        "how_company_works": "Monopolizes high-credit-score Indian consumers (Creditworthy Top 1%). Monetizes through peer-to-peer lending (CRED Mint), merchant checkout payments (CRED Pay), vehicle tracking (CRED Garage), and luxury e-commerce brand drops.",
        "bengaluru_india_footprint": "CRED Headquarters (100 Feet Road, Indiranagar, Bengaluru).",
        "target_operational_role": "Founder's Office Associate - Brand Partnerships & Luxury Commerce Ops",
        "ctc_lpa": "₹12.0L - ₹18.0L LPA",
        "executive_contact": "kunal@cred.club / careers@cred.club",
        "pitch_trigger": "High-touch luxury merchant activation, on-ground VIP brand logistics (Puma & Tata Comm experience), and unit economics."
    },
    {
        "rank": 26,
        "name": "Bhavish Aggarwal",
        "net_worth": "$1.8 Billion",
        "citizenship": "India",
        "primary_enterprise": "Ola Cabs, Ola Electric Mobility, Krutrim AI",
        "family_office": "Aggarwal Family Office",
        "industry": "Electric Mobility, AI Foundation Models, Ride-hailing",
        "market_cap_valuation": "$4.5 Billion (Combined Listed & Private)",
        "how_company_works": "Built India's top ride-hailing network and launched Ola Electric (built the 500-acre Futurefactory in Krishnagiri producing 2-wheelers and proprietary 4680 battery cells). Founded Krutrim, India's first AI unicorn building multilingual LLMs and AI cloud data centers.",
        "bengaluru_india_footprint": "Ola Campus (Regent Insignia, Koramangala) and Krutrim AI Bengaluru Lab.",
        "target_operational_role": "Founder's Office - EV Gigafactory Supply Chain & AI Operations Lead",
        "ctc_lpa": "₹11.0L - ₹16.0L LPA",
        "executive_contact": "bhavish@olacabs.com / careers@olaelectric.com",
        "pitch_trigger": "Extreme operational intensity, factory floor vendor triage, and AI model evaluation (Instawork grounding)."
    },
    {
        "rank": 27,
        "name": "Aadit Palicha & Kaivalya Vohra",
        "net_worth": "$1.2 Billion (Combined)",
        "citizenship": "India",
        "primary_enterprise": "Zepto (KiranaKart Technologies Pvt Ltd)",
        "family_office": "Zepto Founder's Office",
        "industry": "Quick Commerce, Dark Store Logistics, FMCG Retail",
        "market_cap_valuation": "$5.0 Billion",
        "how_company_works": "Hyperlocal 10-minute quick-commerce speed machine. Operates hundreds of optimized micro-fulfillment dark stores across Tier-1 Indian metros. Squeezes every second of picking, packing, and routing to drive positive contribution margins on groceries and electronics.",
        "bengaluru_india_footprint": "Zepto Corporate & Tech Office (Bellandur / Koramangala, Bengaluru) and 60+ dark stores in Bengaluru.",
        "target_operational_role": "Founder's Office Associate - City Expansion & Dark Store Turnaround",
        "ctc_lpa": "₹10.0L - ₹15.0L LPA",
        "executive_contact": "aadit@zeptonow.com / careers@zeptonow.com",
        "pitch_trigger": "Dark store picker SLA enforcement, inventory shrink prevention, and high-velocity ground triage."
    },
    {
        "rank": 28,
        "name": "Sriharsha Majety",
        "net_worth": "$1.5 Billion",
        "citizenship": "India",
        "primary_enterprise": "Swiggy Limited (Swiggy Food, Instamart, Dineout, Swiggy Genie)",
        "family_office": "Majety Family Office",
        "industry": "Food Delivery, Quick Commerce, Hyperlocal On-Demand Logistics",
        "market_cap_valuation": "$11.5 Billion (Listed Mega-Cap)",
        "how_company_works": "Dual on-demand platform: High-frequency restaurant food delivery paired with rapid-growth grocery dark stores (Instamart). Leverages dense delivery fleet algorithms to drive route optimization, advertising revenue from brands, and platform subscription fees.",
        "bengaluru_india_footprint": "Swiggy Global Headquarters (Embassy TechVillage, Devarabeesanahalli, Outer Ring Road, Bengaluru).",
        "target_operational_role": "Chief of Staff Associate - Instamart Logistics & Vendor Governance",
        "ctc_lpa": "₹10.0L - ₹15.0L LPA",
        "executive_contact": "harsha@swiggy.in / recruitment@swiggy.in",
        "pitch_trigger": "Vendor SLA auditing, dark store turnaround optimization, and crowd triage from Aero India 2025."
    },
    {
        "rank": 29,
        "name": "Tarun Mehta & Swapnil Jain",
        "net_worth": "$800 Million+ (Combined)",
        "citizenship": "India",
        "primary_enterprise": "Ather Energy Limited",
        "family_office": "Ather Founder's Office",
        "industry": "Electric 2-Wheelers, Smart Fast-Charging Grid, Battery Systems",
        "market_cap_valuation": "$1.3 Billion",
        "how_company_works": "Engineered the ground-up premium electric scooter (Ather 450X & Rizta) with proprietary aluminum chassis, battery pack thermal management, and India's largest dedicated fast-charging network (Ather Grid).",
        "bengaluru_india_footprint": "Ather Corporate Office (IBC Knowledge Park, Bannerghatta Road) and Ather Factory (Hosur, Karnataka-Tamil Nadu border).",
        "target_operational_role": "Founder's Office - Integrated SCM Trainee & Vendor SLA Coordinator",
        "ctc_lpa": "₹9.0L - ₹13.5L LPA",
        "executive_contact": "tarun@atherenergy.com / careers@atherenergy.com",
        "pitch_trigger": "EV component procurement logistics, battery cell import customs clearance, and manufacturing vendor audits."
    },
    {
        "rank": 30,
        "name": "Ken Griffin",
        "net_worth": "$42 Billion",
        "citizenship": "United States",
        "primary_enterprise": "Citadel LLC (Hedge Fund) & Citadel Securities (Market Maker)",
        "family_office": "Citadel Executive Office",
        "industry": "Quantitative Trading, High-Frequency Market Making, Asset Management",
        "market_cap_valuation": "$65 Billion (Combined AUM & Enterprise)",
        "how_company_works": "The undisputed king of quantitative finance. Citadel Securities executes approximately 27% of all US equity trading volume and over 40% of US retail equity volume, processing billions of daily transactions with sub-microsecond algorithmic latency.",
        "bengaluru_india_footprint": "Citadel India Quantitative Technology Hub (Bengaluru) and regional clearing operations.",
        "target_operational_role": "Quantitative Operations & Collateral Settlement Analyst",
        "ctc_lpa": "₹14.0L - ₹22.0L LPA",
        "executive_contact": "careers@citadel.com / Ken Griffin Office",
        "pitch_trigger": "Trade settlement discrepancy reconciliation, Nostro/Vostro audits, and algorithmic clearing governance."
    }
]

def main():
    print("=" * 80)
    print("  BUILDING WORLD BILLIONAIRES GLOBAL MASTER DATABASE & ENCYCLOPEDIA")
    print("=" * 80)

    # 1. Write CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        fieldnames = list(BILLIONAIRES_DATA[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(BILLIONAIRES_DATA)
    print(f"[+] Saved {len(BILLIONAIRES_DATA)} Billionaires to CSV: {CSV_PATH}")

    # 2. Ingest into SQLite Database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS world_billionaires_mega_master")
    cur.execute("""
    CREATE TABLE world_billionaires_mega_master (
        rank INTEGER PRIMARY KEY,
        name TEXT,
        net_worth TEXT,
        citizenship TEXT,
        primary_enterprise TEXT,
        family_office TEXT,
        industry TEXT,
        market_cap_valuation TEXT,
        how_company_works TEXT,
        bengaluru_india_footprint TEXT,
        target_operational_role TEXT,
        ctc_lpa TEXT,
        executive_contact TEXT,
        pitch_trigger TEXT
    )
    """)

    for b in BILLIONAIRES_DATA:
        cur.execute("""
        INSERT INTO world_billionaires_mega_master VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            b["rank"], b["name"], b["net_worth"], b["citizenship"],
            b["primary_enterprise"], b["family_office"], b["industry"],
            b["market_cap_valuation"], b["how_company_works"],
            b["bengaluru_india_footprint"], b["target_operational_role"],
            b["ctc_lpa"], b["executive_contact"], b["pitch_trigger"]
        ))

    conn.commit()
    conn.close()
    print(f"[+] Ingested into SQLite table 'world_billionaires_mega_master' in {DB_PATH}")

    # 3. Generate Markdown Encyclopedia
    md_text = f"""# THE WORLD'S BILLIONAIRES & THEIR ENTERPRISE EMPIRES: THE MASTER ENCYCLOPEDIA

**Authoritative Dossier for Global Business Operations, Family Office Governance & Career Placement**  
*Candidate Grounding: Aditya Mehra | BBA International Business, DSU Bengaluru '26*  
*Total Profiles Compiled: {len(BILLIONAIRES_DATA)} Global Titans & Billionaires*  

---

## 📊 Quick-Reference Summary Table

| Rank | Billionaire Name | Net Worth | Primary Enterprise | Core Industry | Bengaluru / India Footprint | Target Role | Compensation Bracket |
|:---:|:---|:---:|:---|:---|:---|:---|:---:|
"""
    for b in BILLIONAIRES_DATA:
        md_text += f"| {b['rank']} | **{b['name']}** | `{b['net_worth']}` | {b['primary_enterprise'][:30]}... | {b['industry'][:20]}... | {b['bengaluru_india_footprint'][:25]}... | {b['target_operational_role'][:28]}... | `{b['ctc_lpa']}` |\n"

    md_text += """
---

## 🏛️ Comprehensive Deep-Dive Profiles & Enterprise Mechanics

"""
    for b in BILLIONAIRES_DATA:
        md_text += f"""### #{b['rank']}. {b['name']} — {b['net_worth']}
- **Primary Enterprise Holdings:** {b['primary_enterprise']}
- **Family Office Entity:** {b['family_office']}
- **Industry & Domain:** {b['industry']}
- **Combined Valuation / Market Cap:** {b['market_cap_valuation']}
- **Citizenship & Global HQ:** {b['citizenship']}

#### How Their Enterprise Machine Works:
{b['how_company_works']}

#### Bengaluru & India Footprint:
{b['bengaluru_india_footprint']}

#### Strategic Operational Gateway for Aditya Mehra:
- **Target Role:** **{b['target_operational_role']}**
- **Compensation Bracket:** **{b['ctc_lpa']}**
- **Direct Dispatch Channel:** `{b['executive_contact']}`
- **Surgical Operational Pitch Trigger:**
  > *"{b['pitch_trigger']}"*

---
"""

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_text)
    print(f"[+] Compiled Master Markdown Encyclopedia: {MD_PATH}")

if __name__ == "__main__":
    main()
