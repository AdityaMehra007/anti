"""
Sovereign Core — Priority & Leverage Calculator
Calculates expected value priority using the formula:
Priority = (Impact * Probability * Urgency * Strategic * Leverage) / Cost
"""

class PriorityEngine:
    @staticmethod
    def calculate_priority(impact: float, probability: float, urgency: float,
                           strategic_value: float, leverage: float, cost: float) -> float:
        """
        impact: 1.0 - 10.0
        probability: 0.1 - 1.0
        urgency: 1.0 - 10.0
        strategic_value: 1.0 - 10.0
        leverage: 1.0 - 10.0
        cost: 1.0 - 10.0 (minimum 1.0 to avoid zero division)
        """
        safe_cost = max(1.0, cost)
        safe_prob = min(1.0, max(0.1, probability))
        numerator = impact * safe_prob * urgency * strategic_value * leverage
        score = numerator / safe_cost
        return round(score, 2)
