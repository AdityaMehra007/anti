"""Vector 2: Real-Time ATS Infiltration & Job Signal Detection (30 Capabilities)."""
from typing import Dict, Any, List

class JobSignalAndATSEngine:
    @staticmethod
    def score_ats_compatibility(resume_text: str, jd_text: str) -> Dict[str, Any]:
        jd_words = set([w.lower().strip(".,;:()") for w in jd_text.split() if len(w) > 3])
        resume_words = set([w.lower().strip(".,;:()") for w in resume_text.split() if len(w) > 3])
        
        matched_keywords = list(jd_words.intersection(resume_words))
        missing_keywords = list(jd_words.difference(resume_words))[:5]
        
        match_score = round(len(matched_keywords) / max(1, len(jd_words)) * 100, 1)
        
        return {
            "ats_match_percentage": match_score,
            "matched_keywords_count": len(matched_keywords),
            "missing_top_keywords": missing_keywords,
            "recommendation": "PASS: High ATS threshold" if match_score >= 70.0 else "OPTIMIZE: Inject missing target terms"
        }
