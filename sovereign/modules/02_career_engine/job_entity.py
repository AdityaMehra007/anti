"""
ADI CAREER OS — JOB ENTITY & NORMALIZATION ENGINE (Sections 13, 14, 15, 293-296)
Standardized schema, freshness categorization, provenance tracking, and deduplication.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
import re
import hashlib

@dataclass
class JobEntity:
    """Standard Job Entity strictly adhering to Section 13 of the Codex."""
    id: str
    source: str
    title: str
    description: str
    location: str
    source_job_id: str = ""
    company_id: str = ""
    company_name: str = ""
    country: str = "India"
    work_model: str = "Hybrid"           # On-site, Hybrid, Remote
    employment_type: str = "Full-time"   # Full-time, Internship, Contract
    experience_min: float = 0.0          # 0.0 for Fresher / Entry Level
    experience_max: float = 2.0
    education: str = "BBA / Any Bachelor's"
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "INR"
    posted_at: str = ""
    deadline: str = ""
    application_url: str = ""
    source_url: str = ""
    skills: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    role_family: str = "Business Operations"
    sales_risk_score: int = 0
    fit_score: float = 0.0
    eligibility_score: float = 0.0
    hiring_probability: float = 0.0
    company_quality: float = 0.0
    career_value: float = 0.0
    ai_relevance: float = 0.0
    status: str = "DISCOVERED"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_verified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def canonical_hash(self) -> str:
        """Deterministic fingerprint for duplicate detection (Section 14)."""
        norm_title = re.sub(r"[^a-z0-9]", "", self.title.lower())
        norm_company = re.sub(r"[^a-z0-9]", "", self.company_name.lower())
        norm_loc = "bengaluru" if any(b in self.location.lower() for b in ["bangalore", "bengaluru"]) else self.location.lower()
        key = f"{norm_company}|{norm_title}|{norm_loc}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

    def get_freshness(self, reference_date: Optional[datetime] = None) -> str:
        """
        Classifies job freshness according to Section 15:
        0–3 days:   VERY_FRESH
        4–7 days:   FRESH
        8–14 days:  ACTIVE
        15–30 days: AGING
        30+ days:   STALE
        """
        if not self.posted_at:
            return "ACTIVE"
        try:
            # Handle common date formats
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%d %b %Y"):
                try:
                    p_date = datetime.strptime(self.posted_at[:10], fmt[:len(self.posted_at[:10])])
                    break
                except ValueError:
                    continue
            else:
                return "ACTIVE"

            ref = reference_date or datetime.now()
            days_old = max(0, (ref - p_date).days)

            if days_old <= 3:
                return "VERY_FRESH"
            elif days_old <= 7:
                return "FRESH"
            elif days_old <= 14:
                return "ACTIVE"
            elif days_old <= 30:
                return "AGING"
            else:
                return "STALE"
        except Exception:
            return "ACTIVE"


class JobNormalizer:
    """Standardizes incoming job attributes according to Sections 293-296."""

    @staticmethod
    def normalize_location(raw_loc: str) -> str:
        """Handles Bengaluru / Bangalore variations (Section 294)."""
        if not raw_loc:
            return "Bengaluru, Karnataka, India"
        low = raw_loc.lower()
        if any(b in low for b in ["bangalore", "bengaluru"]):
            return "Bengaluru, Karnataka, India"
        return raw_loc.strip()

    @staticmethod
    def normalize_experience(exp_str: str) -> Dict[str, float]:
        """Interprets fresher, entry-level, and year ranges (Section 296)."""
        if not exp_str:
            return {"min": 0.0, "max": 2.0, "is_fresher": True}
        low = exp_str.lower()
        nums = [float(n) for n in re.findall(r"\b\d+(?:\.\d+)?\b", low)]
        if len(nums) >= 2:
            return {"min": min(nums[0], nums[1]), "max": max(nums[0], nums[1]), "is_fresher": min(nums[0], nums[1]) == 0}
        elif len(nums) == 1:
            return {"min": 0.0, "max": nums[0], "is_fresher": nums[0] <= 1.0}

        if any(w in low for w in ["fresher", "entry", "graduate"]):
            return {"min": 0.0, "max": 1.0, "is_fresher": True}
        return {"min": 0.0, "max": 2.0, "is_fresher": True}

    @staticmethod
    def normalize_salary(salary_str: str) -> Dict[str, Any]:
        """Parses CTC and converts LPA or thousands to float values (Section 295)."""
        if not salary_str:
            return {"currency": "INR", "min": None, "max": None}
        clean = salary_str.replace(",", "").lower()
        currency = "INR"
        if "$" in clean or "usd" in clean:
            currency = "USD"
        elif "eur" in clean or "€" in clean:
            currency = "EUR"

        # Check for Lakhs (LPA)
        lpa_matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:lpa|lakh|lac|l\b)", clean)
        if len(lpa_matches) >= 2:
            return {"currency": currency, "min": float(lpa_matches[0]) * 100000, "max": float(lpa_matches[1]) * 100000}
        elif len(lpa_matches) == 1:
            return {"currency": currency, "min": float(lpa_matches[0]) * 100000, "max": float(lpa_matches[0]) * 100000}

        # Check raw numbers
        raw_nums = [float(n) for n in re.findall(r"\b\d{5,8}\b", clean)]
        if len(raw_nums) >= 2:
            return {"currency": currency, "min": min(raw_nums), "max": max(raw_nums)}
        elif len(raw_nums) == 1:
            return {"currency": currency, "min": raw_nums[0], "max": raw_nums[0]}

        return {"currency": currency, "min": None, "max": None}


class JobDeduplicator:
    """Prevents duplicate opportunities while preserving provenance (Section 14)."""

    def __init__(self):
        self.seen_urls = set()
        self.seen_hashes = {}

    def is_duplicate(self, job: JobEntity) -> bool:
        if job.application_url and job.application_url in self.seen_urls:
            return True
        chash = job.canonical_hash
        if chash in self.seen_hashes:
            return True
        return False

    def register_job(self, job: JobEntity) -> bool:
        """Returns True if registered (new), False if duplicate."""
        if self.is_duplicate(job):
            return False
        if job.application_url:
            self.seen_urls.add(job.application_url)
        self.seen_hashes[job.canonical_hash] = job.id
        return True
