"""Pydantic V2 Domain Models for GLOBAL CAPITAL OS.

Enforces absolute reality rules, strict money categorization,
type safety, and rigorous audit attributes.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CurrencyCode(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    AED = "AED"
    SGD = "SGD"
    JPY = "JPY"
    AUD = "AUD"


class AccountCategory(str, Enum):
    OPERATING = "OPERATING"                  # Day-to-day business receipts & payments
    TAX_RESERVE = "TAX_RESERVE"              # Segregated GST and Advance Tax reserves
    EMERGENCY_RESERVE = "EMERGENCY_RESERVE"  # 6-month liquidity survival buffer
    GROWTH = "GROWTH"                        # Approved reinvestment / CAC / tooling
    INVESTMENT = "INVESTMENT"                # Liquid treasury / approved cash-equivalents
    FOREIGN_CURRENCY = "FOREIGN_CURRENCY"    # Lawful offshore or multi-currency balances


class TransactionCategory(str, Enum):
    REVENUE_CUSTOMER = "REVENUE_CUSTOMER"
    REVENUE_PILOT = "REVENUE_PILOT"
    COST_AI = "COST_AI"
    COST_INFRA = "COST_INFRA"
    COST_SOFTWARE = "COST_SOFTWARE"
    COST_PAYMENT_FEE = "COST_PAYMENT_FEE"
    COST_TAX = "COST_TAX"
    COST_PROFESSIONAL = "COST_PROFESSIONAL"
    DEBT_SERVICE = "DEBT_SERVICE"
    INVESTMENT_DEPLOYMENT = "INVESTMENT_DEPLOYMENT"
    TRANSFER_INTERNAL = "TRANSFER_INTERNAL"


class TransactionStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    RECONCILED = "RECONCILED"
    DISPUTED = "DISPUTED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionTier(str, Enum):
    READ = "READ"
    ANALYZE = "ANALYZE"
    SIMULATE = "SIMULATE"
    RECOMMEND = "RECOMMEND"
    PREPARE = "PREPARE"
    EXECUTE = "EXECUTE"
    APPROVE = "APPROVE"


class OpportunityTier(str, Enum):
    DATABASE = "DATABASE"
    TOP_50 = "TOP_50"
    TOP_20 = "TOP_20"
    TOP_10 = "TOP_10"
    TOP_5 = "TOP_5"
    TOP_3 = "TOP_3"
    PRIMARY_ENGINE = "PRIMARY_ENGINE"


class SalesStage(str, Enum):
    LEAD = "LEAD"
    CONTACT = "CONTACT"
    RESPONSE = "RESPONSE"
    DISCOVERY = "DISCOVERY"
    QUALIFIED = "QUALIFIED"
    DEMO = "DEMO"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    ONBOARDING = "ONBOARDING"
    RETENTION = "RETENTION"
    EXPANSION = "EXPANSION"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FROZEN = "FROZEN"


class LegalCheckStatus(str, Enum):
    COMPLIANT = "COMPLIANT"
    CONDITIONS_APPLY = "CONDITIONS_APPLY"
    ADVISOR_REVIEW_REQUIRED = "ADVISOR_REVIEW_REQUIRED"
    PROHIBITED = "PROHIBITED"


# --- Data Models ---

class LegalEntity(BaseModel):
    id: str
    name: str
    jurisdiction: str = "India"
    entity_type: str = "Sole Proprietorship"  # Or Private Limited
    pan_gst: Optional[str] = None
    status: str = "ACTIVE"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BankAccount(BaseModel):
    id: str
    entity_id: str
    institution: str
    account_name: str
    account_number_masked: str
    currency: CurrencyCode
    category: AccountCategory
    balance: float = Field(ge=0.0, default=0.0)
    balance_inr: float = Field(ge=0.0, default=0.0)
    purpose: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LedgerTransaction(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_account_id: Optional[str] = None
    destination_account_id: Optional[str] = None
    counterparty_name: str
    amount: float
    currency: CurrencyCode
    amount_inr: float
    category: TransactionCategory
    description: str
    tax_reserve_amount_inr: float = 0.0
    status: TransactionStatus = TransactionStatus.PENDING_APPROVAL
    reconciliation_id: Optional[str] = None
    approval_id: Optional[str] = None


class Opportunity(BaseModel):
    id: str
    name: str
    category: str
    target_customer: str
    core_problem: str
    price_usd: float = 0.0
    price_inr: float = 0.0
    delivery_cost_inr: float = 0.0
    gross_margin_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    time_to_first_money_days: int = 0
    founder_hours_week: float = 0.0
    automation_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    recurring_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    capital_requirement_inr: float = 0.0
    zero_capital_score: float = 0.0
    funnel_tier: OpportunityTier = OpportunityTier.DATABASE
    status: str = "ACTIVE"


class LeadRecord(BaseModel):
    id: str
    company_name: str
    website: Optional[str] = None
    contact_name: str
    contact_title: str
    contact_email: str
    industry: str
    location: str
    buying_trigger: str
    custom_icebreaker: str
    lead_score: str = "Hot"  # Hot, Warm, Cold
    icp_fit_score: float = Field(ge=0.0, le=100.0, default=80.0)
    status: str = "NEW"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DealRecord(BaseModel):
    id: str
    lead_id: Optional[str] = None
    deal_name: str
    stage: SalesStage = SalesStage.LEAD
    deal_value_inr: float = 0.0
    deal_value_usd: float = 0.0
    currency: CurrencyCode = CurrencyCode.INR
    win_probability: float = Field(ge=0.0, le=1.0, default=0.1)
    expected_value_inr: float = 0.0
    owner_agent: str = "RevenueCommander"
    next_step: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DebtFacility(BaseModel):
    id: str
    lender_name: str
    facility_type: str  # e.g., Working Capital, Revenue-Based Financing, Overdraft
    principal_inr: float
    interest_rate_apr: float
    monthly_service_inr: float
    maturity_date: str
    collateral_description: str
    covenants: str
    is_compliant_rbi: bool = True
    purpose: str


class InvestmentHolding(BaseModel):
    id: str
    asset_name: str
    asset_type: str  # Cash Equivalent, Overnight Fund, Liquid Fund, T-Bill
    cost_basis_inr: float
    current_value_inr: float
    unrealized_pnl_inr: float = 0.0
    allocation_pct: float = 0.0
    thesis: str
    kill_condition: str
    downside_limit_pct: float = 5.0
    is_authorized: bool = True


class ApprovalRequest(BaseModel):
    id: str
    requester_agent: str
    action_type: str
    amount: float
    currency: CurrencyCode
    amount_inr: float
    source_account: str
    destination: str
    purpose: str
    expected_benefit: str
    worst_case_loss: str
    legal_status: LegalCheckStatus
    tax_considerations: str
    risk_level: RiskLevel
    recommendation: str
    alternatives: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    decision_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None


class MasterScores(BaseModel):
    revenue_score: float = Field(ge=0.0, le=100.0, default=0.0)
    profit_score: float = Field(ge=0.0, le=100.0, default=0.0)
    capital_efficiency_score: float = Field(ge=0.0, le=100.0, default=0.0)
    liquidity_score: float = Field(ge=0.0, le=100.0, default=0.0)
    debt_safety_score: float = Field(ge=0.0, le=100.0, default=0.0)
    investment_quality_score: float = Field(ge=0.0, le=100.0, default=0.0)
    treasury_quality_score: float = Field(ge=0.0, le=100.0, default=0.0)
    ai_leverage_score: float = Field(ge=0.0, le=100.0, default=0.0)
    founder_leverage_score: float = Field(ge=0.0, le=100.0, default=0.0)
    global_readiness_score: float = Field(ge=0.0, le=100.0, default=0.0)
    security_score: float = Field(ge=0.0, le=100.0, default=0.0)
    compliance_score: float = Field(ge=0.0, le=100.0, default=0.0)
    moat_score: float = Field(ge=0.0, le=100.0, default=0.0)
    # Compound Scores
    master_wealth_score: float = Field(ge=0.0, le=100.0, default=0.0)
    master_founder_score: float = Field(ge=0.0, le=100.0, default=0.0)


class FinancialTelemetry(BaseModel):
    total_cash_inr: float = 0.0
    liquid_assets_inr: float = 0.0
    total_debt_inr: float = 0.0
    net_capital_inr: float = 0.0
    monthly_burn_inr: float = 0.0
    runway_months: float = 0.0
    revenue_mtd_inr: float = 0.0
    profit_mtd_inr: float = 0.0
    gross_margin_pct: float = 0.0
    pending_approvals_count: int = 0
    active_deals_count: int = 0
    pipeline_value_inr: float = 0.0
    system_status: str = "NORMAL"  # NORMAL, FROZEN, DEGRADED
    updated_at: datetime = Field(default_factory=datetime.utcnow)
