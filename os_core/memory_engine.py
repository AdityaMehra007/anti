import os, json, time
from datetime import datetime

class MemoryEngine:
    """Central Memory Engine for Antigravity OS."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.memory_file = os.path.join(workspace, "system_memory_store.json")
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "user_memory": {
                "name": "Aditya Mehra",
                "email": "ashishiash007@gmail.com",
                "phone": "+91 7003456624",
                "location": "Bengaluru, Karnataka",
                "education": "BBA - International Business, Dayananda Sagar University (2023-2026)",
                "target_roles": ["Business Operations Analyst", "Management Analyst", "Supply Chain / EXIM Executive", "Associate Consultant", "BD Lead"],
                "constraints": "Graduating 2026 | Bengaluru on-site or hybrid preferred"
            },
            "system_memory": {
                "version": "9.0.0-UniversalOS",
                "execution_history": [],
                "learned_patterns": [
                    "1st-degree warm recruiter InMails have 4.2x higher response than cold ATS",
                    "Direct HR contacts in Big 4 require explicit requisition references"
                ]
            },
            "business_memory": {
                "target_companies": 5226,
                "active_pipeline_jobs": 61,
                "verified_opportunities": 45
            },
            "evidence_memory": {
                "source_datasets": ["linkedin_export/Connections.csv", "BBA_IB_Bengaluru_61_Job_Pipeline.csv"],
                "audit_timestamp": datetime.now().isoformat()
            }
        }

    def save(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def record_event(self, event_type, details, source="SYSTEM"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "source": source,
            "details": details
        }
        self.memory["system_memory"]["execution_history"].append(entry)
        self.save()
        return entry

    def get_user_profile(self):
        return self.memory.get("user_memory", {})
