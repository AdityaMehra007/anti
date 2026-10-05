"""
Live Autonomous Recruiter AI Agent & Interactive Calendar Dispatcher.

Parses inbound recruiter communications, evaluates proposed CTC against verified salary floors,
synthesizes contextual responses/counter-offers, generates RFC 5545 calendar invitations,
records events into data/outreach_tracker.db, and dispatches webhook events to the Cockpit.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any, Dict, List, Optional
import urllib.request
import uuid

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega.orchestration.calendar_dispatcher import CalendarDispatcher


class RecruiterDispatcher:
    """
    Autonomous inbound recruiter parser, negotiation engine, and cockpit dispatcher.
    """

    # Aditya Mehra verified profile constants
    CANDIDATE_NAME = "Aditya Mehra"
    CANDIDATE_EMAIL = "adityamehra007@gmail.com"
    EDUCATION = "BBA International Business (BBA IB), Dayananda Sagar University (DSU) '26"
    EXPERIENCE_HIGHLIGHTS = (
        "AERO India 2025 Coordinator; Operations Specialist; Instawork 99.2% QA Precision; "
        "autonomous multi-agent engineering & process optimization."
    )
    LOCATION_PREFERENCE = "Bangalore GCC Corridor / Hybrid / Remote"

    # Salary Floors (INR in Lakhs Per Annum)
    CTC_MIN_LPA = 3.0
    CTC_TARGET_MAX_LPA = 11.0

    DEFAULT_DB_PATH = REPO_ROOT / "data" / "outreach_tracker.db"

    def __init__(
        self,
        db_path: Optional[Path | str] = None,
        calendar_dispatcher: Optional[CalendarDispatcher] = None,
        cockpit_webhook_url: Optional[str] = None,
    ) -> None:
        self.db_path = Path(db_path) if db_path else self.DEFAULT_DB_PATH
        self.calendar = calendar_dispatcher or CalendarDispatcher(calendar_dir=self.db_path.parent / "calendar_events")
        self.cockpit_webhook_url = cockpit_webhook_url or os.environ.get("COCKPIT_WEBHOOK_URL", "")
        self._ensure_table()

    def _get_connection(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(self.db_path))

    def _ensure_table(self) -> None:
        """Ensures that the inbound_recruiter_events table exists with required schema."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS inbound_recruiter_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE,
                    company TEXT,
                    recruiter_name TEXT,
                    email TEXT,
                    role TEXT,
                    stage TEXT,
                    message TEXT,
                    ctc_lpa REAL,
                    raw_payload TEXT,
                    received_at TEXT
                )
                """
            )
            conn.commit()

    def extract_ctc(self, text: str) -> Optional[float]:
        """
        Extracts proposed CTC in LPA from communication text.
        Supports patterns like '5 LPA', '6.5 Lakhs', 'Rs 8,00,000', '10.5 LPA', etc.
        """
        # Pattern 1: numbers followed by LPA / Lacs / Lakhs / CTC
        p1 = re.search(r"(?:ctc|package|salary|offer|stipend)?\s*[:=]?\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lac|lakh|lakhs)", text, re.IGNORECASE)
        if p1:
            try:
                return float(p1.group(1))
            except ValueError:
                pass

        # Pattern 2: INR / Rs currency numbers in absolute figures (e.g. 500000 or 5,00,000)
        p2 = re.search(r"(?:rs\.?|inr|₹)\s*(\d{1,2}(?:,\d{2})*,\d{3}|\d{5,8})", text, re.IGNORECASE)
        if p2:
            num_str = p2.group(1).replace(",", "")
            try:
                val = float(num_str)
                # Convert raw rupees to LPA
                return round(val / 100000.0, 2)
            except ValueError:
                pass

        return None

    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extracts email address, recruiter name, company, and role from text."""
        # Email
        email_match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
        email = email_match.group(1) if email_match else None

        # Company
        company = None
        comp_match = re.search(r"(?:at|with|from|company:?)\s+([A-Z][A-Za-z0-9&.\s]{2,30}?)(?:[\.,\n\r]| for | as | to )", text)
        if comp_match:
            candidate_comp = comp_match.group(1).strip()
            # Avoid matching generic terms
            if candidate_comp.lower() not in {"an interview", "the role", "our team", "aditya"}:
                company = candidate_comp

        # Role
        role = None
        role_match = re.search(r"(?:role|position|profile|opportunity|hiring for)\s*(?:of|as|:)?\s*([A-Za-z0-9\s\-/]{3,40}?)(?:[\.,\n\r]| at | with )", text, re.IGNORECASE)
        if role_match:
            role = role_match.group(1).strip()

        # Recruiter Name
        recruiter_name = None
        recruiter_match = re.search(r"(?:regards|best|thanks|sincerely),?\s*[\r\n]+\s*([A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+)?)", text, re.IGNORECASE)
        if recruiter_match:
            recruiter_name = recruiter_match.group(1).strip()
        else:
            name_match = re.search(r"(?:i am|this is|my name is)\s+([A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+)?)", text, re.IGNORECASE)
            if name_match:
                recruiter_name = name_match.group(1).strip()

        return {
            "email": email,
            "company": company,
            "role": role,
            "recruiter_name": recruiter_name or "Hiring Team",
        }

    def extract_stage(self, text: str) -> str:
        """Extracts interview or recruiting pipeline stage."""
        lower = text.lower()
        if "screen" in lower or "hr" in lower or "initial" in lower or "intro" in lower:
            return "initial_screening"
        if "technical" in lower or "case study" in lower or "assignment" in lower:
            return "technical_evaluation"
        if "final" in lower or "partner" in lower:
            return "final_round"
        if "job offer" in lower or "offer letter" in lower or "offer extended" in lower:
            return "offer"
        return "recruiter_inbound"

    def extract_proposed_slots(self, text: str) -> List[Dict[str, Any]]:
        """
        Parses proposed interview dates and times from the message.
        Looks for ISO dates or day/time references (e.g. 2026-10-10 14:00).
        """
        slots = []
        # Match YYYY-MM-DD HH:MM
        dt_matches = re.findall(r"(\d{4}-\d{2}-\d{2})\s*(?:at|T)?\s*(\d{2}:\d{2})", text)
        for d_str, t_str in dt_matches:
            try:
                start_dt = datetime.datetime.strptime(f"{d_str} {t_str}", "%Y-%m-%d %H:%M")
                end_dt = start_dt + datetime.timedelta(minutes=45)
                slots.append({"start": start_dt, "end": end_dt})
            except ValueError:
                pass
        return slots

    def parse_inbound_message(self, message_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Comprehensive parser for inbound recruiter email or message.
        """
        meta = metadata or {}
        contacts = self.extract_contact_info(message_text)
        ctc = self.extract_ctc(message_text)
        stage = self.extract_stage(message_text)
        slots = self.extract_proposed_slots(message_text)

        company = meta.get("company") or contacts.get("company") or "Prospective Employer"
        role = meta.get("role") or contacts.get("role") or "Strategic Role"
        recruiter_name = meta.get("recruiter_name") or contacts.get("recruiter_name") or "Hiring Team"
        email = meta.get("email") or contacts.get("email") or "recruiter@unknown.com"

        event_id = meta.get("event_id") or f"REC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

        return {
            "event_id": event_id,
            "company": company,
            "role": role,
            "recruiter_name": recruiter_name,
            "email": email,
            "stage": stage,
            "ctc_lpa": ctc,
            "proposed_slots": slots,
            "message": message_text,
            "received_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

    def evaluate_and_respond(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforces Aditya Mehra's verified profile and salary floor (₹3.0L - ₹11.0L CTC corridor).
        Generates contextual replies and counter-proposals when compensation is under ₹3.0L.
        """
        ctc = parsed.get("ctc_lpa")
        recruiter_name = parsed.get("recruiter_name", "Hiring Team")
        role = parsed.get("role", "Opportunity")
        company = parsed.get("company", "Your Organization")

        # Case 1: CTC specified and below salary floor (₹3.0L)
        if ctc is not None and ctc < self.CTC_MIN_LPA:
            decision = "counter_offer_required"
            reply_subject = f"Re: {role} opportunity at {company} - Aditya Mehra"
            reply_body = (
                f"Dear {recruiter_name},\n\n"
                f"Thank you for reaching out regarding the {role} position at {company}.\n\n"
                f"Based on my qualifications ({self.EDUCATION}), my proven execution track record as "
                f"AERO India 2025 Coordinator, and maintaining 99.2% QA Precision at Instawork, my established "
                f"compensation baseline for the Bangalore GCC corridor is ₹{self.CTC_MIN_LPA}L - ₹{self.CTC_TARGET_MAX_LPA}L CTC.\n\n"
                f"While the proposed figure of ₹{ctc}L LPA falls below this threshold, I would be pleased to explore this role "
                f"if {company} has flexibility to align with the ₹{self.CTC_MIN_LPA}L - ₹{self.CTC_TARGET_MAX_LPA}L band given "
                f"the high-impact operational competencies and autonomous execution capabilities I bring to the team.\n\n"
                f"Please let me know if an aligned package is feasible.\n\n"
                f"Best regards,\n"
                f"{self.CANDIDATE_NAME}\n"
                f"{self.CANDIDATE_EMAIL} | +91 97411 20023"
            )
        # Case 2: CTC acceptable (>= 6.5L)
        elif ctc is not None and ctc >= self.CTC_MIN_LPA:
            decision = "accepted_compensation"
            reply_subject = f"Re: {role} interview schedule - Aditya Mehra"
            reply_body = (
                f"Dear {recruiter_name},\n\n"
                f"Thank you for sharing the details for the {role} role at {company}. The proposed compensation range "
                f"of ₹{ctc}L CTC aligns well with my expectations ({self.CTC_MIN_LPA}L - {self.CTC_TARGET_MAX_LPA}L CTC corridor).\n\n"
                f"I look forward to discussing how my background in {self.EDUCATION} and operational leadership at "
                f"AERO India 2025 can deliver immediate leverage to {company}.\n\n"
                f"I am pleased to confirm availability for our interview discussion.\n\n"
                f"Best regards,\n"
                f"{self.CANDIDATE_NAME}"
            )
        # Case 3: CTC not mentioned upfront
        else:
            decision = "qualify_compensation_and_proceed"
            reply_subject = f"Re: {role} discussion - Aditya Mehra"
            reply_body = (
                f"Dear {recruiter_name},\n\n"
                f"Thank you for getting in touch regarding the {role} opening at {company}.\n\n"
                f"I am enthusiastic about the opportunity and would welcome an initial conversation. "
                f"For calibration across Bangalore GCC opportunities, my expected compensation baseline is "
                f"₹{self.CTC_MIN_LPA}L - ₹{self.CTC_TARGET_MAX_LPA}L CTC. "
                f"Looking forward to connecting.\n\n"
                f"Best regards,\n"
                f"{self.CANDIDATE_NAME}"
            )

        return {
            "decision": decision,
            "reply_subject": reply_subject,
            "reply_body": reply_body,
            "salary_floor_cleared": (ctc is None or ctc >= self.CTC_MIN_LPA),
        }

    def schedule_interview_and_generate_ics(
        self,
        parsed: Dict[str, Any],
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
    ) -> Dict[str, Any]:
        """
        Schedules interview, resolves slot, and generates RFC 5545 .ics calendar invitation.
        """
        slots = parsed.get("proposed_slots", [])
        if not start_time:
            if slots:
                start_time = slots[0]["start"]
                end_time = slots[0]["end"]
            else:
                # Default to next business day at 11:00 AM IST
                tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
                start_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
                end_time = start_time + datetime.timedelta(minutes=45)
        elif not end_time:
            end_time = start_time + datetime.timedelta(minutes=45)

        title = f"Interview: Aditya Mehra <> {parsed.get('company')} ({parsed.get('role')})"
        description = (
            f"Candidate: {self.CANDIDATE_NAME} ({self.EDUCATION})\n"
            f"Stage: {parsed.get('stage')}\n"
            f"Focus: Operations, GCC Architecture, QA Precision (99.2% Instawork benchmark)\n"
            f"Contact: {self.CANDIDATE_EMAIL}"
        )

        ics_payload = self.calendar.generate_ics(
            event_id=parsed["event_id"],
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            attendee_email=parsed.get("email", "recruiter@unknown.com"),
            attendee_name=parsed.get("recruiter_name", "Recruiter"),
        )

        file_path = self.calendar.save_ics_file(parsed["event_id"], ics_payload)

        return {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "ics_content": ics_payload,
            "ics_file_path": str(file_path),
        }

    def persist_event(self, parsed: Dict[str, Any], raw_payload: Optional[str] = None) -> int:
        """
        Inserts the inbound recruiter event record into data/outreach_tracker.db.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO inbound_recruiter_events (
                    event_id, company, recruiter_name, email, role, stage, message, ctc_lpa, raw_payload, received_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    parsed.get("event_id"),
                    parsed.get("company"),
                    parsed.get("recruiter_name"),
                    parsed.get("email"),
                    parsed.get("role"),
                    parsed.get("stage"),
                    parsed.get("message"),
                    parsed.get("ctc_lpa"),
                    raw_payload or json.dumps(parsed),
                    parsed.get("received_at"),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def emit_cockpit_webhook(self, event_data: Dict[str, Any]) -> bool:
        """
        Dispatches event payload to the Cockpit webhook handler.
        If webhook URL is not configured or in test mode, returns True gracefully.
        """
        if not self.cockpit_webhook_url:
            return True

        try:
            req_data = json.dumps(event_data).encode("utf-8")
            req = urllib.request.Request(
                self.cockpit_webhook_url,
                data=req_data,
                headers={"Content-Type": "application/json", "User-Agent": "OmegaRecruiterDispatcher/1.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201, 202, 204)
        except Exception:
            return False

    def process_inbound(
        self,
        message_text: str,
        metadata: Optional[Dict[str, Any]] = None,
        auto_schedule: bool = True,
    ) -> Dict[str, Any]:
        """
        Complete end-to-end processing:
        1. Parse message
        2. Evaluate compensation & synthesize reply
        3. Optional calendar slot & RFC 5545 generation
        4. Database persistence
        5. Cockpit webhook emission
        """
        parsed = self.parse_inbound_message(message_text, metadata)
        response_data = self.evaluate_and_respond(parsed)
        parsed.update(response_data)

        calendar_data = None
        if auto_schedule:
            calendar_data = self.schedule_interview_and_generate_ics(parsed)
            parsed["calendar"] = calendar_data

        record_id = self.persist_event(parsed)
        parsed["db_id"] = record_id

        # Cockpit webhook dispatch
        webhook_dispatched = self.emit_cockpit_webhook(parsed)
        parsed["webhook_dispatched"] = webhook_dispatched

        return parsed
