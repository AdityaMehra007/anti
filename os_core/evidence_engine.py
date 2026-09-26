import os, json
from datetime import datetime

class EvidenceEngine:
    """Strict Evidence & Event Observability Logger for Antigravity OS."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.log_file = os.path.join(workspace, "system_event_log.jsonl")

    def log_event(self, agent_name, action, inputs, outputs, status="EXECUTION_SUCCESS", evidence="SOURCE-BACKED", error=None):
        record = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "status": status,
            "evidence_grade": evidence,
            "inputs_summary": str(inputs)[:200],
            "outputs_summary": str(outputs)[:200],
            "error": error
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        return record
