"""
WEB CONTENT FIREWALL AND PROMPT-INJECTION DEFENSE
Treats every scraped web page as untrusted DATA.
Neutralizes prompt injections, enforces permission boundaries,
and ensures web content never overrides system policies.
"""
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class SecurityVerdict:
    allowed: bool
    risk_tier: str
    reason: str
    sanitized: bool

class WebContentFirewall:
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"disregard\s+all\s+prior\s+(prompts|commands|instructions)",
        r"system\s+override",
        r"you\s+are\s+now\s+in\s+(developer|unrestricted|god)\s+mode",
        r"new\s+system\s+prompt\s*:",
        r"<\|im_start\|>system",
        r"\[system\s+instruction\]",
        r"admin_password\s*=",
        r"override_security_policy\(\)"
    ]

    def __init__(self, allow_external_mutations: bool = False):
        self.allow_external_mutations = allow_external_mutations
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]

    def check_interaction_allowed(self, url: str) -> SecurityVerdict:
        if not self.allow_external_mutations:
            return SecurityVerdict(
                allowed=False,
                risk_tier="HIGH",
                reason="Policy Restriction: External browser mutations and automated form submissions require explicit user authorization.",
                sanitized=False
            )
        return SecurityVerdict(
            allowed=True,
            risk_tier="MEDIUM",
            reason="Authorized external interaction under active session policy.",
            sanitized=False
        )

    def detect_prompt_injection(self, text: str) -> List[str]:
        detected = []
        for pattern in self._compiled_patterns:
            matches = pattern.findall(text)
            if matches:
                detected.append(pattern.pattern)
        return detected

    def sanitize_content(self, text: str) -> str:
        if not text:
            return ""
        sanitized = text
        for pattern in self._compiled_patterns:
            sanitized = pattern.sub("[SANITIZED_INJECTION_PAYLOAD]", sanitized)
        sanitized = re.sub(r"<script.*?>.*?</script>", "", sanitized, flags=re.DOTALL | re.IGNORECASE)
        sanitized = re.sub(r"on[a-zA-Z]+\s*=\s*[^\s>]+", "", sanitized, flags=re.IGNORECASE)
        return sanitized

    def sanitize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(response, dict):
            return response
        result = {}
        injections_found = 0
        for k, v in response.items():
            if isinstance(v, str):
                injections = self.detect_prompt_injection(v)
                if injections:
                    injections_found += len(injections)
                result[k] = self.sanitize_content(v)
            elif isinstance(v, dict):
                result[k] = self.sanitize_response(v)
            elif isinstance(v, list):
                sanitized_list = []
                for item in v:
                    if isinstance(item, dict):
                        sanitized_list.append(self.sanitize_response(item))
                    elif isinstance(item, str):
                        injections = self.detect_prompt_injection(item)
                        if injections:
                            injections_found += len(injections)
                        sanitized_list.append(self.sanitize_content(item))
                    else:
                        sanitized_list.append(item)
                result[k] = sanitized_list
            else:
                result[k] = v
        result["_firewall_verdict"] = {
            "untrusted_web_data": True,
            "injections_neutralized": injections_found,
            "status": "SECURE_DATA_BOUNDARY_ENFORCED"
        }
        return result
