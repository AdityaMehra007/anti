"""
Unit and Integration Test Suite for Live Autonomous Recruiter AI Agent & Interactive Calendar Dispatcher.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
import sqlite3
import pytest

from omega.orchestration.calendar_dispatcher import CalendarDispatcher
from omega.orchestration.recruiter_dispatcher import RecruiterDispatcher


@pytest.fixture
def temp_db(tmp_path: Path) -> Path:
    db_file = tmp_path / "test_outreach.db"
    return db_file


@pytest.fixture
def temp_cal_dir(tmp_path: Path) -> Path:
    cal_dir = tmp_path / "calendar_events"
    cal_dir.mkdir(parents=True, exist_ok=True)
    return cal_dir


@pytest.fixture
def dispatcher(temp_db: Path, temp_cal_dir: Path) -> RecruiterDispatcher:
    cal_disp = CalendarDispatcher(calendar_dir=temp_cal_dir)
    return RecruiterDispatcher(db_path=temp_db, calendar_dispatcher=cal_disp)


class TestRecruiterDispatcherParsing:
    def test_email_parsing_and_field_extraction(self, dispatcher: RecruiterDispatcher):
        sample_email = """
        Hi Aditya,

        I am Priya Sharma from Goldman Sachs. We were impressed with your background and are hiring for
        the position of Operations Analyst at Goldman Sachs.
        The offered package for this role is 9.5 LPA.
        We would love to schedule an initial HR screen on 2026-10-15 at 14:00.

        Best regards,
        Priya Sharma
        priya.sharma@gs.com
        """

        parsed = dispatcher.parse_inbound_message(sample_email)

        assert parsed["company"] == "Goldman Sachs"
        assert "Operations Analyst" in parsed["role"]
        assert parsed["recruiter_name"] == "Priya Sharma"
        assert parsed["email"] == "priya.sharma@gs.com"
        assert parsed["ctc_lpa"] == 9.5
        assert parsed["stage"] == "initial_screening"
        assert len(parsed["proposed_slots"]) == 1
        assert parsed["proposed_slots"][0]["start"].strftime("%Y-%m-%d %H:%M") == "2026-10-15 14:00"

    def test_ctc_extraction_varieties(self, dispatcher: RecruiterDispatcher):
        # Format: "₹ 5.5 Lakhs"
        assert dispatcher.extract_ctc("The salary is ₹5.5 Lakhs per year.") == 5.5
        # Format: "CTC: 8 LPA"
        assert dispatcher.extract_ctc("Compensation CTC: 8 LPA.") == 8.0
        # Format: "Rs 6,00,000"
        assert dispatcher.extract_ctc("Annual compensation is Rs 6,00,000 fixed.") == 6.0
        # Missing CTC
        assert dispatcher.extract_ctc("Let's connect to discuss our current openings.") is None


class TestCompensationFilteringAndCounterNegotiation:
    def test_below_salary_floor_counter_offer(self, dispatcher: RecruiterDispatcher):
        """Under ₹3.0L threshold triggers counter-negotiation with profile evidence."""
        under_floor_message = """
        Dear Aditya,
        Greetings from TechCorp. We have an opening for Operations Associate with a CTC of 2.5 LPA.
        Please let us know your availability.
        Regards,
        Rahul Verma
        rahul@techcorp.com
        """

        result = dispatcher.process_inbound(under_floor_message)

        assert result["ctc_lpa"] == 2.5
        assert result["salary_floor_cleared"] is False
        assert result["decision"] == "counter_offer_required"
        # Profile enforcement check
        body = result["reply_body"]
        assert "₹3.0L - ₹11.0L" in body
        assert "BBA International Business" in body or "DSU" in body
        assert "AERO India 2025" in body
        assert "99.2% QA Precision" in body
        assert "Instawork" in body

    def test_acceptable_compensation_acceptance(self, dispatcher: RecruiterDispatcher):
        """Above or equal to ₹3.0L threshold accepts conversation warmly."""
        good_message = """
        Hi Aditya,
        We have a Senior Operations Analyst role at Morgan Stanley with CTC 8.5 LPA.
        Regards,
        Sarah Jenkins
        sarah@ms.com
        """

        result = dispatcher.process_inbound(good_message)

        assert result["ctc_lpa"] == 8.5
        assert result["salary_floor_cleared"] is True
        assert result["decision"] == "accepted_compensation"
        body = result["reply_body"]
        assert "8.5" in body
        assert "confirm availability" in body

    def test_unspecified_ctc_qualification(self, dispatcher: RecruiterDispatcher):
        """Unspecified CTC qualifies compensation floor politely before committing."""
        vague_message = """
        Hi Aditya,
        We came across your profile and would like to invite you for a discussion for a Lead role at Target.
        Regards,
        Ananya Rao
        ananya@target.com
        """

        result = dispatcher.process_inbound(vague_message)

        assert result["ctc_lpa"] is None
        assert result["decision"] == "qualify_compensation_and_proceed"
        body = result["reply_body"]
        assert "₹3.0L - ₹11.0L" in body


class TestCalendarDispatcherRFC5545:
    def test_rfc5545_ics_generation_and_kolkata_timezone(self, dispatcher: RecruiterDispatcher, temp_cal_dir: Path):
        event_id = "REC-TEST-2026-001"
        start = datetime.datetime(2026, 10, 15, 14, 0, 0)
        end = datetime.datetime(2026, 10, 15, 14, 45, 0)

        ics_payload = dispatcher.calendar.generate_ics(
            event_id=event_id,
            title="Aditya Mehra <> Goldman Sachs Operations Interview",
            description="Interview discussion for Operations Analyst role.",
            start_time=start,
            end_time=end,
            attendee_email="priya@gs.com",
            attendee_name="Priya Sharma",
        )

        # RFC 5545 structural requirements
        assert "BEGIN:VCALENDAR" in ics_payload
        assert "VERSION:2.0" in ics_payload
        assert "PRODID:-//Aditya Mehra//Autonomous Recruiter Dispatcher//EN" in ics_payload
        assert "BEGIN:VTIMEZONE" in ics_payload
        assert "TZID:Asia/Kolkata" in ics_payload
        assert "TZNAME:IST" in ics_payload
        assert "TZOFFSETTO:+0530" in ics_payload
        assert "DTSTART;TZID=Asia/Kolkata:20261015T140000" in ics_payload
        assert "DTEND;TZID=Asia/Kolkata:20261015T144500" in ics_payload
        assert "ATTENDEE;" in ics_payload
        assert "mailto:priya@gs.com" in ics_payload
        assert "ORGANIZER;" in ics_payload
        assert "mailto:adityamehra007@gmail.com" in ics_payload
        assert "END:VEVENT" in ics_payload
        assert "END:VCALENDAR" in ics_payload

        # File persistence test
        saved_file = dispatcher.calendar.save_ics_file(event_id, ics_payload)
        assert saved_file.exists()
        assert saved_file.read_bytes().decode("utf-8") == ics_payload

    def test_calendar_slot_conflict_detection(self, dispatcher: RecruiterDispatcher):
        cal = dispatcher.calendar
        existing_slots = [
            {
                "start": datetime.datetime(2026, 10, 15, 14, 0),
                "end": datetime.datetime(2026, 10, 15, 15, 0),
            }
        ]

        # Overlapping slot (14:30 to 15:30)
        assert cal.check_conflicts(
            datetime.datetime(2026, 10, 15, 14, 30),
            datetime.datetime(2026, 10, 15, 15, 30),
            existing_slots,
        ) is True

        # Non-overlapping slot (15:30 to 16:30)
        assert cal.check_conflicts(
            datetime.datetime(2026, 10, 15, 15, 30),
            datetime.datetime(2026, 10, 15, 16, 30),
            existing_slots,
        ) is False


class TestDatabasePersistenceAndCockpitWebhook:
    def test_database_persistence_in_sqlite(self, dispatcher: RecruiterDispatcher, temp_db: Path):
        message = """
        Hi Aditya,
        Role: Operations Associate at Standard Chartered.
        CTC: 7.2 LPA.
        Looking forward to speaking with you.
        Regards,
        Deepak
        deepak@sc.com
        """

        result = dispatcher.process_inbound(message)
        assert result["db_id"] is not None

        # Query database directly
        with sqlite3.connect(str(temp_db)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT company, recruiter_name, email, ctc_lpa, stage FROM inbound_recruiter_events WHERE id = ?", (result["db_id"],))
            row = cursor.fetchone()

        assert row is not None
        assert row[0] == "Standard Chartered"
        assert row[1] == "Deepak"
        assert row[2] == "deepak@sc.com"
        assert row[3] == 7.2

    def test_cockpit_webhook_event_emission(self, dispatcher: RecruiterDispatcher, monkeypatch):
        called = False
        payload_captured = {}

        class DummyResponse:
            status = 200
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        def mock_urlopen(request, timeout):
            nonlocal called, payload_captured
            called = True
            payload_captured = json.loads(request.data.decode("utf-8"))
            return DummyResponse()

        monkeypatch.setattr("urllib.request.urlopen", mock_urlopen)
        dispatcher.cockpit_webhook_url = "https://cockpit.omega.internal/webhook/inbound-recruiter"

        test_msg = "Recruiter test message from Microsoft for Operations PM, CTC 10 LPA. Email hr@microsoft.com"
        result = dispatcher.process_inbound(test_msg)

        assert called is True
        assert result["webhook_dispatched"] is True
        assert payload_captured["ctc_lpa"] == 10.0
