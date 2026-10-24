"""
Ultrahuman Project BioRing-Synapse: Multi-Biomarker Metabolic Synthesizer
Fuses continuous glucose monitoring (CGM) telemetry, heart rate variability (HRV),
and skin temperature to compute real-time metabolic recovery scores.
"""
from typing import Dict, Any

class MetabolicSynthesizer:
    def compute_metabolic_score(self, glucose_mg_dl: float, hrv_ms: float, skin_temp_delta_c: float) -> Dict[str, Any]:
        # Optimal fasting glucose: 70 - 100 mg/dL
        glucose_penalty = max(0.0, abs(glucose_mg_dl - 90.0) - 15.0) * 0.8
        # Higher HRV indicates superior parasympathetic recovery
        hrv_bonus = min(30.0, (hrv_ms / 60.0) * 30.0)
        # Elevated skin temp indicates potential systemic inflammation or fever
        temp_penalty = max(0.0, skin_temp_delta_c) * 15.0

        base_score = 70.0 + hrv_bonus - glucose_penalty - temp_penalty
        final_score = max(0.0, min(100.0, base_score))

        status = "OPTIMAL" if final_score >= 85 else ("STABLE" if final_score >= 70 else "RECOVERY_NEEDED")
        return {
            "metabolic_score": round(final_score, 1),
            "status": status,
            "glucose_delta": round(glucose_mg_dl - 90.0, 1),
            "hrv_bonus": round(hrv_bonus, 1)
        }
