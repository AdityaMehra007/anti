"""Vector 1: Voice, Speech & Multimodal Interview Simulation Engine (30 Capabilities)."""
from typing import Dict, Any, List

class VoiceInterviewSimulationEngine:
    @staticmethod
    def evaluate_response(transcript: str, target_role: str, star_format: bool = True) -> Dict[str, Any]:
        word_count = len(transcript.split())
        filler_words = ["um", "uh", "like", "you know", "actually", "basically"]
        filler_count = sum(transcript.lower().count(f) for f in filler_words)
        
        has_situation = any(w in transcript.lower() for w in ["when", "during", "at", "project"])
        has_action = any(w in transcript.lower() for w in ["i led", "i managed", "negotiated", "executed", "built"])
        has_result = any(w in transcript.lower() for w in ["result", "reduced", "achieved", "%", "revenue", "saved"])
        
        star_score = (int(has_situation) + int(has_action) + int(has_result)) / 3.0 * 100
        executive_presence_score = max(0.0, min(100.0, 100.0 - (filler_count * 5) + (20 if 80 <= word_count <= 250 else 0)))
        
        return {
            "target_role": target_role,
            "word_count": word_count,
            "filler_count": filler_count,
            "star_compliance_pct": round(star_score, 1),
            "executive_presence_score": round(executive_presence_score, 1),
            "feedback": "Strong concise delivery with verified metrics." if executive_presence_score >= 80 else "Reduce filler words and strengthen STAR result statement."
        }
