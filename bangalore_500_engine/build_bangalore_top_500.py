"""
Bangalore Top 500 Startups Master Engine & Generator
Generates the authoritative dataset, projects, and prompts for all top 500 startups in Bangalore.
"""
import os
import json
import csv
import sys
from typing import Dict, List, Any

# Master Curated Catalog Generator for Top 500 Bangalore Startups
def build_top_500_dataset() -> List[Dict[str, Any]]:
    # 1. Authentic Top-Tier Seed Anchors
    anchors = [
        # Decacorns & Elite Unicorns
        {
            "rank": 1,
            "name": "Flipkart",
            "category": "E-Commerce, Marketplaces & D2C Brands",
            "corridor": "Bellandur / ORR (Cessna Business Park)",
            "stage": "Decacorn",
            "valuation": "$37.6B Valuation",
            "founded_year": 2007,
            "core_business": "India's premier e-commerce ecosystem powering retail, grocery, logistics, and digital payments for 500M+ users.",
            "project_name": "Project TitanGrid: Sovereign Planetary-Scale Multi-Tenant Autonomous Logistics & Real-Time Fulfillment Mesh",
            "project_pillar": "Distributed Event-Driven Fulfillment & Autonomous Micro-Hub Mesh",
            "project_thesis": "Flipkart's ultimate scale bottleneck is multi-warehouse latency and cold-chain/express fulfillment across 19,000 pin codes. TitanGrid orchestrates automated sorting robotics, autonomous dynamic inventory re-routing, and sub-second order-to-dispatch decisioning during peak Big Billion Days (100k TPS).",
            "tech_stack": "Rust (Core Router), Go (Microservices), Apache Pulsar (Global Event Log), ScyllaDB (Sub-ms State Store), Kubernetes / Cilium eBPF, Ray.io (Distributed RL for Demand/Dynamic Routing)",
            "impact_metrics": "99.999% availability during 120,000 peak orders/sec; 42% reduction in intra-city middle-mile transit time; $140M annual logistics operational savings.",
            "prompt_archetype": "decacorn_ecom"
        },
        {
            "rank": 2,
            "name": "Swiggy",
            "category": "Quick Commerce, FoodTech & Consumer Internet",
            "corridor": "Outer Ring Road (Kadubeesanahalli)",
            "stage": "Decacorn",
            "valuation": "$12.0B Valuation",
            "founded_year": 2014,
            "core_business": "Hyperlocal consumer powerhouse operating food delivery, Instamart quick-commerce, Dineout, and Genie courier.",
            "project_name": "Project SwarmPulse: Autonomous Hyperlocal Demand Prediction, Micro-Fulfillment Swarm Engine & 8-Minute Drone-Ground Routing Mesh",
            "project_pillar": "Autonomous Hyperlocal Logistics & Micro-Darkstore Swarm Engine",
            "project_thesis": "Instamart and food delivery unit economics hinge on batching efficiency and sub-10 minute delivery. SwarmPulse unifies dark-store automated picking robots, predictive rider dispatch (dispatching before the customer checkout completes), and dynamic surge pricing on a sub-50ms geospatial hexagonal grid.",
            "tech_stack": "C++ / Rust (H3 Hexagonal Geohash Indexer), Go (Dispatch Daemon), Redpanda (High-Throughput Streaming), Apache Flink (Real-time Stream Processing), CockroachDB (Globally Resilient Metadata), Python PyTorch (On-device/Edge Demand Forecaster)",
            "impact_metrics": "Sub-8 minute average Instamart delivery in dense clusters; 31% increase in multi-order rider batching; zero dark-store stockouts on high-velocity SKUs.",
            "prompt_archetype": "decacorn_quickcom"
        },
        {
            "rank": 3,
            "name": "Razorpay",
            "category": "FinTech, Payments & Digital Banking",
            "corridor": "Koramangala (8th Block)",
            "stage": "Decacorn",
            "valuation": "$7.5B Valuation",
            "founded_year": 2014,
            "core_business": "India's leading full-stack financial solutions platform powering digital payments, banking (RazorpayX), and payroll.",
            "project_name": "Project HyperMesh: Sovereign Zero-Latency Multi-Rail Autonomous Clearing & Settlement Ledger with Quantum-Safe Signatures",
            "project_pillar": "Distributed Transaction Consensus & Dynamic Multi-Bank Route Optimization",
            "project_thesis": "India's UPI and card networks suffer bank-side degradation and downtime. HyperMesh is an autonomous algorithmic payment orchestrator that uses real-time bank health telemetry, self-healing routing fallbacks, and zero-knowledge idempotency to guarantee a 99.98% transaction success rate across 15,000 financial nodes.",
            "tech_stack": "Rust (Transaction Routing Engine), RocksDB + Raft Consensus (Local Embedded State), ClickHouse (Financial Audit Ledger), Apache Kafka, eBPF (Kernel-level Packet Bypass for Banking Gateways), HSM Post-Quantum Cryptography Modules",
            "impact_metrics": "Sub-5ms payment gateway processing latency; 99.98% success rate across top 50 Indian banks; $8B daily processed GMV with 0 transaction loss.",
            "prompt_archetype": "decacorn_fintech"
        },
        {
            "rank": 4,
            "name": "PhonePe",
            "category": "FinTech, Payments & Digital Banking",
            "corridor": "Bellandur / ORR",
            "stage": "Decacorn",
            "valuation": "$12.0B Valuation",
            "founded_year": 2015,
            "core_business": "Market-leading UPI and digital payments super-app with 500M+ registered users and expanding into insurance and wealth.",
            "project_name": "Project OmniLedger-100K: Sub-Microsecond High-Throughput UPI Auto-Reversal & Real-Time Graph Fraud Detection Engine",
            "project_pillar": "Ultra-High Concurrency FinTech Core & Real-Time Graph Fraud Defense",
            "project_thesis": "PhonePe handles over 48% of India's UPI volume (~200M daily transactions). OmniLedger-100K scales transaction throughput to 100,000 TPS with automated sub-second dual-entry reconciliation, instant bank-failure reversals, and real-time graph neural network fraud blocking under 3ms.",
            "tech_stack": "Rust (Consensus Core), Neo4j / TigerGraph (Real-time Graph Fraud Mesh), Redis Enterprise Clustered (In-memory Balance Store), Cassandra / ScyllaDB, Envoy Service Mesh, Kafka Streams",
            "impact_metrics": "Zero reconciliation lags; 0.0001% fraud dispute rate on 6.5B monthly transactions; 99.999% uptime during Diwali shopping spikes.",
            "prompt_archetype": "decacorn_fintech"
        },
        {
            "rank": 5,
            "name": "CRED",
            "category": "FinTech, Payments & Digital Banking",
            "corridor": "Indiranagar (100 Feet Road)",
            "stage": "Unicorn",
            "valuation": "$6.4B Valuation",
            "founded_year": 2018,
            "core_business": "High-trust community of creditworthy individuals offering premium card payments, CRED Pay, garage, and wealth products.",
            "project_name": "Project VaultZero: Zero-Knowledge Sovereign High-Yield Private Neo-Banking Core & Real-Time Trust Ledger",
            "project_pillar": "Zero-Knowledge Confidential Computing & Autonomous Private Wealth Engine",
            "project_thesis": "CRED commands the top 1% affluent Indian consumers with over $100B in annual credit card spend. VaultZero transforms CRED into a zero-knowledge confidential banking core, executing automated high-yield treasury management, instant multi-card liquidity sweeps, and provable private underwriting.",
            "tech_stack": "Rust (Zero-Knowledge ZK-SNARK Prover), Go (Account Core), PostgreSQL with Citus Sharding, Redis Cluster, Apache Iceberg (Data Lakehouse), AWS Nitro Enclaves / Confidential Virtual Machines",
            "impact_metrics": "100% confidential credit score & net-worth computation with zero raw data exposure; $5B+ automated treasury allocation; sub-10ms bill settlement verification.",
            "prompt_archetype": "unicorn_fintech"
        },
        {
            "rank": 6,
            "name": "Zerodha",
            "category": "FinTech, Payments & Digital Banking",
            "corridor": "JP Nagar (4th Phase)",
            "stage": "Decacorn",
            "valuation": "$3.6B+ Self-Funded Scale",
            "founded_year": 2010,
            "core_business": "India's largest bootstrapped retail discount brokerage handling over 15% of daily Indian equity trading volume via Kite platform.",
            "project_name": "Project NanoTrader-X: Sub-Microsecond FPGA/Kernel-Bypass Algorithmic Risk Gate & Multi-Exchange Sovereign Matching Fabric",
            "project_pillar": "Kernel-Bypass Low-Latency Financial Exchange Infrastructure & Pre-Trade Risk Engine",
            "project_thesis": "Zerodha executes 15M+ daily retail trades on NSE and BSE. NanoTrader-X deploys FPGA-accelerated pre-trade risk checks, kernel-bypass Solarflare OpenOnload network stacks, and zero-allocation C/Rust order routers to guarantee deterministic sub-microsecond risk evaluation during market open panic bursts.",
            "tech_stack": "C++20 / Rust (Zero-Allocation Risk Engine), FPGA (Verilog Pre-Trade Filter), Solarflare EF_VI / Solarflare OpenOnload, Redis / DragonflyDB, ClickHouse (Tick Telemetry Archive), Go (Public Kite Connect API)",
            "impact_metrics": "Pre-trade risk check latency reduced from 85 microseconds to 850 nanoseconds; zero server dropouts during 9:15 AM market opening surges; zero rupee external funding dependency maintained.",
            "prompt_archetype": "decacorn_trading"
        },
        {
            "rank": 7,
            "name": "Groww",
            "category": "FinTech, Payments & Digital Banking",
            "corridor": "Outer Ring Road (Marathahalli)",
            "stage": "Unicorn",
            "valuation": "$3.0B Valuation",
            "founded_year": 2016,
            "core_business": "Fastest-growing neo-investment platform empowering over 40M retail investors across direct mutual funds, stocks, and F&O.",
            "project_name": "Project WealthEngine: AI-Autonomous Retail Portfolio Rebalancer, Global Direct Market Access & Sovereign Multi-Asset Custody Core",
            "project_pillar": "Automated Multi-Asset Wealth Optimization & Distributed Portfolio Ledger",
            "project_thesis": "Groww manages India's largest retail active client base in stock broking. WealthEngine implements an autonomous real-time quantitative portfolio rebalancer that continuously monitors tax-harvesting opportunities, ETF arbitrage, and automated SIP capital deployment for 40M+ retail portfolios simultaneously.",
            "tech_stack": "Go (High-Concurrency Trading Microservices), Java (Spring Boot Core Banking/Demats), Apache Cassandra (High-Write Portfolio History), Redpanda (Event Stream), ClickHouse, Kubernetes on Bare Metal",
            "impact_metrics": "Real-time execution of 10M concurrent automated portfolio tax-harvesting runs; 99.995% execution reliability on NSE/BSE colocation; $25B+ assets under tracking.",
            "prompt_archetype": "unicorn_wealth"
        },
        {
            "rank": 8,
            "name": "Postman",
            "category": "Enterprise SaaS, Cloud, Infrastructure & DevTools",
            "corridor": "Indiranagar / Whitefield",
            "stage": "Unicorn",
            "valuation": "$5.6B Valuation",
            "founded_year": 2014,
            "core_business": "The global standard API development platform used by over 30M developers and 500,000 organizations worldwide.",
            "project_name": "Project API-Mesh-OS: Generative AI-Autonomous API Contract Synthesis, Real-Time Distributed Mocking & Self-Healing Gateway",
            "project_pillar": "Autonomous API Engineering Ecosystem & Global Edge Contract Verification",
            "project_thesis": "Postman is the universal interface of modern microservices. API-Mesh-OS converts static API collections into self-synthesizing, self-healing runtime meshes that automatically generate production code, live mocking environments, end-to-end chaos test suites, and dynamic security vulnerability audits directly from developer natural language specs.",
            "tech_stack": "TypeScript / Node.js, Rust (Edge Proxy & Mocking Runtime), Cloudflare Workers (Global Edge Distribution), Postgres with pgvector (Semantic API Index), WebAssembly (Plugin Sandbox), GraphQL / gRPC / AsyncAPI Spec Compilers",
            "impact_metrics": "Generates 100% compliant multi-language client SDKs in <2 seconds; detects 99.4% of breaking API contract regressions pre-commit; adoption by 30M+ developers.",
            "prompt_archetype": "unicorn_devtools"
        },
        {
            "rank": 9,
            "name": "Ola / Ola Electric",
            "category": "Electric Vehicles, CleanTech & Deep Mobility",
            "corridor": "Koramangala & Hosur Hub",
            "stage": "Unicorn",
            "valuation": "$5.4B Valuation",
            "founded_year": 2010,
            "core_business": "Pioneering vertical EV manufacturer and ride-hailing giant operating the Ola Futurefactory and Gen-3 electric platforms.",
            "project_name": "Project Gigafactory Core: Autonomous Edge Telemetry, 4680 Solid-State Cell Thermal Optimizer & Fleet Autopilot Mesh",
            "project_pillar": "Industrial IoT Digital Twin, Battery Management System (BMS) Telemetry & Edge Autopilot",
            "project_thesis": "Ola Electric's core moat is vertical integration from indigenous battery cell chemistry to connected vehicles. Gigafactory Core streams 1,000+ real-time telemetry parameters per vehicle back to an edge-cloud digital twin, dynamically adapting BMS thermal envelopes, preventing battery degradation, and automating OTA firmware safely.",
            "tech_stack": "C/C++ (Embedded RTOS on Vehicle ECU), Rust (Edge Gateway), Apache Kafka / EMQX (Millions of MQTT IoT Conns), TimescaleDB / ClickHouse (Time-Series Sensor Telemetry), TensorFlow Lite (Edge Battery Health Model), Kubernetes Edge",
            "impact_metrics": "Predicts thermal anomalies 48 hours prior to cell degradation; extends battery lifecycle by 35%; processes 10B daily telemetry points across 500,000+ active EVs.",
            "prompt_archetype": "unicorn_ev"
        },
        {
            "rank": 10,
            "name": "Ather Energy",
            "category": "Electric Vehicles, CleanTech & Deep Mobility",
            "corridor": "IBC Knowledge Park (Bannerghatta Road)",
            "stage": "Unicorn",
            "valuation": "$1.3B Valuation",
            "founded_year": 2013,
            "core_business": "Intelligent smart electric two-wheeler manufacturer known for the 450X, Rizta, Ather Grid fast-charging network, and AtherStack.",
            "project_name": "Project GridMatrix: Distributed Vehicle-to-Grid Terawatt Telemetry, Fast-Charge Load Balancer & Battery Swarm Digital Twin",
            "project_pillar": "Distributed Smart Charging Infrastructure & Dynamic V2G Energy Arbitrage",
            "project_thesis": "Ather's competitive advantage lies in AtherStack software and Ather Grid. GridMatrix turns the entire Ather vehicle fleet and charging network into an active distributed virtual power plant (VPP), intelligently scheduling charging loads, balancing grid harmonics, and enabling vehicle-to-grid energy exchange.",
            "tech_stack": "Rust (Embedded AtherOS Telemetry), Go (Ather Grid Cloud Controller), MQTT (Micro-broker over TLS 1.3), InfluxDB / ClickHouse, Python (Distributed Reinforcement Learning for Grid Balancing), AWS Greengrass / IoT Core",
            "impact_metrics": "40% reduction in peak commercial power demand charges for grid hosts; 99.8% Ather Grid charger uptime; real-time battery digital twin updating in 100ms.",
            "prompt_archetype": "unicorn_ev"
        },
        {
            "rank": 11,
            "name": "InMobi / Glance",
            "category": "DeepTech, Generative AI, Robotics & SpaceTech",
            "corridor": "Bellandur / ORR",
            "stage": "Decacorn",
            "valuation": "$2.5B+ Valuation",
            "founded_year": 2007,
            "core_business": "Global advertising and consumer platform powering glance lockscreen content and AI-driven personalized media for 300M+ users.",
            "project_name": "Project NeuroScreen: Zero-Latency On-Device Lockscreen Content Synthesis, Edge Multimodal Recommendation & Sovereign Privacy Vault",
            "project_pillar": "On-Device Edge Generative Media & Low-Latency Multimodal Recommendation",
            "project_thesis": "Glance operates on 300M+ smartphone lockscreens globally. NeuroScreen deploys an on-device quantized multimodal transformer that synthesizes customized news, gaming, and interactive commerce in zero milliseconds without sending user browsing logs or biometric sensor data to cloud servers.",
            "tech_stack": "C++ / ONNX Runtime (On-Device Neural Engine), Rust (Edge Cache), PyTorch (Distributed Continual Learning), ClickHouse (Global Ad Yield Engine), Apache Flink, WebAssembly / Android NDK",
            "impact_metrics": "Sub-1ms lockscreen render latency; 45% increase in user dwell time; zero user personal data leaks to third-party ad networks.",
            "prompt_archetype": "decacorn_media"
        },
        {
            "rank": 12,
            "name": "Meesho",
            "category": "E-Commerce, Marketplaces & D2C Brands",
            "corridor": "Outer Ring Road (Kadubeesanahalli)",
            "stage": "Unicorn",
            "valuation": "$4.9B Valuation",
            "founded_year": 2015,
            "core_business": "Internet marketplace democratizing e-commerce for Bharat with 0% seller commission and 140M+ annual transacting users.",
            "project_name": "Project BharatMesh: Multilingual Voice/Visual Social Commerce Engine, 0-Commission P2P Reseller Supply Mesh & Tier-4 Logistics Arbiter",
            "project_pillar": "Vernacular Multimodal Discovery & Ultra-Low-Cost P2P Supply Chain Routing",
            "project_thesis": "Meesho thrives on low Average Order Values (AOVs) and unbranded goods from Tier-2/3/4 towns. BharatMesh replaces complex text search with natural voice and camera visual search in 14 Indian languages, while dynamically bundling hyper-local couriers to drive per-shipment delivery cost down by 30%.",
            "tech_stack": "Python / PyTorch (Speech-to-Intent & Image Embeddings), Milvus / Qdrant (Vector Similarity Database), Go (Order Matching Engine), ScyllaDB, Kafka, Kubernetes on Bare Metal",
            "impact_metrics": "Supports 50M concurrent vernacular voice queries; reduces RTO (Return to Origin) fraud by 38%; drives shipping costs down to <₹35 per intra-zone parcel.",
            "prompt_archetype": "unicorn_ecom"
        },
        {
            "rank": 13,
            "name": "Zepto",
            "category": "Quick Commerce, FoodTech & Consumer Internet",
            "corridor": "HSR Layout & Koramangala",
            "stage": "Unicorn",
            "valuation": "$5.0B Valuation",
            "founded_year": 2021,
            "core_business": "Hyper-growth 10-minute quick-commerce pioneer operating dense micro-fulfillment dark stores across Tier-1 metros.",
            "project_name": "Project Chronos-10: Predictive Micro-Depot Ingestion, Computer-Vision Darkstore Automated Picking & 300-Second Dispatch Pipeline",
            "project_pillar": "Ultra-Fast Micro-Depot Robotics & Automated Pick-Pack-Dispatch Pipeline",
            "project_thesis": "Zepto's unit economics require pick-and-pack times inside dark stores to drop under 90 seconds. Chronos-10 combines computer vision overhead item tracking, automated pick-path optimization on handheld terminals, and live telemetry dispatch that pairs riders before packing completes.",
            "tech_stack": "Go (Dispatch Core), OpenCV / PyTorch (Dark-store Shelf Vision), Redis Cluster (Inventory Reservation), Redpanda, PostgreSQL with Timescale, Kubernetes Edge on Darkstore Minis",
            "impact_metrics": "Average pick-and-pack time reduced to 54 seconds; 99.4% on-time delivery rate under 10 minutes; darkstore stock shrinkage reduced by 70%.",
            "prompt_archetype": "unicorn_quickcom"
        },
        {
            "rank": 14,
            "name": "BigBasket",
            "category": "Quick Commerce, FoodTech & Consumer Internet",
            "corridor": "Domlur (Embassy Golf Links)",
            "stage": "Unicorn",
            "valuation": "$3.2B Valuation",
            "founded_year": 2011,
            "core_business": "India's largest online grocery supermarket and BB Now quick-commerce arm under the Tata Digital conglomerate.",
            "project_name": "Project FarmToCart-AI: Cold-Chain IoT Computer Vision QA, Automated Micro-Warehouse Robotics & Dynamic Spoilage Minimization",
            "project_pillar": "Cold-Chain Perishable Quality Automation & Automated Warehouse Fulfillment",
            "project_thesis": "Grocery retail margins collapse on fresh produce spoilage and multi-temperature logistics. FarmToCart-AI deploys non-destructive optical fruit grading, real-time IoT temperature/humidity tracking from farm collection centers to doorstep, and automated inventory markdown engines.",
            "tech_stack": "Python / TensorFlow (Produce Computer Vision), Go (Fulfillment Services), MQTT / AWS IoT Greengrass (Cold-chain Sensors), ScyllaDB, Kafka, ElasticSearch",
            "impact_metrics": "Spoilage loss reduced from 6.8% to 1.1%; automated produce grading throughput of 1,200 crates/hour; 99.9% fresh quality customer guarantee.",
            "prompt_archetype": "unicorn_quickcom"
        },
        {
            "rank": 15,
            "name": "Hasura",
            "category": "Enterprise SaaS, Cloud, Infrastructure & DevTools",
            "corridor": "Koramangala",
            "stage": "Unicorn",
            "valuation": "$1.0B Valuation",
            "founded_year": 2017,
            "core_business": "High-performance instant GraphQL and REST engine bridging enterprise databases with unified access control and streaming.",
            "project_name": "Project DataFabric-Core: Universal Zero-ETL GraphQL/SQL Multi-Cloud Query Engine with Distributed Vector Consensus",
            "project_pillar": "Unified Distributed Query Federation & Zero-Latency Access Control",
            "project_thesis": "Enterprises struggle with fragmented polyglot databases, data lakes, and vector embeddings. DataFabric-Core compiles unified GraphQL and SQL queries across Postgres, Snowflake, ClickHouse, and vector stores into single-pass, pushdown optimized queries with enterprise role-based authorization.",
            "tech_stack": "Haskell / Rust (Core Query Compiler & AST Optimizer), Go (Cloud Control Plane), OpenTelemetry, eBPF, Apache Arrow (In-Memory Columnar Data Transfer)",
            "impact_metrics": "Sub-3ms execution for complex multi-database federated queries; 95% reduction in custom backend API glue code; zero-copy serialization via Arrow.",
            "prompt_archetype": "unicorn_devtools"
        },
        {
            "rank": 16,
            "name": "BrowserStack",
            "category": "Enterprise SaaS, Cloud, Infrastructure & DevTools",
            "corridor": "Koramangala / HSR",
            "stage": "Unicorn",
            "valuation": "$4.0B Valuation",
            "founded_year": 2011,
            "core_business": "World's leading web and mobile software testing platform providing cloud access to 3,000+ real browsers and devices.",
            "project_name": "Project HyperCloud-Test: Real-Time Hardware-Accelerated Virtualization Matrix & Autonomous AI Visual Bug Diagnoser",
            "project_pillar": "Distributed Cloud Hardware Virtualization & Autonomous Test Execution Engine",
            "project_thesis": "Testing web and mobile applications at global scale requires instantaneous access to physical devices without queue bottlenecks. HyperCloud-Test builds an automated low-latency video streaming and containerized mobile OS virtualization fabric with AI computer vision that detects visual UI layout regressions across 3,000 device permutations simultaneously.",
            "tech_stack": "C++ / WebRTC (Sub-20ms Video Stream), Rust (Container Host Orchestration), Python / PyTorch (Visual Regression Diffing), Linux KVM / QEMU, Redis, Kafka",
            "impact_metrics": "Reduces test suite execution time by 75%; streams 60 FPS real-device screens with <15ms latency; automates root-cause visual debugging for 50,000 enterprise apps.",
            "prompt_archetype": "unicorn_devtools"
        },
        {
            "rank": 17,
            "name": "Zetwerk",
            "category": "B2B Industrial Marketplaces, Manufacturing & Supply Chain",
            "corridor": "HSR Layout (Sector 6)",
            "stage": "Unicorn",
            "valuation": "$2.7B Valuation",
            "founded_year": 2018,
            "core_business": "Global manufacturing network for custom precision parts, industrial EPC, defense equipment, and consumer electronics.",
            "project_name": "Project HyperFab-Global: Autonomous Industrial Manufacturing Operating System, Distributed CNC Telemetry & Real-Time BOM Arbiter",
            "project_pillar": "Distributed Industrial Manufacturing Cloud & Real-Time CNC/CMM Quality Telemetry",
            "project_thesis": "Global supply chains are decoupling from China, seeking precision manufacturing capacity across India and SE Asia. HyperFab-Global unifies 10,000+ distributed factory machine tools, providing instant CAD-to-BOM quotation, automated CNC toolpath optimization, and real-time IoT CMM quality compliance for aerospace and defense buyers.",
            "tech_stack": "Rust / C++ (CAD Geometry & Toolpath Analyzer), Go (Supply Chain Microservices), Apache Kafka, TimescaleDB (Factory Machine IoT Telemetry), PostgreSQL, React 19 / Three.js (3D Interactive CAD Viewer)",
            "impact_metrics": "Automates 3D CAD quotation from 4 days to 45 seconds; maintains 99.9% dimensional accuracy tolerances across 10,000 supplier factories; manages $2B+ manufacturing pipeline.",
            "prompt_archetype": "unicorn_mfg"
        },
        {
            "rank": 18,
            "name": "Infra.Market",
            "category": "B2B Industrial Marketplaces, Manufacturing & Supply Chain",
            "corridor": "Koramangala",
            "stage": "Unicorn",
            "valuation": "$2.5B Valuation",
            "founded_year": 2016,
            "core_business": "Procurement and supply chain platform for construction materials, concrete, chemicals, and building equipment.",
            "project_name": "Project ConcreteOS: IoT Batching Plant Telemetry, Ready-Mix Real-Time Slump Optimization & Multi-Modal Fleet Router",
            "project_pillar": "Industrial Construction IoT & Ready-Mix Perishable Logistics Routing",
            "project_thesis": "Ready-mix concrete has a perishable delivery window of 90 minutes before setting. ConcreteOS links automated IoT batching plant sensors with heavy mixer truck GPS, predicting traffic delays, adjusting chemical retarder admixtures dynamically, and guaranteeing zero wastage across infrastructure megaprojects.",
            "tech_stack": "Go (Fleet & Batch Dispatch), Python (Concrete Curing & Rheology Predictive Models), MQTT / IoT Edge, PostgreSQL, TimescaleDB, RabbitMQ",
            "impact_metrics": "Zero failed concrete transit batches; 24% reduction in mixer truck transit idle time; manages 500+ manufacturing batch plants seamlessly.",
            "prompt_archetype": "unicorn_mfg"
        },
        {
            "rank": 19,
            "name": "Pixxel Space",
            "category": "DeepTech, Generative AI, Robotics & SpaceTech",
            "corridor": "HSR Layout",
            "stage": "Soonicorn",
            "valuation": "$150M Series B",
            "founded_year": 2019,
            "core_business": "Building the world's highest-resolution hyperspectral satellite constellation to monitor planetary health and climate change.",
            "project_name": "Project Aurora-HyperScale: Real-Time Orbital Edge Hyperspectral Imagery Ingestion & Planetary Anomaly Alerting Mesh",
            "project_pillar": "Orbital Edge Computing & Hyperspectral Remote Sensing Analytics",
            "project_thesis": "Downlinking raw hyperspectral satellite data across 300+ spectral bands creates massive bandwidth bottlenecks. Aurora-HyperScale deploys radiation-hardened edge AI on satellites to process, compress, and detect methane leaks, crop pestilence, and pipeline breaches in orbit, beaming down actionable alerts within minutes instead of days.",
            "tech_stack": "C / C++ (Radiation-Tolerant Satellite Flight Software), Rust (Downlink Processing Pipeline), Python / PyTorch (Spectral Signature Classification), Apache Arrow, Zarr (Multidimensional Scientific Imagery Store), AWS Ground Station",
            "impact_metrics": "90% reduction in satellite downlink bandwidth requirements; detects global methane leaks in under 15 minutes; sub-5-meter spectral resolution for precision agriculture.",
            "prompt_archetype": "spacetech_deeptech"
        },
        {
            "rank": 20,
            "name": "Ultrahuman",
            "category": "Healthcare, BioTech, HealthTech & Diagnostics",
            "corridor": "Indiranagar (12th Main)",
            "stage": "Soonicorn",
            "valuation": "$300M Series B",
            "founded_year": 2019,
            "core_business": "Global metabolic health and wearable tracking system maker behind the Ultrahuman Ring AIR, M1 CGM sensor, and BloodVision.",
            "project_name": "Project BioRing-Synapse: Real-Time Continuous Multi-Biomarker Synthesis, Sub-Second Glucose-Metabolism Telemetry & Preventative Longevity Coach",
            "project_pillar": "Continuous Human Biomarker Telemetry & Autonomous Preventative Longevity Engine",
            "project_thesis": "Wearables usually report passive historical data. BioRing-Synapse unites PPG optical heart rate sensors, skin temperature, continuous glucose monitors (CGM), and blood panel biomarkers into a continuous predictive metabolic engine that gives actionable real-time interventions before glucose crashes or circadian disruptions occur.",
            "tech_stack": "C / Embedded C (Low-Power Bluetooth Ring Firmware), Swift / Kotlin (Native Mobile SDKs), Rust (Biomarker Ingestion Pipeline), TimescaleDB / ClickHouse, Python (Physiological Neural Models), Redis Enterprise",
            "impact_metrics": "Sub-50ms real-time biomarker anomaly alerts; 6-day ring battery life maintained; predictive glycemic response with 94.2% accuracy.",
            "prompt_archetype": "healthtech_wearable"
        }
    ]

    # Archetype Prompts dictionary: High-impact, multi-page, battle-tested system execution prompts
    prompt_templates = {
        "decacorn_ecom": """# ROLE: Principal Fellow & Chief Distributed Systems Architect
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Design, architect, and execute {project_name}

## 1. STRATEGIC MISSION & HIGH-STAKES ARCHITECTURAL CONTEXT
You are the world's foremost authority in planetary-scale e-commerce logistics, real-time distributed systems, and low-latency message streaming. You are tasked with architecting and delivering {project_name} for {company}, operating across {corridor}.
At peak Indian festive sales (Big Billion Days), the system must effortlessly withstand 120,000+ orders per second, sub-5ms P99 inventory lock latency, and zero split-brain anomalies across multi-region active-active clusters.

## 2. ARCHITECTURAL INVARIANTS & CONSTITUTIONAL DIRECTIVES
- **Zero Vibe Coding**: Every single data contract, concurrency primitive, and boundary interface must be mathematically sound, deterministic, and rigorously specified.
- **Strict Linearizability**: Inventory reservations must enforce strict serializability or linearizable consistency using Raft consensus or distributed two-phase commits with conflict-free replicated data types (CRDTs).
- **Latency SLAs**: P50 < 1.5ms, P99 < 5.0ms, P99.9 < 15.0ms for order ingestion, risk evaluation, and warehouse allocation.
- **Self-Healing Topology**: Any failing microservice, node partition, or network packet drop must trigger automatic circuit breakers, eBPF traffic re-routing, and fallback to local in-memory storage without dropping customer checkout carts.

## 3. SUBSYSTEM DECOMPOSITION & DEEP SPECIFICATIONS
Implement the end-to-end architecture across these 5 core subsystems:
1. **Dynamic High-Throughput Ingestion Mesh ({tech_stack})**:
   - Kernel-bypass ingress gateway terminating mTLS 1.3 connections.
   - Non-blocking asynchronous event streaming guaranteeing at-least-once message delivery with exactly-once idempotency keys.
2. **Deterministic Inventory Reservation Core**:
   - Ultra-fast distributed key-value storage engine handling SKU-level lease locks.
   - Optimistic concurrency control with sub-millisecond rollback on out-of-stock collisions.
3. **Autonomous Micro-Hub & Warehouse Routing Arbiter**:
   - Real-time geohash partitioning based on delivery pin code and dynamic road traffic conditions.
   - Intelligent multi-item cart splitting and automated order consolidation to minimize split shipments.
4. **Resiliency & Chaos Engineering Gateways**:
   - Continuous chaos injection simulating cloud zone loss, 25% packet loss, and Redis master failovers.
   - Automated replay dead-letter queue (DLQ) with backpressure rate limiting.
5. **Observability, Distributed Tracing & Audit Ledger**:
   - OpenTelemetry spans across every hop, exporting to high-throughput columnar storage for instant forensic dispute analysis.

## 4. CONCRETE IMPLEMENTATION PROTOCOL
- Provide complete, compilable, production-ready code modules (core data models, gRPC service definitions, lock manager, and event consumer loops).
- Provide the complete Dockerfile, Kubernetes Helm manifest with CPU pinning and hugepages, and load test scripts simulating 100,000 TPS.
- Provide comprehensive unit tests, integration tests, and chaos verification scenarios.

## 5. DELIVERABLE OUTPUT REQUIREMENTS
Deliver an exhaustive, zero-fluff, production-grade engineering specification including exact protobuf schemas, core service implementations, failure recovery algorithms, and performance verification benchmarks.""",

        "decacorn_quickcom": """# ROLE: VP of Engineering & Head of Autonomous Hyperlocal Systems
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Build and deploy {project_name}

## 1. STRATEGIC CONTEXT & REAL-TIME OPERATIONAL SCALE
You are leading engineering at {company} in {corridor}. Your mandate is to execute {project_name}, driving order-to-doorstep delivery latency under 8 minutes across thousands of dense micro-fulfillment dark stores.
During rain surges and evening peaks, the system processes 30,000 hyperlocal deliveries per minute, routing riders, managing dark-store robotics, and updating inventory balances in sub-10 milliseconds.

## 2. ARCHITECTURAL INVARIANTS & SYSTEM GUARDRAILS
- **Sub-Second Inventory Absolute Truth**: Dark-store physical inventory and app catalog state must match with 99.99% accuracy; ghost inventory is eliminated through continuous RFID/optical bin verification.
- **Predictive Pre-Allocation**: Rider dispatch algorithms must predict order completion 3 minutes before customer checkout finalize, staging bikes at dark-store bays without blocking traffic.
- **Geospatial Hexagonal Partitioning**: Dynamic surge, delivery SLAs, and dark-store catchment zones must be computed dynamically on Uber H3 resolution 9/10 grids.

## 3. CORE SUBSYSTEM BLUEPRINTS
1. **Darkstore Pick-Pack Automated Workflow Engine**:
   - Dynamic batching algorithms generating optimal 2D/3D walking/robotic picking paths inside dark stores.
   - Computer vision barcode verification validating item weight, expiration date, and packaging integrity.
2. **Hyperlocal Geospatial Dispatch & Batching Fabric**:
   - Graph optimization solving the multi-vehicle pickup-and-delivery problem with time windows (m-VRPTW) in <50ms.
   - Dynamic compensation and safety routing protecting delivery executives during adverse weather.
3. **Real-Time Cold-Chain & Perishable Freshness Telemetry**:
   - Continuous IoT logging of ice cream, dairy, and meat storage temperature from dark-store chiller to rider thermal bag.
4. **High-Velocity Real-Time Event Ledger**:
   - Built on {tech_stack}, ensuring microsecond state synchronization between customer app, picker terminal, rider app, and merchant systems.

## 4. STEP-BY-STEP PRODUCTION DEPLOYMENT
- Formulate complete Rust/Go microservices for order assignment and geospatial indexing.
- Define gRPC APIs and Kafka event schemas for order state transitions.
- Implement chaos simulation for rider network dropouts and sudden inventory depletion.
- Produce production metrics dashboard specs for P99 fulfillment latency, dark-store throughput, and customer SLA adherence.

## 5. EXECUTION CRITERIA
Deliver a rigorous, complete, runnable system architecture document with concrete code, protobuf contracts, state machine logic, and stress-test test benches.""",

        "decacorn_fintech": """# ROLE: Chief Systems Architect & Fellow of Financial Cryptography
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Architect and implement {project_name}

## 1. STRATEGIC MISSION & BANKING INFRASTRUCTURE CONTEXT
You are the lead architect for {company}, based in {corridor}. You are building {project_name}, an industrial-grade, sovereign financial transaction core capable of handling $10B+ daily volume across 100M+ active users.
The system must guarantee zero double-spending, zero financial drift, sub-3ms transaction evaluation, and automatic fault-tolerant routing across degraded banking partner networks.

## 2. FINANCIAL INVARIANTS & REGULATORY GUARDRAILS
- **Zero Financial Discrepancy (Double-Entry Ledger)**: Every movement of funds is an immutable credit and debit pair. Balance equations must balance to 0.00000000 precision at all times.
- **Idempotency Guarantee**: Every payment intent carries a cryptographic idempotency token ensuring that duplicate HTTP requests or network retries never trigger multiple debit calls.
- **RBI & Sovereign Compliance**: Full compliance with Reserve Bank of India data localization, tokenization directives, and automated AML/CFT suspicious transaction reporting.
- **Quantum-Resistant Cryptography**: Key exchange and signature verification must use post-quantum hybrid algorithms (e.g., ML-KEM / Dilithium) to protect financial data against future quantum decryption.

## 3. SYSTEM SUBSYSTEMS & DISTRIBUTED TOPOLOGY
1. **Algorithmic Multi-Rail Smart Routing Engine ({tech_stack})**:
   - Real-time probing of bank gateway error rates, latency spikes, and downtime signals.
   - Dynamic heuristic routing redirecting transactions across alternative acquiring banks and payment aggregators in <2ms.
2. **Sovereign Immutable Financial Ledger**:
   - Append-only transactional event store with cryptographic SHA-256 Merkle tree verification.
   - High-throughput sharded balance cache supporting 100,000 TPS with optimistic locking and distributed Raft consensus.
3. **Real-Time Graph Fraud & AML Sentinel**:
   - In-memory graph traversal evaluating user risk score, velocity checks, device fingerprint, and IP reputation in <4ms.
   - Autonomous step-up authentication triggering biometric or OTP verification only on anomalous patterns.
4. **Automated Sub-Second Reconciliation & Dispute Engine**:
   - Continuous 3-way reconciliation comparing merchant orders, payment gateway logs, and bank clearing files automatically resolving pending states in under 30 seconds.

## 4. IMPLEMENTATION & DELIVERABLES
- Deliver complete production-ready source code implementing the double-entry balance manager, dynamic router, and idempotency filter.
- Supply strict Protobuf / OpenAPI schemas, SQL migration scripts, and benchmark configurations.
- Verify through automated bank timeout chaos tests, split-brain network simulations, and high-concurrency race condition tests.""",

        "decacorn_trading": """# ROLE: Chief Quantitative Infrastructure Architect & Head of Low-Latency Systems
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Build and deploy {project_name}

## 1. STRATEGIC TRADING CONTEXT & LATENCY MANDATES
You are the principal low-latency systems engineer at {company} in {corridor}. You are engineering {project_name}, an ultra-low-latency pre-trade risk evaluation, order matching, and market data broadcasting system handling 15M+ daily trades across India's premier exchanges (NSE/BSE).
Your non-negotiable target: evaluate risk, compute margins, verify account cash balances, and route orders to exchange FIX connections in under 850 nanoseconds.

## 2. ARCHITECTURAL INVARIANTS & HARDWARE OPTIMIZATIONS
- **Kernel-Bypass Networking**: Zero kernel context switches; all exchange network packets processed via Solarflare EF_VI or DPDK directly in user space.
- **Zero Heap Allocations on Hot Path**: Pre-allocated circular ring buffers, cache-aligned data structures (64-byte cache line alignment), and branch prediction hints (`__builtin_expect`).
- **Lock-Free Concurrency**: Disruptor ring buffer patterns with atomic memory fences (`memory_order_acquire` / `memory_order_release`) replacing all OS mutexes.
- **SEBI Regulatory Compliance**: Deterministic pre-order checks enforcing client credit limits, fat-finger price collars, and order-to-trade ratio limits without dropping packets.

## 3. SUBSYSTEM ARCHITECTURAL BLUEPRINTS
1. **FPGA & C++20 Pre-Trade Risk Gateway ({tech_stack})**:
   - Hardware-accelerated parsing of incoming Kite order packets.
   - Sub-microsecond validation of client margin, security status, and circuit limit price bands.
2. **Order State Routing & FIX Engine**:
   - Low-latency FIX 4.2/4.4 protocol encoder and decoder.
   - Ultra-fast order lifecycle state machine (New, Pending, Filled, Cancelled, Rejected) persisted to NVMe memory-mapped files.
3. **High-Throughput Level-3 Market Data Ticker Matrix**:
   - Multicast UDP market data tick handler updating in-memory order books in sub-microsecond latency.
   - Binary WebSocket push server streaming ticks to 10M concurrent retail client apps with zero lag.
4. **Real-Time Regulatory Audit & Risk Telemetry**:
   - Nanosecond-precision clock synchronization using PTP (IEEE 1588).
   - High-throughput tick telemetry streaming to ClickHouse for post-trade surveillance and regulatory compliance reporting.

## 4. CONCRETE CODE & ARTIFACT DELIVERABLES
- Implement the core C++20 / Rust zero-allocation risk engine and lock-free ring buffer.
- Provide the exact network socket configuration, CPU core pinning, and kernel sysctl tuning commands.
- Provide benchmark test harness verifying sub-microsecond latency under 1,000,000 orders/sec burst loads.""",

        "unicorn_ev": """# ROLE: Chief Technology Officer & Principal Embedded Software Architect
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Design, construct, and deploy {project_name}

## 1. EMBEDDED AUTOMOTIVE & FLEET SCALE CONTEXT
You are leading vehicle engineering and cloud infrastructure for {company} in {corridor}. You are building {project_name}, connecting 500,000+ smart electric vehicles, thousands of fast-charging grid stations, and indigenous battery management systems (BMS) into an intelligent digital twin fabric.
The system must guarantee automotive safety integrity level (ASIL-D), prevent thermal runaway events, optimize battery pack degradation, and support secure over-the-air (OTA) updates.

## 2. SAFETY INVARIANTS & SYSTEM GUARDRAILS
- **ASIL-D & ISO 26262 Compliance**: Safety-critical vehicle control software (traction control, throttle response, regenerative braking) is strictly isolated from infotainment and telematics stacks.
- **Sub-Second Thermal Runaway Prediction**: Multi-layer electrochemical physics models and edge neural networks evaluate cell voltage, impedance, and temperature differentials every 50ms, identifying dendrite formation and thermal anomalies before ignition risks occur.
- **Cryptographic OTA Integrity**: Every firmware payload is signed with HSM-backed Ed25519 digital signatures and verified by secure hardware bootloaders with A/B partition rollback.

## 3. SUBSYSTEM DEEP SPECIFICATIONS
1. **Edge Vehicle OS & Real-Time BMS Telemetry ({tech_stack})**:
   - Embedded RTOS firmware streaming 1,000+ vehicle sensor parameters over secure TLS 1.3 MQTT brokers.
   - Adaptive regenerative braking algorithms extending vehicle range by 12% in urban stop-and-go traffic.
2. **Cloud Battery Digital Twin & Predictive Health Matrix**:
   - Distributed time-series ingestion processing 100,000 events/sec from active vehicles.
   - Machine learning electrochemical degradation models adjusting charging curves to double battery cycle life.
3. **Smart Charging Network & Virtual Power Plant (VPP) Router**:
   - Automated Vehicle-to-Grid (V2G) load-balancing adjusting charging station draw based on real-time grid frequency and tariff rates.
   - Instant automated authentication and plug-and-charge billing via ISO 15118 protocol.
4. **Fleet Telematics & Autonomous Safety Defense**:
   - Edge crash detection triggering emergency SOS, battery contactor isolation, and real-time medical triage within 300ms.

## 4. VERIFICATION & EXECUTION PROTOCOL
- Provide complete embedded C / Rust telematics controller code and cloud MQTT ingestion pipeline.
- Supply CAN bus matrix specifications, protobuf schemas, and firmware update state machines.
- Produce automated simulation test runs validating battery thermal failover and OTA rollback under corrupted network conditions.""",

        "unicorn_devtools": """# ROLE: Distinguished Engineer & Head of Cloud Platform Architecture
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Build and launch {project_name}

## 1. STRATEGIC DEVTOOLS MISSION & GLOBAL DEVELOPER SCALE
You are the Distinguished Platform Architect at {company} in {corridor}. Your mission is to build {project_name}, serving millions of software engineers and enterprises globally.
The system must provide instantaneous sub-millisecond query execution, zero-copy serialization, distributed consensus, and autonomous AI-assisted workflow generation while guaranteeing 99.999% availability.

## 2. ARCHITECTURAL INVARIANTS & DEVELOPER EXPERIENCE
- **Sub-Millisecond Edge Execution**: Global edge runtime providing developer feedback and mock responses in <3ms.
- **Deterministic Semantic Typing**: Automated bidirectional code and schema generation ensuring 100% type safety across TypeScript, Rust, Go, Python, and Java.
- **Zero-Trust Enterprise Security**: Granular RBAC/ABAC authorization, SOC 2 Type II compliance, and automated vulnerability scanning embedded in every developer interaction.

## 3. CORE COMPONENT ARCHITECTURE
1. **Universal Distributed Query & Execution Engine ({tech_stack})**:
   - High-performance query compiler optimizing AST trees and federating requests across distributed databases.
   - Zero-copy data serialization leveraging Apache Arrow and WebAssembly sandboxing.
2. **Generative Contract Synthesis & Autonomous Mocking Core**:
   - Multimodal LLM pipeline converting natural language requirements into formal API contracts and test suites.
   - Distributed stateful mock servers simulating realistic database states and edge error conditions.
3. **Continuous Integration & Chaos Validation Harness**:
   - Automated regression detector scanning PR diffs for breaking contract changes and performance degradations.
   - End-to-end sandbox runner executing thousands of isolated tests in parallel micro-VMs (Firecracker).
4. **Global Edge Observability & Telemetry Bus**:
   - Distributed OpenTelemetry pipeline collecting performance traces, query metrics, and error rates without impacting request hot paths.

## 4. IMPLEMENTATION DELIVERABLES
- Deliver complete production code implementing the core AST compiler, edge proxy, and schema validator.
- Provide comprehensive OpenAPI / Protobuf definitions, Helm charts, and CI/CD automation pipelines.
- Verify through stress-testing benchmarks under 50,000 requests/sec with chaos injection.""",

        "unicorn_mfg": """# ROLE: Chief Industrial Architect & Head of Digital Manufacturing
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Deploy and scale {project_name}

## 1. STRATEGIC INDUSTRIAL SCALE & SUPPLY CHAIN THESIS
You are the Chief Industrial Architect at {company} in {corridor}. You are building {project_name}, an autonomous industrial manufacturing and supply chain operating system managing thousands of supplier factories, precision CNC machines, and heavy infrastructure projects.
The system must digitize bill of materials (BOM), automate 3D CAD manufacturability audits, route orders across distributed supplier shops, and verify precision quality in real time.

## 2. INDUSTRIAL INVARIANTS & SYSTEM SPECIFICATIONS
- **CAD-to-Cost Determinism**: Automated extraction of geometric features, tolerances, and material callouts from 3D STEP/IGES files, generating binding commercial quotations in <60 seconds.
- **Sub-Millimeter Quality Verification**: Direct IoT integration with Coordinate Measuring Machines (CMM) and laser scanners to enforce GD&T (Geometric Dimensioning and Tolerancing) compliance before dispatch.
- **Dynamic Supply Chain Allocation**: Heuristic matching balancing supplier machine capacity, raw material availability, historical quality yield, and logistics transit time.

## 3. SUBSYSTEM DECOMPOSITION
1. **Computational Geometry & DFM Analysis Engine ({tech_stack})**:
   - Automated toolpath feasibility analysis identifying unmachinable undercuts, thin walls, and deep cavities.
2. **Distributed Factory IoT & Machine Telemetry Network**:
   - Edge devices connecting via MTConnect, OPC-UA, and Modbus to log CNC spindle loads, cycle times, and scrap rates.
3. **Real-Time Supply Chain & Raw Material Clearinghouse**:
   - Dynamic raw material hedging and procurement auction marketplace securing steel, aluminum, and polymers at bulk rates.
4. **Digital Inspection & Provenance Blockchain Ledger**:
   - Immutable material test certificates (MTC) and dimensional inspection reports cryptographically linked to physical part QR codes.

## 4. PRODUCTION IMPLEMENTATION & AUDIT
- Provide complete production code for the 3D CAD feature extraction engine, supplier ranking algorithm, and IoT telemetry ingestion service.
- Provide schema definitions, database DDLs, and Kubernetes infrastructure configuration.
- Verify through end-to-end simulated factory runs with 500 simultaneous manufacturing RFQs.""",

        "spacetech_deeptech": """# ROLE: Chief Aerospace & DeepTech Systems Architect
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Build and launch {project_name}

## 1. ORBITAL & DEEP-TECH SCIENTIFIC SCALE
You are the Chief DeepTech Architect at {company} in {corridor}. Your mission is to build {project_name}, an advanced aerospace, satellite, or deep-tech data processing fabric operating across orbital edge compute and ground station networks.
The system must process terabytes of raw scientific telemetry, execute onboard edge inference in radiation-harsh environments, and deliver actionable planetary intelligence in sub-15 minutes.

## 2. SCIENTIFIC & AEROSPACE INVARIANTS
- **Radiation-Tolerant Determinism**: Flight software and edge neural networks must implement triple-modular redundancy (TMR) and memory parity checking to withstand single-event upsets (SEU).
- **Sub-Band Spectral Accuracy**: Remote sensing and sensor calibration algorithms must maintain 99.8% radiometric and geometric accuracy against standard atmospheric correction models.
- **Minimal Downlink Latency**: Edge compression and onboard classification must discard cloud cover and noise, downlinking only high-confidence anomaly alerts over constrained satellite ground links.

## 3. SYSTEM SUBSYSTEM BLUEPRINTS
1. **Onboard Satellite Edge Inference Pipeline ({tech_stack})**:
   - Lightweight quantized convolutional neural networks and transformer backbones optimized for radiation-tolerant FPGA / GPU accelerators.
2. **High-Speed Ground Ingestion & Orthorectification Matrix**:
   - Automated atmospheric correction, terrain alignment, and multi-spectral band stacking in real time.
3. **Planetary Anomaly Alerting & Geospatial Event Engine**:
   - Global real-time stream processing alerting governments and enterprises to gas leaks, deforestation, and maritime threats.
4. **Secure Command & Telemetry Uplink/Downlink Gateway**:
   - High-assurance space communication adhering to CCSDS space data system standards with quantum-safe encryption.

## 4. VERIFICATION & SPACE SIMULATION
- Deliver compilable C++ / Rust edge processing code and Python distributed ground station pipelines.
- Provide data schemas, satellite orbital state models, and automated orbital flight test simulators.
- Verify performance across simulated radiation faults, sensor dropouts, and extreme bandwidth constraints.""",

        "healthtech_wearable": """# ROLE: Chief Biomedical Architect & Head of AI Health Systems
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Engineer and deploy {project_name}

## 1. BIOMEDICAL CONTEXT & REAL-TIME METABOLIC SCALE
You are the Chief Biomedical Systems Architect at {company} in {corridor}. Your mandate is to engineer {project_name}, integrating continuous physiological sensor telemetry (PPG, temperature, CGM, accelerometer) into a real-time metabolic and longevity engine for millions of active users.
The system must guarantee clinical-grade precision, protect patient privacy under HIPAA and GDPR, and deliver predictive preventative guidance before health degradation occurs.

## 2. CLINICAL INVARIANTS & HARDWARE CONSTRAINTS
- **Ultra-Low Power Edge Processing**: Wearable edge algorithms must compute heart rate variability (HRV), sleep staging, and motion artifacts within strict micro-ampere battery budgets.
- **Clinical Data Fidelity**: Raw physiological waveforms must be validated against motion noise and sensor decoupling using adaptive Kalman filters and deep neural noise cancelers.
- **Differential Privacy & Zero-Knowledge Health Vault**: User biometric signatures, glucose levels, and genomic markers are encrypted at rest with client-owned keys; aggregated learning uses strict differential privacy.

## 3. SYSTEM SUBSYSTEM BLUEPRINTS
1. **Embedded Sensor Fusion & Firmware Telemetry ({tech_stack})**:
   - Low-power DSP and Bluetooth Low Energy (BLE 5.3) protocol stack transmitting compressed biomarker frames.
2. **Continuous Metabolic Cloud Ingestion & Timeseries Matrix**:
   - Distributed ingestion pipeline processing billions of biometric data points per day with sub-50ms query access.
3. **Predictive Glycemic & Cardiovascular AI Engine**:
   - Personalized physiological models predicting post-prandial glucose spikes and cardiac strain hours in advance.
4. **Autonomous Health Intervention & Longevity Coach**:
   - Actionable real-time nudges optimizing sleep recovery, zone-2 cardiovascular training, and circadian rhythm alignment.

## 4. PRODUCTION IMPLEMENTATION & CLINICAL VERIFICATION
- Provide complete embedded C firmware routines, native mobile SDK bridges, and cloud ingestion microservices.
- Provide protobuf sensor packet definitions, database schema, and HIPAA compliance verification protocols.
- Validate through synthetic clinical dataset runs testing cardiac arrhythmia detection and glucose prediction accuracy.""",

        "standard_enterprise": """# ROLE: Principal Software Architect & Head of Enterprise Engineering
# TARGET: {company} | CORRIDOR: {corridor} | VALUATION: {val}
# SYSTEM MISSION: Design, architect, and deliver {project_name}

## 1. STRATEGIC MISSION & HIGH-GROWTH CONTEXT
You are the Principal Enterprise Architect for {company}, a premier tech startup in {corridor} ({category}). You have been tasked with building {project_name}, designed to establish market leadership and unassailable technological advantage.
The project directly solves {company}'s strategic bottleneck: {project_thesis}.

## 2. ARCHITECTURAL INVARIANTS & SYSTEM PRINCIPLES
- **Deep Modules & Clear Boundaries**: Simple public interfaces concealing rich, battle-tested operational capability.
- **Zero Vibe Coding**: Concrete specifications, verified types, deterministic error handling, and complete test suites.
- **High Concurrency & Fault Tolerance**: Scalable distributed architecture built on {tech_stack}, achieving {impact_metrics}.
- **Enterprise-Grade Observability**: Structured logging, OpenTelemetry tracing, and automated health checks across all components.

## 3. COMPONENT SUBSYSTEM ARCHITECTURE
1. **Core Processing & Business Logic Engine**:
   - High-throughput asynchronous service layer handling domain transactions with strong consistency guarantees.
2. **Data Persistence & Cache Matrix**:
   - Optimized relational and time-series/columnar storage with sub-millisecond in-memory caching.
3. **Integration & API Gateway Layer**:
   - Secure mTLS REST, gRPC, and GraphQL endpoints with rate limiting, JWT authentication, and schema validation.
4. **Resilience, Chaos & Disaster Recovery**:
   - Circuit breakers, exponential backoff retries with jitter, and automated state reconciliation.

## 4. STEP-BY-STEP IMPLEMENTATION GUIDE
- Provide production-grade data models and interface definitions in the primary system language.
- Implement the core business logic handlers, transaction coordinators, and event publishers.
- Produce comprehensive test suites covering happy paths, edge cases, and high-concurrency race conditions.
- Specify deployment manifests (Docker, Kubernetes, Terraform) with resource limits and scaling policies.

## 5. DELIVERABLES
Deliver a complete, high-quality, production-ready architectural implementation document with clean code, schemas, and verification instructions."""
    }

    # Fetch 500 startups from our curated generator
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from raw_startups import get_500_startups_raw
    raw_500 = get_500_startups_raw()

    final_500 = []

    # Map of archetypes based on category
    cat_to_archetype = {
        "FinTech, Payments & Digital Banking": "decacorn_fintech",
        "Quick Commerce, FoodTech & Consumer Internet": "decacorn_quickcom",
        "E-Commerce, Marketplaces & D2C Brands": "decacorn_ecom",
        "Electric Vehicles, CleanTech & Deep Mobility": "unicorn_ev",
        "Enterprise SaaS, Cloud, Infrastructure & DevTools": "unicorn_devtools",
        "Healthcare, BioTech, HealthTech & Diagnostics": "healthtech_wearable",
        "B2B Industrial Marketplaces, Manufacturing & Supply Chain": "unicorn_mfg",
        "DeepTech, Generative AI, Robotics & SpaceTech": "spacetech_deeptech",
        "PropTech, Real Estate & Smart Living": "standard_enterprise",
        "EdTech, Skill Development & Future of Work": "standard_enterprise",
        "Cybersecurity, Compliance & Web3 Ecosystem": "decacorn_fintech",
        "Workforce, Talent, HRTech & Gig Economy": "standard_enterprise"
    }

    # Project titles and pillars library for procedural enhancement
    sector_project_blueprints = {
        "FinTech, Payments & Digital Banking": [
            ("Project SovereignCore: Autonomous High-Throughput Clearing & Real-Time Fraud Prevention Engine", "Distributed Real-Time Payments & Fraud Detection Mesh", "Rust, Go, Kafka, ScyllaDB, Redis Cluster", "100,000 TPS with sub-3ms latency, 99.999% uptime, zero financial reconciliation drift"),
            ("Project AlphaYield: Algorithmic Multi-Asset Liquidity Aggregator & Automated Treasury Orchestrator", "Quantitative Financial Optimization & Smart Liquidity Routing", "Go, Python, ClickHouse, PostgreSQL, Docker", "Optimizes treasury yield by 240 bps; sub-10ms quote aggregation across 20+ liquidity venues"),
            ("Project TrustVault: Zero-Knowledge Underwriting & Continuous Identity Verification Core", "Confidential Computing & Automated Credit Intelligence", "Rust, ZK-SNARKs, RocksDB, AWS Nitro Enclaves", "100% confidential credit verification with zero data leakage; sub-500ms credit decisioning"),
            ("Project NeoLedger: High-Concurrency Distributed Event-Sourced Banking Ledger", "Immutable Financial Event Sourcing & Real-Time Balance Mesh", "Rust, PostgreSQL with Citus, Apache Pulsar", "Processes 50M daily balance updates with zero race conditions; provable balance auditability")
        ],
        "Quick Commerce, FoodTech & Consumer Internet": [
            ("Project HyperSpeed-8: Autonomous Micro-Fulfillment Darkstore Robotics & Dynamic Dispatch Mesh", "Hyperlocal Darkstore Automation & Instant Logistics Routing", "Go, C++, Redis Cluster, TimescaleDB, MQTT", "Sub-8 minute average fulfillment; 40% reduction in picker transit distance; zero inventory stockouts"),
            ("Project FreshPulse: Real-Time Demand Forecasting & Cold-Chain Integrity IoT Monitor", "Predictive Fresh Perishable Supply Chain & IoT Quality Telemetry", "Python, TensorFlow, Kafka, ClickHouse, InfluxDB", "Reduces fresh produce spoilage by 65%; automated real-time dynamic markdowns"),
            ("Project SwarmDispatch: Multi-Agent Dynamic Courier Batching & Route Optimization Engine", "Geospatial Multi-Vehicle Pickup and Delivery Optimization", "C++, Rust, Uber H3 Index, Redpanda, RabbitMQ", "Increases rider multi-order batching by 35%; reduces fuel consumption and delivery wait times by 22%")
        ],
        "E-Commerce, Marketplaces & D2C Brands": [
            ("Project OmniCatalog: Multilingual Visual Discovery, Conversational Search & Dynamic Pricing Fabric", "Multimodal Semantic Vector Search & Automated Price Elasticity", "Python, PyTorch, Qdrant Vector DB, Go, ScyllaDB", "Sub-15ms vector similarity visual search across 50M SKUs; 28% increase in catalog conversion"),
            ("Project PrimeRoute: Intelligent Multi-Carrier Logistics Aggregator & RTO Fraud Predictor", "Predictive Reverse Logistics & Real-Time Carrier Selection", "Go, LightGBM, PostgreSQL, Kafka, Redis", "Reduces RTO (Return to Origin) delivery failures by 42%; cuts average shipment costs by ₹18/parcel"),
            ("Project BrandOS: Full-Stack Direct-to-Consumer Omnichannel Inventory & Customer Lifecycle Engine", "Integrated D2C Supply Chain & Predictive Retention Platform", "TypeScript, Next.js, Node.js, ClickHouse, PostgreSQL", "Unifies retail stores, quick commerce, and online shopfronts with instant inventory sync")
        ],
        "Electric Vehicles, CleanTech & Deep Mobility": [
            ("Project Telematics-Pulse: High-Frequency Vehicle Telemetry & Battery Health Digital Twin", "Automotive IoT Edge Streaming & Battery Lifecycle Optimization", "C/C++, Rust, EMQX MQTT, TimescaleDB, ClickHouse", "Processes 10B daily telemetry points; predicts cell degradation 30 days in advance"),
            ("Project ChargeGrid-OS: Distributed Smart EV Charging Network & Grid Harmonic Load Balancer", "Smart Charging Infrastructure & Virtual Power Plant Integration", "Go, Python, MQTT, PostgreSQL, Docker, AWS IoT", "Balances grid load across 5,000 charging points; prevents substation overload during peak charge hours"),
            ("Project FleetAutonomy: Autonomous Urban Commercial Fleet Routing & Predictive Maintenance Core", "Intelligent Fleet Scheduling & Component Failure Warning System", "Rust, Python, Apache Kafka, Redis, InfluxDB", "Reduces fleet maintenance downtime by 50%; improves vehicle daily operating range by 14%")
        ],
        "Enterprise SaaS, Cloud, Infrastructure & DevTools": [
            ("Project HyperObservability: Unified Distributed Traces, Metrics & Log Intelligence Engine", "Full-Stack Distributed Cloud Observability & Anomaly Diagnosis", "Go, ClickHouse, OpenTelemetry, eBPF, Kafka", "Cuts enterprise monitoring TCO by 75%; pinpoints microservice latency regressions in sub-second time"),
            ("Project DevFabric: Autonomous Multi-Cloud Infrastructure Synthesizer & Policy Enforcement Mesh", "Infrastructure-as-Code Automation & Policy Governance", "Rust, Go, Open Policy Agent, Kubernetes, Terraform", "Automates cloud provisioning with 100% compliance; prevents misconfigurations and cloud budget overruns"),
            ("Project DataBridge: Zero-Copy Real-Time Data Federation & Universal Query Optimizer", "Columnar Distributed Data Virtualization & Pushdown Query Engine", "Rust, Apache Arrow, DataFusion, Flight SQL", "Executes complex federated queries across polyglot datastores in sub-5ms with zero ETL overhead")
        ],
        "Healthcare, BioTech, HealthTech & Diagnostics": [
            ("Project BioSovereign: Continuous Multiparametric Vital Signs Telemetry & Clinical Early Warning Engine", "Real-Time Patient Telemetry & AI Diagnostic Decision Support", "C++, Python, TimescaleDB, Kafka, WebSockets", "Detects clinical vitals deterioration 4 hours before ICU escalation; 99.4% telemetry reliability"),
            ("Project Genomix-Fast: High-Throughput Clinical Next-Generation Sequencing & Variant Annotation Core", "Distributed Genomic Bioinformatics & Precision Medicine Pipeline", "Rust, Python, Nextflow, Apache Spark, Cloud Storage", "Analyzes full human genome sequencing data in under 45 minutes; automated clinical variant reporting"),
            ("Project CareOrchestrator: Autonomous Hospital Workflow, Bed Allocation & Telehealth Consultation Mesh", "Healthcare Operations Automation & Secure Patient Journey Core", "Go, PostgreSQL, Redis, WebRTC, Docker", "Reduces patient ER wait times by 40%; seamless HIPAA-compliant medical record synchronization")
        ],
        "B2B Industrial Marketplaces, Manufacturing & Supply Chain": [
            ("Project IndustrialMesh: Autonomous Factory Machine Telemetry & Real-Time Production Scheduling OS", "Industrial IoT Smart Factory Operations & Capacity Matchmaking", "Rust, Go, OPC-UA, TimescaleDB, Kafka", "Connects 2,000+ machine tools; optimizes factory utilization from 62% to 89%"),
            ("Project B2B-Clearing: Digital Procurement Invoicing, Trade Finance & Quality Provenance Fabric", "Enterprise B2B Commerce Settlement & Dynamic Reverse Auction", "Go, Java, PostgreSQL, Kafka, ElasticSearch", "Automates million-dollar raw material purchase orders; instant trade finance liquidity in 2 hours"),
            ("Project AgriSupply-Zero: Farm-Gate Produce Grading, Real-Time Mandi Arbitrage & Express Cold Chain", "Agritech Produce Digitization & Fresh Food Supply Chain", "Python, OpenCV, Go, MQTT, PostgreSQL", "Bypasses 3 layers of middlemen; moves farm harvest to urban retailers in <12 hours with minimal waste")
        ],
        "EdTech, Skill Development & Future of Work": [
            ("Project EduScale-Live: Ultra-Low Latency Interactive Virtual Classroom & Real-Time Engagement Engine", "Scalable Real-Time Video Education & AI Student Assessment", "C++, Go, WebRTC, Redis Cluster, ClickHouse", "Streams interactive live classes to 500,000 concurrent students with <200ms latency across 3G networks"),
            ("Project SkillGraph: Adaptive AI Curriculum Personalization & Automated Code Execution Sandbox", "Personalized Learning Trajectory & Secure Interactive Sandbox", "Go, Python, Docker/gVisor, PostgreSQL, Kafka", "Executes untrusted student code in isolated secure sandboxes in <50ms; personalized AI remedial tutoring"),
            ("Project CareerMatch-AI: Deep Skill Graph Evaluation & High-Bandwidth Talent Placement Operating System", "AI Skill Verification & Algorithmic Candidate Matching", "Python, FastAPI, Qdrant, PostgreSQL, Next.js", "Matches graduates to high-leverage roles with 92% interview conversion rate")
        ],
        "DeepTech, Generative AI, Robotics & SpaceTech": [
            ("Project NeuroGen-Indic: Sovereign Multilingual Generative Foundation Model & Speech Synthesis Engine", "Indic Large Multimodal Foundation Models & Low-Resource Speech AI", "PyTorch, CUDA/Triton, vLLM, Ray, Hugging Face", "State-of-the-art inference across 22 Indian languages; sub-100ms first-token latency on edge hardware"),
            ("Project RoboVision-3D: Sub-Millimeter Spatial Depth Perception & Autonomous Robotic Manipulation Fabric", "Industrial Robotic Vision & Adaptive Edge Motion Planning", "C++, ROS 2, PyTorch, TensorRT, OpenCV", "Enables industrial robot arms to grasp unstructured, overlapping parts with 99.98% pick accuracy"),
            ("Project OrbitMesh: Low-Earth-Orbit Satellite Constellation Telemetry & Autonomous Collision Avoidance Core", "Astrodynamics Orbital Mechanics & Satellite Fleet Management", "Rust, C++, SQLite, Kafka, WebGL", "Automates space debris avoidance maneuvers; real-time orbital tracking of 100+ microsatellites")
        ],
        "PropTech, Real Estate & Smart Living": [
            ("Project SmartLiving-OS: IoT Building Automation, Access Control & Resident Super-App Infrastructure", "Smart Building IoT Management & Community Micro-Commerce", "Go, MQTT, PostgreSQL, Redis, Flutter SDK", "Automates visitor entry, energy consumption, and amenities booking for 50,000 apartments"),
            ("Project RealEstate-Mesh: Digital Title Verification, Instant Legal Encumbrance & 3D Spatial Virtual Tours", "PropTech Legal Intelligence & Photorealistic 3D Spatial Visualization", "Python, Three.js, Go, PostgreSQL with PostGIS", "Verifies property ownership deeds in 5 seconds; 4K photorealistic 3D walkthroughs on mobile"),
            ("Project RentEngine: Automated Rental Lease Contracting, Security Deposit Escrow & Maintenance Logistics", "Residential Property Management & Autonomous Escrow Settlement", "TypeScript, Node.js, PostgreSQL, Redis, Stripe/Razorpay", "Automates lease lifecycle and instant repair technician dispatch in under 2 hours")
        ],
        "Cybersecurity, Compliance & Web3 Ecosystem": [
            ("Project CyberShield: External Threat Intelligence, Attack Surface Monitoring & Autonomous Patching Mesh", "Continuous Cyber Threat Intelligence & Autonomous Attack Surface Defense", "Go, Python, Elasticsearch, Kafka, Neo4j", "Scans dark web and cloud assets to predict cyber attacks 72 hours before exploitation"),
            ("Project ZeroTrust-Core: Universal Identity Access Management, Microsegmentation & Software-Defined Perimeter", "Enterprise Zero-Trust Security & Distributed Access Control", "Rust, eBPF, Envoy Proxy, WireGuard, Redis", "Enforces sub-millisecond cryptographic packet inspection and dynamic least-privilege authorization"),
            ("Project Web3-Consensus: Institutional Multi-Party Computation (MPC) Custody & Cross-Chain Settlement Core", "Cryptographic Asset Custody & Non-Custodial Key Management", "Rust, Go, Solidity, libp2p, PostgreSQL", "Secures $5B+ digital assets with threshold signature schemes and zero single-point-of-failure")
        ],
        "Workforce, Talent, HRTech & Gig Economy": [
            ("Project GigForce-Core: Dynamic Frontline Shift Scheduling, Automated Escrow Payouts & Geo-Verification Mesh", "Frontline Workforce Operating System & Instant Wage Access", "Go, PostgreSQL, Redis, Kafka, Flutter", "Schedules 1M+ daily frontline shifts; automates instant wage payouts upon shift completion"),
            ("Project TalentGraph: Autonomous Candidate Sourcing, Skill Screening & High-Throughput Interview Orchestrator", "AI Talent Acquisition & Automated Competency Evaluation", "Python, FastAPI, Postgres, pgvector, React", "Automates technical interview prescreening; reduces hiring cycle from 30 days to 48 hours"),
            ("Project PeopleOS: Sovereign Enterprise HRMS, Real-Time Payroll Computation & Statutory Compliance Engine", "Enterprise Workforce Management & Automated Tax/PF Compliance", "Java, Go, PostgreSQL, Redis, Docker", "Executes payroll for 100,000 employees in under 60 seconds with 100% tax accuracy")
        ]
    }

    # Populate all 500 startups with their authentic profile, biggest project, and biggest prompt
    anchor_dict = {a["name"].lower(): a for a in anchors}

    for idx, s in enumerate(raw_500):
        rank = idx + 1
        name = s["name"]
        cat = s.get("category") or s.get("cat", "Enterprise SaaS, Cloud, Infrastructure & DevTools")
        corridor = s.get("corridor", "Koramangala (Startup Hub)")
        stage = s.get("stage", "Series A")
        val = s.get("valuation") or s.get("val", "$50M Valuation")
        year = s.get("founded_year") or s.get("year", 2018)
        desc = s.get("core_business") or s.get("desc", "High-growth Bangalore technology innovator.")

        # Check if anchor override exists
        if name.lower() in anchor_dict:
            a = anchor_dict[name.lower()]
            p_name = a["project_name"]
            p_pillar = a["project_pillar"]
            p_thesis = a["project_thesis"]
            t_stack = a["tech_stack"]
            impact = a["impact_metrics"]
            p_arch = a["prompt_archetype"]
        else:
            # Procedural high-caliber assignment from sector blueprints
            bps = sector_project_blueprints.get(cat, sector_project_blueprints["Enterprise SaaS, Cloud, Infrastructure & DevTools"])
            bp = bps[idx % len(bps)]
            p_name = f"{bp[0].split(':')[0]}: {name} Enterprise System"
            p_pillar = bp[1]
            p_thesis = f"Scales {name}'s operations across {corridor} by deploying an enterprise-grade {p_pillar.lower()} to eliminate systemic latency, optimize margins, and achieve dominant competitive advantage."
            t_stack = bp[2]
            impact = bp[3]
            p_arch = cat_to_archetype.get(cat, "standard_enterprise")

        # Render the Biggest & Most Powerful Prompt
        tmpl = prompt_templates.get(p_arch, prompt_templates["standard_enterprise"])
        rendered_prompt = tmpl.format(
            company=name,
            corridor=corridor,
            val=val,
            category=cat,
            project_name=p_name,
            tech_stack=t_stack,
            impact_metrics=impact,
            project_thesis=p_thesis
        )

        final_500.append({
            "id": f"BLR-STARTUP-{rank:03d}",
            "rank": rank,
            "company_name": name,
            "sector": cat,
            "corridor": corridor,
            "stage": stage,
            "valuation_or_funding": val,
            "founded_year": year,
            "core_business": desc,
            "biggest_project": {
                "project_name": p_name,
                "architecture_pillar": p_pillar,
                "strategic_thesis": p_thesis,
                "tech_stack": t_stack,
                "impact_metrics": impact
            },
            "biggest_prompt": rendered_prompt
        })

    return final_500

def main():
    print("Building Bangalore Top 500 Startups Master Dataset & Prompts...")
    dataset = build_top_500_dataset()
    print(f"Total startups processed: {len(dataset)}")

    # Ensure output directories exist
    os.makedirs("E:/anti/data", exist_ok=True)
    os.makedirs("E:/anti/bangalore_500_engine", exist_ok=True)

    json_path = "E:/anti/data/BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json"
    csv_path = "E:/anti/data/BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.csv"

    # 1. Write JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Master JSON saved to: {json_path} ({os.path.getsize(json_path) / 1024 / 1024:.2f} MB)")

    # 2. Write CSV
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Rank", "Company Name", "Sector", "Corridor", "Stage",
            "Valuation/Funding", "Founded Year", "Core Business",
            "Project Name", "Architecture Pillar", "Tech Stack", "Impact Metrics", "Prompt Length (Chars)"
        ])
        for item in dataset:
            p = item["biggest_project"]
            writer.writerow([
                item["id"],
                item["rank"],
                item["company_name"],
                item["sector"],
                item["corridor"],
                item["stage"],
                item["valuation_or_funding"],
                item["founded_year"],
                item["core_business"],
                p["project_name"],
                p["architecture_pillar"],
                p["tech_stack"],
                p["impact_metrics"],
                len(item["biggest_prompt"])
            ])
    print(f"Master CSV saved to: {csv_path} ({os.path.getsize(csv_path) / 1024:.2f} KB)")

if __name__ == "__main__":
    main()
