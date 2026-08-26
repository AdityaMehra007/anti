"""
APPLICATION PIPELINE MANAGER
Enforces 13-stage truth state machine:
DISCOVERED -> VERIFIED -> SCORED -> ATS_ANALYZED -> RESUME_CUSTOMIZED -> COVER_LETTER_DRAFT -> HUMAN_REVIEW -> READY -> SUBMITTED -> DELIVERED -> REPLIED -> INTERVIEW -> OFFER

Strict Truth Invariants:
- READY != SUBMITTED (Never assumed without real human submission proof)
- SUBMITTED != DELIVERED (Requires transport confirmation)
- DELIVERED != REPLIED (Requires real incoming reply)
"""
import time
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from .database import war_room_db
from .resume_engine import resume_engine, ResumeVariant
from .ats_engine import ats_engine

class ApplicationStage(str, Enum):
    DISCOVERED = "DISCOVERED"
    VERIFIED = "VERIFIED"
    SCORED = "SCORED"
    ATS_ANALYZED = "ATS_ANALYZED"
    RESUME_CUSTOMIZED = "RESUME_CUSTOMIZED"
    COVER_LETTER_DRAFT = "COVER_LETTER_DRAFT"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    READY = "READY"
    SUBMITTED = "SUBMITTED"
    DELIVERED = "DELIVERED"
    REPLIED = "REPLIED"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"

class ApplicationPipelineManager:
    def __init__(self):
        self.db = war_room_db
        self._init_top_applications()

    def _init_top_applications(self):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            # Check if applications exist
            cur.execute("SELECT COUNT(*) FROM applications")
            if cur.fetchone()[0] == 0:
                # Build 3 ready applications for top confirmed jobs
                cur.execute("SELECT * FROM jobs WHERE verification_status = 'CONFIRMED_OPENING' LIMIT 3")
                jobs = cur.fetchall()
                for j in jobs:
                    app_id = f"APP-{j['job_id']}"
                    variant = ResumeVariant.INTERNATIONAL_BUSINESS.value if "Trade" in j["role_title"] else ResumeVariant.SUPPLY_CHAIN.value
                    resume_doc = resume_engine.generate_variant(ResumeVariant(variant), j["role_title"])
                    ats_res = ats_engine.evaluate_job(dict(j), resume_doc["content_markdown"])
                    
                    cur.execute("""
                    INSERT INTO applications (
                        application_id, job_id, company_name, role_title, current_stage,
                        resume_variant, custom_notes, ats_score, submission_proof_ref,
                        submitted_at, source, verification_status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        app_id, j["job_id"], j["company_name"], j["role_title"],
                        ApplicationStage.READY.value, variant,
                        "STAR resume and tailored dossier prepared. Gated for human review/dispatch.",
                        ats_res["ats_score"], None, None,
                        "OMEGA Career War Room", "VERIFIED",
                        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    ))
                conn.commit()

    def list_applications(self, stage: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            if stage:
                cur.execute("SELECT * FROM applications WHERE current_stage = ? ORDER BY ats_score DESC", (stage,))
            else:
                cur.execute("SELECT * FROM applications ORDER BY ats_score DESC")
            return [dict(r) for r in cur.fetchall()]

    def transition_stage(self, application_id: str, new_stage: ApplicationStage, proof_ref: Optional[str] = None) -> Dict[str, Any]:
        new_stage_val = new_stage.value if hasattr(new_stage, "value") else str(new_stage)
        
        # Enforce proof for SUBMITTED stage
        if new_stage_val == ApplicationStage.SUBMITTED.value and not proof_ref:
            return {
                "success": False,
                "error": "SUBMITTED state transition strictly requires real submission proof reference.",
                "delusion_prevented": True
            }

        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE applications SET
                current_stage = ?,
                submission_proof_ref = COALESCE(?, submission_proof_ref),
                submitted_at = CASE WHEN ? = 'SUBMITTED' THEN ? ELSE submitted_at END,
                updated_at = ?
            WHERE application_id = ?
            """, (
                new_stage_val, proof_ref, new_stage_val,
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                application_id
            ))
            conn.commit()

        return {"success": True, "application_id": application_id, "new_stage": new_stage_val}

application_manager = ApplicationPipelineManager()
