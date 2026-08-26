"""
CHANGE DETECTION ENGINE
Compares normalized states across scrape refreshes and emits granular change events.
"""
import time
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

class ChangeType(str, Enum):
    JOB_ADDED = "JOB_ADDED"
    JOB_REMOVED = "JOB_REMOVED"
    JOB_SALARY_CHANGED = "JOB_SALARY_CHANGED"
    JOB_REQUIREMENT_CHANGED = "JOB_REQUIREMENT_CHANGED"
    JOB_DEADLINE_CHANGED = "JOB_DEADLINE_CHANGED"
    COMPANY_EXPANSION = "COMPANY_EXPANSION"
    COMPANY_LEADERSHIP_CHANGED = "COMPANY_LEADERSHIP_CHANGED"
    NO_CHANGE = "NO_CHANGE"

@dataclass
class ChangeEvent:
    change_type: ChangeType
    entity_id: str
    company: str
    field_name: Optional[str]
    old_value: Any
    new_value: Any
    timestamp: str
    evidence_url: str

class ChangeDetector:
    def __init__(self):
        self._state_store: Dict[str, Dict[str, Any]] = {}

    def compare_job_state(self, job_record: Dict[str, Any]) -> List[ChangeEvent]:
        job_id = job_record.get("requisition_id") or job_record.get("source_url", "")
        company = job_record.get("company", "Unknown")
        now_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        events: List[ChangeEvent] = []

        if job_id not in self._state_store:
            self._state_store[job_id] = dict(job_record)
            events.append(ChangeEvent(
                change_type=ChangeType.JOB_ADDED,
                entity_id=job_id,
                company=company,
                field_name=None,
                old_value=None,
                new_value=job_record.get("role"),
                timestamp=now_ts,
                evidence_url=job_record.get("source_url", "")
            ))
            return events

        prev = self._state_store[job_id]

        if prev.get("salary") != job_record.get("salary") and job_record.get("salary"):
            events.append(ChangeEvent(
                change_type=ChangeType.JOB_SALARY_CHANGED,
                entity_id=job_id,
                company=company,
                field_name="salary",
                old_value=prev.get("salary"),
                new_value=job_record.get("salary"),
                timestamp=now_ts,
                evidence_url=job_record.get("source_url", "")
            ))

        if prev.get("deadline") != job_record.get("deadline") and job_record.get("deadline"):
            events.append(ChangeEvent(
                change_type=ChangeType.JOB_DEADLINE_CHANGED,
                entity_id=job_id,
                company=company,
                field_name="deadline",
                old_value=prev.get("deadline"),
                new_value=job_record.get("deadline"),
                timestamp=now_ts,
                evidence_url=job_record.get("source_url", "")
            ))

        self._state_store[job_id] = dict(job_record)
        return events
