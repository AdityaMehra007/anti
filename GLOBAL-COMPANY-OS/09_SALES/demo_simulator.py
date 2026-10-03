#!/usr/bin/env python3
"""
TradeNexus Enterprise Sales Demo Simulator & Objection Handling Trainer
Allows founder and AI sales agents to simulate realistic enterprise customer interactions.
"""

import sys
import time

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILES = {
    "1": {
        "company": "Sansera Engineering Limited",
        "exec": "B. R. Preetham (Group CEO & Executive Director)",
        "pain": "EU CBAM carbon price liabilities on steel forged components (HS 7326.90)",
        "objection": "We already have an in-house EXIM team and 3 CHAs. Why do we need this?",
        "counter": "CHAs handle physical port clearing, not upstream carbon calculation and 8-digit ITC-HS validation. TradeNexus gives your EXIM team a pre-filing shield preventing €2,400 port demurrage charges.",
        "deal_size": "₹25,000 Pilot -> ₹45,000/mo Retainer"
    },
    "2": {
        "company": "Dynamatic Technologies Limited",
        "exec": "Udayant Malhoutra (CEO & Managing Director)",
        "pain": "SCOMET Category 6 aerospace dual-use clearance delays on aircraft assemblies (HS 8803.30)",
        "objection": "Aerospace parts require strict DGFT SCOMET licensing. Can software really guarantee compliance?",
        "counter": "TradeNexus validates end-user certificates and SCOMET Annexure II parameters against live DGFT gazette notifications, ensuring 0% license discrepancy before ICEGATE submission.",
        "deal_size": "₹25,000 Pilot -> ₹75,000/mo Retainer"
    },
    "3": {
        "company": "Kemwell Chemical Industries",
        "exec": "Vikram Kemwell (VP Supply Chain & Operations)",
        "pain": "EU REACH compliance & GHS hazardous declaration on organic chemical esters (HS 2915.39)",
        "objection": "Can we test this for free before committing funds?",
        "counter": "The ₹25,000 pilot includes customized chemical SDS cross-referencing and is backed by our 100% money-back demurrage guarantee. If we miss an error, the pilot is completely free.",
        "deal_size": "₹25,000 Pilot -> ₹35,000/mo Retainer"
    }
}

def run_simulation():
    print("=" * 70)
    print("TRADENEXUS AI — ENTERPRISE SALES DEMO SIMULATION & CLOSING ENGINE")
    print("=" * 70)
    print("Select a target exporter account for live simulation:")
    for k, v in PROFILES.items():
        print(f"[{k}] {v['company']} ({v['exec']})")
    
    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"
    target = PROFILES.get(choice, PROFILES["1"])
    
    print("\n" + "-" * 70)
    print(f"SIMULATION ENGAGED: {target['company']}")
    print(f"EXECUTIVE: {target['exec']}")
    print(f"PRIMARY PAIN POINT: {target['pain']}")
    print("-" * 70)
    
    print("\n[FOUNDER SCRIPT]:")
    print("  'Good morning! We audited your recent EU export shipments and found a 6-digit")
    print("   tariff truncation and missing EORI risk that could cost €2,400 in demurrage.'")
    
    time.sleep(1)
    print(f"\n[PROSPECT OBJECTION from {target['exec']}]:")
    print(f"  \"{target['objection']}\"")
    
    time.sleep(1)
    print("\n[WINNING CLOSING COUNTER]:")
    print(f"  \"{target['counter']}\"")
    
    print(f"\n[CLOSING OUTCOME]:")
    print(f"  Deal Size: {target['deal_size']}")
    print("  Contract Dispatched: 09_SALES/contracts/ pre-filled pilot agreement.")
    print("  Status: READY_FOR_COUNTERSIGNATURE")
    print("=" * 70)

if __name__ == "__main__":
    run_simulation()
