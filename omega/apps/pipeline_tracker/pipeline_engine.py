#!/usr/bin/env python3
"""
========================================================================================
OMEGA OUTREACH & PIPELINE LIFECYCLE TRACKER (v8.0)
========================================================================================
"""
import os, sys, json
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum

class PipelineStage(str, Enum):
    STAGED = "STAGED"
    DISPATCH_READY = "DISPATCH_READY"
    SENT = "SENT"
    FOLLOWUP_1 = "FOLLOWUP_1"
    FOLLOWUP_2 = "FOLLOWUP_2"
    REPLIED = "REPLIED"
    CALL_SCHEDULED = "CALL_SCHEDULED"
    CONVERTED = "CONVERTED"
    CLOSED = "CLOSED"

class PipelineTrackerEngine:
    TIER_1_COMPANIES = {
        "EY", "Accenture", "Deloitte", "Goldman Sachs", "IBM", "PwC", "Amazon",
        "KPMG", "Capgemini", "Tata Communications", "Google", "TCS", "JPMorgan"
    }

    VALID_TRANSITIONS = {
        PipelineStage.STAGED: [PipelineStage.DISPATCH_READY, PipelineStage.CLOSED],
        PipelineStage.DISPATCH_READY: [PipelineStage.SENT, PipelineStage.STAGED, PipelineStage.CLOSED],
        PipelineStage.SENT: [PipelineStage.FOLLOWUP_1, PipelineStage.REPLIED, PipelineStage.CLOSED],
        PipelineStage.FOLLOWUP_1: [PipelineStage.FOLLOWUP_2, PipelineStage.REPLIED, PipelineStage.CLOSED],
        PipelineStage.FOLLOWUP_2: [PipelineStage.REPLIED, PipelineStage.CLOSED],
        PipelineStage.REPLIED: [PipelineStage.CALL_SCHEDULED, PipelineStage.CLOSED],
        PipelineStage.CALL_SCHEDULED: [PipelineStage.CONVERTED, PipelineStage.CLOSED],
        PipelineStage.CONVERTED: [],
        PipelineStage.CLOSED: [PipelineStage.STAGED]
    }

    def __init__(self, execution_pack_path: Optional[str] = None):
        if execution_pack_path is None:
            execution_pack_path = os.path.join(r"e:\anti", "outreach_execution_pack.json")
        self.pack_path = execution_pack_path
        self.records: List[Dict[str, Any]] = []
        self._load_or_initialize()

    def _load_or_initialize(self):
        if os.path.exists(self.pack_path):
            with open(self.pack_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                actions = data.get("actions", [])
                base_time = datetime.now()
                for i, act in enumerate(actions):
                    company = act.get("company", "Target Company")
                    contact = act.get("contact_name", "Contact")
                    priority = act.get("priority", "MEDIUM")
                    action_type = act.get("action_type", "Recruiter Outreach")
                    cadence = self.generate_4_touch_cadence(contact, company, action_type)
                    
                    record = {
                        "id": act.get("id", f"ACT-{i+1:04d}"),
                        "contact_name": contact,
                        "company": company,
                        "is_tier_1": any(t.lower() in company.lower() for t in self.TIER_1_COMPANIES),
                        "action_type": action_type,
                        "priority": priority,
                        "current_stage": PipelineStage.DISPATCH_READY.value,
                        "last_updated": base_time.isoformat(),
                        "touch_1_initial": {
                            "subject": act.get("subject_line", f"Inquiry regarding {company}"),
                            "message": act.get("message_template", cadence["touch_1"]["body"]),
                            "scheduled_day": "Day 0",
                            "status": "READY"
                        },
                        "touch_2_proof_of_work": {
                            "subject": cadence["touch_2"]["subject"],
                            "message": cadence["touch_2"]["body"],
                            "scheduled_day": "Day +3",
                            "status": "PENDING_TOUCH_1"
                        },
                        "touch_3_value_add": {
                            "subject": cadence["touch_3"]["subject"],
                            "message": cadence["touch_3"]["body"],
                            "scheduled_day": "Day +7",
                            "status": "PENDING_TOUCH_2"
                        },
                        "touch_4_breakup": {
                            "subject": cadence["touch_4"]["subject"],
                            "message": cadence["touch_4"]["body"],
                            "scheduled_day": "Day +14",
                            "status": "PENDING_TOUCH_3"
                        },
                        "history": [
                            {"timestamp": base_time.isoformat(), "from": "STAGED", "to": "DISPATCH_READY", "note": "Action synthesized and staged"}
                        ]
                    }
                    self.records.append(record)

    def generate_4_touch_cadence(self, contact: str, company: str, action_type: str) -> Dict[str, Dict[str, str]]:
        first_name = contact.split()[0] if contact else "there"
        t1_subject = f"Connecting regarding {company} Operations & Strategy"
        t1_body = (
            f"Hi {first_name}, I noticed your leadership at {company}. Given my background in BBA International Business "
            f"and hands-on event operations (Aero India 2025 VIP pavilion coordination, Tata Communications, Puma), "
            f"I am actively tracking strategic operations and BD openings at {company}. Would you be open to connecting?"
        )
        t2_subject = f"Re: Connecting regarding {company} Operations (Quick Proof-of-Work Context)"
        t2_body = (
            f"Hi {first_name}, following up briefly. To give quick context on my execution background: at Aero India 2025, "
            f"I led high-security operations managing vendor SLAs across 100k+ attendees and coordinated B2B defense delegation logistics. "
            f"I bring this structured, zero-defect execution mindset to {company}'s strategic workflows."
        )
        t3_subject = f"Strategic operations alignment for {company}"
        t3_body = (
            f"Hi {first_name}, wanted to share a quick operational observation. Given {company}'s rapid scaling in global "
            f"delivery and GCC operations, having talent with combined international business training, rigorous vendor governance, "
            f"and cross-border compliance fluency accelerates project velocity. Would welcome 5 minutes if your team is hiring."
        )
        t4_subject = f"Closing the loop / Staying connected at {company}"
        t4_body = (
            f"Hi {first_name}, I know how busy your schedule is so I won't crowd your inbox. I'll follow {company}'s "
            f"milestones from here. If an operations, BD, or international trade requirement arises down the road, "
            f"I would be glad to reconnect. Wishing you continued success!"
        )
        return {
            "touch_1": {"subject": t1_subject, "body": t1_body},
            "touch_2": {"subject": t2_subject, "body": t2_body},
            "touch_3": {"subject": t3_subject, "body": t3_body},
            "touch_4": {"subject": t4_subject, "body": t4_body}
        }

    def transition_stage(self, action_id: str, to_stage: PipelineStage, note: str = "") -> bool:
        for rec in self.records:
            if rec["id"] == action_id:
                current = PipelineStage(rec["current_stage"])
                valid_next = self.VALID_TRANSITIONS.get(current, [])
                if to_stage in valid_next:
                    rec["current_stage"] = to_stage.value
                    rec["last_updated"] = datetime.now().isoformat()
                    rec["history"].append({
                        "timestamp": datetime.now().isoformat(),
                        "from": current.value,
                        "to": to_stage.value,
                        "note": note
                    })
                    return True
                else:
                    return False
        return False

    def get_funnel_summary(self) -> Dict[str, Any]:
        counts = {stage.value: 0 for stage in PipelineStage}
        priority_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        tier_1_count = 0
        for r in self.records:
            counts[r["current_stage"]] += 1
            priority_counts[r["priority"]] += 1
            if r.get("is_tier_1"):
                tier_1_count += 1
        total = len(self.records)
        active = sum(counts[s] for s in [
            PipelineStage.DISPATCH_READY.value,
            PipelineStage.SENT.value,
            PipelineStage.FOLLOWUP_1.value,
            PipelineStage.FOLLOWUP_2.value,
            PipelineStage.REPLIED.value,
            PipelineStage.CALL_SCHEDULED.value
        ])
        return {
            "total_contacts": total,
            "active_pipeline": active,
            "tier_1_coverage_pct": round((tier_1_count / max(1, total)) * 100, 1),
            "stage_breakdown": counts,
            "priority_breakdown": priority_counts,
            "projected_response_rate_pct": 24.5,
            "estimated_calls_generated": round(total * 0.245 * 0.6, 1)
        }

    def export_pipeline_state(self, output_json: Optional[str] = None):
        if output_json is None:
            output_json = os.path.join(r"e:\anti", "outreach_pipeline_state.json")
        data = {
            "exported_at": datetime.now().isoformat(),
            "funnel_summary": self.get_funnel_summary(),
            "records": self.records
        }
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return output_json
