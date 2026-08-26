"""
APPROVAL ENGINE
Mandatory policy gate for high-impact actions:
- External Email Dispatch
- Application Submissions
- External Phone Calls
- Deployments / Deletions
- Financial Transactions
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class ApprovalRequest:
    request_id: str
    action_type: str
    target_entity: str
    details: Dict[str, Any]
    status: str = "PENDING_APPROVAL" # PENDING_APPROVAL, APPROVED, REJECTED
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    approved_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ApprovalEngine:
    def __init__(self):
        self._requests: Dict[str, ApprovalRequest] = {}

    def request_approval(self, action_type: str, target: str, details: Dict[str, Any]) -> ApprovalRequest:
        req_id = f"APPR-{len(self._requests)+1:04d}"
        req = ApprovalRequest(req_id, action_type, target, details)
        self._requests[req_id] = req
        return req

    def approve(self, req_id: str, approver: str = "User") -> bool:
        if req_id in self._requests:
            self._requests[req_id].status = "APPROVED"
            self._requests[req_id].approved_by = approver
            return True
        return False

    def is_action_authorized(self, req_id: str) -> bool:
        req = self._requests.get(req_id)
        return bool(req and req.status == "APPROVED")
