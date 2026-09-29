-- REVENUE OS Database Schema
-- Master Relational Storage for 24/7 Autonomous Revenue Engine

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. REVENUE METRICS & FINANCIAL TELEMETRY
CREATE TABLE IF NOT EXISTS revenue_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE, -- YYYY-MM-DD
    revenue_inr REAL DEFAULT 0.0,
    gross_profit_inr REAL DEFAULT 0.0,
    variable_cost_inr REAL DEFAULT 0.0,
    fixed_cost_inr REAL DEFAULT 0.0,
    mrr_inr REAL DEFAULT 0.0,
    arr_inr REAL DEFAULT 0.0,
    active_customers INTEGER DEFAULT 0,
    churned_customers INTEGER DEFAULT 0,
    ai_cost_usd REAL DEFAULT 0.0,
    ai_cost_inr REAL DEFAULT 0.0,
    founder_hours REAL DEFAULT 0.0,
    revenue_per_founder_hour REAL DEFAULT 0.0,
    revenue_per_ai_dollar REAL DEFAULT 0.0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 2. OPPORTUNITIES (200-Opportunity Funnel)
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    target_customer TEXT NOT NULL,
    core_problem TEXT NOT NULL,
    demand_signal TEXT NOT NULL,
    willingness_to_pay_score REAL DEFAULT 0.0,
    suggested_price_inr REAL DEFAULT 0.0,
    suggested_price_usd REAL DEFAULT 0.0,
    acquisition_channel TEXT NOT NULL,
    competition_level TEXT NOT NULL,
    delivery_cost_inr REAL DEFAULT 0.0,
    automation_potential_pct REAL DEFAULT 0.0,
    gross_margin_pct REAL DEFAULT 0.0,
    recurring_potential_pct REAL DEFAULT 0.0,
    scalability_score REAL DEFAULT 0.0,
    founder_time_hours_per_week REAL DEFAULT 0.0,
    legal_risk_level TEXT NOT NULL,
    platform_risk_level TEXT NOT NULL,
    ai_leverage_score REAL DEFAULT 0.0,
    time_to_first_money_days INTEGER DEFAULT 0,
    total_score REAL DEFAULT 0.0,
    funnel_tier TEXT DEFAULT 'DATABASE', -- 'DATABASE', 'TOP_50', 'TOP_20', 'TOP_10', 'TOP_5', 'TOP_3', 'PRIMARY_ENGINE', 'SECONDARY_EXP'
    status TEXT DEFAULT 'ACTIVE',
    created_at TEXT DEFAULT (datetime('now'))
);

-- 3. ETHICAL LEADS
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    website TEXT,
    industry TEXT NOT NULL,
    geography TEXT NOT NULL,
    company_size TEXT,
    contact_name TEXT,
    contact_role TEXT,
    contact_email TEXT,
    contact_url TEXT,
    buying_trigger TEXT,
    source TEXT NOT NULL,
    icp_fit_score REAL DEFAULT 0.0,
    pain_score REAL DEFAULT 0.0,
    trigger_score REAL DEFAULT 0.0,
    ability_to_pay_score REAL DEFAULT 0.0,
    urgency_score REAL DEFAULT 0.0,
    reachability_score REAL DEFAULT 0.0,
    total_lead_score REAL DEFAULT 0.0,
    next_action TEXT,
    status TEXT DEFAULT 'NEW', -- NEW, RESEARCHED, CONTACTED, QUALIFIED, DISQUALIFIED
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 4. 12-STAGE SALES CRM PIPELINE
CREATE TABLE IF NOT EXISTS deals (
    id TEXT PRIMARY KEY,
    lead_id TEXT REFERENCES leads(id) ON DELETE SET NULL,
    deal_name TEXT NOT NULL,
    stage TEXT NOT NULL, -- LEAD, CONTACT, RESPONSE, DISCOVERY, QUALIFIED, DEMO, PROPOSAL, NEGOTIATION, WON, ONBOARDING, RETENTION, EXPANSION
    deal_value_inr REAL NOT NULL,
    currency TEXT DEFAULT 'INR',
    win_probability REAL DEFAULT 0.1,
    expected_revenue_inr REAL NOT NULL,
    owner_agent TEXT DEFAULT 'SalesAssistant',
    objections_noted TEXT,
    loss_reason TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 5. OFFERS & PACKAGES
CREATE TABLE IF NOT EXISTS offers (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    tier TEXT NOT NULL, -- LEVEL_1_SERVICE, LEVEL_2_PRODUCTIZED, LEVEL_3_AUTOMATION, LEVEL_4_SOFTWARE, LEVEL_5_SUBSCRIPTION
    target_customer TEXT NOT NULL,
    core_problem TEXT NOT NULL,
    promised_outcome TEXT NOT NULL,
    price_inr REAL NOT NULL,
    price_usd REAL NOT NULL,
    delivery_cost_inr REAL NOT NULL,
    gross_margin_pct REAL NOT NULL,
    delivery_turnaround_days INTEGER NOT NULL,
    proof_points TEXT,
    guarantee_policy TEXT,
    objections_handled TEXT,
    primary_channel TEXT,
    active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 6. FOUNDER APPROVAL CENTER (Consequential Actions Queue)
CREATE TABLE IF NOT EXISTS approval_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_agent TEXT NOT NULL,
    request_type TEXT NOT NULL, -- FINANCIAL_SPEND, CONTRACT, HIGH_VALUE_OUTREACH, PRICING_CHANGE, SECURITY_CREDENTIAL
    title TEXT NOT NULL,
    reason TEXT NOT NULL,
    cost_inr REAL DEFAULT 0.0,
    upside_inr REAL DEFAULT 0.0,
    risk_level TEXT DEFAULT 'LOW', -- LOW, MEDIUM, HIGH, CRITICAL
    recommendation TEXT NOT NULL,
    status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED
    decision_notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    resolved_at TEXT
);

-- 7. AUDIT LOGS (Tamper-Evident Trail)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    action_tier TEXT NOT NULL, -- READ, ANALYZE, DRAFT, RECOMMEND, EXECUTE, APPROVE
    action_name TEXT NOT NULL,
    payload_json TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 8. EXPERIMENTS
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    hypothesis TEXT NOT NULL,
    target_metric TEXT NOT NULL,
    cost_inr REAL DEFAULT 0.0,
    duration_days INTEGER DEFAULT 14,
    status TEXT DEFAULT 'DRAFT', -- DRAFT, RUNNING, COMPLETED, CANCELLED
    result TEXT,
    decision TEXT, -- KEEP, SCALE, KILL
    created_at TEXT DEFAULT (datetime('now'))
);

-- 9. AUTOMATIONS & SCHEDULED RUNS
CREATE TABLE IF NOT EXISTS automations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    schedule TEXT NOT NULL, -- HOURLY, DAILY, WEEKLY, MONTHLY
    target_agent TEXT NOT NULL,
    last_run TEXT,
    next_run TEXT,
    status TEXT DEFAULT 'ACTIVE', -- ACTIVE, PAUSED, ERROR
    last_result_summary TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 10. DAILY CASH TRANSACTIONS & PROFIT LEDGER
CREATE TABLE IF NOT EXISTS daily_cash_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT NOT NULL, -- YYYY-MM-DD
    transaction_time TEXT NOT NULL, -- HH:MM:SS
    source_type TEXT NOT NULL, -- 'B2B_RETAINER', 'MICRO_SAAS_TOOL', 'CONSULTING_HOURLY', 'CAREER_ACCRUAL', 'GLOBAL_EXPORT'
    client_or_customer TEXT NOT NULL,
    description TEXT NOT NULL,
    gross_amount_inr REAL NOT NULL,
    currency TEXT DEFAULT 'INR',
    original_currency_amount REAL NOT NULL,
    variable_cost_inr REAL DEFAULT 0.0,
    net_profit_inr REAL NOT NULL,
    profit_margin_pct REAL NOT NULL,
    payment_rail TEXT NOT NULL, -- 'UPI_HDFC', 'STRIPE_USD', 'WISE_ACH', 'RAZORPAY_INR', 'BANK_NEFT'
    payment_status TEXT DEFAULT 'COMPLETED', -- 'COMPLETED', 'PENDING', 'SCHEDULED'
    reference_id TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
