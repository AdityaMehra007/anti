"""
Postman Project API-Mesh-OS: Autonomous Contract Synthesizer & Breaking Change Detector
Parses API contracts, detects breaking semantic changes, and generates mock responses in real time.
"""
from typing import Dict, List, Any, Tuple

class ApiMeshSynthesizer:
    def __init__(self):
        self.endpoints: Dict[str, Dict[str, Any]] = {}

    def register_endpoint(self, path: str, method: str, required_params: List[str], schema_version: int):
        self.endpoints[f"{method.upper()}:{path}"] = {
            "required_params": set(required_params),
            "schema_version": schema_version
        }

    def check_breaking_changes(self, path: str, method: str, new_required_params: List[str]) -> Tuple[bool, List[str]]:
        key = f"{method.upper()}:{path}"
        if key not in self.endpoints:
            return False, [] # New endpoint is not breaking

        old_params = self.endpoints[key]["required_params"]
        new_params = set(new_required_params)

        # Breaking change: newly added required parameters that clients don't yet supply
        added_required = list(new_params - old_params)
        is_breaking = len(added_required) > 0
        return is_breaking, added_required
