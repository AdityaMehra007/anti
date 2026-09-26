#!/usr/bin/env python3
"""
ai_career_copilot.py — Sovereign Career Copilot for Aditya Mehra
Powered by Local GPU Ollama (11434) & OmniRoute AI Router (20128)
100% Free, Zero-Cost, Autonomous Career Intelligence.
"""

import sys
import os
import json
import urllib.request
import urllib.error
import time
import argparse

OLLAMA_BASE = "http://127.0.0.1:11434/v1"
OMNIROUTE_BASE = "http://127.0.0.1:20128/v1"
OMNIROUTE_KEY = os.environ.get("OMNIROUTE_API_KEY", "sk-47d56e1c83c613b8-340fcd-4b5d015f")

CANDIDATE_PROFILE = """
Candidate: Aditya Mehra
Education: BBA in International Business, Dayananda Sagar University (DSU), Bengaluru
Key Evidence & Achievements:
1. Aero India 2025: Operational Lead managing international defense delegations, bilateral protocol, high-stakes logistics, and cross-border liaison across 100+ VIPs.
2. Pencil Mark (Digital BD): Drove international business development, enterprise client acquisition, CRM pipeline management, and global sales workflows.
3. Tata Communications & Puma: Cross-functional client engagement, operational coordination, and process analytics.
4. Core Strengths: International Business, Enterprise BD, Cross-Border Logistics, Trade Compliance, Strategic Negotiations, AI Agentic Automation.
"""

def check_endpoint(url, headers=None, timeout=2):
    try:
        req = urllib.request.Request(url, headers=headers or {}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def query_llm(prompt, system_prompt=None, engine="auto", max_tokens=600):
    """
    engine can be 'gpu' (Ollama Local), 'frontier' (OmniRoute Gemini 3.7), or 'auto' (tries GPU first, falls back to OmniRoute).
    """
    sys_content = system_prompt or (
        "You are the Sovereign Career AI Copilot for Aditya Mehra. "
        "You always produce concise, high-impact, professional content strictly grounded in the candidate's authentic achievements. "
        "Never hallucinate fake credentials."
    )
    messages = [
        {"role": "system", "content": f"{sys_content}\n\n{CANDIDATE_PROFILE}"},
        {"role": "user", "content": prompt}
    ]

    # Decide engine order
    engines_to_try = []
    if engine == "gpu":
        engines_to_try = [("gpu", OLLAMA_BASE, "qwen2.5-coder:3b", {})]
    elif engine == "frontier":
        engines_to_try = [("frontier", OMNIROUTE_BASE, "antigravity/gemini-3.7-flash-high", {"Authorization": f"Bearer {OMNIROUTE_KEY}"})]
    else: # auto
        engines_to_try = [
            ("gpu", OLLAMA_BASE, "qwen2.5-coder:3b", {}),
            ("frontier", OMNIROUTE_BASE, "antigravity/gemini-3.7-flash-high", {"Authorization": f"Bearer {OMNIROUTE_KEY}"})
        ]

    for name, base_url, model, extra_headers in engines_to_try:
        url = f"{base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        headers.update(extra_headers)
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.4
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            start = time.time()
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                elapsed = time.time() - start
                content = data["choices"][0]["message"]["content"]
                return content, f"{name} ({model}) in {elapsed:.2f}s"
        except Exception as e:
            continue

    return None, "All local and routed LLM endpoints failed to respond."

def load_opportunities():
    path = os.path.join(os.path.dirname(__file__), "data", "omega_opportunity_master.json")
    if not os.path.exists(path):
        path = "data/omega_opportunity_master.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("opportunities", [])
    return []

def cmd_status():
    ollama_ok = check_endpoint("http://127.0.0.1:11434/api/tags")
    omniroute_ok = check_endpoint("http://127.0.0.1:20128/api/monitoring/health")
    print("=" * 60)
    print("  OMEGA SOVEREIGN CAREER COPILOT — ENGINE STATUS")
    print("=" * 60)
    print(f"  [1] Local GPU Ollama (Port 11434)  : {'ONLINE (NVIDIA GTX 960M GPU)' if ollama_ok else 'OFFLINE'}")
    print(f"  [2] OmniRoute Gateway (Port 20128)  : {'ONLINE (Ready for Inference)' if omniroute_ok else 'OFFLINE'}")
    print(f"  [3] Default Local Model            : qwen2.5-coder:3b (VRAM Warm)")
    print(f"  [4] Default Frontier Model         : antigravity/gemini-3.7-flash-high")
    print("=" * 60)

def cmd_list(top=10):
    opps = load_opportunities()
    if not opps:
        print("No opportunities found in data/omega_opportunity_master.json")
        return
    print("=" * 75)
    print(f"  TOP {top} TARGET CAREER OPPORTUNITIES (BENGALURU / GLOBAL)")
    print("=" * 75)
    print(f"  {'ID':<12} {'SCORE':<7} {'TIER':<6} {'COMPANY':<22} {'ROLE'}")
    print("-" * 75)
    sorted_opps = sorted(opps, key=lambda x: x.get("opportunity_score", 0), reverse=True)[:top]
    for o in sorted_opps:
        print(f"  {o.get('job_id',''):<12} {o.get('opportunity_score',0):<7.1f} {o.get('priority_tier',''):<6} {o.get('canonical_company', o.get('target_company',''))[:20]:<22} {o.get('job_role','')[:26]}")
    print("=" * 75)

def find_opp(job_id_or_company):
    opps = load_opportunities()
    target = job_id_or_company.strip().lower()
    for o in opps:
        if o.get("job_id", "").lower() == target:
            return o
        if target in o.get("canonical_company", "").lower() or target in o.get("target_company", "").lower():
            return o
    return None

def cmd_pitch(target_id, engine="auto"):
    opp = find_opp(target_id)
    if not opp:
        print(f"Could not find opportunity matching '{target_id}'. Use 'list' command.")
        return
    prompt = (
        f"Generate a high-conversion 3-sentence LinkedIn outreach message from Aditya Mehra to the hiring manager or recruiter at "
        f"{opp.get('canonical_company')} for the '{opp.get('job_role')}' position ({opp.get('location')}). "
        f"Anchor the pitch specifically around his Aero India 2025 leadership and BBA IB background at DSU Bengaluru. "
        f"Tone: sharp, executive, humble yet authoritative."
    )
    print(f"\n[AI Copilot] Generating tailored pitch for {opp.get('canonical_company')} via {engine}...")
    reply, meta = query_llm(prompt, engine=engine)
    if reply:
        print("\n" + "=" * 65)
        print(f"  OUTREACH PITCH: {opp.get('canonical_company')} ({opp.get('job_role')})")
        print(f"  Generated via: {meta}")
        print("=" * 65 + "\n")
        print(reply)
        print("\n" + "=" * 65)
    else:
        print(f"Error: {meta}")

def cmd_cover(target_id, engine="auto"):
    opp = find_opp(target_id)
    if not opp:
        print(f"Could not find opportunity matching '{target_id}'. Use 'list' command.")
        return
    prompt = (
        f"Write a sharp, 3-paragraph executive cover letter for Aditya Mehra applying to {opp.get('canonical_company')} for '{opp.get('job_role')}'.\n"
        f"Paragraph 1: Clear application intent, citing specific alignment with {opp.get('canonical_company')}'s global operations.\n"
        f"Paragraph 2: The Proof — Aero India 2025 international delegation coordination and Pencil Mark business development execution.\n"
        f"Paragraph 3: BBA International Business grounding from DSU and forward value commitment."
    )
    print(f"\n[AI Copilot] Generating cover letter for {opp.get('canonical_company')} via {engine}...")
    reply, meta = query_llm(prompt, engine=engine, max_tokens=750)
    if reply:
        print("\n" + "=" * 65)
        print(f"  COVER LETTER: {opp.get('canonical_company')} ({opp.get('job_role')})")
        print(f"  Generated via: {meta}")
        print("=" * 65 + "\n")
        print(reply)
        print("\n" + "=" * 65)
    else:
        print(f"Error: {meta}")

def cmd_interview(target_id, engine="auto"):
    opp = find_opp(target_id)
    company = opp.get("canonical_company") if opp else target_id
    role = opp.get("job_role", "Business Operations / BD") if opp else "Business Operations / BD"
    prompt = (
        f"You are the senior interviewer at {company} conducting an interview for {role}. "
        f"Generate 3 tough behavioral questions tailored to this role and provide the exact STAR-framework response structure "
        f"that Aditya Mehra should use, drawing from Aero India 2025, Pencil Mark, and his BBA IB degree at DSU."
    )
    print(f"\n[AI Copilot] Generating interview prep for {company} via {engine}...")
    reply, meta = query_llm(prompt, engine=engine, max_tokens=800)
    if reply:
        print("\n" + "=" * 65)
        print(f"  INTERVIEW SIMULATION: {company} ({role})")
        print(f"  Generated via: {meta}")
        print("=" * 65 + "\n")
        print(reply)
        print("\n" + "=" * 65)
    else:
        print(f"Error: {meta}")

def main():
    parser = argparse.ArgumentParser(description="OMEGA Sovereign Career AI Copilot")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # status
    subparsers.add_parser("status", help="Check live health of AI inference engines")

    # list
    list_p = subparsers.add_parser("list", help="List top opportunities")
    list_p.add_argument("--top", type=int, default=10, help="Number of opportunities to show")

    # pitch
    pitch_p = subparsers.add_parser("pitch", help="Generate outreach pitch for a job")
    pitch_p.add_argument("target", help="Job ID (e.g. BLR-JOB-001) or company name")
    pitch_p.add_argument("--engine", choices=["auto", "gpu", "frontier"], default="auto")

    # cover
    cover_p = subparsers.add_parser("cover", help="Generate executive cover letter")
    cover_p.add_argument("target", help="Job ID or company name")
    cover_p.add_argument("--engine", choices=["auto", "gpu", "frontier"], default="auto")

    # interview
    interview_p = subparsers.add_parser("interview", help="Generate interview questions & STAR answers")
    interview_p.add_argument("target", help="Job ID or company name")
    interview_p.add_argument("--engine", choices=["auto", "gpu", "frontier"], default="auto")

    # ask
    ask_p = subparsers.add_parser("ask", help="Direct query to the copilot")
    ask_p.add_argument("prompt", help="Your question or prompt")
    ask_p.add_argument("--engine", choices=["auto", "gpu", "frontier"], default="auto")

    args = parser.parse_args()

    if not args.command or args.command == "status":
        cmd_status()
    elif args.command == "list":
        cmd_list(args.top)
    elif args.command == "pitch":
        cmd_pitch(args.target, args.engine)
    elif args.command == "cover":
        cmd_cover(args.target, args.engine)
    elif args.command == "interview":
        cmd_interview(args.target, args.engine)
    elif args.command == "ask":
        ans, meta = query_llm(args.prompt, engine=args.engine)
        if ans:
            print(f"\n[{meta}]\n{ans}\n")
        else:
            print(f"Error: {meta}")

if __name__ == "__main__":
    main()
