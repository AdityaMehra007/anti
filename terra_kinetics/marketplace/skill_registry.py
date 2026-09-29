"""
Terra Physical Skill Registry & Marketplace.
Allows third-party robotic engineers and automation vendors to publish, license,
and execute certified physical skill modules with a 30% platform take-rate.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import hashlib
import time
from ..protocol.ukp_schema import RobotMorphology


class SkillCertificationLevel(str, Enum):
    EXPERIMENTAL = "experimental"
    INDUSTRIAL_ISO = "industrial_iso"
    SURGICAL_MEDICAL = "surgical_medical"
    AEROSPACE_CLEANROOM = "aerospace_cleanroom"


@dataclass
class PhysicalSkillPackage:
    skill_id: str
    name: str
    author: str
    version: str
    supported_morphologies: List[RobotMorphology]
    certification: SkillCertificationLevel
    hourly_license_fee_usd: float
    per_cycle_fee_usd: float
    description: str
    cryptographic_signature: str = ""

    def sign(self, secret_key: str):
        payload = f"{self.skill_id}:{self.version}:{self.author}:{self.hourly_license_fee_usd}:{secret_key}"
        self.cryptographic_signature = hashlib.sha256(payload.encode()).hexdigest()

    def verify(self, secret_key: str) -> bool:
        expected = hashlib.sha256(
            f"{self.skill_id}:{self.version}:{self.author}:{self.hourly_license_fee_usd}:{secret_key}".encode()
        ).hexdigest()
        return self.cryptographic_signature == expected


class SkillMarketplaceRegistry:
    """
    Central repository of verified physical manipulation and locomotion skills.
    """

    def __init__(self, platform_take_rate: float = 0.30):
        self.platform_take_rate = platform_take_rate
        self.catalog: Dict[str, PhysicalSkillPackage] = {}
        self.active_deployments: Dict[str, List[str]] = {}  # robot_id -> list of skill_ids

    def register_skill(self, skill: PhysicalSkillPackage) -> bool:
        if skill.skill_id in self.catalog:
            return False
        self.catalog[skill.skill_id] = skill
        return True

    def deploy_skill_to_robot(
        self, robot_id: str, skill_id: str, morphology: RobotMorphology
    ) -> Tuple[bool, str]:
        if skill_id not in self.catalog:
            return False, f"Skill '{skill_id}' not found in registry."

        skill = self.catalog[skill_id]
        if morphology not in skill.supported_morphologies:
            return (
                False,
                f"Morphology mismatch: skill requires {skill.supported_morphologies}, robot has {morphology}.",
            )

        if robot_id not in self.active_deployments:
            self.active_deployments[robot_id] = []

        if skill_id not in self.active_deployments[robot_id]:
            self.active_deployments[robot_id].append(skill_id)

        return True, f"Skill '{skill.name}' successfully deployed to robot {robot_id}."

    def calculate_revenue_split(self, skill_id: str, billing_amount_usd: float) -> Tuple[float, float]:
        """
        Returns (platform_share_usd, author_share_usd)
        """
        platform_fee = billing_amount_usd * self.platform_take_rate
        author_royalty = billing_amount_usd - platform_fee
        return round(platform_fee, 4), round(author_royalty, 4)
