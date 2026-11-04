"""
deploy_all_repo_readmes.py
===========================
Generates and deploys comprehensive, production-grade READMEs and metadata
for all 12 owned Kotlin/Android repositories of Aditya Mehra (AdityaMehra007).
"""

import os
import shutil
import subprocess
import tempfile
import sys
import json

REPOS_CONFIG = {
    "PROJECT-AURELION-THE-LEGACY-OILWORKS-INTELLIGENCE-PLATFORM": {
        "title": "Aurelion Industrial OS",
        "tagline": "AI-Powered Chemical Engineering & Legacy Oilworks Industrial Operating System",
        "description": "Aurelion Industrial OS — AI-Powered Chemical Engineering & Legacy Oilworks Industrial Platform",
        "topics": ["android", "kotlin", "jetpack-compose", "chemical-engineering", "industrial-iot", "gemini-ai", "operations", "scada", "digital-twin"],
        "modules": [
            ("Digital Twin & Process Flow", "Real-time visual monitoring of refinery towers, catalytic cracking units, pipelines, and heat exchangers with live pressure, temperature, and throughput indicators."),
            ("Inventory & Tank Telemetry", "High-precision volumetric tank telemetry tracking crude stock, intermediate distillates, finished fuel reserves, and automated ullage calculations."),
            ("LIMS (Laboratory Information Management)", "Automated testing logbook for viscosity, sulfur content, flash points, and API gravity compliance with ASTM standards."),
            ("Compliance & Financial Modeling", "Operational cost modeling, crude yield economics, environmental compliance audit logs, and refinery margin optimization algorithms."),
            ("Archive AI & Knowledge Vault", "Integrated Gemini AI copilot for querying decades of legacy operational schematics, standard operating procedures (SOPs), and incident mitigation playbooks."),
            ("Process Engineering Calculators", "Embedded thermodynamic and hydraulic calculation suite for flow rates, vapor pressure, heat duty, and pressure drops across complex valve networks.")
        ],
        "screens": ["DigitalTwinScreen", "InventoryTankScreen", "LimsScreen", "ComplianceFinanceScreen", "CalculatorsScreen", "ArchiveAiScreen", "DashboardScreen"]
    },
    "Moneyverse": {
        "title": "Moneyverse",
        "tagline": "Strategic Financial Freedom, Wealth Creation & Business Empire Architecture",
        "description": "Moneyverse — Strategic Financial Freedom, Wealth Creation & Business Empire Architecture",
        "topics": ["android", "kotlin", "jetpack-compose", "fintech", "wealth-creation", "business-empire", "financial-modeling", "gemini-ai", "state-machine"],
        "modules": [
            ("The Atlas: Global Macro & Wealth Mapping", "Interactive asset mapping visualizing capital allocations across equities, sovereign debt, real estate, precious metals, and cash equivalents."),
            ("Empire Lab: Business Architecture State Machine", "Deterministic modeling sandbox for building and stress-testing multi-entity holding structures, subsidiary dividends, and corporate reinvestment cycles."),
            ("War Room: High-Conviction Investment Decisions", "Structured deal room evaluating capital deployment opportunities, IRR benchmarks, downside moat analysis, and strategic risk-reward asymmetries."),
            ("Economics & Yield Engine", "Live macroeconomic dashboard tracking inflation differentials, central bank interest rate trajectories, and compounding interest projections over 10-to-30 year horizons."),
            ("Verdict: AI Strategic Intelligence", "Gemini Pro-powered financial advisory engine delivering scenario analysis, stress-testing black swan events, and evaluating portfolio antifragility."),
            ("Luxury Financial Canvas", "Custom Jetpack Compose visualization library featuring dynamic sparklines, allocation donuts, and high-status financial telemetry.")
        ],
        "screens": ["AtlasScreen", "EmpireLabScreen", "WarRoomScreen", "EconomicsScreen", "VerdictScreen"]
    },
    "AI-Executive-OS": {
        "title": "AI Executive OS",
        "tagline": "Strategic Planning, Business Performance Analytics & Autonomous Workforce Orchestration",
        "description": "AI Executive OS — Strategic Planning, Business Performance Analytics & Workforce Orchestration",
        "topics": ["android", "kotlin", "jetpack-compose", "executive-dashboard", "business-intelligence", "ai-workforce", "operations", "kpi-telemetry", "gemini-ai"],
        "modules": [
            ("Executive Command Scaffold", "C-suite dashboard aggregating enterprise health metrics, burn rate velocity, cash runway, headcount efficiency, and operational bottlenecks."),
            ("KPI Detail Sheets & Sparkline Visuals", "Dynamic micro-charts and drill-down sheets providing multi-quarter variance analysis and trend decomposition for financial and operational indicators."),
            ("Autonomous Agent Workforce Orchestration", "Dispatcher interface for monitoring and directing specialized AI subagents across sales development, financial auditing, customer success, and market research."),
            ("Command Palette & Quick Actions", "Universal keyboard/touch modal allowing instant search, prompt execution, priority delegation, and cross-departmental status checks in milliseconds."),
            ("Bespoke Enterprise Analytics", "Custom Canvas-rendered bar charts, trend curves, and cohort retention visualizers built natively in Jetpack Compose without heavyweight charting bloat."),
            ("Executive AI Assistant", "Context-aware Gemini-powered strategic advisor synthesizing executive board memos, board deck briefing bullet points, and quarterly scenario models.")
        ],
        "screens": ["AnalyticsScreen", "AssistantScreen", "KPIDetailSheet", "CommandPaletteModal", "AgentExecutionModal"]
    },
    "Every-Toy.-Every-Imagination.-One-Universe.": {
        "title": "Toyverse Elite",
        "tagline": "Global Toy Universe, Play Platform, Learning Ecosystem & Family Super-App",
        "description": "Toyverse Elite — Global Toy Marketplace, Play Platform & Family Super-App Operating System",
        "topics": ["android", "kotlin", "jetpack-compose", "marketplace", "e-commerce", "family-tech", "gemini-ai", "learning-ecosystem"],
        "modules": [
            ("Omni-Channel Toy Catalog", "Curated global showcase featuring collectible action figures, educational STEM kits, modular construction sets, and artisanal wooden toys with rich imagery."),
            ("Play & Learn Quests", "Interactive developmental challenges designed to stimulate spatial reasoning, problem-solving, and creative storytelling for growing children."),
            ("Orbit AI: Child-Safe Learning Companion", "Gemini-powered interactive storyteller and creative brainstorming companion strictly guarded with child-safe content filtering."),
            ("Family Command Hub", "Multi-child profile management, wish-list curation, gift registries, screen-time allowance balancing, and parental approval workflows."),
            ("Artisanal Checkout & Order Tracking", "Frictionless checkout experience with order fulfillment timeline, automated delivery milestones, and doorstep tracking."),
            ("Collectible Rarity Index", "Real-time cataloging of limited-edition collector pieces, manufacturer provenance, and estimated secondary market valuation curves.")
        ],
        "screens": ["HomeScreen", "CatalogScreen", "PlayLearnScreen", "FamilyScreen", "OrbitAiScreen"]
    },
    "ARTISTRY-ONE-The-Grand-Digital-Atelier": {
        "title": "Artistry One",
        "tagline": "The Global Digital Atelier & Fine Art Collective Platform",
        "description": "Artistry One — The Global Digital Atelier & Operating System for Art Collectives & Ecosystems",
        "topics": ["android", "kotlin", "jetpack-compose", "art-marketplace", "creative-tech", "gemini-ai", "curation", "provenance", "digital-atelier"],
        "modules": [
            ("Digital Atelier & Master Studio", "Personalized studio workstation for fine artists to manage active canvases, catalog physical mediums, record pigments, and log drying schedules."),
            ("Fine Art Marketplace & Curation", "Global gallery marketplace connecting artists directly with collectors, featuring high-resolution image zoom, certificates of authenticity, and provenance history."),
            ("Private Collector Viewing Rooms", "Bespoke digital viewing salons allowing collectors to inspect curated collections with dynamic ambient lighting controls and dimension previews."),
            ("Commission Studio & Contract Engine", "Structured commission workflow managing client briefs, sketch approval milestones, escrow payment stages, and direct artist communication."),
            ("Academy & Masterclasses", "Structured art curriculum covering classical drawing, oil glazing, acrylic pouring, and digital painting techniques with step-by-step progress tracking."),
            ("Artistry AI Critic & Mentor", "Gemini-powered artistic copilot providing compositional feedback, color harmony suggestions, art history cross-references, and exhibition statement drafting.")
        ],
        "screens": ["DiscoverScreen", "MyAtelierScreen", "MarketplaceScreen", "CollectorRoomScreen", "CommissionStudioScreen", "LearnScreen", "ExhibitionsScreen", "ArtistryAIScreen"]
    },
    "Numisma-Elite": {
        "title": "Numisma Elite",
        "tagline": "Global Coin Intelligence, Optical Authentication, Valuation & Numismatic Marketplace",
        "description": "Numisma Elite — Coin Intelligence, Authentication, Valuation & Numismatic Marketplace",
        "topics": ["android", "kotlin", "jetpack-compose", "numismatics", "coin-grading", "marketplace", "fintech", "computer-vision", "gemini-ai"],
        "modules": [
            ("Optical Authentication & Grading Engine", "High-resolution macro inspection interface analyzing strike quality, surface wear, mint luster, and die varieties against Sheldon 70-point standards."),
            ("Global Numismatic Catalog", "Extensive database covering ancient coinage, colonial emissions, modern commemoratives, and bullion strikes with comprehensive mint mark guides."),
            ("Auction History & Valuation Curves", "Historical auction realization aggregator displaying realized price trends, population reports, and historical CAGR appreciation metrics."),
            ("Verified Dealer Directory", "Direct connection portal to certified numismatic dealerships, PCGS/NGC authorized submitters, and professional auction houses worldwide."),
            ("Numisma AI Appraiser", "Multimodal Gemini-powered numismatic advisor providing instant preliminary identification, historical context, rarity scoring, and market insights."),
            ("Personal Vault Management", "Secure collection tracking with insurance appraisal documentation, acquisition cost basis, and automated net collection valuation updates.")
        ],
        "screens": ["HomeScreen", "CatalogScreen", "CoinDetailScreen", "DealerDirectoryScreen", "CommunityScreen", "AiChatScreen"]
    },
    "GameVerse": {
        "title": "GameVerse",
        "tagline": "Universal Gaming Discovery Super-App, AI Copilot & Esports Hub",
        "description": "GameVerse — Universal Gaming Discovery Super-App, AI Copilot & Esports Hub",
        "topics": ["android", "kotlin", "jetpack-compose", "gaming", "ai-copilot", "esports", "gemini-ai", "room-database", "game-discovery"],
        "modules": [
            ("Universal Game Discovery Engine", "Cross-platform discovery catalog tracking PC, console, and mobile releases with dynamic genre tags, user metacritics, and release calendars."),
            ("GameVerse AI Copilot", "Integrated Gemini-powered gaming assistant providing real-time walkthroughs, boss battle strategies, build optimizations, and lore summaries."),
            ("Esports Hub & Tournament Brackets", "Live match schedules, tournament brackets, competitive rosters, and live score telemetry across major global esports leagues."),
            ("Squad Finder & Matchmaking", "Real-time squad matching portal filtering players by rank, communication style, regional server ping, and preferred team composition."),
            ("Hardware & Benchmark Diagnostics", "Device performance analyzer matching system specifications against minimum and recommended game requirements with FPS estimates."),
            ("Local Game Collection (Room DB)", "Offline-first library architecture persisting played titles, backlog queue, completion percentage, and personal reviews.")
        ],
        "screens": ["DiscoverScreen", "CopilotScreen", "EsportsScreen", "GameDetailScreen"]
    },
    "GymVerse-OS": {
        "title": "GymVerse OS",
        "tagline": "Complete Gym Operations, Live Equipment Intelligence & Crowd Monitoring Platform",
        "description": "GymVerse OS — Complete Gym Operations, Live Equipment Intelligence & Crowd Monitoring Platform",
        "topics": ["android", "kotlin", "jetpack-compose", "gym-management", "fitness-tech", "iot-telemetry", "crowd-monitoring", "operations", "gemini-ai"],
        "modules": [
            ("Live Equipment & Zone Heatmap", "Interactive gym floorplan visualizing live equipment availability, cardio vs. resistance zoning, and peak-hour density heatmaps."),
            ("Crowd Monitoring & Occupancy Telemetry", "Real-time facility occupancy rate tracking, optimal training time forecasts, and turnstile throughput statistics."),
            ("Comprehensive Workout Tracker", "Progressive overload tracking logbook for sets, reps, RPE, volume loads, and rest timers with historical strength progression curves."),
            ("Class Scheduling & Personal Trainer Roster", "Booking engine for group fitness sessions, HIIT classes, and 1-on-1 personal training reservations with calendar synchronization."),
            ("GymVerse IQ: AI Fitness Coach", "Gemini-powered athletic training assistant drafting personalized periodization routines, nutrition macro targets, and form cues."),
            ("Staff & Management Control Center", "Facility operations console managing equipment maintenance tickets, member check-ins, subscription renewals, and sanitization schedules.")
        ],
        "screens": ["MemberDashboardScreen", "EquipmentMapScreen", "WorkoutTrackerScreen", "ClassesAndTrainersScreen", "GymverseIQScreen", "ControlCenterScreen"]
    },
    "Zuno": {
        "title": "Zuno",
        "tagline": "Gen Z Social Network, Creator Studio, Micro-Communities & AI Cultural Copilot",
        "description": "Zuno — Gen Z Social Network, Creator Studio, Micro-Communities & AI Cultural Copilot",
        "topics": ["android", "kotlin", "jetpack-compose", "gen-z", "social-network", "creator-economy", "gemini-ai", "firebase-firestore", "wellbeing"],
        "modules": [
            ("Algorithmic Flow Feed", "Ultra-fast short-form media and visual card stream optimized for sub-16ms touch responsiveness and modern aesthetic typography."),
            ("Micro-Community Pods", "Interest-driven closed and open community rooms focused on subcultures, indie aesthetics, gaming clans, and creative collaborations."),
            ("Creator Monetization & Studio", "Native creator tooling for post curation, audio pairing, digital tip jars, and engagement analytics breakdown."),
            ("AI Cultural Copilot", "Gemini-powered creative copilot generating caption inspirations, aesthetic moodboards, hashtag trend analysis, and cultural meme context."),
            ("Digital Wellbeing & Mindful Breaks", "Built-in mindful usage dialogs, screen-time balance indicators, and ambient focus modes designed to prevent doom-scrolling."),
            ("Secure Identity & Auth (Firebase)", "Robust authentication layer powered by Firebase Auth, Google Sign-In, and App Check protection against automated spam bots.")
        ],
        "screens": ["HomeScreen", "DiscoverScreen", "CommunitiesScreen", "CreateScreen", "ProfileScreen", "InboxScreen", "WellbeingDialog"]
    },
    "JOYVERSE": {
        "title": "JOYVERSE",
        "tagline": "Global Entertainment, Comedy Streaming & Human Connection Platform",
        "description": "JOYVERSE — Global Entertainment, Comedy Streaming & Human Connection Platform",
        "topics": ["android", "kotlin", "jetpack-compose", "streaming", "entertainment", "comedy", "social-platform", "gemini-ai", "bengaluru"],
        "modules": [
            ("Bengaluru Laughs & Regional Comedy", "Dedicated regional comedy showcase celebrating Bengaluru's vibrant stand-up scene, indie clubs, open mics, and local humor luminaries."),
            ("A Little Lighter: Mood-Elevating Streams", "Curated bite-sized feel-good video and audio streams categorized by humor styles (slapstick, witty satire, absurdism, observational)."),
            ("Interactive Comedy Player", "Custom media player featuring real-time crowd reaction floating emojis, audio clapping effects, and bookmarking favorite punchlines."),
            ("Community Comedy Rooms", "Virtual comedy club rooms where audiences can stream sets together, laugh in synchronized voice/chat rooms, and cheer comedians live."),
            ("Creator Studio & Tipping", "Direct support platform enabling emerging comedians to publish original audio clips, monetize performances, and build verified fanbases."),
            ("Joy AI & 'Make Me Laugh' Engine", "Interactive humor AI trained to deliver tailored punchlines, comedic roasts, witty banter, and personalized uplifting pick-me-ups on demand.")
        ],
        "screens": ["HomeScreen", "BengaluruLaughsScreen", "ALittleLighterScreen", "ContentPlayerDetailScreen", "CommunityRoomDetailScreen", "CreatorStudioScreen", "JoyAiScreen"]
    },
    "cloudbite-": {
        "title": "CloudBite Black Label",
        "tagline": "Luxury Cloud Kitchen Platform, Kitchen Display System & Recipe Financials",
        "description": "CloudBite Black Label — Luxury Cloud Kitchen Platform, Kitchen Display System & Recipe Financials",
        "topics": ["android", "kotlin", "jetpack-compose", "cloud-kitchen", "foodtech", "kds", "recipe-costing", "operations", "gemini-ai", "room-database"],
        "modules": [
            ("Artisanal Multi-Brand Storefront", "Luxury digital ordering catalog supporting multiple virtual restaurant concepts from a single centralized kitchen infrastructure."),
            ("Kitchen Display System (KDS)", "High-contrast kitchen display order queue organizing tickets by prep station, cooking timers, delivery courier arrival ETAs, and bump states."),
            ("Dynamic Recipe Costing Engine (Room DB)", "Relational database tracking raw ingredient prices, batch yields, food cost percentage, and gross contribution margin per menu item."),
            ("Live Order Fulfillment & Dispatch", "Real-time order lifecycle tracking from order placement, prep validation, packaging QA, to dispatch handoff."),
            ("Owner Executive Console", "Operations command room summarizing gross revenue, popular dishes, inventory burn rate, and wastage telemetry."),
            ("CloudBite AI Culinary Assistant", "Gemini Pro-powered kitchen intelligence analyzing leftover ingredient permutations, generating seasonal specials, and optimizing food costs.")
        ],
        "screens": ["OwnerConsoleScreen", "KitchenDisplayScreen", "OrderTrackingScreen", "CartCheckoutSheet", "ProductDetailModal", "AiAssistantScreen"]
    },
    "Cvlizations": {
        "title": "Civilization OS",
        "tagline": "The Universal Human Life Operating System & Future Planning Architecture",
        "description": "Civilization OS — The Universal Human Life Operating System & Future Planning Architecture",
        "topics": ["android", "kotlin", "jetpack-compose", "life-os", "habit-system", "biometrics", "gemini-ai", "firebase", "personal-development"],
        "modules": [
            ("Habit Level & Mastery Hierarchy", "Deterministic life progression system leveling habits across physical vitality, cognitive clarity, financial discipline, and social impact."),
            ("Universal Human Blueprint", "Holistic life architecture canvas mapping lifelong milestones, core values, annual objectives, and daily operational execution."),
            ("Biometric Security & Vault", "Hardware-backed biometric authentication (fingerprint/face recognition) securing deeply personal goals, financial assets, and private reflections."),
            ("Demo Personas & Benchmark Blueprints", "Pre-configured archetypes (The Polymath, The Sovereign Operator, The High-Performance Athlete) illustrating high-velocity life configurations."),
            ("Gemini Life Copilot", "Integrated AI mentor synthesizing daily schedules, evaluating decision trade-offs, and running mental models against long-term ambitions."),
            ("Cloud Synchronization (Firebase + Room)", "Hybrid offline-first architecture pairing local Android Room SQLite persistence with real-time cloud Firestore replication.")
        ],
        "screens": ["MainActivity", "CivilizationPersonalizationCard", "BiometricSecurityComponents", "CloudAccountSheet"]
    }
}

def generate_readme(repo_name, cfg):
    modules_md = ""
    for title, desc in cfg["modules"]:
        modules_md += f"### {title}\n{desc}\n\n"

    screens_list = ", ".join([f"`{s}`" for s in cfg["screens"]])

    topics_badges = " ".join([f"`#{t}`" for t in cfg["topics"]])

    readme_content = f"""# {cfg['title']}

> **{cfg['tagline']}**  
> *Engineered by **[Aditya Mehra](https://adityamehra007.github.io)** | Bengaluru, Karnataka, India*  
> *Portfolio:* [adityamehra007.github.io](https://adityamehra007.github.io) | *Flagship System:* [AdityaMehra007/anti](https://github.com/AdityaMehra007/anti)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Kotlin](https://img.shields.io/badge/Kotlin-2.0+-7F52FF.svg?logo=kotlin&logoColor=white)](https://kotlinlang.org/)
[![Jetpack Compose](https://img.shields.io/badge/Jetpack%20Compose-Material%203-4285F4.svg?logo=android&logoColor=white)](https://developer.android.com/jetpack/compose)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini-Pro%20%2F%20Flash%20AI-8E75B2.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![Android SDK](https://img.shields.io/badge/Android%20SDK-34+-3DDC84.svg?logo=android&logoColor=white)](https://developer.android.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%2B%20MVVM%20%2B%20StateFlow-00599C.svg)](https://developer.android.com/topic/architecture)

---

## 📌 Executive Overview

**{cfg['title']}** is a production-grade Android mobile application and operational platform engineered using modern **Kotlin 2.0+**, **Jetpack Compose (Material 3)**, and integrated **Google Gemini AI** intelligence.

Designed to solve complex real-world workflows with deterministic software reliability, **{cfg['title']}** combines responsive reactive UI state machines, robust offline-first local persistence, and cloud AI inference to deliver an elite digital experience.

---

## 🏗️ Core Architecture & Technical Design

The platform strictly follows Android's recommended **Clean Architecture & MVVM** paradigm with unidirectional data flow (UDF):

```mermaid
graph TD
    UI[Jetpack Compose UI & Material 3] -->|User Actions| VM[Android ViewModel & StateFlow]
    VM -->|UI State / Coroutine Dispatchers| UI
    VM -->|Data Requests| REPO[Repository Abstraction Layer]
    REPO -->|Local Cache / Queries| LOCAL[(Room SQLite / SharedPreferences)]
    REPO -->|Cloud State / Sync| CLOUD[(Firebase / Remote APIs)]
    REPO -->|Inference & Prompts| AI[Google Gemini AI Engine]
```

### Architectural Tenets
1. **Zero Vibe Coding & Predictable State**: State is modeled strictly via immutable Kotlin data classes and exposed via Kotlin `StateFlow`.
2. **Deep Modules**: High cohesion within feature domains; UI components communicate with repositories exclusively through clear, testable interfaces.
3. **Hardware & Battery Optimization**: Minimal memory overhead, zero redundant recompositions, and non-blocking asynchronous I/O via Kotlin Coroutines on `Dispatchers.IO`.
4. **Resilient Network & AI Tier**: Graceful fallback patterns for network partitions and rate limits on LLM API endpoints.

---

## 🚀 Key Modules & Capabilities

{modules_md}---

## 📱 Primary Screens & Visual Components

Key Compose screens and interface destinations include:
{screens_list}

Each screen incorporates custom Material 3 typography, fluid gestures, dark/light theme elevation surfaces, and accessible semantics.

---

## 🛠️ Technology Stack & Dependencies

| Layer | Technologies |
|---|---|
| **Core Language** | Kotlin 2.0+ (100% Kotlin codebase) |
| **UI Framework** | Jetpack Compose, Material 3, Foundation, Animation |
| **Asynchronous Engine** | Kotlin Coroutines & Asynchronous Flow (`StateFlow`, `SharedFlow`) |
| **Architecture** | ViewModel, Lifecycle Runtime, Navigation Compose |
| **Persistence** | Room Database (SQLite) / Firebase Firestore / DataStore |
| **AI Integration** | Google Gemini Generative AI SDK |
| **Build & Tooling** | Gradle Kotlin DSL (`build.gradle.kts`), Android Studio |

---

## 💻 Getting Started & Local Build

### Prerequisites
- **Android Studio** Hedgehog (2023.1.1) or newer
- **JDK 17** (LTS) or higher
- **Android SDK** API Level 34 installed

### Installation & Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AdityaMehra007/{repo_name}.git
   cd {repo_name}
   ```

2. **Configure Environment Keys**:
   Create or update `local.properties` in the project root:
   ```properties
   gemini.api.key=YOUR_GOOGLE_GEMINI_API_KEY
   ```

3. **Build the Debug APK**:
   ```bash
   # Windows PowerShell
   .\\gradlew.bat assembleDebug

   # macOS / Linux
   ./gradlew assembleDebug
   ```

4. **Execute Unit Tests**:
   ```bash
   .\\gradlew.bat test
   ```

---

## 👤 Engineering & Operational Leadership

**Aditya Mehra**  
*Strategic Operations Leader & Systems Architect*  
- **Alma Mater**: BBA International Business, Dayananda Sagar University (DSU), Bengaluru  
- **GitHub**: [@AdityaMehra007](https://github.com/AdityaMehra007)  
- **Portfolio & Mission Control**: [https://adityamehra007.github.io](https://adityamehra007.github.io)  
- **Flagship Autonomous System**: [AdityaMehra007/anti](https://github.com/AdityaMehra007/anti)

---

## 📄 License

This repository is distributed under the **MIT License**. See [LICENSE](LICENSE) for complete terms.
"""
    return readme_content.strip()

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=isinstance(cmd, str))
    if res.returncode != 0:
        print(f"ERROR: {cmd} failed with returncode {res.returncode}")
        print(f"STDOUT: {res.stdout}")
        print(f"STDERR: {res.stderr}")
    return res

def main():
    print("Starting automated deployment of READMEs for all 12 repositories...")
    temp_base = os.path.join(tempfile.gettempdir(), "gh_repo_deployments")
    os.makedirs(temp_base, exist_ok=True)
    
    success_count = 0
    total = len(REPOS_CONFIG)

    for i, (repo_name, cfg) in enumerate(REPOS_CONFIG.items(), 1):
        print(f"\n[{i}/{total}] Processing repository: AdityaMehra007/{repo_name}")
        clone_dir = os.path.join(temp_base, repo_name)
        if os.path.exists(clone_dir):
            shutil.rmtree(clone_dir, ignore_errors=True)
        
        # 1. Clone
        print(f"  Cloning {repo_name}...")
        clone_res = run_cmd(["gh", "repo", "clone", f"AdityaMehra007/{repo_name}", clone_dir])
        if clone_res.returncode != 0:
            print(f"  Failed to clone {repo_name}. Skipping.")
            continue
        
        # 2. Write README.md
        print(f"  Generating tailored README.md...")
        readme_text = generate_readme(repo_name, cfg)
        readme_path = os.path.join(clone_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_text + "\n")
        
        # 3. Commit & Push
        print(f"  Committing and pushing...")
        run_cmd(["git", "add", "README.md"], cwd=clone_dir)
        commit_res = run_cmd(["git", "commit", "-m", "docs: establish comprehensive production README and architecture showcase"], cwd=clone_dir)
        if commit_res.returncode == 0 or "nothing to commit" in commit_res.stdout:
            push_res = run_cmd(["git", "push", "origin"], cwd=clone_dir)
            if push_res.returncode == 0:
                print(f"  Successfully pushed README.md to {repo_name}!")
            else:
                print(f"  Push failed for {repo_name}.")
        else:
            print(f"  Commit note: {commit_res.stdout}")

        # 4. Update Description and Topics via GitHub CLI
        print(f"  Updating repo description & topics...")
        edit_cmd = [
            "gh", "repo", "edit", f"AdityaMehra007/{repo_name}",
            "--description", cfg["description"]
        ]
        if cfg["topics"]:
            edit_cmd.extend(["--add-topic", ",".join(cfg["topics"])])
        run_cmd(edit_cmd)

        # 5. Clean up temp folder
        shutil.rmtree(clone_dir, ignore_errors=True)
        success_count += 1

    print(f"\n==========================================")
    print(f"Completed deployment: {success_count}/{total} repositories updated successfully!")
    print(f"==========================================")

if __name__ == "__main__":
    main()
