/**
 * OMNIVANTA — Commercial Metering & Billing Engine
 * 
 * Tracks real AI usage, compute runtime, agent tasks, and workflow runs.
 * Manages SaaS tiers (Starter, Team, Business, Enterprise) and generates itemized invoices.
 * 
 * @module billing/metering
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('billing');

const TIERS = {
    'starter': {
        name: 'Starter',
        monthlyPriceUSD: 99,
        includedTokens: 1000000,
        includedAgentRuns: 500,
        includedWorkflows: 100,
        maxAutonomyLevel: 2
    },
    'team': {
        name: 'Team',
        monthlyPriceUSD: 499,
        includedTokens: 10000000,
        includedAgentRuns: 5000,
        includedWorkflows: 1000,
        maxAutonomyLevel: 3
    },
    'business': {
        name: 'Business',
        monthlyPriceUSD: 1999,
        includedTokens: 50000000,
        includedAgentRuns: 25000,
        includedWorkflows: 5000,
        maxAutonomyLevel: 4
    },
    'enterprise': {
        name: 'Enterprise',
        monthlyPriceUSD: 9999,
        includedTokens: 500000000,
        includedAgentRuns: 200000,
        includedWorkflows: 50000,
        maxAutonomyLevel: 5
    }
};

/**
 * Ensure billing usage records table exists
 */
function ensureBillingTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS billing_usage (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            resource_type TEXT NOT NULL, -- 'tokens', 'agent_run', 'workflow_run', 'api_call'
            units INTEGER NOT NULL,
            cost_usd REAL NOT NULL,
            metadata TEXT,
            recorded_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_billing_org ON billing_usage(org_id);
    `);
}

/**
 * Record a billable event (token usage, agent task execution, workflow run)
 */
function recordUsage({ orgId = 'org-default', resourceType, units = 1, costUSD = 0, metadata = {} }) {
    ensureBillingTable();
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();

    db.prepare(`
        INSERT INTO billing_usage (id, org_id, resource_type, units, cost_usd, metadata, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(id, orgId, resourceType, units, costUSD, JSON.stringify(metadata), now);

    recordAudit({ actor: 'billing', action: 'billing.usage_recorded', details: { orgId, resourceType, units, costUSD } });
    return { id, orgId, resourceType, units, costUSD, recordedAt: now };
}

/**
 * Aggregate usage metrics for an organization
 */
function getUsageSummary(orgId = 'org-default') {
    ensureBillingTable();
    const db = getDb();
    const rows = db.prepare(`
        SELECT resource_type, SUM(units) as total_units, SUM(cost_usd) as total_cost 
        FROM billing_usage 
        WHERE org_id = ? 
        GROUP BY resource_type
    `).all(orgId);

    const summary = {
        orgId,
        tokens: 0,
        agentRuns: 0,
        workflowRuns: 0,
        apiCalls: 0,
        totalCostUSD: 0
    };

    rows.forEach(r => {
        if (r.resource_type === 'tokens') summary.tokens = r.total_units;
        if (r.resource_type === 'agent_run') summary.agentRuns = r.total_units;
        if (r.resource_type === 'workflow_run') summary.workflowRuns = r.total_units;
        if (r.resource_type === 'api_call') summary.apiCalls = r.total_units;
        summary.totalCostUSD += (r.total_cost || 0);
    });

    return summary;
}

/**
 * Generate an itemized billing invoice
 */
function generateInvoice(orgId = 'org-default', tierName = 'business') {
    const tier = TIERS[tierName.toLowerCase()] || TIERS.business;
    const usage = getUsageSummary(orgId);

    const invoice = {
        invoiceNumber: `INV-${Date.now().toString().substring(5)}`,
        orgId,
        tier: tier.name,
        period: `${new Date().toLocaleString('en-US', { month: 'long', year: 'numeric' })}`,
        baseSubscriptionUSD: tier.monthlyPriceUSD,
        usageSummary: usage,
        overageCostUSD: Math.max(0, usage.totalCostUSD - 100),
        totalDueUSD: tier.monthlyPriceUSD + Math.max(0, usage.totalCostUSD - 100),
        currency: 'USD',
        status: 'CURRENT_PERIOD_UNBILLED',
        generatedAt: new Date().toISOString()
    };

    return invoice;
}

function listTiers() {
    return TIERS;
}

module.exports = {
    recordUsage,
    getUsageSummary,
    generateInvoice,
    listTiers,
    TIERS
};
