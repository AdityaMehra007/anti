"""
ANTIGRAVITY OMNIVERSE: CHIPFLOW AI PILOT OUTREACH ENGINE
========================================================
Generates target manifest and multi-touch technical outreach sequences
for 250 fabless Edge AI chip VP/Directors of Silicon Engineering.
"""
import json
from typing import Dict, Any, List
from pathlib import Path

class ChipFlowPilotOutreach:
    """Manages the pilot commercial rollout for ChipFlow AI."""

    @classmethod
    def generate_pilot_manifest(cls, limit: int = 250) -> List[Dict[str, Any]]:
        """Generates representative target manifest for fabless AI chip leadership."""
        sample_companies = [
            ("Hailo Technologies", "Israel / US", "Edge AI Accelerators for Vision"),
            ("Tenstorrent", "Toronto / Austin", "RISC-V & Chiplet AI Processors"),
            ("Ambarella", "Santa Clara, CA", "Low-Power Edge AI Silicon"),
            ("SiMa.ai", "San Jose, CA", "Machine Learning SoC for Robotics"),
            ("Axelera AI", "Eindhoven / Leuven", "In-Memory Computing NPU"),
            ("Syntiant", "Irvine, CA", "Ultra-Low Power Neural Decision Processors"),
            ("BrainChip", "Laguna Hills, CA", "Neuromorphic Processing Units"),
            ("Untether AI", "Toronto, ON", "Energy-Centric At-Memory Compute"),
            ("Mindgrove Technologies", "Chennai / Bengaluru", "Edge IoT Microcontrollers"),
            ("InCore Semiconductors", "Bengaluru, India", "Customizable RISC-V Processor Cores")
        ]
        
        titles = [
            "VP of Silicon Engineering",
            "Head of Advanced Packaging & OSAT",
            "Chief Technology Officer",
            "Director of Foundry Operations",
            "VP of Hardware Architecture"
        ]

        targets = []
        for i in range(1, limit + 1):
            comp_idx = (i - 1) % len(sample_companies)
            comp_name, geo, focus = sample_companies[comp_idx]
            title = titles[(i - 1) % len(titles)]
            targets.append({
                "target_id": f"TGT-FABLESS-{i:03d}",
                "name": f"Executive Candidate {i}",
                "title": title,
                "company": comp_name,
                "geography": geo,
                "focus_area": focus,
                "tier": "TIER_1_PILOT" if i <= 50 else "TIER_2_EXPANSION",
                "wafer_node": "12nm-28nm ASIC",
                "pilot_offering": "Complimentary 5-Lot Wafer Yield & Packaging Defect Audit"
            })
        return targets

    @classmethod
    def get_three_touch_sequence(cls) -> Dict[str, Any]:
        """Multi-touch sequence designed for engineering leadership."""
        return {
            "touch_1": {
                "day": 1,
                "channel": "LinkedIn / Technical InMail",
                "subject": "CoWoS & Flip-Chip packaging queues for {{company}} wafer lots",
                "body": (
                    "Hi {{name}},\n\n"
                    "Noticed {{company}}'s impressive tape-out trajectory in {{focus_area}}. "
                    "Most fabless teams running 12nm-28nm ASICs right now are seeing packaging yield drop 3-8% "
                    "due to thermal warpage on secondary OSAT lines, blowing out Cost-Per-Good-Die (CPGD).\n\n"
                    "We built ChipFlow AI—an autonomous yield arbitrage engine that models negative-binomial "
                    "defect distribution and secures pre-qualified secondary packaging slots.\n\n"
                    "We're offering 5 complimentary wafer lot audits for select silicon teams this quarter. "
                    "Would you be open to seeing our benchmark on a 25-wafer batch?"
                )
            },
            "touch_2": {
                "day": 4,
                "channel": "Email / Data Annex",
                "subject": "Benchmarking $57k savings per 25-wafer lot (ChipFlow Yield Model)",
                "body": (
                    "Hi {{name}},\n\n"
                    "Following up with concrete data: our Murphy-model simulator recently ran an evaluation on a "
                    "standard 300mm wafer lot (48mm² die area) under Flip-Chip BGA packaging. By dynamically "
                    "optimizing edge-exclusion zones and defect clustering parameters, the engine recovered "
                    "$57,378 in net arbitrage savings per 25-wafer run.\n\n"
                    "Here is the interactive simulator: file:///e:/anti/omniverse/ui/chipflow_landing_page.html\n\n"
                    "Happy to plug in {{company}}'s exact die dimensions under NDA if that's helpful."
                )
            },
            "touch_3": {
                "day": 9,
                "channel": "Executive Briefing Request",
                "subject": "Yield audit for {{company}}'s upcoming tape-out?",
                "body": (
                    "Hi {{name}},\n\n"
                    "Wrapping up our Q3 pilot intake. If you have an active wafer lot scheduled with TSMC, "
                    "UMC, or GlobalFoundries over the next 90 days, we can run our yield allocation model "
                    "and deliver a full CPGD arbitrage report within 48 hours.\n\n"
                    "Let me know if next Tuesday works for a 15-minute screen share with our silicon architects."
                )
            }
        }
