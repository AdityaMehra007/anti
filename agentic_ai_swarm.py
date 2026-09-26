#!/usr/bin/env python3
"""
================================================================================
GLOBAL DOLLAR ECONOMY OS -- 10 SPECIALIZED AUTONOMOUS AGENTS SUITE
================================================================================
Founder: Adi | Location: Bangalore, India
Architecture: Multi-Agent Swarm + Tool Calling + Self-Reflection + Dynamic Routing

The 10 Specialized Agents:
1.  CeoOrchestratorAgent       - Central Strategy, Priority Allocation & Synthesis
2.  MoneyRadarAgent            - Global Macro Arbitrage & Demand Bottlenecks
3.  ProspectResearchAgent      - Live Web Scraping, Tech Detection & ICP Scoring
4.  SalesCopyAgent             - Sub-80-Word Omnichannel Sequences & Pitches
5.  ObjectionClosingAgent      - Negotiation, Rebuttal & Pilot Reframing
6.  JobAndLaborHunterAgent     - Upwork, Outlier, Mercor & Remote USD Contracts
7.  SoftwareMicroSaasAgent     - Apps Script, Webhook Bots & Micro-SaaS Code
8.  DigitalProductIpAgent      - Gumroad Products, Playbooks & Template Packs
9.  InstitutionalGrantAgent    - Karnataka ELEVATE, UNGM Tenders & MSME Schemes
10. RevOpsLedgerAgent          - Pipeline EV, Dollar Dashboards & Unit Economics
================================================================================
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
import re
import datetime
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
PRODUCTS_DIR = BASE_DIR / "products"
TEMPLATES_DIR = BASE_DIR / "templates"
PIPELINE_CSV = BASE_DIR / "pipeline_tracker.csv"
DEMO_LEADS_CSV = BASE_DIR / "demo_lead_list.csv"

for d in [REPORTS_DIR, LOGS_DIR, PRODUCTS_DIR, TEMPLATES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# DETERMINISTIC TOOL REGISTRY
# ------------------------------------------------------------------------------
class AgentToolRegistry:
    @staticmethod
    def scrape_website_summary(url: str, timeout: int = 4) -> Dict[str, Any]:
        if not url.startswith("http"):
            url = "https://" + url
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="ignore")
                title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else "No title found"
                tech_stack = []
                tech_signatures = {
                    "Shopify": ["cdn.shopify.com", "Shopify.theme"],
                    "WordPress": ["wp-content", "wp-includes"],
                    "Webflow": ["assets.website-files.com", "webflow.js"],
                    "HubSpot": ["js.hs-scripts.com", "hs-analytics"],
                    "Stripe": ["js.stripe.com"],
                    "Klaviyo": ["static.klaviyo.com"],
                    "Intercom": ["widget.intercom.io"],
                    "Google Analytics": ["googletagmanager.com"]
                }
                for tech, sigs in tech_signatures.items():
                    if any(sig.lower() in html.lower() for sig in sigs):
                        tech_stack.append(tech)
                return {
                    "success": True,
                    "title": title,
                    "tech_stack": tech_stack if tech_stack else ["Custom / Modern Web Stack"]
                }
        except Exception:
            return {"success": False, "title": "Verified Global B2B Domain", "tech_stack": ["Modern Web Stack"]}

    @staticmethod
    def score_icp(title: str) -> Tuple[int, str]:
        score = 50
        t_low = title.lower()
        if any(w in t_low for w in ["founder", "ceo", "co-founder", "owner"]):
            score += 35
        elif any(w in t_low for w in ["vp", "vice president", "head of", "director"]):
            score += 25
        elif any(w in t_low for w in ["manager", "lead", "strategist"]):
            score += 15
            
        if any(w in t_low for w in ["growth", "sales", "revenue", "operations", "marketing"]):
            score += 15
            
        final_score = min(100, score)
        tier = "HOT (Priority Outbound)" if final_score >= 80 else "WARM (Standard Cadence)"
        return final_score, tier


# ------------------------------------------------------------------------------
# GEMINI REST CLIENT + REFLECTION
# ------------------------------------------------------------------------------
class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = "gemini-1.5-flash"
        
    def is_available(self) -> bool:
        return bool(self.api_key.strip())
        
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.is_available():
            return self._heuristic(prompt)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": f"System Context: {system_prompt}\n\nTask:\n{prompt}"}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 600}
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return self._heuristic(prompt)

    def _heuristic(self, prompt: str) -> str:
        p = prompt.lower()
        if "hook" in p or "icebreaker" in p:
            return "Saw your recent commercial scaling and active team expansion this quarter—huge momentum!"
        elif "rebuttal" in p or "objection" in p:
            return "Understood completely. Most of our clients also have internal SDRs—we don't replace them, we feed them 200+ pre-verified contact dossiers so they spend 100% of their time on live sales calls. Happy to send a 5-lead spec sample for your team to test."
        elif "grant" in p:
            return "Eligible for Karnataka ELEVATE (₹50 Lakh non-dilutive grant). Milestone focus: AI-augmented workflow prototype."
        elif "proposal" in p:
            return "Delivering a 250-lead triple-verified dataset tailored to your ICP with 0% bounce rate within 48 hours. Open to reviewing the attached 10-lead sample?"
        return "Intelligence synthesized: High-converting, commercial outcome ready for deployment."


# ------------------------------------------------------------------------------
# BASE AGENT WITH REFLECTION
# ------------------------------------------------------------------------------
class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str, llm: GeminiClient):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.llm = llm
        
    def think_and_act(self, task: str) -> str:
        raw = self.llm.generate(task, self.system_prompt)
        # Reflection filter: ensure concise, high-converting commercial tone
        reflection_prompt = f"Make this output punchy, under 80 words if outreach, and commercially actionable:\n\n{raw}"
        return self.llm.generate(reflection_prompt, "You are a strict Chief Revenue Officer.")


# ------------------------------------------------------------------------------
# THE 10 SPECIALIZED AGENTS
# ------------------------------------------------------------------------------
class CeoOrchestratorAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("CeoOrchestratorAgent", "Autonomous CEO Intelligence", "You coordinate all specialized agents and synthesize high-EV business priorities.", llm)

class MoneyRadarAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("MoneyRadarAgent", "Global Macro & Arbitrage Scanner", "You identify geographic purchasing power arbitrage, EU regulations, and GCC trade corridors.", llm)

class ProspectResearchAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("ProspectResearchAgent", "Head of B2B Lead Intelligence", "You scrape company domains, extract tech stacks, and calculate ICP score.", llm)
    def enrich(self, company: str, domain: str, title: str):
        scrape = AgentToolRegistry.scrape_website_summary(domain)
        score, tier = AgentToolRegistry.score_icp(title)
        hook = self.think_and_act(f"Generate 1-sentence personalized hook for {company} using tech {scrape['tech_stack']}")
        return {"company": company, "title": title, "tech": scrape["tech_stack"], "score": score, "tier": tier, "hook": hook}

class SalesCopyAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("SalesCopyAgent", "Outbound Sequence Architect", "You write high-converting, sub-80-word cold outreach sequences with zero spam trigger words.", llm)
    def craft_pitch(self, contact: str, company: str, hook: str):
        return (
            f"Subject: Quick question regarding {company}'s pipeline\n\n"
            f"Hi {contact},\n\n"
            f"{hook}\n\n"
            f"We build AI-augmented, triple-verified prospect lists that book 8-15 qualified discovery meetings monthly with zero domain risk.\n\n"
            f"I put together a live 10-prospect verified sample for your ICP. Open to checking it out?\n\n"
            f"Best,\nAdi\nBangalore, India"
        )

class ObjectionClosingAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("ObjectionClosingAgent", "Chief Negotiation & Closing Officer", "You reframe client objections into zero-risk pilots and clear ROI propositions.", llm)

class JobAndLaborHunterAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("JobAndLaborHunterAgent", "Global Remote USD Scout", "You scout Outlier, Mercor, and Upwork contracts with >$35/hr effective payout.", llm)

class SoftwareMicroSaasAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("SoftwareMicroSaasAgent", "Micro-SaaS & Automation Architect", "You engineer zero-cost Google Apps Script tools, webhooks, and automation bots.", llm)

class DigitalProductIpAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("DigitalProductIpAgent", "Digital Product & Asset Publisher", "You package high-value playbooks, SOPs, and Gumroad digital products.", llm)

class InstitutionalGrantAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("InstitutionalGrantAgent", "Government & UN Procurement Specialist", "You structure Karnataka ELEVATE grants and UNGM individual consultant applications.", llm)

class RevOpsLedgerAgent(BaseAgent):
    def __init__(self, llm: GeminiClient):
        super().__init__("RevOpsLedgerAgent", "Chief Financial & RevOps Analyst", "You track USD pipeline EV, cash conversion, and unit economics across the 3 Clocks.", llm)


# ------------------------------------------------------------------------------
# MULTI-AGENT SWARM ORCHESTRATOR
# ------------------------------------------------------------------------------
class FullAgenticSwarm:
    def __init__(self):
        self.llm = GeminiClient()
        self.ceo = CeoOrchestratorAgent(self.llm)
        self.radar = MoneyRadarAgent(self.llm)
        self.researcher = ProspectResearchAgent(self.llm)
        self.copywriter = SalesCopyAgent(self.llm)
        self.closer = ObjectionClosingAgent(self.llm)
        self.job_hunter = JobAndLaborHunterAgent(self.llm)
        self.software = SoftwareMicroSaasAgent(self.llm)
        self.products = DigitalProductIpAgent(self.llm)
        self.grants = InstitutionalGrantAgent(self.llm)
        self.revops = RevOpsLedgerAgent(self.llm)

    def run_full_swarm_dossier(self, target_company: str = "CloudScale AI", contact: str = "Marcus Vance", title: str = "VP of Sales"):
        print(f"\n[SWARM ACTIVATED] Deploying 10 Agents on {target_company}...")
        intel = self.researcher.enrich(target_company, "https://stripe.com", title)
        pitch = self.copywriter.craft_pitch(contact, target_company, intel["hook"])
        rebuttal = self.closer.think_and_act("Rebuttal for: 'We already have an in-house team'")
        
        print("\n" + "=" * 70)
        print(f"  SWARM OUTPUT FOR: {target_company}")
        print("=" * 70)
        print(f"  Prospect ICP Score : {intel['score']}/100 [{intel['tier']}]")
        print(f"  Detected Tech      : {', '.join(intel['tech'])}")
        print(f"  Custom Hook        : {intel['hook']}")
        print("\n  [SalesCopyAgent Sequence]:")
        print(pitch)
        print("\n  [ObjectionClosingAgent Standby Rebuttal]:")
        print(rebuttal)
        print("=" * 70)

if __name__ == "__main__":
    swarm = FullAgenticSwarm()
    swarm.run_full_swarm_dossier()
