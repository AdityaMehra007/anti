#!/usr/bin/env python3
"""
================================================================================
GLOBAL DOLLAR ECONOMY OS -- 24/7 DAEMON & CRM DISPATCHER
================================================================================
Principal Operator: Adi | Location: Bangalore, India
Domain: Global B2B Lead Generation, Market Intelligence & Data Research
Architecture: Pure Python Standard Library (Zero External Dependencies)

Core Capabilities:
1. 24/7 Background Monitoring Daemon for Pipeline & Revenue Velocity
2. Real-Time Dynamic Expected Value (EV) & Multi-Currency (USD/INR) Analytics
3. Automated Morning & Evening CEO Briefings in Markdown
4. B2B AI Prospect Enrichment Engine (Seniority Scoring, Icebreakers, ICP Fit)
5. Interactive Command Center CLI with Lead Capture & Payment Logging
6. Automated Data Integrity Audits, File Backups & Asset Inventory Tracking
================================================================================
"""

import sys
import os
import csv
import time
import math
import shutil
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Base Directory & Path Configuration
BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
BACKUPS_DIR = BASE_DIR / "backups"

# Core Data & Template Assets
PIPELINE_CSV = BASE_DIR / "pipeline_tracker.csv"
MONEY_CSV = BASE_DIR / "money_dashboard.csv"
DEMO_LEADS_CSV = BASE_DIR / "demo_lead_list.csv"
PITCH_TOOLKIT_MD = BASE_DIR / "pitch_toolkit.md"
DAEMON_LOG = LOGS_DIR / "global_dollar_daemon.log"

# Default Economic Constants
USD_TO_INR_DEFAULT = 83.50
MORNING_BRIEF_HOUR = 8   # 08:00 AM
EVENING_BRIEF_HOUR = 20  # 08:00 PM

# Ensure directory tree exists
for directory in [REPORTS_DIR, LOGS_DIR, BACKUPS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# CONSOLE STYLING & LOGGING UTILITIES
# ==============================================================================

class ConsoleStyle:
    """Safe ANSI Color & Border Formatting with Windows Console fallback."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    WHITE = "\033[97m"

    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal environment supports ANSI color codes."""
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False
        if os.name == "nt":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except Exception:
                return "WT_SESSION" in os.environ or "ANSICON" in os.environ
        return True


COLOR_ENABLED = ConsoleStyle.supports_color()


def colorize(text: str, color_code: str) -> str:
    """Wrap text in ANSI color if supported."""
    if COLOR_ENABLED:
        return f"{color_code}{text}{ConsoleStyle.RESET}"
    return text


def log_event(message: str, level: str = "INFO"):
    """Write timestamped event to log file."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now_str}] [{level.upper()}] {message}\n"
    try:
        with open(DAEMON_LOG, mode="a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"Failed writing to daemon log: {e}", file=sys.stderr)


# ==============================================================================
# DATA LAYER (CSV PARSING, NORMALIZATION, AND BACKUPS)
# ==============================================================================

def clean_float(val: Any, default: float = 0.0) -> float:
    """Safely parse floats from currency strings ($1,250.50 -> 1250.5)."""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("$", "").replace(",", "").replace("%", "").strip()
    if not val_str:
        return default
    try:
        return float(val_str)
    except ValueError:
        return default


def parse_date_safe(date_str: Any) -> Optional[datetime.date]:
    """Parse date strings safely with multiple format fallbacks."""
    if not date_str:
        return None
    val = str(date_str).strip()
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(val, fmt).date()
        except ValueError:
            continue
    return None


def create_backup(file_path: Path):
    """Creates a timestamped snapshot of a CSV before mutating it."""
    if file_path.exists() and file_path.stat().st_size > 0:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dest = BACKUPS_DIR / f"{file_path.stem}_{timestamp}{file_path.suffix}"
        try:
            shutil.copy2(file_path, backup_dest)
        except Exception as e:
            log_event(f"Backup failed for {file_path.name}: {e}", level="WARN")


def initialize_csv_templates():
    """Initializes CSV files with proper headers if they do not exist."""
    if not PIPELINE_CSV.exists():
        headers = [
            "Date Added", "Company", "Contact Name", "Contact Title", "Channel",
            "Service Offered", "Stage", "Potential Revenue (USD)", "Probability (%)",
            "Expected Value (USD)", "Next Action", "Next Action Date", "Notes", "Status"
        ]
        with open(PIPELINE_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        log_event(f"Initialized new pipeline tracker template at {PIPELINE_CSV}")

    if not MONEY_CSV.exists():
        headers = [
            "Date", "Source", "Client/Platform", "Service/Product", "Revenue (USD)",
            "Revenue (INR)", "Cost (USD)", "Profit (USD)", "Hours Spent",
            "Profit Per Hour (USD)", "Payment Status", "Payment Method", "Recurring?", "Notes"
        ]
        with open(MONEY_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        log_event(f"Initialized new money dashboard template at {MONEY_CSV}")


def load_pipeline_data(filepath: Path = PIPELINE_CSV) -> List[Dict[str, Any]]:
    """Load and normalize pipeline records from CSV."""
    if not filepath.exists():
        initialize_csv_templates()
        return []

    records = []
    try:
        with open(filepath, mode="r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not any(row.values()) or not row.get("Company", "").strip():
                    continue
                
                potential_rev = clean_float(row.get("Potential Revenue (USD)"))
                probability = clean_float(row.get("Probability (%)"))
                
                ev = clean_float(row.get("Expected Value (USD)"))
                if ev == 0.0 and potential_rev > 0:
                    ev = round(potential_rev * (probability / 100.0), 2)

                normalized = {
                    "Date Added": row.get("Date Added", "").strip(),
                    "Company": row.get("Company", "").strip(),
                    "Contact Name": row.get("Contact Name", "").strip(),
                    "Contact Title": row.get("Contact Title", "").strip(),
                    "Channel": row.get("Channel", "").strip(),
                    "Service Offered": row.get("Service Offered", "").strip(),
                    "Stage": row.get("Stage", "Lead").strip(),
                    "Potential Revenue (USD)": potential_rev,
                    "Probability (%)": probability,
                    "Expected Value (USD)": ev,
                    "Next Action": row.get("Next Action", "").strip(),
                    "Next Action Date": row.get("Next Action Date", "").strip(),
                    "Notes": row.get("Notes", "").strip(),
                    "Status": row.get("Status", "Active").strip()
                }
                records.append(normalized)
    except Exception as e:
        log_event(f"Error loading pipeline data: {e}", level="ERROR")
    return records


def save_pipeline_lead(lead_dict: Dict[str, Any], filepath: Path = PIPELINE_CSV) -> bool:
    """Appends a new lead record to the pipeline tracker CSV safely."""
    try:
        create_backup(filepath)
        file_exists = filepath.exists()
        
        headers = [
            "Date Added", "Company", "Contact Name", "Contact Title", "Channel",
            "Service Offered", "Stage", "Potential Revenue (USD)", "Probability (%)",
            "Expected Value (USD)", "Next Action", "Next Action Date", "Notes", "Status"
        ]

        with open(filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            
            row = {
                "Date Added": lead_dict.get("Date Added", datetime.date.today().strftime("%Y-%m-%d")),
                "Company": lead_dict.get("Company", ""),
                "Contact Name": lead_dict.get("Contact Name", ""),
                "Contact Title": lead_dict.get("Contact Title", ""),
                "Channel": lead_dict.get("Channel", "LinkedIn"),
                "Service Offered": lead_dict.get("Service Offered", "Lead Gen"),
                "Stage": lead_dict.get("Stage", "Lead"),
                "Potential Revenue (USD)": f"{clean_float(lead_dict.get('Potential Revenue (USD)')):.2f}",
                "Probability (%)": f"{clean_float(lead_dict.get('Probability (%)')):.0f}",
                "Expected Value (USD)": f"{clean_float(lead_dict.get('Expected Value (USD)')):.2f}",
                "Next Action": lead_dict.get("Next Action", ""),
                "Next Action Date": lead_dict.get("Next Action Date", ""),
                "Notes": lead_dict.get("Notes", ""),
                "Status": lead_dict.get("Status", "Active")
            }
            writer.writerow(row)
        log_event(f"Added new pipeline lead: {lead_dict.get('Company')} ({lead_dict.get('Contact Name')})")
        return True
    except Exception as e:
        log_event(f"Failed to append pipeline lead: {e}", level="ERROR")
        return False


def load_money_data(filepath: Path = MONEY_CSV) -> List[Dict[str, Any]]:
    """Load and normalize revenue records from CSV."""
    if not filepath.exists():
        initialize_csv_templates()
        return []

    records = []
    try:
        with open(filepath, mode="r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not any(row.values()) or not row.get("Client/Platform", "").strip():
                    continue

                rev_usd = clean_float(row.get("Revenue (USD)"))
                rev_inr = clean_float(row.get("Revenue (INR)"))
                cost_usd = clean_float(row.get("Cost (USD)"))
                profit_usd = clean_float(row.get("Profit (USD)"))
                hours = clean_float(row.get("Hours Spent"))
                
                if rev_inr == 0.0 and rev_usd > 0:
                    rev_inr = round(rev_usd * USD_TO_INR_DEFAULT, 2)
                if profit_usd == 0.0 and rev_usd > 0:
                    profit_usd = round(rev_usd - cost_usd, 2)
                
                pph = clean_float(row.get("Profit Per Hour (USD)"))
                if pph == 0.0 and hours > 0 and profit_usd > 0:
                    pph = round(profit_usd / hours, 2)

                normalized = {
                    "Date": row.get("Date", "").strip(),
                    "Source": row.get("Source", "").strip(),
                    "Client/Platform": row.get("Client/Platform", "").strip(),
                    "Service/Product": row.get("Service/Product", "").strip(),
                    "Revenue (USD)": rev_usd,
                    "Revenue (INR)": rev_inr,
                    "Cost (USD)": cost_usd,
                    "Profit (USD)": profit_usd,
                    "Hours Spent": hours,
                    "Profit Per Hour (USD)": pph,
                    "Payment Status": row.get("Payment Status", "Received").strip(),
                    "Payment Method": row.get("Payment Method", "Wise").strip(),
                    "Recurring?": row.get("Recurring?", "No").strip(),
                    "Notes": row.get("Notes", "").strip()
                }
                records.append(normalized)
    except Exception as e:
        log_event(f"Error loading money dashboard data: {e}", level="ERROR")
    return records


def save_money_entry(entry_dict: Dict[str, Any], filepath: Path = MONEY_CSV) -> bool:
    """Appends a new financial transaction to money_dashboard.csv."""
    try:
        create_backup(filepath)
        file_exists = filepath.exists()
        
        headers = [
            "Date", "Source", "Client/Platform", "Service/Product", "Revenue (USD)",
            "Revenue (INR)", "Cost (USD)", "Profit (USD)", "Hours Spent",
            "Profit Per Hour (USD)", "Payment Status", "Payment Method", "Recurring?", "Notes"
        ]

        rev_usd = clean_float(entry_dict.get("Revenue (USD)"))
        inr_rate = clean_float(entry_dict.get("Exchange Rate"), USD_TO_INR_DEFAULT)
        rev_inr = clean_float(entry_dict.get("Revenue (INR)"), round(rev_usd * inr_rate, 2))
        cost_usd = clean_float(entry_dict.get("Cost (USD)"))
        profit_usd = clean_float(entry_dict.get("Profit (USD)"), round(rev_usd - cost_usd, 2))
        hours = clean_float(entry_dict.get("Hours Spent"))
        pph = clean_float(entry_dict.get("Profit Per Hour (USD)"), round(profit_usd / hours, 2) if hours > 0 else profit_usd)

        with open(filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()

            row = {
                "Date": entry_dict.get("Date", datetime.date.today().strftime("%Y-%m-%d")),
                "Source": entry_dict.get("Source", "B2B Client"),
                "Client/Platform": entry_dict.get("Client/Platform", ""),
                "Service/Product": entry_dict.get("Service/Product", "Lead Gen & Data Research"),
                "Revenue (USD)": f"{rev_usd:.2f}",
                "Revenue (INR)": f"{rev_inr:.2f}",
                "Cost (USD)": f"{cost_usd:.2f}",
                "Profit (USD)": f"{profit_usd:.2f}",
                "Hours Spent": f"{hours:.1f}",
                "Profit Per Hour (USD)": f"{pph:.2f}",
                "Payment Status": entry_dict.get("Payment Status", "Received"),
                "Payment Method": entry_dict.get("Payment Method", "Wise"),
                "Recurring?": entry_dict.get("Recurring?", "No"),
                "Notes": entry_dict.get("Notes", "")
            }
            writer.writerow(row)
        log_event(f"Logged new revenue entry: ${rev_usd:.2f} from {entry_dict.get('Client/Platform')}")
        return True
    except Exception as e:
        log_event(f"Failed to log revenue entry: {e}", level="ERROR")
        return False


# ==============================================================================
# FINANCIAL & PIPELINE ANALYTICS ENGINE
# ==============================================================================

class AnalyticsEngine:
    """Calculates operational and dollar performance metrics."""

    @staticmethod
    def calculate_metrics(target_date: Optional[datetime.date] = None) -> Dict[str, Any]:
        if target_date is None:
            target_date = datetime.date.today()

        pipeline_records = load_pipeline_data()
        money_records = load_money_data()

        # Money / Cash Flow Analytics
        total_rev_usd = 0.0
        total_rev_inr = 0.0
        total_profit_usd = 0.0
        total_cost_usd = 0.0
        total_hours = 0.0
        total_received_usd = 0.0
        total_pending_usd = 0.0

        daily_rev_usd = 0.0
        weekly_rev_usd = 0.0
        monthly_rev_usd = 0.0

        seven_days_ago = target_date - datetime.timedelta(days=7)
        first_of_month = target_date.replace(day=1)

        for row in money_records:
            r_usd = row["Revenue (USD)"]
            r_inr = row["Revenue (INR)"]
            p_usd = row["Profit (USD)"]
            c_usd = row["Cost (USD)"]
            hrs = row["Hours Spent"]
            status = row["Payment Status"].lower()

            total_rev_usd += r_usd
            total_rev_inr += r_inr
            total_profit_usd += p_usd
            total_cost_usd += c_usd
            total_hours += hrs

            if "received" in status or "settled" in status or "paid" in status:
                total_received_usd += r_usd
            else:
                total_pending_usd += r_usd

            row_date = parse_date_safe(row.get("Date"))
            if row_date:
                if row_date == target_date:
                    daily_rev_usd += r_usd
                if row_date >= seven_days_ago:
                    weekly_rev_usd += r_usd
                if row_date >= first_of_month:
                    monthly_rev_usd += r_usd

        profit_margin_pct = (total_profit_usd / total_rev_usd * 100.0) if total_rev_usd > 0 else 0.0
        blended_pph = (total_profit_usd / total_hours) if total_hours > 0 else 0.0

        # Pipeline & Active Expected Value (EV) Analytics
        total_deals = len(pipeline_records)
        active_deals = []
        won_deals = []
        lost_deals = []
        
        total_pipeline_val = 0.0
        total_pipeline_ev = 0.0
        deals_due_today = []
        overdue_deals = []

        stage_breakdown: Dict[str, Dict[str, Any]] = {
            "Lead": {"count": 0, "val": 0.0, "ev": 0.0},
            "Outreach": {"count": 0, "val": 0.0, "ev": 0.0},
            "Meeting": {"count": 0, "val": 0.0, "ev": 0.0},
            "Proposal": {"count": 0, "val": 0.0, "ev": 0.0},
            "Negotiation": {"count": 0, "val": 0.0, "ev": 0.0},
            "Won": {"count": 0, "val": 0.0, "ev": 0.0},
            "Lost": {"count": 0, "val": 0.0, "ev": 0.0}
        }

        for deal in pipeline_records:
            stage = deal["Stage"].title()
            status = deal["Status"].title()
            pot_rev = deal["Potential Revenue (USD)"]
            ev = deal["Expected Value (USD)"]
            act_date = parse_date_safe(deal.get("Next Action Date"))

            matched_stage = "Lead"
            for k in stage_breakdown.keys():
                if k.lower() in stage.lower():
                    matched_stage = k
                    break
            stage_breakdown[matched_stage]["count"] += 1
            stage_breakdown[matched_stage]["val"] += pot_rev
            stage_breakdown[matched_stage]["ev"] += ev

            if "Won" in stage or status == "Closed Won" or status == "Closed":
                won_deals.append(deal)
            elif "Lost" in stage or status == "Closed Lost":
                lost_deals.append(deal)
            else:
                active_deals.append(deal)
                total_pipeline_val += pot_rev
                total_pipeline_ev += ev

                if act_date:
                    if act_date == target_date:
                        deals_due_today.append(deal)
                    elif act_date < target_date:
                        overdue_deals.append(deal)

        active_deals_count = len(active_deals)
        weighted_win_prob = (total_pipeline_ev / total_pipeline_val * 100.0) if total_pipeline_val > 0 else 0.0
        top_active_deals = sorted(active_deals, key=lambda x: x["Expected Value (USD)"], reverse=True)

        return {
            "target_date": target_date.strftime("%Y-%m-%d"),
            "total_revenue_usd": total_rev_usd,
            "total_revenue_inr": total_rev_inr,
            "total_profit_usd": total_profit_usd,
            "total_cost_usd": total_cost_usd,
            "total_hours": total_hours,
            "total_received_usd": total_received_usd,
            "total_pending_usd": total_pending_usd,
            "daily_revenue_usd": daily_rev_usd,
            "weekly_revenue_usd": weekly_rev_usd,
            "monthly_revenue_usd": monthly_rev_usd,
            "profit_margin_pct": profit_margin_pct,
            "blended_pph": blended_pph,
            "total_deals_count": total_deals,
            "active_deals_count": active_deals_count,
            "won_deals_count": len(won_deals),
            "lost_deals_count": len(lost_deals),
            "total_pipeline_val_usd": total_pipeline_val,
            "total_pipeline_ev_usd": total_pipeline_ev,
            "weighted_win_prob": weighted_win_prob,
            "stage_breakdown": stage_breakdown,
            "deals_due_today": deals_due_today,
            "overdue_deals": overdue_deals,
            "top_active_deals": top_active_deals,
            "raw_pipeline": pipeline_records,
            "raw_money": money_records
        }


# ==============================================================================
# AI PROSPECT ENRICHMENT & SCORING ENGINE
# ==============================================================================

class ProspectEnricher:
    """
    Simulates high-velocity B2B prospect enrichment, seniority scoring,
    trigger analysis, and personalized icebreaker synthesis.
    """

    SENIORITY_WEIGHTS = {
        "founder": 30, "ceo": 30, "co-founder": 30, "owner": 28, "managing director": 28,
        "vp": 25, "vice president": 25, "head": 22, "director": 20, "chief": 25,
        "lead": 15, "manager": 12, "sdr": 8, "bdr": 8, "consultant": 10
    }

    TRIGGER_PATTERNS = [
        ("Series A", "Funding", 25, "Saw the massive Series A funding announcement—huge runway to accelerate pipeline"),
        ("Seed", "Funding", 20, "Congrats on closing your seed round—primed for scaling customer acquisition"),
        ("Hiring", "Expansion", 20, "Noticed you are actively expanding the commercial sales and SDR team"),
        ("Award", "Prestige", 15, "Huge congratulations on winning the recent industry performance award"),
        ("Launch", "Product", 15, "Loved seeing the recent v2.0 product feature release on Product Hunt"),
        ("Partner", "Ecosystem", 15, "Congrats on unlocking top-tier partner status—massive validation for the ecosystem"),
        ("Enterprise", "Deal", 20, "Incredible milestone securing the new Tier-1 enterprise contract"),
    ]

    @classmethod
    def enrich_prospect(cls, prospect: Dict[str, Any]) -> Dict[str, Any]:
        """Enriches a single raw prospect with scores, trigger classification and hook."""
        company = prospect.get("Company Name") or prospect.get("Company", "Target Co")
        name = prospect.get("Contact Name", "Executive")
        title = prospect.get("Title") or prospect.get("Contact Title", "Growth Leader")
        website = prospect.get("Website", "")
        industry = prospect.get("Industry", "B2B SaaS")
        trigger = prospect.get("Recent Trigger Event") or prospect.get("Notes", "")
        location = prospect.get("Location", "Global")

        title_lower = title.lower()
        seniority_score = 10
        seniority_label = "Individual Contributor"
        for kw, weight in cls.SENIORITY_WEIGHTS.items():
            if kw in title_lower:
                seniority_score = weight
                seniority_label = kw.title()
                break

        trigger_category = "Organic Growth"
        trigger_score = 10
        custom_hook = f"Noticed {company}'s impressive momentum in {industry}"
        for kw, cat, t_score, hook in cls.TRIGGER_PATTERNS:
            if kw.lower() in trigger.lower():
                trigger_category = cat
                trigger_score = t_score
                custom_hook = hook
                break

        total_score = min(100, seniority_score + trigger_score + 40)
        lead_category = "Hot" if total_score >= 70 else ("Warm" if total_score >= 50 else "Cold")

        first_name = name.split()[0] if name else "there"
        if any(w in custom_hook for w in ["Saw the", "Loved seeing", "Congrats", "Noticed", "Incredible"]):
            icebreaker = f"{custom_hook}—congrats {first_name}!"
        else:
            icebreaker = f"Loved following {company}'s recent work in the {industry} space—especially regarding {trigger or 'market expansion'}, {first_name}."

        if "SaaS" in industry or "Tech" in industry:
            pitch_angle = "Verified Decision-Maker Contact Lists (Zero-Bounce Guarantee) & Multi-Channel SDR Outbound"
        elif "Agency" in industry or "Marketing" in industry:
            pitch_angle = "High-Intent B2B Prospect Data & Competitor Intelligence Dossiers"
        else:
            pitch_angle = "Custom B2B Market Research & C-Level Lead Enrichment"

        return {
            "Company": company,
            "Contact Name": name,
            "Title": title,
            "Industry": industry,
            "Seniority Level": seniority_label,
            "Trigger Category": trigger_category,
            "Trigger Details": trigger or "Active market expansion",
            "Lead Score": lead_category,
            "Score Value": total_score,
            "Synthesized Icebreaker": icebreaker,
            "Recommended Service Angle": pitch_angle,
            "Website": website,
            "Location": location
        }


# ==============================================================================
# CEO BRIEFING GENERATION (MARKDOWN AUTOMATION)
# ==============================================================================

class BriefingGenerator:
    """Generates executive-grade Morning and Evening CEO briefs in Markdown."""

    @staticmethod
    def generate_morning_brief(target_date: Optional[datetime.date] = None) -> Tuple[Path, str]:
        if target_date is None:
            target_date = datetime.date.today()

        metrics = AnalyticsEngine.calculate_metrics(target_date)
        date_str = target_date.strftime("%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%H:%M:%S")

        md = []
        md.append(f"# ☀️ DAILY MORNING CEO BRIEFING — {date_str}")
        md.append(f"*Generated by Global Dollar Economy OS Daemon at {now_time} IST*\n")
        md.append(f"**Principal Operator:** Adi (Bangalore, India) | **Operational Mode:** 24/7 Global B2B Dispatch\n")
        md.append("---\n")

        # Section 1: Executive Pulse
        md.append("## ⚡ 1. EXECUTIVE PULSE & FINANCIAL RUNWAY\n")
        md.append("| Metric | USD Value | INR Equivalent (Est.) | Operational Status |")
        md.append("| :--- | :--- | :--- | :--- |")
        md.append(f"| **All-Time Realized Cash** | `${metrics['total_received_usd']:,.2f}` | `₹{metrics['total_received_usd']*USD_TO_INR_DEFAULT:,.2f}` | Settled & Verified |")
        md.append(f"| **In-Escrow / Pending Cash** | `${metrics['total_pending_usd']:,.2f}` | `₹{metrics['total_pending_usd']*USD_TO_INR_DEFAULT:,.2f}` | Awaiting QA / Release |")
        md.append(f"| **Total Net Profit** | `${metrics['total_profit_usd']:,.2f}` | `₹{metrics['total_profit_usd']*USD_TO_INR_DEFAULT:,.2f}` | Margin: **{metrics['profit_margin_pct']:.1f}%** |")
        md.append(f"| **Blended Effective Rate** | **`${metrics['blended_pph']:.2f}/hr`** | `₹{metrics['blended_pph']*USD_TO_INR_DEFAULT:,.2f}/hr` | High-Leverage Global Tier |")
        md.append(f"| **MTD Revenue ({target_date.strftime('%B %Y')})** | `${metrics['monthly_revenue_usd']:,.2f}` | `₹{metrics['monthly_revenue_usd']*USD_TO_INR_DEFAULT:,.2f}` | Pacing Active |")
        md.append("")

        # Section 2: Pipeline Radar
        md.append("## 🎯 2. ACTIVE PIPELINE & EXPECTED VALUE (EV) RADAR\n")
        md.append(f"- **Active Pipeline Opportunities:** `{metrics['active_deals_count']}` deals")
        md.append(f"- **Total Gross Pipeline Value:** **`${metrics['total_pipeline_val_usd']:,.2f}`**")
        md.append(f"- **Total Active Pipeline Expected Value (EV):** **`${metrics['total_pipeline_ev_usd']:,.2f}`** *(Probability Weighted)*")
        md.append(f"- **Blended Win Probability:** `{metrics['weighted_win_prob']:.1f}%`\n")

        md.append("### 📊 Funnel Breakdown by Stage")
        md.append("| Stage | Deal Count | Gross Pipeline (USD) | Expected Value (USD) |")
        md.append("| :--- | :--- | :--- | :--- |")
        for stage, data in metrics["stage_breakdown"].items():
            if data["count"] > 0:
                md.append(f"| **{stage}** | {data['count']} | `${data['val']:,.2f}` | `${data['ev']:,.2f}` |")
        md.append("")

        # Section 3: Today's Action Items
        md.append("## 🚨 3. TODAY'S ACTION ITEMS & CRITICAL DISPATCHES\n")
        if metrics["deals_due_today"]:
            md.append("### 🔔 Actions Due Today:")
            for deal in metrics["deals_due_today"]:
                md.append(f"- **{deal['Company']}** ({deal['Contact Name']} - {deal['Contact Title']})")
                md.append(f"  - **Stage:** `{deal['Stage']}` | **Potential:** `${deal['Potential Revenue (USD)']}` | **EV:** `${deal['Expected Value (USD)']}`")
                md.append(f"  - **Action Required:** {deal['Next Action']}")
                md.append(f"  - **Notes:** {deal['Notes']}\n")
        else:
            md.append("✅ *No active pipeline deals scheduled specifically for today. Focus on new outbound generation and proposal delivery.*\n")

        if metrics["overdue_deals"]:
            md.append("### ⚠️ Overdue Follow-ups Requiring Immediate Nudge:")
            for deal in metrics["overdue_deals"]:
                md.append(f"- **{deal['Company']}** ({deal['Contact Name']}) — Due: `{deal['Next Action Date']}` | Action: {deal['Next Action']}")
            md.append("")

        # Section 4: Daily Tactical Priorities
        md.append("## 🏹 4. TACTICAL DAILY BATTLEPLAN (THE 3-LEVER MATRIX)\n")
        md.append("1. **Lever 1: High-Intent Outbound Dispatches (5-10 Targets)**")
        md.append("   - Deploy personalized icebreakers to B2B SaaS Founders / Heads of Growth.")
        md.append("   - Pitch angle: 500 Verified Decision-Maker Lead List + Custom Market Intelligence Sample.")
        md.append("2. **Lever 2: Pipeline Velocity & Follow-Up Closes**")
        md.append("   - Nudge active proposals with concrete proof-of-work and turnaround guarantees.")
        md.append("3. **Lever 3: Asset Quality QA & Client Fulfillment**")
        md.append("   - Maintain 0% bounce rate on verified datasets; deliver zero-friction CSV deliverables.\n")

        # Section 5: Operating Philosophy
        md.append("## 💡 5. GLOBAL DOLLAR OPERATING PRINCIPLE\n")
        md.append("> *\"Arbitrage geography by delivering US/UK-grade speed, precision, and intelligence while operating from Bangalore. Earn in Dollars, execute with sovereign discipline, build compounding assets every single day.\"*\n")

        full_content = "\n".join(md)

        dated_path = REPORTS_DIR / f"DAILY_MORNING_CEO_BRIEF_{date_str}.md"
        canonical_path = REPORTS_DIR / "DAILY_MORNING_CEO_BRIEF.md"
        root_path = BASE_DIR / "DAILY_MORNING_BRIEFING.md"

        for p in [dated_path, canonical_path, root_path]:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(full_content)
            except Exception as e:
                log_event(f"Error writing morning briefing to {p}: {e}", level="WARN")

        log_event(f"Generated Morning CEO Briefing: {dated_path.name}")
        return dated_path, full_content

    @staticmethod
    def generate_evening_brief(target_date: Optional[datetime.date] = None) -> Tuple[Path, str]:
        if target_date is None:
            target_date = datetime.date.today()

        metrics = AnalyticsEngine.calculate_metrics(target_date)
        date_str = target_date.strftime("%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%H:%M:%S")

        md = []
        md.append(f"# 🌙 DAILY EVENING CEO CLOSE BRIEFING — {date_str}")
        md.append(f"*Generated by Global Dollar Economy OS Daemon at {now_time} IST*\n")
        md.append(f"**Principal Operator:** Adi (Bangalore, India) | **Close-of-Day Audit**\n")
        md.append("---\n")

        md.append("## 🏁 1. CLOSE-OF-DAY FINANCIAL AUDIT\n")
        md.append(f"- **Today's Realized Revenue:** `${metrics['daily_revenue_usd']:,.2f}` (`₹{metrics['daily_revenue_usd']*USD_TO_INR_DEFAULT:,.2f}`)")
        md.append(f"- **7-Day Rolling Revenue:** `${metrics['weekly_revenue_usd']:,.2f}` (`₹{metrics['weekly_revenue_usd']*USD_TO_INR_DEFAULT:,.2f}`)")
        md.append(f"- **Active Pipeline Expected Value:** **`${metrics['total_pipeline_ev_usd']:,.2f}`** across `{metrics['active_deals_count']}` live accounts\n")

        md.append("## 📈 2. PIPELINE CONVERSION & STAGE STATUS\n")
        md.append("| Company | Contact | Stage | Potential Value | Next Scheduled Step |")
        md.append("| :--- | :--- | :--- | :--- | :--- |")
        for deal in metrics["top_active_deals"][:5]:
            md.append(f"| **{deal['Company']}** | {deal['Contact Name']} | `{deal['Stage']}` | `${deal['Potential Revenue (USD)']}` | {deal['Next Action'][:40]}... |")
        md.append("")

        md.append("## 🌅 3. TOMORROW'S MORNING ATTACK VECTOR\n")
        md.append("1. Follow up on all pending proposals sent in the last 48 hours.")
        md.append("2. Batch generate 20 new enriched prospect dossiers for US/UK SaaS clients.")
        md.append("3. Verify all pending escrow milestones and invoice releases.")
        md.append("\n---\n*Status: System Ready for Overnight Autonomous Standby.*")

        full_content = "\n".join(md)

        dated_path = REPORTS_DIR / f"DAILY_EVENING_CEO_BRIEF_{date_str}.md"
        canonical_path = REPORTS_DIR / "DAILY_EVENING_CEO_BRIEF.md"

        for p in [dated_path, canonical_path]:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(full_content)
            except Exception as e:
                log_event(f"Error writing evening brief to {p}: {e}", level="WARN")

        log_event(f"Generated Evening CEO Briefing: {dated_path.name}")
        return dated_path, full_content


# ==============================================================================
# SYSTEM HEALTH & ASSET INVENTORY ENGINE
# ==============================================================================

class HealthCheck:
    """Performs deep sanity checks on data integrity and asset repository."""

    @classmethod
    def run_audit(cls) -> Dict[str, Any]:
        issues = []

        file_inventory = {
            "Pipeline Tracker CSV": PIPELINE_CSV,
            "Money Dashboard CSV": MONEY_CSV,
            "Demo Lead List CSV": DEMO_LEADS_CSV,
            "Pitch Toolkit Master": PITCH_TOOLKIT_MD,
            "Reports Directory": REPORTS_DIR,
            "Logs Directory": LOGS_DIR,
            "Backups Directory": BACKUPS_DIR,
        }

        inventory_status = []
        for name, path in file_inventory.items():
            exists = path.exists()
            size = path.stat().st_size if exists and path.is_file() else (len(list(path.iterdir())) if exists and path.is_dir() else 0)
            status_str = "OK" if exists else "MISSING"
            if not exists:
                issues.append(f"{name} is missing at {path}")
            inventory_status.append({
                "Asset": name,
                "Path": str(path),
                "Exists": exists,
                "Size_or_Count": size,
                "Status": status_str
            })

        pipeline_data = load_pipeline_data()
        money_data = load_money_data()

        backup_files = list(BACKUPS_DIR.glob("*.*")) if BACKUPS_DIR.exists() else []
        report_files = list(REPORTS_DIR.glob("*.md")) if REPORTS_DIR.exists() else []

        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "inventory": inventory_status,
            "pipeline_count": len(pipeline_data),
            "money_records_count": len(money_data),
            "backups_count": len(backup_files),
            "reports_count": len(report_files),
            "issues": issues,
            "system_status": "HEALTHY" if not issues else "ATTENTION_REQUIRED"
        }


# ==============================================================================
# TERMINAL UI & INTERACTIVE DASHBOARD VIEWS
# ==============================================================================

class TerminalUI:
    """Renders formatted ASCII tables, status dashboards and interactive menus."""

    @staticmethod
    def print_banner():
        print(colorize("=" * 78, ConsoleStyle.CYAN))
        print(colorize("   GLOBAL DOLLAR ECONOMY OS  |  24/7 DAEMON & CRM DISPATCHER", ConsoleStyle.BOLD + ConsoleStyle.WHITE))
        print(colorize("   Founder: Adi  |  Bangalore, India  |  B2B Lead Gen & Intelligence", ConsoleStyle.DIM))
        print(colorize("=" * 78, ConsoleStyle.CYAN))

    @staticmethod
    def render_command_center():
        """Renders live ASCII Dollar Command Center."""
        metrics = AnalyticsEngine.calculate_metrics()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + colorize("+----------------------------------------------------------------------------+", ConsoleStyle.CYAN))
        print(colorize(f"|  LIVE GLOBAL DOLLAR COMMAND CENTER               Timestamp: {now_str} |", ConsoleStyle.BOLD + ConsoleStyle.WHITE))
        print(colorize("+----------------------------------------------------------------------------+", ConsoleStyle.CYAN))

        rev_usd_str = f"${metrics['total_revenue_usd']:,.2f}"
        rev_inr_str = f"INR {metrics['total_revenue_inr']:,.2f}"
        profit_usd_str = f"${metrics['total_profit_usd']:,.2f}"
        pph_str = f"${metrics['blended_pph']:.2f}/hr"
        received_str = f"${metrics['total_received_usd']:,.2f}"
        pending_str = f"${metrics['total_pending_usd']:,.2f}"

        print(colorize("|  REVENUE & CASH FLOW (REALIZED & INVOICED)                                 |", ConsoleStyle.YELLOW))
        print(f"|  Total Gross Revenue : {colorize(rev_usd_str.ljust(15), ConsoleStyle.GREEN)} ({rev_inr_str})")
        print(f"|  Realized Cash       : {colorize(received_str.ljust(15), ConsoleStyle.GREEN)} Pending / Escrow : {pending_str}")
        print(f"|  Net Profit (USD)    : {colorize(profit_usd_str.ljust(15), ConsoleStyle.GREEN)} Margin           : {metrics['profit_margin_pct']:.1f}%")
        print(f"|  Effective Rate      : {colorize(pph_str.ljust(15), ConsoleStyle.CYAN)} Total Hours Logged: {metrics['total_hours']:.1f} hrs")
        print(colorize("+----------------------------------------------------------------------------+", ConsoleStyle.CYAN))

        pipe_val_str = f"${metrics['total_pipeline_val_usd']:,.2f}"
        pipe_ev_str = f"${metrics['total_pipeline_ev_usd']:,.2f}"
        active_cnt_str = str(metrics['active_deals_count'])

        print(colorize("|  PIPELINE & EXPECTED VALUE (EV) MATRIX                                     |", ConsoleStyle.YELLOW))
        print(f"|  Active Deals        : {colorize(active_cnt_str.ljust(15), ConsoleStyle.BOLD)} Blended Win Prob : {metrics['weighted_win_prob']:.1f}%")
        print(f"|  Gross Pipeline      : {colorize(pipe_val_str.ljust(15), ConsoleStyle.WHITE)} Active Pipeline EV: {colorize(pipe_ev_str, ConsoleStyle.GREEN)}")
        print(colorize("+----------------------------------------------------------------------------+", ConsoleStyle.CYAN))

        print(colorize("|  TOP ACTIVE DEALS IN PIPELINE                                              |", ConsoleStyle.YELLOW))
        print("|  " + f"{'Company':<22} {'Contact':<18} {'Stage':<12} {'Value':<10} {'EV':<10}")
        print("|  " + "-" * 72)
        if metrics["top_active_deals"]:
            for d in metrics["top_active_deals"][:5]:
                comp = d["Company"][:20]
                contact = d["Contact Name"][:16]
                stage = d["Stage"][:10]
                val = f"${d['Potential Revenue (USD)']:.0f}"
                ev = f"${d['Expected Value (USD)']:.0f}"
                print(f"|  {comp:<22} {contact:<18} {stage:<12} {val:<10} {ev:<10}")
        else:
            print("|  No active deals currently in pipeline tracker.")

        print(colorize("+----------------------------------------------------------------------------+", ConsoleStyle.CYAN))

        print(colorize("|  ACTION ITEMS & DISPATCH QUEUE                                             |", ConsoleStyle.YELLOW))
        if metrics["deals_due_today"]:
            for d in metrics["deals_due_today"]:
                act_snip = d['Next Action'][:45]
                print(f"|  [DUE TODAY] {d['Company']} ({d['Contact Name']}): {act_snip}")
        elif metrics["overdue_deals"]:
            for d in metrics["overdue_deals"][:2]:
                act_snip = d['Next Action'][:47]
                print(f"|  [OVERDUE] {d['Company']} ({d['Contact Name']}): {act_snip}")
        else:
            print("|  [ALL CLEAR] No overdue follow-ups. Ready to dispatch outbound batches.")

        print(colorize("+----------------------------------------------------------------------------+", ConsoleStyle.CYAN) + "\n")

    @staticmethod
    def interactive_add_lead():
        """Interactive form to add a new lead to pipeline tracker."""
        print("\n" + colorize("--- ADD NEW LEAD / CLIENT TO PIPELINE TRACKER ---", ConsoleStyle.BOLD + ConsoleStyle.CYAN))
        try:
            company = input("Company Name: ").strip()
            if not company:
                print(colorize("Company name cannot be empty. Aborted.", ConsoleStyle.RED))
                return

            contact_name = input("Contact Name (e.g. Marcus Vance): ").strip()
            contact_title = input("Contact Title (e.g. Head of Growth / VP Sales): ").strip()
            channel = input("Outreach Channel [LinkedIn / Upwork / Email / Referral] (Default: LinkedIn): ").strip() or "LinkedIn"
            service = input("Service Offered [Lead Gen / Market Intel / Data Research / Custom] (Default: Lead Gen): ").strip() or "Lead Gen"
            stage = input("Pipeline Stage [Lead / Outreach / Meeting / Proposal / Negotiation / Won] (Default: Lead): ").strip() or "Lead"
            
            pot_rev_str = input("Potential Revenue in USD (e.g. 1200): ").strip() or "1000"
            pot_rev = clean_float(pot_rev_str, 1000.0)

            prob_str = input("Probability % [0-100] (Default: 50): ").strip() or "50"
            prob = clean_float(prob_str, 50.0)

            ev = round(pot_rev * (prob / 100.0), 2)
            print(f"-> Calculated Expected Value (EV): ${ev:,.2f}")

            next_action = input("Next Action (e.g. Send customized 500 ICP sample list): ").strip()
            next_action_date = input("Next Action Date [YYYY-MM-DD] (Default: Tomorrow): ").strip()
            if not next_action_date:
                next_action_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

            notes = input("Key Notes / Scope summary: ").strip()

            lead_data = {
                "Date Added": datetime.date.today().strftime("%Y-%m-%d"),
                "Company": company,
                "Contact Name": contact_name,
                "Contact Title": contact_title,
                "Channel": channel,
                "Service Offered": service,
                "Stage": stage,
                "Potential Revenue (USD)": pot_rev,
                "Probability (%)": prob,
                "Expected Value (USD)": ev,
                "Next Action": next_action,
                "Next Action Date": next_action_date,
                "Notes": notes,
                "Status": "Active" if stage.lower() not in ["won", "lost"] else ("Won" if stage.lower() == "won" else "Lost")
            }

            if save_pipeline_lead(lead_data):
                print(colorize(f"\n[SUCCESS] Successfully added {company} to pipeline_tracker.csv!", ConsoleStyle.GREEN))
            else:
                print(colorize("\n[ERROR] Failed to save lead record.", ConsoleStyle.RED))
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")

    @staticmethod
    def interactive_log_revenue():
        """Interactive form to log received or invoiced dollar revenue."""
        print("\n" + colorize("--- LOG REVENUE / PAYMENT RECEIVED ---", ConsoleStyle.BOLD + ConsoleStyle.GREEN))
        try:
            client = input("Client / Platform Name (e.g. Elevate Talent Partners): ").strip()
            if not client:
                print(colorize("Client name cannot be empty. Aborted.", ConsoleStyle.RED))
                return

            source = input("Revenue Source [B2B Client / Upwork / Retainer / Direct] (Default: B2B Client): ").strip() or "B2B Client"
            service = input("Service / Deliverable (e.g. Data Research & Lead List Building): ").strip() or "Lead Gen & Data Research"
            
            rev_usd_str = input("Revenue in USD (e.g. 600): ").strip() or "500"
            rev_usd = clean_float(rev_usd_str, 500.0)

            cost_str = input("Direct Cost in USD [Tools/APIs/Proxy] (Default: 0): ").strip() or "0"
            cost_usd = clean_float(cost_str, 0.0)

            hours_str = input("Hours Spent on Delivery (Default: 5.0): ").strip() or "5.0"
            hours = clean_float(hours_str, 5.0)

            status = input("Payment Status [Received / Pending / In Escrow] (Default: Received): ").strip() or "Received"
            method = input("Payment Method [Wise / Stripe / Wire / Upwork Escrow] (Default: Wise): ").strip() or "Wise"
            recurring = input("Is this Recurring Monthly Retainer? [Yes / No] (Default: No): ").strip() or "No"
            notes = input("Delivery Notes (e.g. Delivered 1,000 verified leads with 0% bounce): ").strip()

            entry_data = {
                "Date": datetime.date.today().strftime("%Y-%m-%d"),
                "Source": source,
                "Client/Platform": client,
                "Service/Product": service,
                "Revenue (USD)": rev_usd,
                "Cost (USD)": cost_usd,
                "Hours Spent": hours,
                "Payment Status": status,
                "Payment Method": method,
                "Recurring?": recurring,
                "Notes": notes
            }

            if save_money_entry(entry_data):
                inr_equiv = rev_usd * USD_TO_INR_DEFAULT
                profit = rev_usd - cost_usd
                pph = profit / hours if hours > 0 else profit
                print(colorize(f"\n[SUCCESS] Logged ${rev_usd:.2f} (INR {inr_equiv:,.2f}) | Profit: ${profit:.2f} (${pph:.2f}/hr)", ConsoleStyle.GREEN))
            else:
                print(colorize("\n[ERROR] Failed to record transaction.", ConsoleStyle.RED))
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")

    @staticmethod
    def run_prospect_enrichment_demo():
        """Runs the B2B AI Prospect Enrichment Demo."""
        print("\n" + colorize("--- AI PROSPECT ENRICHMENT & SCORING DEMO ---", ConsoleStyle.BOLD + ConsoleStyle.MAGENTA))
        print("Enriching live sample leads from demo database...\n")

        demo_leads = []
        if DEMO_LEADS_CSV.exists():
            try:
                with open(DEMO_LEADS_CSV, mode="r", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        if any(r.values()):
                            demo_leads.append(r)
            except Exception as e:
                log_event(f"Error reading demo lead list: {e}", level="WARN")

        if not demo_leads:
            demo_leads = [
                {
                    "Company Name": "CloudScale AI",
                    "Contact Name": "Marcus Vance",
                    "Title": "VP of Sales & Growth",
                    "Industry": "B2B SaaS / DevOps",
                    "Recent Trigger Event": "Raised $8.5M Series A; actively hiring 4 enterprise SDRs"
                },
                {
                    "Company Name": "RevOptima Solutions",
                    "Contact Name": "Eleanor Wright",
                    "Title": "Head of Revenue Operations",
                    "Industry": "B2B SaaS / SalesTech",
                    "Recent Trigger Event": "Launched new European localization features and expanded into DACH"
                },
                {
                    "Company Name": "Nexus Digital Media",
                    "Contact Name": "David Sterling",
                    "Title": "Managing Director & Founder",
                    "Industry": "Performance Marketing Agency",
                    "Recent Trigger Event": "Won Best UK Performance Agency at 2026 Agency Awards"
                }
            ]

        for idx, raw_lead in enumerate(demo_leads[:4], start=1):
            enriched = ProspectEnricher.enrich_prospect(raw_lead)
            score_color = ConsoleStyle.GREEN if enriched["Lead Score"] == "Hot" else ConsoleStyle.YELLOW
            score_str = f"{enriched['Lead Score']} ({enriched['Score Value']}/100)"

            print(colorize(f"[{idx}] {enriched['Company']} - {enriched['Contact Name']} ({enriched['Title']})", ConsoleStyle.BOLD + ConsoleStyle.WHITE))
            print(f"    * Industry & Trigger : {enriched['Industry']} | [{enriched['Trigger Category']}] {enriched['Trigger Details']}")
            print(f"    * Lead Quality Score : {colorize(score_str, score_color)}")
            print(f"    * Recommended Service: {enriched['Recommended Service Angle']}")
            print(f"    * AI Synthesized Hook: {colorize(enriched['Synthesized Icebreaker'], ConsoleStyle.CYAN)}")
            print("    " + "-" * 68)

        print(colorize("\n[TIP] Prospect enrichment engine is ready to batch-enrich custom lead lists into CRM.", ConsoleStyle.DIM))

    @staticmethod
    def render_health_check():
        """Renders System Health & Asset Inventory report."""
        audit = HealthCheck.run_audit()
        print("\n" + colorize("--- SYSTEM HEALTH CHECK & ASSET INVENTORY ---", ConsoleStyle.BOLD + ConsoleStyle.CYAN))
        print(f"Timestamp: {audit['timestamp']} | Status: {colorize(audit['system_status'], ConsoleStyle.GREEN if audit['system_status'] == 'HEALTHY' else ConsoleStyle.RED)}\n")

        print(f"{'Asset Name':<28} {'Status':<12} {'Size / Items':<15} {'Path'}")
        print("-" * 78)
        for item in audit["inventory"]:
            status_c = colorize(item["Status"].ljust(10), ConsoleStyle.GREEN if item["Exists"] else ConsoleStyle.RED)
            print(f"{item['Asset']:<28} {status_c} {str(item['Size_or_Count']).ljust(15)} {item['Path']}")

        print("-" * 78)
        print(f"Total Pipeline Leads Tracked  : {colorize(str(audit['pipeline_count']), ConsoleStyle.BOLD)}")
        print(f"Total Revenue Entries Tracked : {colorize(str(audit['money_records_count']), ConsoleStyle.BOLD)}")
        print(f"Automated Markdown Briefings  : {colorize(str(audit['reports_count']), ConsoleStyle.BOLD)}")
        print(f"Historical Backup Snapshots   : {colorize(str(audit['backups_count']), ConsoleStyle.BOLD)}")
        if audit["issues"]:
            print(colorize("\n[WARNINGS DETECTED]:", ConsoleStyle.YELLOW))
            for iss in audit["issues"]:
                print(f"  * {iss}")
        else:
            print(colorize("\n[ALL SYSTEMS NOMINAL] Zero integrity errors detected across all core OS databases.", ConsoleStyle.GREEN))


# ==============================================================================
# CONTINUOUS 24/7 DAEMON ENGINE
# ==============================================================================

class DaemonRunner:
    """Continuous background loop monitoring files, computing EV, and generating scheduled reports."""

    def __init__(self, check_interval_seconds: int = 60):
        self.interval = max(5, check_interval_seconds)
        self.running = False
        self.last_pipeline_mtime = 0.0
        self.last_money_mtime = 0.0
        self.last_morning_brief_date = None
        self.last_evening_brief_date = None

    def start(self):
        self.running = True
        log_event("Starting 24/7 Global Dollar Automation Daemon loop...")
        print(colorize(f"\n[DAEMON INITIALIZED] Running continuous monitoring loop (Interval: {self.interval}s).", ConsoleStyle.GREEN))
        print(colorize("Press Ctrl+C at any time to return to menu or stop.\n", ConsoleStyle.DIM))

        try:
            while self.running:
                now = datetime.datetime.now()
                today_date = now.date()

                # 1. File Modification Checks
                if PIPELINE_CSV.exists():
                    mtime = PIPELINE_CSV.stat().st_mtime
                    if self.last_pipeline_mtime != 0.0 and mtime > self.last_pipeline_mtime:
                        log_event("Detected update in pipeline_tracker.csv. Recalculating Expected Value...")
                        metrics = AnalyticsEngine.calculate_metrics()
                        print(colorize(f"[{now.strftime('%H:%M:%S')}] Pipeline Updated: {metrics['active_deals_count']} active deals | EV: ${metrics['total_pipeline_ev_usd']:,.2f}", ConsoleStyle.CYAN))
                    self.last_pipeline_mtime = mtime

                if MONEY_CSV.exists():
                    mtime = MONEY_CSV.stat().st_mtime
                    if self.last_money_mtime != 0.0 and mtime > self.last_money_mtime:
                        log_event("Detected update in money_dashboard.csv. Recalculating Financial Metrics...")
                        metrics = AnalyticsEngine.calculate_metrics()
                        print(colorize(f"[{now.strftime('%H:%M:%S')}] Revenue Updated: Total Gross ${metrics['total_revenue_usd']:,.2f} | Profit: ${metrics['total_profit_usd']:,.2f}", ConsoleStyle.GREEN))
                    self.last_money_mtime = mtime

                # 2. Scheduled Morning CEO Briefing Trigger
                if now.hour >= MORNING_BRIEF_HOUR and self.last_morning_brief_date != today_date:
                    log_event("Triggering automated Daily Morning CEO Briefing generation...")
                    path, _ = BriefingGenerator.generate_morning_brief(today_date)
                    self.last_morning_brief_date = today_date
                    print(colorize(f"[{now.strftime('%H:%M:%S')}] [AUTO-DISPATCH] Generated Morning CEO Briefing -> {path.name}", ConsoleStyle.GREEN))

                # 3. Scheduled Evening CEO Briefing Trigger
                if now.hour >= EVENING_BRIEF_HOUR and self.last_evening_brief_date != today_date:
                    log_event("Triggering automated Daily Evening CEO Briefing generation...")
                    path, _ = BriefingGenerator.generate_evening_brief(today_date)
                    self.last_evening_brief_date = today_date
                    print(colorize(f"[{now.strftime('%H:%M:%S')}] [AUTO-DISPATCH] Generated Evening CEO Briefing -> {path.name}", ConsoleStyle.BLUE))

                time.sleep(self.interval)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        log_event("24/7 Global Dollar Automation Daemon stopped by operator.")
        print(colorize("\n[DAEMON STOPPED] Returning to Command Center...\n", ConsoleStyle.YELLOW))


# ==============================================================================
# MAIN CLI & DISPATCH CONTROLLER
# ==============================================================================

def main_interactive_menu():
    """Runs the primary interactive command line interface."""
    while True:
        TerminalUI.print_banner()
        print(colorize("COMMAND MENU:", ConsoleStyle.BOLD + ConsoleStyle.WHITE))
        print("  " + colorize("[1]", ConsoleStyle.CYAN) + " View Live Dollar Command Center")
        print("  " + colorize("[2]", ConsoleStyle.CYAN) + " Add New Lead / Client to Pipeline Tracker")
        print("  " + colorize("[3]", ConsoleStyle.CYAN) + " Log New Revenue / Payment Received")
        print("  " + colorize("[4]", ConsoleStyle.CYAN) + " Run AI Prospect Enrichment Demo")
        print("  " + colorize("[5]", ConsoleStyle.CYAN) + " Generate Today's Morning CEO Briefing")
        print("  " + colorize("[6]", ConsoleStyle.CYAN) + " Run Health Check & Asset Inventory")
        print("  " + colorize("[7]", ConsoleStyle.CYAN) + " Generate Today's Evening CEO Briefing")
        print("  " + colorize("[8]", ConsoleStyle.CYAN) + " Start Continuous 24/7 Background Daemon Loop")
        print("  " + colorize("[0]", ConsoleStyle.RED) + " Exit OS")
        print(colorize("-" * 78, ConsoleStyle.DIM))

        try:
            choice = input(colorize("Select Option [0-8]: ", ConsoleStyle.BOLD)).strip()
            if choice == "1":
                TerminalUI.render_command_center()
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "2":
                TerminalUI.interactive_add_lead()
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "3":
                TerminalUI.interactive_log_revenue()
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "4":
                TerminalUI.run_prospect_enrichment_demo()
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "5":
                path, preview = BriefingGenerator.generate_morning_brief()
                print(colorize(f"\n[SUCCESS] Generated Morning CEO Briefing at: {path}", ConsoleStyle.GREEN))
                print("\n" + colorize("--- PREVIEW ---", ConsoleStyle.CYAN))
                print("\n".join(preview.splitlines()[:18]))
                print(colorize("... [Full briefing saved to disk]", ConsoleStyle.DIM))
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "6":
                TerminalUI.render_health_check()
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "7":
                path, preview = BriefingGenerator.generate_evening_brief()
                print(colorize(f"\n[SUCCESS] Generated Evening CEO Briefing at: {path}", ConsoleStyle.GREEN))
                print("\n" + colorize("--- PREVIEW ---", ConsoleStyle.CYAN))
                print("\n".join(preview.splitlines()[:16]))
                input(colorize("\nPress Enter to return to menu...", ConsoleStyle.DIM))
            elif choice == "8":
                daemon = DaemonRunner(check_interval_seconds=10)
                daemon.start()
            elif choice == "0":
                print(colorize("\nExiting Global Dollar Economy OS. Keep compounding.\n", ConsoleStyle.GREEN))
                break
            else:
                print(colorize("Invalid selection. Please choose an option from 0 to 8.\n", ConsoleStyle.YELLOW))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


def cli_entrypoint():
    """Command-line argument parser for automated daemon / cron invocations."""
    parser = argparse.ArgumentParser(
        description="Global Dollar Economy OS - 24/7 Daemon & CRM Dispatcher",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--daemon", "--loop", action="store_true", help="Launch continuous 24/7 background monitoring daemon loop")
    parser.add_argument("--interval", type=int, default=60, help="Check interval for daemon loop in seconds (default: 60)")
    parser.add_argument("--morning-brief", action="store_true", help="Generate today's Morning CEO Briefing in Markdown and exit")
    parser.add_argument("--evening-brief", action="store_true", help="Generate today's Evening CEO Briefing in Markdown and exit")
    parser.add_argument("--status", "--dashboard", action="store_true", help="Print live Dollar Command Center ASCII dashboard and exit")
    parser.add_argument("--health", action="store_true", help="Run System Health Check & Asset Inventory audit and exit")
    parser.add_argument("--enrich", action="store_true", help="Run AI Prospect Enrichment Demo and exit")

    args = parser.parse_args()

    if args.daemon:
        TerminalUI.print_banner()
        daemon = DaemonRunner(check_interval_seconds=args.interval)
        daemon.start()
    elif args.morning_brief:
        path, _ = BriefingGenerator.generate_morning_brief()
        print(f"Generated Morning CEO Briefing: {path}")
    elif args.evening_brief:
        path, _ = BriefingGenerator.generate_evening_brief()
        print(f"Generated Evening CEO Briefing: {path}")
    elif args.status:
        TerminalUI.render_command_center()
    elif args.health:
        TerminalUI.render_health_check()
    elif args.enrich:
        TerminalUI.run_prospect_enrichment_demo()
    else:
        main_interactive_menu()


if __name__ == "__main__":
    cli_entrypoint()
