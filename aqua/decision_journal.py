"""
AQUA Founder Decision Journal (Section 77)
Logs strategic decisions, probability estimates, assumptions, and retrospective accuracy.
"""

import json
import os
import time
from typing import Dict, Any, List, Optional

class DecisionJournal:
    def __init__(self, storage_path: str = "e:/anti/aqua/decision_journal.jsonl"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(os.path.abspath(storage_path)), exist_ok=True)

    def record_decision(
        self,
        decision_id: str,
        decision: str,
        context: str,
        options: List[str],
        assumptions: List[str],
        expected_outcome: str,
        probability: float,
        risk: str
    ) -> Dict[str, Any]:
        record = {
            "decision_id": decision_id,
            "timestamp": time.time(),
            "date": time.strftime("%Y-%m-%d %H:%M:%S IST", time.localtime()),
            "decision": decision,
            "context": context,
            "options": options,
            "assumptions": assumptions,
            "expected_outcome": expected_outcome,
            "probability": probability,
            "risk": risk,
            "actual_outcome": None,
            "accuracy_score": None,
            "lesson": None
        }

        with open(self.storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        return record

    def list_decisions(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.storage_path):
            return []
        records = []
        with open(self.storage_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def update_outcome(
        self,
        decision_id: str,
        actual_outcome: str,
        accuracy_score: float, # 0.0 to 1.0
        lesson: str
    ) -> bool:
        records = self.list_decisions()
        found = False
        for r in records:
            if r["decision_id"] == decision_id:
                r["actual_outcome"] = actual_outcome
                r["accuracy_score"] = accuracy_score
                r["lesson"] = lesson
                found = True
                break

        if found:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                for r in records:
                    f.write(json.dumps(r) + "\n")

        return found

    def calculate_calibration_stats(self) -> Dict[str, Any]:
        records = self.list_decisions()
        reviewed = [r for r in records if r.get("accuracy_score") is not None]
        if not reviewed:
            return {"total_decisions": len(records), "reviewed_decisions": 0, "mean_accuracy": None}

        mean_acc = sum(r.get("accuracy_score", 0) for r in reviewed) / len(reviewed)
        return {
            "total_decisions": len(records),
            "reviewed_decisions": len(reviewed),
            "mean_accuracy": round(mean_acc, 3)
        }
