import os, traceback
from datetime import datetime
from memory import SovereignMemory

class SelfHealingEngine:
    '''Automatic Failure Diagnosis, Root-Cause Analysis & Repair Pipeline.'''
    def __init__(self, memory=None):
        self.memory = memory or SovereignMemory()

    def diagnose_and_record(self, component_name, error_exception, context=None):
        err_msg = str(error_exception)
        tb_str = traceback.format_exc()
        now = datetime.now().isoformat()

        diagnosis = {
            "component": component_name,
            "error_type": type(error_exception).__name__,
            "message": err_msg,
            "traceback": tb_str[:500],
            "context": context,
            "recommended_remediation": self._suggest_fix(err_msg),
            "timestamp": now
        }

        # Store in Failure Memory Layer
        mem_id = self.memory.store(
            layer="FAILURE",
            scope=component_name,
            key_tag=f"ERROR_{type(error_exception).__name__}",
            content=diagnosis,
            confidence=1.0,
            provenance="SelfHealingEngine"
        )
        return diagnosis, mem_id

    def _suggest_fix(self, err_msg):
        msg_lower = err_msg.lower()
        if "syntaxerror" in msg_lower or "quote" in msg_lower:
            return "Sanitize Python heredoc strings or avoid unescaped multiline quotes."
        if "filenotfounderror" in msg_lower:
            return "Verify path existence and create parent directories with exist_ok=True."
        if "permission" in msg_lower:
            return "Route consequential action to approval_queue.csv for explicit human signoff."
        return "Inspect log trace and apply targeted defensive check."
