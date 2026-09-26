/**
 * OMNIVANTA — AI Service Desk & Incident Automation Engine
 * 
 * Provides automated ticket triage, AI categorization, priority assignment,
 * and autonomous workflow resolution for IT and Enterprise Operations.
 * 
 * @module applications/service-desk/service
 */

const { createLogger, recordAudit } = require('../../platform/core');
const { getDb } = require('../../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('service-desk');

function ensureTicketsTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS service_tickets (
            id TEXT PRIMARY KEY,
            org_id TEXT DEFAULT 'org-default',
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL, -- 'IT_INCIDENT', 'ACCESS_REQUEST', 'BILLING', 'SECURITY', 'INFRASTRUCTURE'
            priority TEXT NOT NULL CHECK(priority IN ('P1_CRITICAL', 'P2_HIGH', 'P3_MEDIUM', 'P4_LOW')),
            status TEXT NOT NULL CHECK(status IN ('OPEN', 'TRIAGED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')),
            assigned_agent_id TEXT,
            resolution TEXT,
            sla_deadline TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_tickets_status ON service_tickets(status);
        CREATE INDEX IF NOT EXISTS idx_tickets_priority ON service_tickets(priority);
    `);
}

/**
 * Automatically categorize and assign priority based on keywords & severity
 */
function triageIncident(title, description) {
    const fullText = `${title} ${description}`.toLowerCase();
    
    let category = 'IT_INCIDENT';
    let priority = 'P3_MEDIUM';

    if (fullText.includes('security') || fullText.includes('breach') || fullText.includes('unauthorized')) {
        category = 'SECURITY';
        priority = 'P1_CRITICAL';
    } else if (fullText.includes('down') || fullText.includes('outage') || fullText.includes('crash') || fullText.includes('500 error')) {
        category = 'INFRASTRUCTURE';
        priority = 'P1_CRITICAL';
    } else if (fullText.includes('access') || fullText.includes('permission') || fullText.includes('login') || fullText.includes('password')) {
        category = 'ACCESS_REQUEST';
        priority = 'P3_MEDIUM';
    } else if (fullText.includes('billing') || fullText.includes('invoice') || fullText.includes('subscription')) {
        category = 'BILLING';
        priority = 'P2_HIGH';
    }

    return { category, priority };
}

/**
 * Create a new service ticket with automated AI triage
 */
function createTicket({ title, description, orgId = 'org-default', manualCategory, manualPriority }) {
    ensureTicketsTable();
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();

    const triaged = triageIncident(title, description);
    const category = manualCategory || triaged.category;
    const priority = manualPriority || triaged.priority;

    // SLA: P1 = 2h, P2 = 8h, P3 = 24h, P4 = 72h
    const slaHours = { 'P1_CRITICAL': 2, 'P2_HIGH': 8, 'P3_MEDIUM': 24, 'P4_LOW': 72 }[priority] || 24;
    const slaDeadline = new Date(Date.now() + slaHours * 3600 * 1000).toISOString();

    db.prepare(`
        INSERT INTO service_tickets (id, org_id, title, description, category, priority, status, sla_deadline, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 'OPEN', ?, ?, ?)
    `).run(id, orgId, title, description, category, priority, slaDeadline, now, now);

    log.info(`Created Service Ticket [${id.substring(0,8)}] "${title}" -> ${priority} (${category})`);
    recordAudit({ actor: 'user', action: 'ticket.created', resourceType: 'ticket', resourceId: id, details: { priority, category } });

    return getTicket(id);
}

function getTicket(id) {
    ensureTicketsTable();
    return getDb().prepare('SELECT * FROM service_tickets WHERE id = ?').get(id) || null;
}

function listTickets({ status, priority, category, limit = 50 } = {}) {
    ensureTicketsTable();
    const db = getDb();
    const conds = [];
    const params = [];

    if (status) { conds.push('status = ?'); params.push(status); }
    if (priority) { conds.push('priority = ?'); params.push(priority); }
    if (category) { conds.push('category = ?'); params.push(category); }

    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const tickets = db.prepare(`SELECT * FROM service_tickets ${where} ORDER BY created_at DESC LIMIT ?`).all(...params, limit);
    const total = db.prepare(`SELECT COUNT(*) as count FROM service_tickets ${where}`).get(...params).count;

    return { tickets, total };
}

/**
 * Resolve ticket with resolution summary
 */
function resolveTicket(id, resolutionText, agentId = 'autonomous-service-agent') {
    ensureTicketsTable();
    const db = getDb();
    const now = new Date().toISOString();

    db.prepare(`
        UPDATE service_tickets 
        SET status = 'RESOLVED', resolution = ?, assigned_agent_id = ?, updated_at = ?
        WHERE id = ?
    `).run(resolutionText, agentId, now, id);

    log.info(`Resolved ticket ${id.substring(0,8)} by ${agentId}`);
    recordAudit({ actor: agentId, action: 'ticket.resolved', resourceType: 'ticket', resourceId: id, details: { resolution: resolutionText } });

    return getTicket(id);
}

function getServiceDeskStats() {
    ensureTicketsTable();
    const db = getDb();
    const total = db.prepare('SELECT COUNT(*) as count FROM service_tickets').get().count;
    const open = db.prepare("SELECT COUNT(*) as count FROM service_tickets WHERE status = 'OPEN'").get().count;
    const resolved = db.prepare("SELECT COUNT(*) as count FROM service_tickets WHERE status = 'RESOLVED'").get().count;
    const critical = db.prepare("SELECT COUNT(*) as count FROM service_tickets WHERE priority = 'P1_CRITICAL'").get().count;

    return { total, open, resolved, critical };
}

module.exports = {
    createTicket,
    getTicket,
    listTickets,
    resolveTicket,
    getServiceDeskStats,
    triageIncident,
    ensureTicketsTable
};
