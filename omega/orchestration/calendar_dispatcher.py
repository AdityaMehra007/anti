"""
Calendar Dispatcher and RFC 5545 iCalendar (.ics) Generator.

Generates iCalendar (.ics) files with timezone Asia/Kolkata (IST),
handles interview slot verification, conflict detection, and schedule persistence.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


class CalendarDispatcher:
    """
    Builds RFC 5545 compliant .ics calendar invitation streams and manages interview slots.
    """

    TIMEZONE_ID = "Asia/Kolkata"
    ORGANIZER_NAME = "Aditya Mehra"
    ORGANIZER_EMAIL = "adityamehra007@gmail.com"

    def __init__(self, calendar_dir: Optional[Path | str] = None) -> None:
        self.calendar_dir = Path(calendar_dir) if calendar_dir else Path("data/calendar_events")
        self.calendar_dir.mkdir(parents=True, exist_ok=True)

    def generate_ics(
        self,
        event_id: str,
        title: str,
        description: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        attendee_email: str,
        attendee_name: str = "Recruiter",
        location: str = "Google Meet / Microsoft Teams",
    ) -> str:
        """
        Generates RFC 5545 .ics text payload with Asia/Kolkata VTIMEZONE and VEVENT.
        """
        uid = f"{event_id}-{uuid.uuid4().hex[:8]}@adityamehra.in"
        now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        # Format datetimes (Local Asia/Kolkata format: YYYYMMDDTHHMMSS)
        dtstart_str = start_time.strftime("%Y%m%dT%H%M%S")
        dtend_str = end_time.strftime("%Y%m%dT%H%M%S")

        # Sanitize text fields for ics compliance (escape commas and semicolons, newlines to \n)
        sanitized_summary = title.replace("\n", " ").replace(",", "\\,").replace(";", "\\;")
        sanitized_desc = description.replace("\r", "").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")
        sanitized_loc = location.replace("\n", " ").replace(",", "\\,").replace(";", "\\;")

        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Aditya Mehra//Autonomous Recruiter Dispatcher//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:REQUEST",
            "BEGIN:VTIMEZONE",
            f"TZID:{self.TIMEZONE_ID}",
            "X-LIC-LOCATION:Asia/Kolkata",
            "BEGIN:STANDARD",
            "TZOFFSETFROM:+0530",
            "TZOFFSETTO:+0530",
            "TZNAME:IST",
            "DTSTART:19700101T000000",
            "END:STANDARD",
            "END:VTIMEZONE",
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{now_utc}",
            f"ORGANIZER;CN={self.ORGANIZER_NAME}:mailto:{self.ORGANIZER_EMAIL}",
            f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;CN={attendee_name}:mailto:{attendee_email}",
            f"SUMMARY:{sanitized_summary}",
            f"DESCRIPTION:{sanitized_desc}",
            f"LOCATION:{sanitized_loc}",
            f"DTSTART;TZID={self.TIMEZONE_ID}:{dtstart_str}",
            f"DTEND;TZID={self.TIMEZONE_ID}:{dtend_str}",
            "STATUS:CONFIRMED",
            "SEQUENCE:0",
            "TRANSP:OPAQUE",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "DESCRIPTION:Interview Reminder",
            "TRIGGER:-PT15M",
            "END:VALARM",
            "END:VEVENT",
            "END:VCALENDAR",
        ]

        return "\r\n".join(ics_lines) + "\r\n"

    def save_ics_file(
        self,
        event_id: str,
        ics_content: str,
    ) -> Path:
        """Saves generated ICS content to disk with exact CRLF line endings."""
        filepath = self.calendar_dir / f"{event_id}.ics"
        filepath.write_bytes(ics_content.encode("utf-8"))
        return filepath

    def check_conflicts(
        self,
        new_start: datetime.datetime,
        new_end: datetime.datetime,
        existing_slots: List[Dict[str, datetime.datetime]],
    ) -> bool:
        """
        Returns True if new_start and new_end overlap with any existing slot in existing_slots.
        Each existing slot should have 'start' and 'end' keys.
        """
        for slot in existing_slots:
            e_start = slot["start"]
            e_end = slot["end"]
            # Overlap condition: max(start1, start2) < min(end1, end2)
            if max(new_start, e_start) < min(new_end, e_end):
                return True
        return False
