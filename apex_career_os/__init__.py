"""
APEX CAREER SUPREMACY OS (Ω-CAREER-UNIVERSE)
=============================================
Version: 10.0.0-APEX-SUPREME
The ultimate autonomous career intelligence, job discovery, online learning,
recruiter orchestration, ATS tailoring, and career velocity platform.
"""

from apex_career_os.core.truth_layer import (
    get_candidate_profile, VERIFIED_EVIDENCE, VERIFIED_CERTIFICATIONS, VERIFIED_SKILLS
)
from apex_career_os.core.knowledge_learning_vault import KnowledgeLearningVault
from apex_career_os.scrapers.multi_portal_harvester import MultiPortalHarvester
from apex_career_os.orchestrator import ApexCareerOrchestrator

__version__ = "10.0.0-APEX-SUPREME"
__all__ = [
    "get_candidate_profile",
    "KnowledgeLearningVault",
    "MultiPortalHarvester",
    "ApexCareerOrchestrator"
]
