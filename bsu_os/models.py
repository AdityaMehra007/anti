"""BSU OS Domain Schemas and Pydantic Data Models.

Defines typed representations for startups, founders, investors, funding,
jobs, events, clusters, scoring payloads, and multi-agent copilot contracts.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FounderModel(BaseModel):
    id: Optional[int] = None
    startup_id: Optional[int] = None
    name: str
    role: str
    bio: str
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    prior_exits: bool = False
    educational_background: Optional[str] = None
    verified_status: bool = True


class FundingRoundModel(BaseModel):
    id: Optional[int] = None
    startup_id: Optional[int] = None
    round_name: str
    amount_usd: float
    round_date: str
    lead_investors: List[str] = Field(default_factory=list)
    valuation_usd: Optional[float] = None
    source_url: Optional[str] = None


class JobModel(BaseModel):
    id: Optional[int] = None
    startup_id: int
    startup_name: Optional[str] = None
    title: str
    department: str
    employment_type: str = "Full-time"
    experience_level: str = "Mid-Senior"
    location_cluster_id: str
    remote_policy: str = "In-office / Hybrid"
    min_salary_lpa: Optional[float] = None
    max_salary_lpa: Optional[float] = None
    skills_required: List[str] = Field(default_factory=list)
    description: str
    apply_url: Optional[str] = None
    career_score: float = 75.0
    posted_date: str
    is_active: bool = True


class EventModel(BaseModel):
    id: Optional[int] = None
    title: str
    event_type: str
    date_time: str
    location_cluster_id: str
    venue_name: str
    organizer: str
    registration_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_featured: bool = False


class InvestorModel(BaseModel):
    id: Optional[int] = None
    name: str
    firm_name: str
    investor_type: str  # Institutional VC, Micro VC, Angel Network, Corporate VC
    thesis: str
    aum_usd: Optional[float] = None
    key_investments: List[str] = Field(default_factory=list)
    cluster_id: str = "cbd_central"
    website_url: Optional[str] = None
    verified_status: bool = True


class StartupModel(BaseModel):
    id: Optional[int] = None
    name: str
    slug: str
    sector: str
    sub_sector: str
    stage: str  # Pre-seed, Seed, Series A, Series B, Series C+, Unicorn, Bootstrapped, Public
    founded_year: int
    cluster_id: str
    location_address: str
    website_url: str
    logo_url: Optional[str] = None
    elevator_pitch: str
    full_description: str
    headcount: int
    hiring_status: bool = True
    tech_stack: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    verified_status: bool = True
    
    # Quantified Scores (0.0 to 100.0)
    power_score: float = 0.0
    career_score: float = 0.0
    momentum_score: float = 0.0
    risk_score: float = 0.0
    future_potential_score: float = 0.0
    
    total_funding_usd: float = 0.0
    latest_valuation_usd: Optional[float] = None
    
    # Nested relations when hydrated
    founders: List[FounderModel] = Field(default_factory=list)
    funding_rounds: List[FundingRoundModel] = Field(default_factory=list)
    open_jobs: List[JobModel] = Field(default_factory=list)


class ClusterModel(BaseModel):
    id: str
    name: str
    description: str
    lat: float
    lng: float
    zoom: int
    primary_sectors: List[str]
    vibe: str
    startup_count: int = 0
    average_power_score: float = 0.0
    total_funding_usd: float = 0.0


class ScoreCardModel(BaseModel):
    startup_id: int
    startup_name: str
    power_score: float
    career_score: float
    momentum_score: float
    risk_score: float
    future_potential_score: float
    breakdown: Dict[str, Any]


class WatchlistModel(BaseModel):
    id: Optional[int] = None
    user_id: str = "guest_default"
    entity_type: str  # startup, job, investor, founder
    entity_id: int
    notes: Optional[str] = None
    created_at: Optional[str] = None


class AlertModel(BaseModel):
    id: Optional[int] = None
    alert_type: str  # funding_surge, hiring_spurt, event_alert, leadership_move
    headline: str
    summary: str
    entity_name: str
    cluster_id: Optional[str] = None
    severity: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    created_at: str


class CopilotQueryModel(BaseModel):
    query: str
    mode: str = "general"  # general, founder, investor, career, recruiter, geo
    user_persona: Optional[str] = "explorer"


class CopilotResponseModel(BaseModel):
    verdict: str
    evidence: List[str]
    why_it_matters: str
    fit_score: float
    recommended_action: str
    risk_factors: List[str]
    references: List[Dict[str, Any]]
