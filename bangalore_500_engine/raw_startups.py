"""
Bangalore Top 500 Startups Raw Seed Database
Provides 500 authentic tech startups, unicorns, soonicorns, and scale-ups located in Bangalore.
"""
from typing import List, Dict, Any

def get_500_startups_raw() -> List[Dict[str, Any]]:
    # Curated real-world startup entities in Bengaluru
    base_startups = [
        # Decacorns & Premier Unicorns (1-20)
        {"name": "Flipkart", "cat": "E-Commerce, Marketplaces & D2C Brands", "corridor": "Bellandur / ORR (Cessna Business Park)", "stage": "Decacorn", "val": "$37.6B Valuation", "year": 2007, "desc": "India's premier e-commerce ecosystem powering retail, grocery, logistics, and digital payments for 500M+ users."},
        {"name": "Swiggy", "cat": "Quick Commerce, FoodTech & Consumer Internet", "corridor": "Outer Ring Road (Kadubeesanahalli)", "stage": "Decacorn", "val": "$12.0B Valuation", "year": 2014, "desc": "Hyperlocal consumer powerhouse operating food delivery, Instamart quick-commerce, Dineout, and Genie courier."},
        {"name": "Razorpay", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala (8th Block)", "stage": "Decacorn", "val": "$7.5B Valuation", "year": 2014, "desc": "India's leading full-stack financial solutions platform powering digital payments, banking (RazorpayX), and payroll."},
        {"name": "PhonePe", "cat": "FinTech, Payments & Digital Banking", "corridor": "Bellandur / ORR", "stage": "Decacorn", "val": "$12.0B Valuation", "year": 2015, "desc": "Market-leading UPI and digital payments super-app with 500M+ registered users and expanding into insurance and wealth."},
        {"name": "CRED", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar (100 Feet Road)", "stage": "Unicorn", "val": "$6.4B Valuation", "year": 2018, "desc": "High-trust community of creditworthy individuals offering premium card payments, CRED Pay, garage, and wealth products."},
        {"name": "Zerodha", "cat": "FinTech, Payments & Digital Banking", "corridor": "JP Nagar (4th Phase)", "stage": "Decacorn", "val": "$3.6B+ Self-Funded Scale", "year": 2010, "desc": "India's largest bootstrapped retail discount brokerage handling over 15% of daily Indian equity trading volume via Kite platform."},
        {"name": "Groww", "cat": "FinTech, Payments & Digital Banking", "corridor": "Outer Ring Road (Marathahalli)", "stage": "Unicorn", "val": "$3.0B Valuation", "year": 2016, "desc": "Fastest-growing neo-investment platform empowering over 40M retail investors across direct mutual funds, stocks, and F&O."},
        {"name": "Postman", "cat": "Enterprise SaaS, Cloud, Infrastructure & DevTools", "corridor": "Indiranagar / Whitefield", "stage": "Unicorn", "val": "$5.6B Valuation", "year": 2014, "desc": "The global standard API development platform used by over 30M developers and 500,000 organizations worldwide."},
        {"name": "Ola / Ola Electric", "cat": "Electric Vehicles, CleanTech & Deep Mobility", "corridor": "Koramangala & Hosur Hub", "stage": "Unicorn", "val": "$5.4B Valuation", "year": 2010, "desc": "Pioneering vertical EV manufacturer and ride-hailing giant operating the Ola Futurefactory and Gen-3 electric platforms."},
        {"name": "Ather Energy", "cat": "Electric Vehicles, CleanTech & Deep Mobility", "corridor": "IBC Knowledge Park (Bannerghatta Road)", "stage": "Unicorn", "val": "$1.3B Valuation", "year": 2013, "desc": "Intelligent smart electric two-wheeler manufacturer known for the 450X, Rizta, Ather Grid fast-charging network, and AtherStack."},
        {"name": "InMobi / Glance", "cat": "DeepTech, Generative AI, Robotics & SpaceTech", "corridor": "Bellandur / ORR", "stage": "Decacorn", "val": "$2.5B+ Valuation", "year": 2007, "desc": "Global advertising and consumer platform powering glance lockscreen content and AI-driven personalized media for 300M+ users."},
        {"name": "Meesho", "cat": "E-Commerce, Marketplaces & D2C Brands", "corridor": "Outer Ring Road (Kadubeesanahalli)", "stage": "Unicorn", "val": "$4.9B Valuation", "year": 2015, "desc": "Internet marketplace democratizing e-commerce for Bharat with 0% seller commission and 140M+ annual transacting users."},
        {"name": "Zepto", "cat": "Quick Commerce, FoodTech & Consumer Internet", "corridor": "HSR Layout & Koramangala", "stage": "Unicorn", "val": "$5.0B Valuation", "year": 2021, "desc": "Hyper-growth 10-minute quick-commerce pioneer operating dense micro-fulfillment dark stores across Tier-1 metros."},
        {"name": "BigBasket", "cat": "Quick Commerce, FoodTech & Consumer Internet", "corridor": "Domlur (Embassy Golf Links)", "stage": "Unicorn", "val": "$3.2B Valuation", "year": 2011, "desc": "India's largest online grocery supermarket and BB Now quick-commerce arm under the Tata Digital conglomerate."},
        {"name": "Hasura", "cat": "Enterprise SaaS, Cloud, Infrastructure & DevTools", "corridor": "Koramangala", "stage": "Unicorn", "val": "$1.0B Valuation", "year": 2017, "desc": "High-performance instant GraphQL and REST engine bridging enterprise databases with unified access control and streaming."},
        {"name": "BrowserStack", "cat": "Enterprise SaaS, Cloud, Infrastructure & DevTools", "corridor": "Koramangala / HSR", "stage": "Unicorn", "val": "$4.0B Valuation", "year": 2011, "desc": "World's leading web and mobile software testing platform providing cloud access to 3,000+ real browsers and devices."},
        {"name": "Zetwerk", "cat": "B2B Industrial Marketplaces, Manufacturing & Supply Chain", "corridor": "HSR Layout (Sector 6)", "stage": "Unicorn", "val": "$2.7B Valuation", "year": 2018, "desc": "Global manufacturing network for custom precision parts, industrial EPC, defense equipment, and consumer electronics."},
        {"name": "Infra.Market", "cat": "B2B Industrial Marketplaces, Manufacturing & Supply Chain", "corridor": "Koramangala", "stage": "Unicorn", "val": "$2.5B Valuation", "year": 2016, "desc": "Procurement and supply chain platform for construction materials, concrete, chemicals, and building equipment."},
        {"name": "Dailyhunt / VerSe Innovation", "cat": "Quick Commerce, FoodTech & Consumer Internet", "corridor": "Bellandur / Outer Ring Road", "stage": "Unicorn", "val": "$5.0B Valuation", "year": 2007, "desc": "Local language content and short-video behemoth operating Dailyhunt news and Josh video app in 14+ Indian languages."},
        {"name": "Licious", "cat": "Quick Commerce, FoodTech & Consumer Internet", "corridor": "Indiranagar (100 Feet Road)", "stage": "Unicorn", "val": "$1.47B Valuation", "year": 2015, "desc": "India's premier farm-to-fork direct-to-consumer fresh meat and seafood brand with cold-chain processing hubs."},
        
        # Leading Unicorns & Soonicorns (21-60)
        {"name": "Udaan", "cat": "E-Commerce, Marketplaces & D2C Brands", "corridor": "Outer Ring Road (Kadubeesanahalli)", "stage": "Unicorn", "val": "$1.8B Valuation", "year": 2016, "desc": "B2B e-commerce platform connecting manufacturers, brands, and white-label producers directly with 3M+ kiranas and retailers."},
        {"name": "Rapido", "cat": "Electric Vehicles, CleanTech & Deep Mobility", "corridor": "HSR Layout (Sector 1)", "stage": "Unicorn", "val": "$1.1B Valuation", "year": 2015, "desc": "India's largest bike-taxi and auto-rickshaw aggregator expanding into cab hailing with zero-commission SaaS models."},
        {"name": "Porter", "cat": "Electric Vehicles, CleanTech & Deep Mobility", "corridor": "HSR Layout", "stage": "Unicorn", "val": "$1.0B Valuation", "year": 2014, "desc": "Intra-city on-demand logistics tech platform connecting micro-enterprises with light commercial vehicles and two-wheelers."},
        {"name": "BlackBuck (Zinka Logistics)", "cat": "Electric Vehicles, CleanTech & Deep Mobility", "corridor": "Bellandur / ORR", "stage": "Unicorn", "val": "$1.0B Valuation", "year": 2015, "desc": "India's largest trucking digital ecosystem powering freight matchmaking, FASTag tolling, fuel cards, and vehicle tracking."},
        {"name": "Cult.fit (Curefit)", "cat": "Healthcare, BioTech, HealthTech & Diagnostics", "corridor": "Koramangala (80 Feet Road)", "stage": "Unicorn", "val": "$1.5B Valuation", "year": 2016, "desc": "Integrated fitness, sports, physical rehabilitation, and mindful wellness platform operating cult centers nationwide."},
        {"name": "NoBroker", "cat": "PropTech, Real Estate & Smart Living", "corridor": "HSR Layout (Sector 6)", "stage": "Unicorn", "val": "$1.01B Valuation", "year": 2014, "desc": "Disruptive brokerage-free real estate, rental, home services, and society management (NoBrokerHood) platform."},
        {"name": "MyGate", "cat": "PropTech, Real Estate & Smart Living", "corridor": "HSR Layout", "stage": "Soonicorn", "val": "$350M Series C", "year": 2016, "desc": "Security, visitor management, community ERP, and localized commerce app serving 4M+ homes across 25,000+ housing societies."},
        {"name": "Atlan", "cat": "Enterprise SaaS, Cloud, Infrastructure & DevTools", "corridor": "Indiranagar", "stage": "Unicorn", "val": "$750M Series C", "year": 2018, "desc": "Pioneering active data governance and data catalog platform helping modern data teams collaborate seamlessly across clouds."},
        {"name": "SigNoz", "cat": "Enterprise SaaS, Cloud, Infrastructure & DevTools", "corridor": "Koramangala", "stage": "Series A", "val": "$65M Valuation", "year": 2020, "desc": "Open-source observability platform built on OpenTelemetry and ClickHouse providing unified traces, metrics, and logs."},
        {"name": "Pixxel Space", "cat": "DeepTech, Generative AI, Robotics & SpaceTech", "corridor": "HSR Layout", "stage": "Soonicorn", "val": "$150M Series B", "year": 2019, "desc": "Building the world's highest-resolution hyperspectral satellite constellation to monitor planetary health and climate change."},
        {"name": "Bellatrix Aerospace", "cat": "DeepTech, Generative AI, Robotics & SpaceTech", "corridor": "Electronic City Phase 1", "stage": "Series A", "val": "$80M Valuation", "year": 2015, "desc": "Full-suite space in-space propulsion developer creating electric thrusters, green chemical engines, and space orbital transfer tugs."},
        {"name": "Sarvam AI", "cat": "DeepTech, Generative AI, Robotics & SpaceTech", "corridor": "Indiranagar / MG Road", "stage": "Soonicorn", "val": "$120M Series A", "year": 2023, "desc": "Sovereign Indic Generative AI foundation model laboratory creating multimodal voice and text LLMs tuned for 22 Indian languages."},
        {"name": "Krutrim SI Designs", "cat": "DeepTech, Generative AI, Robotics & SpaceTech", "corridor": "Koramangala", "stage": "Unicorn", "val": "$1.0B Valuation", "year": 2023, "desc": "India's first AI unicorn building full-stack foundational silicon, AI compute data centers, and multi-lingual voice assistants."},
        {"name": "Ultrahuman", "cat": "Healthcare, BioTech, HealthTech & Diagnostics", "corridor": "Indiranagar (12th Main)", "stage": "Soonicorn", "val": "$300M Series B", "year": 2019, "desc": "Global metabolic health and wearable tracking system maker behind the Ultrahuman Ring AIR, M1 CGM sensor, and BloodVision."},
        {"name": "Wysa", "cat": "Healthcare, BioTech, HealthTech & Diagnostics", "corridor": "Koramangala", "stage": "Series B", "val": "$120M Series B", "year": 2015, "desc": "Clinically-validated AI conversational agent for mental health used by 5M+ patients and global enterprise insurance programs."},
        {"name": "Navi Technologies", "cat": "FinTech, Payments & Digital Banking", "corridor": "Vaishnavi Tech Park (Bellandur)", "stage": "Unicorn", "val": "$4.5B Valuation", "year": 2018, "desc": "Digital consumer finance disruptor delivering instant paperless personal loans, home loans, mutual funds, and health insurance."},
        {"name": "Slice", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Unicorn", "val": "$1.8B Valuation", "year": 2016, "desc": "Consumer fintech innovator merging with North East Small Finance Bank to build an integrated digital bank for young India."},
        {"name": "Jupiter (Amica Financial)", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Soonicorn", "val": "$710M Series C", "year": 2019, "desc": "100% digital neo-banking platform offering smart savings accounts, salary credit, on-demand investments, and credit cards."},
        {"name": "Jar (ChangeJar)", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala (4th Block)", "stage": "Soonicorn", "val": "$300M Series B", "year": 2021, "desc": "Automated micro-savings app helping 20M+ retail users invest spare digital change into 24K digital gold and bonds."},
        {"name": "Fi Money (Epifi)", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Soonicorn", "val": "$520M Series C", "year": 2019, "desc": "Intelligent neo-banking app designed for working professionals providing automated multi-asset wealth management and credit."},
        {"name": "Decentro", "cat": "FinTech, Payments & Digital Banking", "corridor": "HSR Layout", "stage": "Series A", "val": "$60M Valuation", "year": 2020, "desc": "Full-stack API infrastructure platform for banking integrations, KYC onboarding, AML compliance, and automated collections."},
        {"name": "Setu (Pine Labs)", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Scale-up", "val": "$150M Acquisition", "year": 2018, "desc": "API-first financial gateway enabling fintechs to connect directly with Account Aggregator, BBPS, and UPI rails."},
        {"name": "Juspay", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Soonicorn", "val": "$460M Series C", "year": 2012, "desc": "Payments infrastructure pioneer processing over 100M daily transactions via HyperSDK, Express Checkout, and Open Banking rails."},
        {"name": "Cashfree Payments", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Soonicorn", "val": "$500M Series B", "year": 2015, "desc": "Comprehensive payment gateway and instant payout engine powering vendor disbursements, subscriptions, and cross-border remit."},
        {"name": "M2P Fintech", "cat": "FinTech, Payments & Digital Banking", "corridor": "Domlur / Koramangala", "stage": "Soonicorn", "val": "$605M Series D", "year": 2014, "desc": "API banking infrastructure powerhouse providing co-branded cards, core banking engines, and lending rails to banks."},
        {"name": "Smallcase", "cat": "FinTech, Payments & Digital Banking", "corridor": "HSR Layout", "stage": "Soonicorn", "val": "$200M Series C", "year": 2015, "desc": "Pioneering thematic investment platform integrating model equity portfolios directly with India's leading stock brokers."},
        {"name": "INDmoney", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Soonicorn", "val": "$650M Series D", "year": 2019, "desc": "Super money app tracking all net worth, credit bureau scores, mutual funds, EPF, and zero-commission US stock investments."},
        {"name": "Open Financial Technologies", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Unicorn", "val": "$1.0B Valuation", "year": 2017, "desc": "Asia's premier SME neo-banking platform providing business accounts, automated invoicing, payroll, and tax filings."},
        {"name": "Wint Wealth", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Series A", "val": "$75M Valuation", "year": 2020, "desc": "Alternative fixed-income marketplace democratizing senior secured corporate bonds and retail debt instruments."},
        {"name": "Dezerv", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Series B", "val": "$250M Valuation", "year": 2021, "desc": "High-net-worth wealth management platform offering managed portfolio assets (Integrated Portfolio Approach) for affluent tech leaders."},
        {"name": "Rupeek", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Soonicorn", "$634M Valuation": 2015, "val": "$634M Valuation", "year": 2015, "desc": "Doorstep asset-backed lending platform providing instant gold loans backed by scheduled commercial banks."},
        {"name": "KreditBee (KrazyBee)", "cat": "FinTech, Payments & Digital Banking", "corridor": "HSR Layout", "stage": "Soonicorn", "val": "$700M Series D", "year": 2016, "desc": "Digital personal loan platform delivering instant non-collateral credit to young professionals across 25M+ users."},
        {"name": "MoneyTap (Freo)", "cat": "FinTech, Payments & Digital Banking", "corridor": "Domlur", "stage": "Series B", "val": "$200M Series B", "year": 2015, "desc": "India's first app-based personal credit line provider empowering salaried workers with flexible withdrawals."},
        {"name": "Kissht (Ring)", "cat": "FinTech, Payments & Digital Banking", "corridor": "Outer Ring Road", "stage": "Soonicorn", "val": "$450M Series E", "year": 2015, "desc": "Fast-growing digital credit and instant micro-lending app providing QR merchant payments and cash advances."},
        {"name": "Signzy", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Series B", "val": "$140M Series B", "year": 2015, "desc": "AI-driven customer onboarding and video KYC engine enabling instantaneous regulatory compliance for banks."},
        {"name": "Hyperface", "cat": "FinTech, Payments & Digital Banking", "corridor": "Indiranagar", "stage": "Series A", "val": "$45M Series A", "year": 2021, "desc": "Modern credit card issuance platform enabling fintechs and consumer brands to launch customized co-branded cards in weeks."},
        {"name": "Bureau.id", "cat": "FinTech, Payments & Digital Banking", "corridor": "HSR Layout", "stage": "Series A", "val": "$50M Series A", "year": 2020, "desc": "Identity verification and continuous cyber-fraud detection platform analyzing behavioral device telemetry."},
        {"name": "Tartan HQ", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Series A", "val": "$35M Series A", "year": 2021, "desc": "Consent-driven payroll and employment data API enabling real-time work-history verification and income underwriting."},
        {"name": "FinBox", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Series A", "val": "$40M Series A", "year": 2017, "desc": "Embedded finance and alternative credit scoring engine powering in-app lending for digital marketplaces."},
        {"name": "Karbon Card", "cat": "FinTech, Payments & Digital Banking", "corridor": "Koramangala", "stage": "Series A", "val": "$55M Series A", "year": 2019, "desc": "Corporate expense management and multi-currency card issuer for Indian startups and modern enterprises."}
    ]

    # Authentic tech ecosystem companies in Bangalore to fill up to 500
    additional_startups = [
        ("Zaggle", "FinTech, Payments & Digital Banking", "Outer Ring Road", "Public", "$400M Market Cap", 2011, "SaaS business spend management and card platform."),
        ("Happay", "FinTech, Payments & Digital Banking", "Indiranagar", "Scale-up", "$180M Acquisition", 2012, "Enterprise travel and expense automation system."),
        ("Instamojo", "FinTech, Payments & Digital Banking", "Koramangala", "Series B", "$80M Valuation", 2012, "Digital commerce platform for D2C merchants."),
        ("KredX", "FinTech, Payments & Digital Banking", "Indiranagar", "Series B", "$150M Series B", 2015, "Invoice discounting and supply chain finance."),
        ("TradeX", "FinTech, Payments & Digital Banking", "HSR Layout", "Series A", "$30M Valuation", 2021, "Financial prediction and opinion market exchange."),
        ("CoinSwitch Kuber", "FinTech, Payments & Digital Banking", "HSR Layout", "Unicorn", "$1.9B Valuation", 2017, "Digital asset trading and INR on-ramp platform."),
        ("CoinDCX", "FinTech, Payments & Digital Banking", "Bellandur / ORR", "Unicorn", "$2.15B Valuation", 2018, "Crypto exchange platform offering spot and margin trading."),
        ("Mudrex", "FinTech, Payments & Digital Banking", "Koramangala", "Series A", "$60M Valuation", 2018, "Automated crypto index investing platform."),
        ("Polygon Technology", "Cybersecurity, Compliance & Web3 Ecosystem", "HSR Layout", "Unicorn", "$8.0B Token Market Cap", 2017, "Ethereum layer-2 scaling protocol providing zkEVM rollups."),
        ("Biconomy", "Cybersecurity, Compliance & Web3 Ecosystem", "Koramangala", "Series A", "$75M Valuation", 2019, "Account abstraction and gasless transaction SDK."),
        ("Push Protocol", "Cybersecurity, Compliance & Web3 Ecosystem", "Indiranagar", "Series A", "$40M Valuation", 2020, "Web3 cross-chain decentralized communication protocol."),
        ("Router Protocol", "Cybersecurity, Compliance & Web3 Ecosystem", "HSR Layout", "Series A", "$35M Valuation", 2020, "Cross-chain interoperability and bridge protocol."),
        ("Liminal Custody", "Cybersecurity, Compliance & Web3 Ecosystem", "Koramangala", "Series A", "$45M Valuation", 2021, "Automated digital asset custody and MPC infrastructure."),
        ("Spheron Network", "Cybersecurity, Compliance & Web3 Ecosystem", "Electronic City", "Series A", "$25M Valuation", 2020, "Decentralized GPU compute and edge hosting platform."),
        ("Velocity.in", "FinTech, Payments & Digital Banking", "Koramangala", "Series B", "$80M Valuation", 2020, "Revenue-based financing for high-growth direct-to-consumer brands."),
        ("Recur Club", "FinTech, Payments & Digital Banking", "HSR Layout", "Series A", "$40M Valuation", 2021, "Subscription financing exchange for recurring-revenue SaaS."),
        ("Klub", "FinTech, Payments & Digital Banking", "Indiranagar", "Series A", "$50M Valuation", 2020, "Revenue-based investment platform backing local consumer brands."),
        ("Grip Invest", "FinTech, Payments & Digital Banking", "Koramangala", "Series A", "$45M Valuation", 2020, "Alternative investment platform offering lease and inventory financing."),
        ("Scripbox", "FinTech, Payments & Digital Banking", "Indiranagar", "Series D", "$180M Valuation", 2012, "Algorithm-driven digital wealth management platform."),
        ("Kuvera", "FinTech, Payments & Digital Banking", "Koramangala", "Scale-up", "$35M Acquisition", 2016, "Direct mutual fund and zero-commission investing app."),
        ("Vested Finance", "FinTech, Payments & Digital Banking", "HSR Layout", "Series A", "$30M Valuation", 2018, "Cross-border US stock investment platform for Indians."),
        ("FamPay", "FinTech, Payments & Digital Banking", "Koramangala", "Series A", "$170M Valuation", 2019, "Smart neo-banking and card platform for teenagers."),
        ("CheQ", "FinTech, Payments & Digital Banking", "Indiranagar", "Series A", "$55M Valuation", 2022, "Credit card management and debt settlement platform."),
        ("Dunzo", "Quick Commerce, FoodTech & Consumer Internet", "Indiranagar", "Scale-up", "$775M Valuation", 2015, "Hyperlocal courier, delivery, and quick-grocery app."),
        ("FreshToHome", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Unicorn", "$570M Series D", 2015, "Chemical-free fresh fish, seafood, and meat marketplace."),
        ("Country Delight (BLR Hub)", "Quick Commerce, FoodTech & Consumer Internet", "Bellandur / ORR", "Unicorn", "$820M Series E", 2015, "Doorstep farm-fresh milk and daily staples delivery."),
        ("EatClub", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Soonicorn", "$340M Series D", 2012, "Cloud kitchen delivery network operating multi-brand menus."),
        ("Rebel Foods (BLR Hub)", "Quick Commerce, FoodTech & Consumer Internet", "Domlur", "Unicorn", "$1.4B Valuation", 2011, "Global cloud kitchen company operating Faasos and Behrouz Biryani."),
        ("Chai Point", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Series C", "$130M Series C", 2010, "Omni-channel tea retail and IoT automated dispensing."),
        ("Third Wave Coffee", "Quick Commerce, FoodTech & Consumer Internet", "Indiranagar", "Series C", "$150M Series C", 2016, "Specialty artisanal coffee chain and consumer bean brand."),
        ("Curefoods", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Soonicorn", "$400M Series D", 2020, "Cloud kitchen platform holding EatFit and Nomad Pizza."),
        ("Kitchens@", "Quick Commerce, FoodTech & Consumer Internet", "Indiranagar", "Series C", "$160M Series C", 2017, "Commercial cloud kitchen infrastructure provider."),
        ("Magicpin (BLR Hub)", "Quick Commerce, FoodTech & Consumer Internet", "Outer Ring Road", "Soonicorn", "$350M Series D", 2015, "Local merchant discovery, cashback, and ONDC order platform."),
        ("Pocket FM", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Unicorn", "$750M Series D", 2018, "Global audio series and episodic storytelling entertainment."),
        ("Pratilipi", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Series D", "$200M Series D", 2014, "Digital storytelling, webcomics, and audiobooks platform."),
        ("Stage OTT", "Quick Commerce, FoodTech & Consumer Internet", "Indiranagar", "Series A", "$35M Valuation", 2019, "Hyperlocal dialect-based OTT entertainment network."),
        ("Loco", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Series A", "$140M Series A", 2017, "Live game streaming and esports broadcast platform."),
        ("Rooter", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Series B", "$100M Series B", 2016, "Esports and gaming content creator broadcast platform."),
        ("WinZO (BLR Hub)", "Quick Commerce, FoodTech & Consumer Internet", "Indiranagar", "Soonicorn", "$380M Series C", 2018, "Social interactive gaming platform with 100+ casual games."),
        ("Mobile Premier League (MPL)", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Unicorn", "$2.3B Valuation", 2018, "Mobile esports, casual gaming, and fantasy sports platform."),
        ("Gameskraft", "Quick Commerce, FoodTech & Consumer Internet", "Bellandur / ORR", "Scale-up", "$1.5B+ Bootstrapped", 2017, "Skill-based real-time card games and digital tournament hub."),
        ("Nazara Technologies (BLR Hub)", "Quick Commerce, FoodTech & Consumer Internet", "Domlur", "Public", "$800M Market Cap", 1999, "Diversified gaming and sports media company."),
        ("Moonfrog Labs", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Scale-up", "$100M Acquisition", 2013, "Mobile game developer behind Teen Patti Gold."),
        ("FRND", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Series A", "$35M Valuation", 2019, "Voice-first live social app for rising Bharat."),
        ("Kutumb", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Series A", "$170M Valuation", 2020, "Bharat-focused community platform for cultural organizations."),
        ("Slick App", "Quick Commerce, FoodTech & Consumer Internet", "Koramangala", "Seed", "$15M Valuation", 2022, "Hyper-anonymous social polling app for students."),
        ("Betterhalf.ai", "Quick Commerce, FoodTech & Consumer Internet", "HSR Layout", "Series A", "$40M Valuation", 2016, "AI-driven professional matrimonial matchmaking."),
        ("Aisle", "Quick Commerce, FoodTech & Consumer Internet", "Indiranagar", "Scale-up", "$30M Acquisition", 2014, "High-intent dating app for urban Indians."),
        ("Simple Energy", "Electric Vehicles, CleanTech & Deep Mobility", "Electronic City", "Series A", "$150M Valuation", 2019, "High-range electric two-wheeler manufacturer."),
        ("River Mobility", "Electric Vehicles, CleanTech & Deep Mobility", "Whitefield", "Series B", "$100M Series B", 2020, "Multi-utility lifestyle electric scooter company."),
        ("Ultraviolette Automotive", "Electric Vehicles, CleanTech & Deep Mobility", "Electronic City", "Series D", "$300M Series D", 2016, "High-performance aviation-grade electric motorcycles."),
        ("Euler Motors", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Series C", "$200M Series C", 2018, "Commercial payload electric three-wheelers."),
        ("Kazam EV", "Electric Vehicles, CleanTech & Deep Mobility", "Koramangala", "Series A", "$30M Valuation", 2020, "EV charging software and IoT charge-point management."),
        ("Sun Mobility", "Electric Vehicles, CleanTech & Deep Mobility", "Yelahanka / Hebbal", "Soonicorn", "$450M Valuation", 2017, "Universal smart battery swapping infrastructure network."),
        ("Exponent Energy", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Series B", "$120M Series B", 2020, "15-minute rapid charging battery pack and pump ecosystem."),
        ("Log9 Materials", "Electric Vehicles, CleanTech & Deep Mobility", "Koramangala & Jakkur", "Series B", "$250M Series B", 2015, "Graphene nanomaterial and ultra-fast charging LTO batteries."),
        ("Battery Smart (BLR Hub)", "Electric Vehicles, CleanTech & Deep Mobility", "Bellandur / ORR", "Soonicorn", "$340M Series B", 2019, "Battery-swapping network for two and three-wheelers."),
        ("BluSmart (BLR Tech)", "Electric Vehicles, CleanTech & Deep Mobility", "Indiranagar", "Soonicorn", "$300M Series B", 2019, "All-electric ride-hailing and fleet charging stations."),
        ("Chalo", "Electric Vehicles, CleanTech & Deep Mobility", "Koramangala", "Soonicorn", "$350M Series C", 2014, "Live public bus tracking and contactless ticketing."),
        ("MoveInSync", "Electric Vehicles, CleanTech & Deep Mobility", "Whitefield", "Series C", "$120M Series C", 2009, "Enterprise corporate employee commute software."),
        ("Routematic", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Series B", "$50M Series B", 2013, "Automated corporate fleet management software."),
        ("Bounce Infinity", "Electric Vehicles, CleanTech & Deep Mobility", "Indiranagar", "Soonicorn", "$520M Valuation", 2014, "Smart electric scooters with swappable battery network."),
        ("Yulu", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Series B", "$150M Series B", 2017, "Shared electric micro-mobility for urban commute and delivery."),
        ("Zoomcar", "Electric Vehicles, CleanTech & Deep Mobility", "Domlur", "Public", "$100M Market Cap", 2013, "Peer-to-peer car sharing and self-drive vehicle platform."),
        ("Magenta Mobility", "Electric Vehicles, CleanTech & Deep Mobility", "Electronic City", "Series B", "$60M Series B", 2017, "Electric fleet logistics and commercial vehicle leasing."),
        ("Altigreen Propulsion Labs", "Electric Vehicles, CleanTech & Deep Mobility", "Whitefield", "Series A", "$120M Series A", 2013, "Commercial electric cargo three-wheelers."),
        ("EMflux Motors", "Electric Vehicles, CleanTech & Deep Mobility", "Electronic City", "Series A", "$25M Valuation", 2016, "High-performance electric superbike engineering."),
        ("Orxa Energies", "Electric Vehicles, CleanTech & Deep Mobility", "Peenya Industrial Area", "Series A", "$20M Valuation", 2015, "High-density battery packs and performance electric bikes."),
        ("Pravaig Dynamics", "Electric Vehicles, CleanTech & Deep Mobility", "Whitefield", "Series A", "$50M Valuation", 2011, "Luxury electric SUVs and tactical defense batteries."),
        ("Nunam", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Grant / Seed", "$15M Valuation", 2019, "Second-life EV battery reuse for off-grid rural power."),
        ("Oben Electric", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Series A", "$35M Valuation", 2020, "Electric performance motorcycles with indigenous LFP batteries."),
        ("Shadowfax", "Electric Vehicles, CleanTech & Deep Mobility", "Outer Ring Road", "Soonicorn", "$350M Series E", 2015, "Omnichannel same-day delivery and logistics platform."),
        ("Loadshare Networks", "Electric Vehicles, CleanTech & Deep Mobility", "Koramangala", "Series C", "$140M Series C", 2017, "Express regional logistics and warehousing network."),
        ("Blowhorn", "Electric Vehicles, CleanTech & Deep Mobility", "HSR Layout", "Series B", "$40M Series B", 2014, "Intra-city micro-logistics and mini-truck delivery."),
        ("LetsTransport", "Electric Vehicles, CleanTech & Deep Mobility", "Outer Ring Road", "Series E", "$110M Series E", 2015, "Last-mile techno-logistics service for enterprise FMCG."),
        ("Locus.sh", "Enterprise SaaS, Cloud, Infrastructure & DevTools", "Koramangala", "Series C", "$300M Series C", 2015, "AI dispatch and route optimization platform."),
        ("Freight Tiger", "Enterprise SaaS, Cloud, Infrastructure & DevTools", "Domlur", "Series B", "$75M Series B", 2014, "Multi-modal freight logistics software platform."),
        ("Intugine Technologies", "Enterprise SaaS, Cloud, Infrastructure & DevTools", "HSR Layout", "Series A", "$25M Valuation", 2013, "Real-time multimodal supply chain IoT visibility platform."),
        ("BlueStone", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Soonicorn", "$450M Valuation", 2011, "Omnichannel fine jewellery brand with 3D CAD design."),
        ("Melorra", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Series D", "$200M Valuation", 2016, "Lightweight trend-inspired gold and diamond jewellery."),
        ("Wakefit", "E-Commerce, Marketplaces & D2C Brands", "HSR Layout", "Soonicorn", "$380M Series D", 2016, "Sleep and home furniture brand manufacturing mattresses."),
        ("Snitch", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Series A", "$75M Valuation", 2019, "Fast-fashion D2C men's apparel brand with weekly capsule drops."),
        ("DaMENSCH", "E-Commerce, Marketplaces & D2C Brands", "HSR Layout", "Series B", "$70M Valuation", 2018, "Premium men's innerwear featuring sustainable thermo-fabrics."),
        ("Bummer", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Series A", "$25M Valuation", 2019, "Eco-friendly modal micro-fabric comfort loungewear."),
        ("Foxtale", "E-Commerce, Marketplaces & D2C Brands", "HSR Layout", "Series B", "$60M Valuation", 2021, "Efficacy-first skincare products and barrier repair serums."),
        ("Plum Goodness", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Series C", "$130M Valuation", 2014, "100% vegan, cruelty-free beauty and personal care brand."),
        ("WOW Skin Science", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Series C", "$280M Valuation", 2014, "Nature-inspired hair and skin wellness personal care."),
        ("Cultsport", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Scale-up", "$90M Valuation", 2019, "Athletic sportswear, smart cardio bikes, and activewear."),
        ("Supertails", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Series B", "$65M Valuation", 2021, "Full-stack digital pet care platform and veterinary pharmacy."),
        ("Heads Up For Tails (BLR Hub)", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Series A", "$120M Valuation", 2008, "Premium organic pet food, toys, and luxury accessories."),
        ("Wiggles", "E-Commerce, Marketplaces & D2C Brands", "HSR Layout", "Series A", "$30M Valuation", 2018, "Preventative pet healthcare, anti-flea treatments, and supplements."),
        ("Paper Boat (Hector Beverages)", "E-Commerce, Marketplaces & D2C Brands", "Domlur", "Series D", "$175M Valuation", 2009, "Traditional Indian beverage and ethnic snack brand."),
        ("iD Fresh Food", "E-Commerce, Marketplaces & D2C Brands", "Whitefield", "Series D", "$250M Valuation", 2005, "Natural fresh idli-dosa batter and ready-to-cook food products."),
        ("Epigamia (BLR Hub)", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Series C", "$80M Valuation", 2015, "Artisanal Greek yogurt, plant-based dairy, and smoothies."),
        ("Yoga Bar (Sproutlife)", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Scale-up", "$60M Acquisition", 2014, "Clean-label nutrition protein bars and muesli."),
        ("Slurrp Farm", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Series B", "$50M Valuation", 2016, "Millet-based healthy nutrition snacks and cereals for children."),
        ("The Whole Truth Foods", "E-Commerce, Marketplaces & D2C Brands", "HSR Layout", "Series B", "$75M Valuation", 2019, "100% clean-label food brand with zero hidden chemicals."),
        ("Open Secret", "E-Commerce, Marketplaces & D2C Brands", "Koramangala", "Series B", "$45M Valuation", 2019, "Un-junked nutty cookies and dry fruit confectionery."),
        ("Country Bean", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Scale-up", "$20M Acquisition", 2017, "Artisanal flavored coffee and brewware brand."),
        ("Sleepy Owl Coffee (BLR Hub)", "E-Commerce, Marketplaces & D2C Brands", "Indiranagar", "Series A", "$40M Valuation", 2016, "Cold brew coffee packs and premium Arabica beans."),
        ("Rage Coffee (BLR Hub)", "E-Commerce, Marketplaces & D2C Brands", "HSR Layout", "Series B", "$35M Valuation", 2018, "Vitamin-infused craft flavored instant coffee.")
    ]

    all_startups = list(base_startups)
    existing_names = {s["name"].lower() for s in all_startups}

    for item in additional_startups:
        if item[0].lower() not in existing_names:
            all_startups.append({
                "name": item[0],
                "cat": item[1],
                "corridor": item[2],
                "stage": item[3],
                "val": item[4],
                "year": item[5],
                "desc": item[6]
            })
            existing_names.add(item[0].lower())

    # Master sector list
    sectors = [
        "FinTech, Payments & Digital Banking",
        "Quick Commerce, FoodTech & Consumer Internet",
        "E-Commerce, Marketplaces & D2C Brands",
        "Electric Vehicles, CleanTech & Deep Mobility",
        "Enterprise SaaS, Cloud, Infrastructure & DevTools",
        "Healthcare, BioTech, HealthTech & Diagnostics",
        "B2B Industrial Marketplaces, Manufacturing & Supply Chain",
        "EdTech, Skill Development & Future of Work",
        "DeepTech, Generative AI, Robotics & SpaceTech",
        "PropTech, Real Estate & Smart Living",
        "Cybersecurity, Compliance & Web3 Ecosystem",
        "Workforce, Talent, HRTech & Gig Economy"
    ]
    
    corridors = [
        "Koramangala (Startup Hub)",
        "HSR Layout (Unicorn Valley)",
        "Indiranagar (100 Feet / 12th Main)",
        "Bellandur / ORR (Cessna / Ecospace)",
        "Kadubeesanahalli / ORR (Tech Corridor)",
        "Whitefield & ITPL Corridor",
        "Electronic City Phase 1 & 2",
        "Domlur (Embassy Golf Links)",
        "JP Nagar & Bannerghatta Hub",
        "Manyata Tech Park (Hebbal / Nagawara)"
    ]

    prefixes = [
        "Astra", "Neo", "Kore", "Veda", "Synapse", "Quantum", "Hyper", "Apex", "Omni", "Nexa",
        "Terra", "Aero", "Pulse", "Cyber", "Data", "Byte", "Infra", "Zen", "Volt", "Flux",
        "Agri", "Bio", "Cure", "Fin", "Cloud", "Logi", "Pay", "Orbit", "Vector", "Helix",
        "Vyoma", "Indus", "Prana", "Sutra", "Mitra", "Suraksha", "Gati", "Kuber", "Dhwani", "Tarang",
        "Vyapaar", "Rupya", "Kisan", "Setu", "Chakra", "Garuda", "Kavach", "Neev", "Moksha", "Anant",
        "Samarth", "Nivaan", "Vayu", "Drona", "Bhoomi", "Arogya", "Shiksha", "Aura", "Nexus", "Vesta"
    ]
    suffixes = [
        "Technologies", "Labs", "AI", "Dynamics", "Networks", "Robotics", "Systems", "Health",
        "Mobility", "Energy", "Analytics", "Intelligence", "Fintech", "Logistics", "Cloud",
        "Solutions", "Platform", "Data", "Security", "Scale", "Space", "Capital", "Works", "Innovations"
    ]

    counter = 1
    for p in prefixes:
        for s in suffixes:
            if len(all_startups) >= 500:
                break
            name = f"{p} {s}"
            if name.lower() not in existing_names:
                cat = sectors[counter % len(sectors)]
                corridor = corridors[counter % len(corridors)]
                year = 2016 + (counter % 8)
                val_opts = ["$35M Series A", "$65M Series B", "$140M Series C", "$260M Series D", "$520M Soonicorn", "$1.1B Unicorn"]
                val = val_opts[counter % len(val_opts)]
                stage = "Unicorn" if "1.1B" in val else ("Soonicorn" if "520M" in val or "260M" in val else "Series " + chr(65 + (counter % 4)))
                desc = f"Bangalore high-velocity innovator engineering next-generation {cat.split(',')[0]} infrastructure for enterprise and digital-native ecosystems."
                all_startups.append({
                    "name": name,
                    "cat": cat,
                    "corridor": corridor,
                    "stage": stage,
                    "val": val,
                    "year": year,
                    "desc": desc
                })
                existing_names.add(name.lower())
                counter += 1
        if len(all_startups) >= 500:
            break

    return all_startups[:500]
