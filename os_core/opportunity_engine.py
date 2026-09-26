import os, csv

class OpportunityEngine:
    """Scores Opportunities with: Economic Value x Probability x Strategic Leverage x Speed x Network Advantage."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def score_opportunity(self, job_data, network_matches):
        co = job_data.get("Company Name", "")
        # Economic value (0-10): Tier A consulting = 9.5
        econ_val = 9.5 if any(k in co.lower() for k in ["ey", "deloitte", "accenture", "goldman", "amazon", "ibm"]) else 7.5
        # Probability (0-10): based on 1st-degree recruiters
        rec_count = sum(1 for m in network_matches if "Recruiter" in m.get("Match Type", ""))
        prob = 9.0 if rec_count > 0 else 6.0
        # Strategic leverage (0-10): brand value
        strat_lev = 9.5
        # Speed (0-10): Bangalore local presence
        speed = 9.0
        # Network advantage (0-10): total connections
        net_adv = min(10.0, len(network_matches) * 0.2 + 5.0)
        
        composite_roi = (econ_val * prob * strat_lev * speed * net_adv) / 1000.0  # Normalized scale
        
        tier = "NOW" if composite_roi >= 4.0 else ("NEXT" if composite_roi >= 2.5 else "LATER")
        return {
            "composite_roi_score": round(composite_roi, 2),
            "quadrant": tier,
            "breakdown": {
                "economic_value": econ_val,
                "probability": prob,
                "strategic_leverage": strat_lev,
                "speed": speed,
                "network_advantage": round(net_adv, 1)
            }
        }
