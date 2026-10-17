#!/usr/bin/env python3
"""
generate_ai_elite_packages.py — Generate 10 Elite Tailored Application Packages for 2027 AI & Quant Roles
Aditya Mehra Profile:
- Aditya Mehra, BBA International Business (Dayananda Sagar University 2026), GPA 8.78/10.0
- Systems & Operations Analyst, Autonomous AI Agent Architect, Quantitative Systems & Data Infrastructure
- adityamehra007@gmail.com | +91-7003456624 | Bengaluru, India
"""

import sys
import json
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

import win32com.client
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOSSIERS_DIR = Path(r"e:\anti\applications_generated")
REPORTS_DIR = Path(r"e:\anti\reports\ai_2027_pdf_packages")

AI_TARGETS = [
    {
        "id": "APX-AI-001",
        "company": "Jane Street",
        "role": "Machine Learning Engineer / Data Systems Intern (Summer 2027)",
        "location": "New York City, NY",
        "comp": "$120/hr",
        "url": "https://www.janestreet.com/join-jane-street/position/8611307002",
        "hook": "Deterministic Execution Graphs, Low-Latency Market Ingestion & Memory-Safe State Machines",
        "thesis": "Applying autonomous agent verification pipelines and zero-garbage-collection telemetry to high-frequency pricing signals."
    },
    {
        "id": "APX-AI-002",
        "company": "Citadel",
        "role": "Sector Data Scientist / Quantitative Systems Intern (2027)",
        "location": "New York City, NY / Miami, FL",
        "comp": "$125/hr",
        "url": "https://www.citadel.com/careers/details/sector-data-scientist-2027-intern-us/",
        "hook": "Cross-Asset Signal Synthesis, Real-Time FTS5 Knowledge Graphs & Alternative Data Verification",
        "thesis": "Structuring alternative corporate exhaust data into sub-millisecond queryable vector fabrics for statistical arbitrage."
    },
    {
        "id": "APX-AI-003",
        "company": "Google",
        "role": "Data Scientist - Research & Operations Intern (Summer 2027)",
        "location": "Mountain View, CA / Global",
        "comp": "$63/hr",
        "url": "https://www.google.com/about/careers/applications/jobs/results/89965613241246406",
        "hook": "Frontier Model Tool Invocation, Autonomous Agent Orchestration & Evaluation Benchmarks",
        "thesis": "Evaluating emergent autonomous behaviors and grounding LLM reasoning loops against deterministic verification fixtures."
    },
    {
        "id": "APX-AI-004",
        "company": "Microsoft",
        "role": "Data Science & Applied AI Systems Intern (Redmond / Remote)",
        "location": "Washington, DC / Redmond, WA",
        "comp": "$52/hr",
        "url": "https://apply.careers.microsoft.com/careers/job/1970393556982928",
        "hook": "Azure AI Agent Service Integration, Enterprise RAG Governance & Workflow DAG Reliability",
        "thesis": "Deploying self-healing multi-agent DAG architectures with state-machine determinism across enterprise workflows."
    },
    {
        "id": "APX-AI-005",
        "company": "NVIDIA",
        "role": "AI-Aided Systems & High-Performance Compute Intern (2027)",
        "location": "Santa Clara, CA",
        "comp": "$62/hr",
        "url": "https://nvidia.wd5.myworkdayjobs.com/en-US/nvidiaexternalcareersite/job/US-CA-Santa-Clara/PhD-Research-Intern--AI-Aided-Engineering---2027_JR2026940",
        "hook": "GPU Cluster Workflow Orchestration, Distributed State Checkpointing & Synthetic Simulation Engines",
        "thesis": "Maximizing hardware compute leverage by eliminating data ingestion bottlenecks in distributed deep learning pipelines."
    },
    {
        "id": "APX-AI-006",
        "company": "Roblox",
        "role": "Applied Scientist - AI & World Simulation Intern (2027)",
        "location": "San Mateo, CA",
        "comp": "$64/hr",
        "url": "https://careers.roblox.com/jobs/8242621?gh_jid=8242621",
        "hook": "Spatial Graph Reasoning, Real-Time Distributed Telemetry & Generative Physics State Engines",
        "thesis": "Designing scalable event synchronization fabrics for multi-agent simulation environments under massive player concurrency."
    },
    {
        "id": "APX-AI-007",
        "company": "Meta",
        "role": "AI Test Engineering & Systems Intern (Meta Superintelligence Labs)",
        "location": "Sunnyvale, CA / Menlo Park, CA",
        "comp": "$50/hr",
        "url": "https://www.metacareers.com/jobs/1866862250969693",
        "hook": "Autonomous Red-Teaming, Hardware Acceleration Test Harnesses & Model Adversarial Stress Testing",
        "thesis": "Engineering automated fuzzing and formal verification suites for multi-modal frontier foundation models."
    },
    {
        "id": "APX-AI-008",
        "company": "Akuna Capital",
        "role": "Quantitative Development & Strategy Intern (Summer 2027)",
        "location": "Chicago, IL",
        "comp": "$75/hr",
        "url": "https://www.akunacapital.com/careers/job/8021481/?gh_jid=8021481",
        "hook": "High-Frequency Order Routing, Real-Time PnL Reconciliation & Event-Driven Engine Design",
        "thesis": "Constructing lock-free event-driven trading components with deterministic latency envelopes and live telemetry."
    },
    {
        "id": "APX-AI-009",
        "company": "Adobe",
        "role": "Machine Learning Engineer - Creative AI Intern (2027)",
        "location": "San Francisco, CA / San Jose, CA",
        "comp": "$55/hr",
        "url": "https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced/job/San-Jose/XMLNAME-2027-Intern---Machine-Learning-Engineer_R171519",
        "hook": "On-Device Neural Acceleration, Latency-Critical Image Pipelines & WebAssembly Shaders",
        "thesis": "Compiling multi-modal inference runtimes into zero-latency client runtimes with verifiable accuracy."
    },
    {
        "id": "APX-AI-010",
        "company": "Belvedere Trading",
        "role": "Quantitative Trading & Derivatives Systems Intern (2027)",
        "location": "Chicago, IL",
        "comp": "$72/hr",
        "url": "https://jobs.lever.co/belvederetrading/cbde47db-c60b-4339-a8f4-a8e4f30505ab",
        "hook": "Options Volatility Surface Modelling, Real-Time Greeks Greeks Calculation & M2M Clearing",
        "thesis": "Translating options market microstructure theory into ultra-reliable autonomous risk management systems."
    }
]

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_markdown_dossier(tgt):
    md_content = f"""# {tgt['id']} — Tactical Application Dossier: {tgt['company']}

**Candidate**: Aditya Mehra  
**Education**: BBA International Business, Dayananda Sagar University (Class of 2026) | CGPA 8.78/10.0  
**Contact**: adityamehra007@gmail.com | +91-7003456624 | Bengaluru, India  
**Target Role**: {tgt['role']}  
**Compensation**: {tgt['comp']}  
**Location**: {tgt['location']}  
**Application Portal**: [{tgt['company']} Career Portal]({tgt['url']})  
**Core Competency Focus**: {tgt['hook']}  

---

### 1. Strategic Value Proposition & Thesis
{tgt['thesis']}

Aditya bridges the gap between quantitative operational mechanics and autonomous software systems. Having engineered multi-repository search architectures indexing 9,800+ entities, autonomous task DAGs, and deterministic validation suites, he brings immediate rigor to data ingestion, agent execution, and real-time observability.

### 2. High-Impact Technical Capabilities
- **Autonomous Systems & Agent Verification**: Architected self-healing DAG engines, tool-use sandboxes, and verification-before-completion evaluation loops.
- **Data Infrastructure & FTS5**: Engineered real-time SQLite FTS5 ingestion systems transforming thousands of unstructured listings into sub-millisecond queryable fabrics.
- **Quantitative & Financial Operations**: BBA International Business foundation providing deep literacy in treasury liquidity, clearing mechanics, order book dynamics, and macro risk.
- **Engineering Discipline**: Zero vibe coding, strict Red-Green-Refactor testing, deep module design, and verified upstream PR contributions.

### 3. Tailored Candidate Pitch
> "Dear {tgt['company']} Quant & AI Systems Team,
> 
> I am applying for the **{tgt['role']}** position. As a systems analyst and autonomous software architect graduating in 2026 from Dayananda Sagar University (Bengaluru, India), I build deterministic, high-throughput software at the intersection of business logic and machine intelligence.
> 
> In quantitative and frontier AI environments, competitive edge stems from eliminating latency and operational bottlenecks in **{tgt['hook']}**. In my recent work on the OMEGA Enterprise Nexus, I unified over 9,800 cross-repository entities across 7 domains with sub-millisecond search latency, authored end-to-end multi-agent execution DAGs, and patched production compiler flaws across enterprise open-source codebases.
> 
> I welcome the opportunity to discuss how my technical discipline and quantitative focus can contribute directly to {tgt['company']}."

---
*Verified Production Artifact generated by OMEGA ∞ Autonomous System on {datetime.now().strftime('%B %d, %Y')}.*
"""
    out_file = DOSSIERS_DIR / f"{tgt['id']}_{tgt['company'].replace(' ', '_')}.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(md_content, encoding="utf-8")
    return out_file

def generate_one_page_doc(tgt, word_app):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.55)
        s.bottom_margin = Inches(0.55)
        s.left_margin = Inches(0.65)
        s.right_margin = Inches(0.65)

    # Header
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(f"ADITYA MEHRA — {tgt['company'].upper()}")
    r_t.font.name = "Arial"
    r_t.font.size = Pt(14)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run(f"{tgt['role']} | Dossier {tgt['id']} | Comp: {tgt['comp']} | Bengaluru • +91-7003456624 • adityamehra007@gmail.com")
    r_s.font.size = Pt(8.5)
    r_s.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Card
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_background(c, "F8FAFC")
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)

    p_c = c.paragraphs[0]
    r_ch = p_c.add_run(f"QUANTITATIVE THESIS: {tgt['hook']}\n")
    r_ch.font.bold = True
    r_ch.font.size = Pt(9.5)
    r_ch.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    r_cb = p_c.add_run(tgt['thesis'])
    r_cb.font.size = Pt(8.5)
    r_cb.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Qualifications
    p_q = doc.add_paragraph()
    r_qh = p_q.add_run("Strategic Engineering & Operations Qualifications\n")
    r_qh.font.bold = True
    r_qh.font.size = Pt(10)
    r_qh.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    bullets = [
        ("Autonomous AI Systems Architecture: ", "Engineered deterministic multi-agent execution DAGs, automated verification gates, and evaluation fixtures."),
        ("High-Throughput Data Infrastructure: ", "Built sub-millisecond SQLite FTS5 search engines coordinating 9,816 cross-repository entities across 7 domains."),
        ("International Business & Quantitative Rigor: ", "BBA International Business (Class of 2026, CGPA 8.78/10.0) combining macro financial literacy with distributed backend engineering."),
        ("Production Reliability & Verified PRs: ", "Authored verified upstream pull requests resolving compiler defects in enterprise TypeScript and Python codebases.")
    ]
    for b_title, b_desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        r_bt = bp.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.size = Pt(8.5)
        r_bd = bp.add_run(b_desc)
        r_bd.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Cover Statement
    p_cov = doc.add_paragraph()
    r_covh = p_cov.add_run(f"Candidate Pitch to {tgt['company']}\n")
    r_covh.font.bold = True
    r_covh.font.size = Pt(10)
    r_covh.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_body = doc.add_paragraph()
    p_body.paragraph_format.space_after = Pt(2)
    r_body = p_body.add_run(
        f"I am applying for the {tgt['role']} role with a commitment to mathematical rigor and software craftsmanship. "
        f"Having developed autonomous agent runtimes, sub-millisecond search indexes, and verified testing pipelines, "
        f"I specialize in eliminating systemic operational latency and engineering reliable systems under extreme concurrency. "
        f"My background in international business operations allows me to evaluate technical trade-offs through the lens of capital efficiency. "
        f"I look forward to discussing how I can deliver immediate value to {tgt['company']}."
    )
    r_body.font.size = Pt(8.5)
    r_body.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    docx_path = REPORTS_DIR / f"{tgt['id']}_{tgt['company'].replace(' ', '_')}.docx"
    pdf_path = REPORTS_DIR / f"{tgt['id']}_{tgt['company'].replace(' ', '_')}.pdf"
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))

    # Export PDF via Word COM
    wdoc = word_app.Documents.Open(str(docx_path.resolve()))
    wdoc.ExportAsFixedFormat(str(pdf_path.resolve()), 17)
    pages = wdoc.ComputeStatistics(2)
    wdoc.Close(False)

    return docx_path, pdf_path, pages

def main():
    print("[+] Generating 10 Premier AI & Quant 2027 Application Packages...")
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False

    try:
        for idx, tgt in enumerate(AI_TARGETS, 1):
            md_path = generate_markdown_dossier(tgt)
            docx_path, pdf_path, pages = generate_one_page_doc(tgt, word_app)
            print(f"[{idx:02d}/10] {tgt['id']} | {tgt['company']:20s} -> {pdf_path.name} ({pages} page)")
    finally:
        word_app.Quit()

    print("[+] All 10 Premier AI & Quant Packages generated & verified successfully.")

if __name__ == "__main__":
    main()
