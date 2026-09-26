import json
from datetime import datetime

class SovereignBIEngine:
    '''Financial Anomaly Detection & Operational Explanation Engine.'''
    def __init__(self):
        self.metrics_history = []

    def analyze_variance(self, metric_name, current_val, baseline_val):
        pct_change = ((current_val - baseline_val) / max(0.001, baseline_val)) * 100
        severity = "HIGH_ALERT" if abs(pct_change) > 25 else "NORMAL"
        
        explanation = f"Metric '{metric_name}' changed by {pct_change:+.1f}% compared to baseline."
        recommendation = "Investigate marketing spend efficiency." if pct_change < 0 else "Scale top-performing referral channel."
        
        return {
            "metric": metric_name,
            "current_value": current_val,
            "baseline_value": baseline_val,
            "percentage_change": round(pct_change, 2),
            "severity": severity,
            "what_changed": explanation,
            "recommended_action": recommendation,
            "analyzed_at": datetime.now().isoformat()
        }
