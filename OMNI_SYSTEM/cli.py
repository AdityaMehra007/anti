"""
Master Command Line Interface for OMNI_SYSTEM.
Usage:
    python -m OMNI_SYSTEM.cli --status
    python -m OMNI_SYSTEM.cli --hunt
    python -m OMNI_SYSTEM.cli --launch
    python -m OMNI_SYSTEM.cli --json
    python -m OMNI_SYSTEM.cli --brief
"""

import sys
import json
import argparse
import webbrowser
import subprocess
from pathlib import Path

# Always ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from OMNI_SYSTEM.core.config import settings, ROOT_DIR
from OMNI_SYSTEM.orchestrator import orchestrator


def cmd_status() -> None:
    """Print full executive daily briefing."""
    print(orchestrator.format_daily_briefing())


def cmd_json() -> None:
    """Print full JSON telemetry payload."""
    status = orchestrator.get_full_status()
    print(json.dumps(status, indent=2))


def cmd_hunt() -> None:
    """
    Run daily cash hunt: audit current daily net profit,
    display top target deals to reach daily quotas, and output instant pay links.
    """
    telemetry = orchestrator.aggregate_telemetry()
    print("=" * 74)
    print("  OMNI-SYSTEM :: DAILY CASH HUNTER & QUOTA ENGINE")
    print(f"  OPERATOR: {settings.FOUNDER_NAME} | PRIMARY UPI: {settings.PRIMARY_UPI_ID}")
    print("=" * 74)
    print(f"  Today's Net Profit:        INR {telemetry.today_net_profit_inr:,.2f}")
    print(f"  Daily Target:              INR {telemetry.daily_target_inr:,.2f}")
    print(f"  Achievement:               {telemetry.target_achievement_pct:.1f}%")

    if telemetry.today_net_profit_inr >= telemetry.daily_target_inr:
        surplus = telemetry.today_net_profit_inr - telemetry.daily_target_inr
        print(f"  Pacing:                    QUOTA CRUSHED! Surplus: +INR {surplus:,.2f}")
    else:
        gap = telemetry.daily_target_inr - telemetry.today_net_profit_inr
        print(f"  Pacing:                    HUNTING! Remaining to Target: INR {gap:,.2f}")

    print("\n  [TOP HIGH-LEVERAGE B2B TARGETS IN PLAY]")
    top_deals = [
        {"client": "Porter (SmartMove Logistics)", "offering": "Agentic Operations Automation Retainer", "val": 150000, "prob": 0.50},
        {"client": "Shadowfax Tech", "offering": "Express Dispatch API Integration", "val": 120000, "prob": 0.45},
        {"client": "BrowserStack", "offering": "Enterprise QA Copilot Pipeline", "val": 180000, "prob": 0.40},
        {"client": "Ather Energy", "offering": "EV Telemetry AI Data Operations", "val": 95000, "prob": 0.35},
        {"client": "Postman Bengaluru", "offering": "Autonomous API Workflow Retainer", "val": 200000, "prob": 0.30},
    ]
    for idx, d in enumerate(top_deals, 1):
        print(f"    {idx}. {d['client']:<22} | {d['offering']:<35} | INR {d['val']:>8,d} ({int(d['prob']*100)}% prob)")

    print("\n  [INSTANT GLOBAL COLLECTION RAILS]")
    print(f"    - Instant Domestic UPI:    upi://pay?pa={settings.PRIMARY_UPI_ID}&pn=AdityaMehra&cu=INR")
    print(f"    - Worldwide Direct Pay:    file:///{ROOT_DIR.as_posix()}/apps/global_pay/index.html")
    print(f"    - B2B 1-Click Outbound:    file:///{ROOT_DIR.as_posix()}/apps/daily_cash_machine/b2b_strike_launcher.html")
    print("=" * 74)


def cmd_launch() -> None:
    """Launch Master Mission Control HUD in default browser and verify daemons."""
    health = orchestrator.check_subsystems()
    print("Checking Subsystems...")
    print(f"  - Revenue OS (8765):       {'[ONLINE]' if health['revenue_os'].is_live else '[OFFLINE]'}")
    print(f"  - Global Capital OS (8766): {'[ONLINE]' if health['global_capital_os'].is_live else '[OFFLINE]'}")

    hud_path = ROOT_DIR / "apps" / "omni_command" / "index.html"
    if hud_path.exists():
        print(f"\nOpening Sovereign Mission Control HUD: {hud_path}")
        webbrowser.open(hud_path.as_uri())
    else:
        # Fallback to apps index
        apps_index = ROOT_DIR / "apps" / "index.html"
        print(f"\nOpening Master Apps Index: {apps_index}")
        webbrowser.open(apps_index.as_uri())


def cmd_brief() -> None:
    """Print ultra-concise executive summary."""
    t = orchestrator.aggregate_telemetry()
    status_str = "CRUSHING" if t.target_achievement_pct >= 100 else "PACING"
    print(
        f"[OMNI-SYSTEM] Operator: {t.operator} | "
        f"Today Net: INR {t.today_net_profit_inr:,.0f} ({t.target_achievement_pct:.0f}% of Target) | "
        f"Pipeline: INR {t.active_pipeline_inr:,.0f} | "
        f"Status: {status_str}"
    )


def cmd_siphon() -> None:
    """Print World GDP Daily Siphon radar and corridor flow."""
    from OMNI_SYSTEM.world_gdp_siphon import siphon_engine
    rev = orchestrator.get_revenue_telemetry()
    today_gross = rev.get("gross_revenue_inr", 47131.33)
    print(siphon_engine.format_siphon_briefing(today_gross))


def main() -> None:
    parser = argparse.ArgumentParser(description="OMNI-SYSTEM Universal Autonomous Operating System")
    parser.add_argument("--status", action="store_true", help="Display full executive briefing and telemetry")
    parser.add_argument("--hunt", action="store_true", help="Audit daily profit, view pipeline deals and instant pay links")
    parser.add_argument("--launch", action="store_true", help="Verify daemons and launch Master Mission Control HUD")
    parser.add_argument("--json", action="store_true", help="Output raw telemetry JSON")
    parser.add_argument("--brief", action="store_true", help="Print 1-line executive brief")
    parser.add_argument("--siphon", "--world-gdp", action="store_true", dest="siphon", help="Audit World GDP daily extraction flows")
    parser.add_argument("command", nargs="?", choices=["status", "hunt", "launch", "json", "brief", "siphon", "world-gdp"], help="Command alias")

    args = parser.parse_args()

    cmd = args.command or (
        "status" if args.status else
        "hunt" if args.hunt else
        "launch" if args.launch else
        "json" if args.json else
        "brief" if args.brief else
        "siphon" if args.siphon else
        "status"
    )

    if cmd in ("siphon", "world-gdp"):
        cmd_siphon()
    elif cmd == "status":
        cmd_status()
    elif cmd == "hunt":
        cmd_hunt()
    elif cmd == "launch":
        cmd_launch()
    elif cmd == "json":
        cmd_json()
    elif cmd == "brief":
        cmd_brief()


if __name__ == "__main__":
    main()

