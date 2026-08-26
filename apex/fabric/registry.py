"""
APEX V3 Universal Capability Fabric - Capability Registry
Maintains typed registry across all 13 Capability Categories.
"""
from typing import Dict, List, Optional, Any
from .schema import UniversalCapability, CapabilityCategory, CapabilityHealth, CapabilityScore

class CapabilityRegistry:
    def __init__(self):
        self._capabilities: Dict[str, UniversalCapability] = {}
        self._seed_baseline_capabilities()

    def _seed_baseline_capabilities(self):
        baseline = [
            UniversalCapability(
                capability_id="CAP-COMP-01",
                name="Python Runtime Executor",
                category=CapabilityCategory.COMPUTE,
                purpose="Executes validated Python scripts and unit tests deterministically.",
                tools=["run_command", "python_executor"],
                agents=["developer", "qa_agent"],
                tests=["test_apex_master.py"]
            ),
            UniversalCapability(
                capability_id="CAP-DATA-01",
                name="Data Ingestion & Integrity Validator",
                category=CapabilityCategory.DATA,
                purpose="Validates, normalizes, and cleans multi-source tabular data.",
                tools=["file_reader", "qa_test_runner"],
                agents=["data_analyst"],
                skills=["analytics-skill-01", "analytics-skill-02"]
            ),
            UniversalCapability(
                capability_id="CAP-RES-01",
                name="Market Intelligence & Web Research",
                category=CapabilityCategory.RESEARCH,
                purpose="Performs systematic search, extraction, and contradiction checks.",
                tools=["search_web", "read_url_content"],
                agents=["researcher"],
                skills=["market-intel-skill-01", "b2b-sales-skill-01"]
            ),
            UniversalCapability(
                capability_id="CAP-AI-01",
                name="Truth & Evidence Classifier",
                category=CapabilityCategory.AI,
                purpose="Classifies claims into OBSERVED, VERIFIED, INFERRED, ESTIMATED, UNKNOWN.",
                tools=["echo"],
                agents=["verification_agent"],
                skills=["genai-skill-01"]
            ),
            UniversalCapability(
                capability_id="CAP-DEV-01",
                name="Microservice & Web App Scaffolder",
                category=CapabilityCategory.DEVELOPMENT,
                purpose="Generates production-grade HTML/JS/CSS and FastAPI services.",
                tools=["file_writer", "qa_test_runner"],
                agents=["developer", "architect"],
                skills=["devops-skill-01", "devops-skill-02"]
            ),
            UniversalCapability(
                capability_id="CAP-SEC-01",
                name="Security Policy & Destructive Command Filter",
                category=CapabilityCategory.SECURITY,
                purpose="Audits command strings and enforces A0-A5 autonomy bounds.",
                tools=["echo"],
                agents=["security_agent"],
                skills=["devops-skill-20"]
            ),
            UniversalCapability(
                capability_id="CAP-BIZ-01",
                name="Financial 3-Statement & DCF Modeler",
                category=CapabilityCategory.BUSINESS,
                purpose="Generates balance sheets, cash flow models, and valuations.",
                tools=["file_writer"],
                agents=["executive_agent"],
                skills=["finance-skill-01", "finance-skill-02"]
            ),
            UniversalCapability(
                capability_id="CAP-AUTO-01",
                name="Self-Healing Fault Recovery",
                category=CapabilityCategory.AUTOMATION,
                purpose="Detects, diagnoses, repairs, and re-tests failed operations.",
                tools=["echo", "qa_test_runner"],
                agents=["qa_agent", "developer"],
                skills=["devops-skill-10"]
            ),
            UniversalCapability(
                capability_id="CAP-KNOW-01",
                name="Scoped Memory & Knowledge Indexer",
                category=CapabilityCategory.KNOWLEDGE,
                purpose="Maintains task, project, and session memory without context flooding.",
                tools=["file_reader"],
                agents=["planner", "researcher"]
            ),
            UniversalCapability(
                capability_id="CAP-COMM-01",
                name="Executive Deliverable & Artifact Generator",
                category=CapabilityCategory.COMMUNICATION,
                purpose="Formats and writes structured markdown executive summaries.",
                tools=["file_writer"],
                agents=["planner", "verification_agent"]
            )
        ]
        for cap in baseline:
            self.register(cap)

    def register(self, capability: UniversalCapability):
        self._capabilities[capability.capability_id] = capability

    def get(self, capability_id: str) -> Optional[UniversalCapability]:
        return self._capabilities.get(capability_id)

    def list_all(self) -> List[UniversalCapability]:
        return list(self._capabilities.values())

    def list_by_category(self, category: CapabilityCategory) -> List[UniversalCapability]:
        return [c for c in self._capabilities.values() if c.category == category]

    def update_health(self, capability_id: str, new_health: CapabilityHealth):
        if capability_id in self._capabilities:
            self._capabilities[capability_id].status = new_health
