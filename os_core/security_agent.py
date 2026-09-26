import os, re

class SecurityAgent:
    """Zero-Leakage Secrets Protection & Permission Boundary Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def sanitize_log_output(self, text):
        if not text: return ""
        # Redact any accidental tokens/keys/passwords
        sanitized = re.sub(r"(?i)(password|secret|key|token|bearer)\s*[:=]\s*[\w\-]+", r": [REDACTED]", str(text))
        return sanitized

    def verify_permission_boundary(self, action_type):
        if action_type in ["OUTBOUND_EMAIL", "LINKEDIN_INMAIL_POST", "PORTAL_SUBMISSION"]:
            return "REQUIRES_HUMAN_APPROVAL"
        return "SAFE_LOCAL_EXECUTION"
