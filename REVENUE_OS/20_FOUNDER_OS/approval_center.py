"""
Founder Approval Center for REVENUE OS
Adheres strictly to Directives 5, 14, 88.
Presents approval cards displaying:
- request
- reason
- cost
- upside
- risk
- recommendation
- approve/reject
Guarantees human founder sovereignty for all consequential financial, legal, or high-risk actions.
"""

from typing import Any, Dict, List, Optional
from REVENUE_OS.database.db import DatabaseManager, get_db

class ApprovalCenter:
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()

    def queue_request(
        self,
        requester_agent: str,
        request_type: str,
        title: str,
        reason: str,
        cost_inr: float,
        upside_inr: float,
        risk_level: str,
        recommendation: str
    ) -> int:
        return self.db.create_approval_request(
            requester_agent=requester_agent,
            request_type=request_type,
            title=title,
            reason=reason,
            cost_inr=cost_inr,
            upside_inr=upside_inr,
            risk_level=risk_level,
            recommendation=recommendation
        )

    def get_pending_cards(self) -> List[Dict[str, Any]]:
        return self.db.get_pending_approvals()

    def approve_request(self, request_id: int, notes: str = "Approved by Founder"):
        self.db.resolve_approval(request_id=request_id, decision="APPROVED", notes=notes)

    def reject_request(self, request_id: int, notes: str = "Rejected by Founder"):
        self.db.resolve_approval(request_id=request_id, decision="REJECTED", notes=notes)
