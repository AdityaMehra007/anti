"""
OMEGA JOB APPLICATION AUTOMATOR & EXECUTION DISPATCHER
Orchestrates end-to-end application package preparation, ATS customization,
and portal application dispatch for confirmed live job openings.

Strict Governance:
- READY != SUBMITTED, SUBMITTED != DELIVERED.
- Every application package is assembled in READY state with tailored resume & cover letter.
- Provides one-click browser opening and automated clipboard copy for seamless human submission.
"""
import sqlite3
import json
import os
import time
from typing import Dict, Any, List

from .database import war_room_db
from .resume_engine import resume_engine
from .ats_engine import ats_engine
from .outreach_engine import outreach_engine
from .live_job_discovery import live_job_discovery

class JobApplicationAutomator:
    def __init__(self):
        self.db = war_room_db
        self.resume_eng = resume_engine
        self.ats_eng = ats_engine
        self.outreach_eng = outreach_engine
        self.discovery = live_job_discovery
        self.output_dir = "E:/OMNI_OS/CAREER_HQ/APPLICATION_PACKAGES"
        os.makedirs(self.output_dir, exist_ok=True)

    def prepare_all_confirmed_applications(self) -> List[Dict[str, Any]]:
        confirmed_jobs = self.discovery.list_confirmed_jobs(limit=50)
        prepared_dossiers = []

        with self.db.get_connection() as conn:
            cur = conn.cursor()
            for job in confirmed_jobs:
                job_id = job["job_id"]
                company = job["company_name"]
                role = job["role_title"]
                app_url = job["application_url"]
                location = job["location"]

                # Determine best resume variant
                role_lower = role.lower()
                if "trade" in role_lower or "custom" in role_lower:
                    variant = "INTERNATIONAL_BUSINESS"
                elif "supply" in role_lower or "procure" in role_lower:
                    variant = "SUPPLY_CHAIN"
                elif "logistic" in role_lower:
                    variant = "LOGISTICS"
                else:
                    variant = "OPERATIONS"

                resume_doc = self.resume_eng.generate_variant(variant, role)
                skills_list = json.loads(job.get("skills", "[]")) if isinstance(job.get("skills"), str) else (job.get("skills") or [])
                ats_analysis = self.ats_eng.evaluate_job({"role_title": role, "skills": skills_list}, resume_doc["content_markdown"])
                ats_score = ats_analysis["ats_score"]

                app_id = f"APP-{job_id}"
                cur.execute("SELECT * FROM applications WHERE application_id = ?", (app_id,))
                existing = cur.fetchone()
                now_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

                if not existing:
                    cur.execute("""
                    INSERT INTO applications (
                        application_id, job_id, company_name, role_title, current_stage,
                        resume_variant, custom_notes, ats_score, submission_proof_ref,
                        submitted_at, source, verification_status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        app_id, job_id, company, role, "READY",
                        variant, f"Automated ATS Tailoring Score: {ats_score}%. Matched skills: {ats_analysis.get('strong_matches', [])}",
                        ats_score, None, None, "OMEGA_AUTOMATOR", "READY_FOR_HUMAN", now_ts, now_ts
                    ))

                clean_job_id = job_id.replace(":", "_").replace("/", "_")
                dossier_filename = f"{company.replace(' ', '_')}_{clean_job_id}.md"
                dossier_path = os.path.join(self.output_dir, dossier_filename)

                cover_letter_body = (
                    f"Dear Hiring Team at {company},\n\n"
                    f"I am writing to express my strong enthusiasm for the {role} position in {location}. "
                    f"As a final-year BBA student specializing in International Business at Dayananda Sagar University, Bengaluru, "
                    f"I bring hands-on experience in high-velocity operations, vendor management, budget tracking, and process optimization.\n\n"
                    f"During my tenure as Event Coordinator for TRILOGY Live Music and Commercial Operations & Business Development Specialist, "
                    f"I managed end-to-end operational workflows, client onboarding, and vendor logistics coordination. "
                    f"My academic foundation in Incoterms 2020, supply chain modeling, and cross-border trade compliance directly aligns with the operational rigor required at {company}.\n\n"
                    f"I would welcome the opportunity to discuss how my proactive operational leadership, analytical discipline in MS Excel, and commitment to SLA excellence can drive measurable value for your team in Bengaluru.\n\n"
                    f"Thank you for your time and consideration.\n\n"
                    f"Sincerely,\nAditya Mehra\nPhone: +91 7003456624 | Email: adityamehra799@gmail.com\nBengaluru, Karnataka, India\nLinkedIn: linkedin.com/in/aditya-mehra-b8644b326"
                )

                dossier_content = (
                    f"# APPLICATION DOSSIER: {role} @ {company}\n\n"
                    f"**Application ID**: `{app_id}`  \n"
                    f"**Status**: **`READY FOR SUBMISSION`** (Human Review Gated)  \n"
                    f"**Company**: {company}  \n"
                    f"**Location**: {location}  \n"
                    f"**Direct Apply URL**: [{app_url}]({app_url})  \n"
                    f"**ATS Score**: {ats_score}%  \n"
                    f"**Recommended Resume Variant**: `{variant}`  \n\n"
                    f"---\n\n"
                    f"## 1. Tailored Cover Letter\n\n"
                    f"```text\n{cover_letter_body}\n```\n\n"
                    f"---\n\n"
                    f"## 2. ATS Matched Keywords\n{json.dumps(ats_analysis.get('strong_matches', []), indent=2)}\n\n"
                    f"---\n\n"
                    f"## 3. Recommended Resume Variant ({variant})\n\n"
                    f"```markdown\n{resume_doc['content_markdown']}\n```\n\n"
                    f"---\n\n"
                    f"## 4. Application Submission Checklist\n"
                    f"- [ ] 1. Open the direct application link: [{app_url}]({app_url})\n"
                    f"- [ ] 2. Attach `Aditya_Mehra_Resume.pdf` or paste the tailored resume text above.\n"
                    f"- [ ] 3. Paste the tailored Cover Letter.\n"
                    f"- [ ] 4. Fill personal contact details: `Aditya Mehra`, `adityamehra799@gmail.com`, `+91 7003456624`.\n"
                    f"- [ ] 5. Submit application on portal and copy the application confirmation receipt/number into OMEGA War Room.\n"
                )

                with open(dossier_path, "w", encoding="utf-8") as f:
                    f.write(dossier_content)

                prepared_dossiers.append({
                    "app_id": app_id,
                    "company": company,
                    "role": role,
                    "location": location,
                    "application_url": app_url,
                    "ats_score": ats_score,
                    "variant": variant,
                    "dossier_path": dossier_path
                })

            conn.commit()

        self._update_job_pipeline_doc(prepared_dossiers)
        return prepared_dossiers

    def _update_job_pipeline_doc(self, dossiers: List[Dict[str, Any]]):
        pipeline_path = "E:/OMNI_OS/CAREER_HQ/JOB_PIPELINE.md"
        lines = [
            "# CAREER HQ — ACTIVE JOB APPLICATION PIPELINE\n\n",
            "**Governance Standard**: `READY != SUBMITTED`, `SUBMITTED != DELIVERED`  \n",
            f"**Total Applications Prepared in READY Stage**: {len(dossiers)}  \n\n",
            "| # | Company | Role Title | Location | ATS Match | Resume Variant | Direct Application Link | Pipeline Stage |\n",
            "| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :---: |\n"
        ]
        for idx, d in enumerate(dossiers, 1):
            lines.append(f"| **{idx}** | **{d['company']}** | {d['role']} | {d['location']} | **{d['ats_score']}%** | `{d['variant']}` | [Apply Now]({d['application_url']}) | **`READY FOR SUBMISSION`** |\n")

        lines.append("\n---\n\n### Next Action for Candidate:\nClick on the **Apply Now** link for your priority openings, submit via portal, and record the application receipt in OMEGA to advance stage to `SUBMITTED`.\n")

        with open(pipeline_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

job_application_automator = JobApplicationAutomator()
