"""
JOB VERIFICATION ENGINE
Classifies each discovered job into one of 7 canonical verification states:
VERIFIED_ACTIVE, LIKELY_ACTIVE, UNCERTAIN, EXPIRED, CLOSED, DUPLICATE, BROKEN
"""
import time
from enum import Enum
from typing import Dict, Any
from .job_extractor import CanonicalJobRecord
from ..live_web.evidence import SourceTier, SourceQualityEngine

class VerificationState(str, Enum):
    VERIFIED_ACTIVE = "VERIFIED_ACTIVE"
    LIKELY_ACTIVE = "LIKELY_ACTIVE"
    UNCERTAIN = "UNCERTAIN"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"
    DUPLICATE = "DUPLICATE"
    BROKEN = "BROKEN"

class JobVerifier:
    @classmethod
    def verify_job(cls, job: CanonicalJobRecord, raw_response_status: int = 200) -> CanonicalJobRecord:
        if raw_response_status in (404, 410):
            job.verification_state = VerificationState.CLOSED.value
            job.confidence = 0.99
            return job

        if raw_response_status >= 500:
            job.verification_state = VerificationState.BROKEN.value
            job.confidence = 0.50
            return job

        desc = (job.description or "").lower()
        if "position closed" in desc or "no longer accepting applications" in desc or "job expired" in desc:
            job.verification_state = VerificationState.CLOSED.value
            return job

        tier = SourceQualityEngine.classify_source_tier(job.source_url)
        tier_weight = SourceQualityEngine.get_tier_weight(tier)

        if tier == SourceTier.TIER_1_PRIMARY:
            job.verification_state = VerificationState.VERIFIED_ACTIVE.value
            job.confidence = round(0.95 * tier_weight, 2)
        elif tier == SourceTier.TIER_2_PROFESSIONAL:
            job.verification_state = VerificationState.LIKELY_ACTIVE.value
            job.confidence = round(0.85 * tier_weight, 2)
        elif tier == SourceTier.TIER_3_SECONDARY:
            job.verification_state = VerificationState.LIKELY_ACTIVE.value
            job.confidence = round(0.75 * tier_weight, 2)
        else:
            job.verification_state = VerificationState.UNCERTAIN.value
            job.confidence = 0.45

        return job
