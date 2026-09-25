"""
OMNIMONEY OS - Outreach Vault Connector
Bridges the outreach_vault_4500.sqlite to track dispatch status, response rates,
and daily conversion metrics for the B2B prospecting pipeline.
"""

import os
import sqlite3
import datetime
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class OutreachRecord:
    id: str
    company: str
    hr_name: str
    hr_email: str
    phone: str
    corridor: str
    sector: str
    target_role: str
    status: str          # DRAFTED, SENT, OPENED, REPLIED, CONVERTED, BOUNCED
    sent_timestamp: str
    response_status: str  # NONE, POSITIVE, NEGATIVE, NO_REPLY
    notes: str


class OutreachVault:
    """Connects to the outreach vault database for tracking dispatched outreach."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(base, "data", "outreach_vault_4500.sqlite")
            self.db_path = candidate if os.path.exists(candidate) else None
        else:
            self.db_path = db_path

    def _connect(self) -> Optional[sqlite3.Connection]:
        if not self.db_path or not os.path.exists(self.db_path):
            return None
        return sqlite3.connect(self.db_path)

    def get_vault_stats(self) -> Dict[str, Any]:
        """Returns overall outreach vault statistics."""
        conn = self._connect()
        if not conn:
            return {"connected": False, "reason": "Outreach vault not found"}

        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM outreach_ledger")
        total = cur.fetchone()[0]

        cur.execute("SELECT status, count(*) FROM outreach_ledger GROUP BY status")
        status_counts = {r[0]: r[1] for r in cur.fetchall()}

        cur.execute("SELECT response_status, count(*) FROM outreach_ledger GROUP BY response_status")
        response_counts = {r[0]: r[1] for r in cur.fetchall()}

        cur.execute("SELECT DISTINCT sector FROM outreach_ledger")
        sectors = [r[0] for r in cur.fetchall()]

        conn.close()
        return {
            "connected": True,
            "total_records": total,
            "status_breakdown": status_counts,
            "response_breakdown": response_counts,
            "sectors_covered": len(sectors),
            "sectors": sectors,
        }

    def get_drafted_outreach(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns records ready to be sent (status=DRAFTED)."""
        conn = self._connect()
        if not conn:
            return []

        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM outreach_ledger WHERE status='DRAFTED' LIMIT ?",
            (limit,),
        )
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_by_sector(self, sector: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns outreach records filtered by sector."""
        conn = self._connect()
        if not conn:
            return []

        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM outreach_ledger WHERE sector LIKE ? LIMIT ?",
            (f"%{sector}%", limit),
        )
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        conn.close()
        return rows

    def mark_sent(self, record_id: str) -> bool:
        """Marks a record as SENT with current timestamp."""
        conn = self._connect()
        if not conn:
            return False

        cur = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cur.execute(
            "UPDATE outreach_ledger SET status='SENT', sent_timestamp=? WHERE id=?",
            (now, record_id),
        )
        affected = cur.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def mark_response(self, record_id: str, response: str, notes: str = "") -> bool:
        """Records a response status for an outreach record."""
        conn = self._connect()
        if not conn:
            return False

        cur = conn.cursor()
        cur.execute(
            "UPDATE outreach_ledger SET response_status=?, notes=? WHERE id=?",
            (response, notes, record_id),
        )
        affected = cur.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def get_conversion_metrics(self) -> Dict[str, Any]:
        """Calculates outreach conversion funnel metrics."""
        conn = self._connect()
        if not conn:
            return {"connected": False}

        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM outreach_ledger")
        total = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM outreach_ledger WHERE status='SENT'")
        sent = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM outreach_ledger WHERE response_status='POSITIVE'")
        positive = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM outreach_ledger WHERE status='CONVERTED'")
        converted = cur.fetchone()[0]

        conn.close()
        return {
            "total_drafted": total,
            "total_sent": sent,
            "positive_responses": positive,
            "converted_deals": converted,
            "send_rate": round(sent / total * 100, 1) if total else 0,
            "response_rate": round(positive / sent * 100, 1) if sent else 0,
            "conversion_rate": round(converted / total * 100, 1) if total else 0,
        }

    def get_daily_dispatch_queue(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """Returns the next batch of records to dispatch today, prioritized by sector diversity."""
        conn = self._connect()
        if not conn:
            return []

        cur = conn.cursor()
        # Get one from each sector first for diversity, then fill remainder
        cur.execute("""
            SELECT * FROM outreach_ledger
            WHERE status='DRAFTED'
            GROUP BY sector
            ORDER BY RANDOM()
            LIMIT ?
        """, (batch_size,))
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]

        if len(rows) < batch_size:
            existing_ids = [r["id"] for r in rows]
            placeholders = ",".join("?" * len(existing_ids)) if existing_ids else "''"
            query = f"""
                SELECT * FROM outreach_ledger
                WHERE status='DRAFTED' AND id NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            """
            params = existing_ids + [batch_size - len(rows)]
            cur.execute(query, params)
            cols2 = [d[0] for d in cur.description]
            rows.extend(dict(zip(cols2, r)) for r in cur.fetchall())

        conn.close()
        return rows[:batch_size]
