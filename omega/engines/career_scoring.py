"""
EXPECTED CAREER VALUE (ECV) SCORING ENGINE
ECV = Fit * Probability * Network * Compensation * Upside * Learning * Effort * Location * Company Quality
"""
from typing import Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class CareerValueScore:
    expected_career_value: float  # 0 - 100
    fit_score: float
    probability_score: float
    network_leverage_score: float
    compensation_index: float
    long_term_upside: float
    learning_velocity: float
    location_fit: float
    company_prestige: float
    strategic_verdict: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class CareerScoringEngine:
    @classmethod
    def calculate_ecv(
        cls,
        role_fit: float = 0.95,
        hire_probability: float = 0.85,
        network_access: float = 0.90,
        comp_tier: float = 0.92,
        upside: float = 0.94,
        learning: float = 0.95,
        location: float = 1.0,
        company_quality: float = 0.98
    ) -> CareerValueScore:
        # Weighted ECV calculation
        raw = (
            (role_fit * 0.20) +
            (hire_probability * 0.15) +
            (network_access * 0.10) +
            (comp_tier * 0.15) +
            (upside * 0.15) +
            (learning * 0.10) +
            (location * 0.05) +
            (company_quality * 0.10)
        ) * 100.0

        ecv = min(99.5, round(raw, 1))
        verdict = "PRIORITY_S_TIER_TARGET" if ecv >= 90.0 else ("STRONG_OPPORTUNITY" if ecv >= 80.0 else "GENERAL_PIPELINE")

        return CareerValueScore(
            expected_career_value=ecv,
            fit_score=role_fit * 100.0,
            probability_score=hire_probability * 100.0,
            network_leverage_score=network_access * 100.0,
            compensation_index=comp_tier * 100.0,
            long_term_upside=upside * 100.0,
            learning_velocity=learning * 100.0,
            location_fit=location * 100.0,
            company_prestige=company_quality * 100.0,
            strategic_verdict=verdict
        )
