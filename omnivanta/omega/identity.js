/**
 * OMNIVANTA OMEGA — Identity & Digital Agent Identity Engine
 * 
 * Enforces least-privilege RBAC for users, services, and digital agents (Sections 6, 7 & 8).
 * Ensures agents never inherit unrestricted permissions.
 * 
 * Autonomy Levels:
 * - LEVEL 0: Read-only observation
 * - LEVEL 1: Analysis & recommendation
 * - LEVEL 2: Create local artifacts & drafts
 * - LEVEL 3: Modify internal staging systems
 * - LEVEL 4: Staging / external preparation (requires approval)
 * - LEVEL 5: Production external action (requires multi-party authorization)
 * 
 * @module omega/identity
 */

const { getDb } = require('../platform/db');
const { createLogger, recordAudit } = require('../platform/core');
const { v4: uuid } = require('uuid');

const log = createLogger('identity');

const AUTONOMY_LEVELS = {
    0: { level: 0, name: 'READ_ONLY', maxRisk: 'NONE', requiresApproval: false },
    1: { level: 1, name: 'ANALYZE', maxRisk: 'LOW', requiresApproval: false },
    2: { level: 2, name: 'CREATE_ARTIFACTS', maxRisk: 'LOW', requiresApproval: false },
    3: { level: 3, name: 'MODIFY_INTERNAL', maxRisk: 'MEDIUM', requiresApproval: false },
    4: { level: 4, name: 'EXTERNAL_PREPARATION', maxRisk: 'HIGH', requiresApproval: true },
    5: { level: 5, name: 'PRODUCTION_EXTERNAL', maxRisk: 'CRITICAL', requiresApproval: true }
};

function ensureIdentityTables() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS agent_identities (
            id TEXT PRIMARY KEY,
            agent_name TEXT NOT NULL,
            role TEXT NOT NULL,
            autonomy_level INTEGER DEFAULT 0 CHECK(autonomy_level BETWEEN 0 AND 5),
            data_scope TEXT NOT NULL, -- JSON array of allowed domains (e.g. ['finance', 'crm'])
            tool_scope TEXT NOT NULL, -- JSON array of allowed tool names
            max_cost_per_mission REAL DEFAULT 10.0,
            max_daily_executions INTEGER DEFAULT 500,
            executions_today INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ACTIVE',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS authorizations (
            id TEXT PRIMARY KEY,
            action_type TEXT NOT NULL,
            requested_by_agent_id TEXT NOT NULL,
            target_resource TEXT NOT NULL,
            payload TEXT,
            risk_level TEXT NOT NULL CHECK(risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
            status TEXT NOT NULL CHECK(status IN ('PENDING', 'APPROVED', 'REJECTED', 'EXECUTED')),
            approved_by_user TEXT,
            rejection_reason TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            resolved_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_auth_status ON authorizations(status);
    `);
}

/**
 * Register or update an Agent Digital Identity
 */
function registerAgentIdentity({
    id = uuid(),
    agent_name,
    role,
    autonomy_level = 0,
    data_scope = ['general'],
    tool_scope = ['system_time'],
    max_cost_per_mission = 10.0,
    max_daily_executions = 500
}) {
    ensureIdentityTables();
    const db = getDb();
    const now = new Date().toISOString();

    const existing = db.prepare('SELECT id FROM agent_identities WHERE id = ?').get(id);
    if (existing) {
        db.prepare(`
            UPDATE agent_identities 
            SET agent_name = ?, role = ?, autonomy_level = ?, data_scope = ?, tool_scope = ?,
                max_cost_per_mission = ?, max_daily_executions = ?, updated_at = ?
            WHERE id = ?
        `).run(
            agent_name, role, autonomy_level, JSON.stringify(data_scope), JSON.stringify(tool_scope),
            max_cost_per_mission, max_daily_executions, now, id
        );
        return getAgentIdentity(id);
    }

    db.prepare(`
        INSERT INTO agent_identities (
            id, agent_name, role, autonomy_level, data_scope, tool_scope,
            max_cost_per_mission, max_daily_executions, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)
    `).run(
        id, agent_name, role, autonomy_level, JSON.stringify(data_scope), JSON.stringify(tool_scope),
        max_cost_per_mission, max_daily_executions, now, now
    );

    log.info(`Registered Agent Digital Identity [${id.substring(0,8)}] "${agent_name}" (Autonomy L${autonomy_level})`);
    recordAudit({ actor: 'identity', action: 'agent.identity_registered', resourceType: 'agent_identity', resourceId: id });

    return getAgentIdentity(id);
}

function getAgentIdentity(id) {
    ensureIdentityTables();
    const db = getDb();
    const row = db.prepare('SELECT * FROM agent_identities WHERE id = ?').get(id);
    if (!row) return null;
    return {
        ...row,
        data_scope: JSON.parse(row.data_scope || '[]'),
        tool_scope: JSON.parse(row.tool_scope || '[]')
    };
}

function listAgentIdentities() {
    ensureIdentityTables();
    const db = getDb();
    const rows = db.prepare('SELECT * FROM agent_identities ORDER BY autonomy_level DESC').all();
    return rows.map(r => ({
        ...r,
        data_scope: JSON.parse(r.data_scope || '[]'),
        tool_scope: JSON.parse(r.tool_scope || '[]')
    }));
}

/**
 * Request authorization for an action requiring Level 4 or Level 5 approval
 */
function requestAuthorization({ action_type, agent_id, target_resource, payload = {}, risk_level = 'HIGH' }) {
    ensureIdentityTables();
    const db = getDb();
    const id = `auth-${uuid()}`;
    const now = new Date().toISOString();

    db.prepare(`
        INSERT INTO authorizations (id, action_type, requested_by_agent_id, target_resource, payload, risk_level, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?)
    `).run(id, action_type, agent_id, target_resource, JSON.stringify(payload), risk_level, now);

    log.warn(`Authorization request [${id}] created for agent [${agent_id}] -> ${action_type} on ${target_resource}`);
    recordAudit({ actor: agent_id, action: 'authorization.requested', resourceType: 'authorization', resourceId: id, details: { risk_level, action_type } });

    return getAuthorization(id);
}

function getAuthorization(id) {
    ensureIdentityTables();
    const db = getDb();
    const row = db.prepare('SELECT * FROM authorizations WHERE id = ?').get(id);
    if (!row) return null;
    return {
        ...row,
        payload: JSON.parse(row.payload || '{}')
    };
}

function listPendingAuthorizations() {
    ensureIdentityTables();
    const db = getDb();
    const rows = db.prepare("SELECT * FROM authorizations WHERE status = 'PENDING' ORDER BY created_at ASC").all();
    return rows.map(r => ({
        ...r,
        payload: JSON.parse(r.payload || '{}')
    }));
}

function resolveAuthorization(id, decision, { approved_by = 'admin', reason = null } = {}) {
    ensureIdentityTables();
    const db = getDb();
    const now = new Date().toISOString();
    const status = decision.toUpperCase() === 'APPROVE' ? 'APPROVED' : 'REJECTED';

    db.prepare(`
        UPDATE authorizations 
        SET status = ?, approved_by_user = ?, rejection_reason = ?, resolved_at = ?
        WHERE id = ?
    `).run(status, approved_by, reason, now, id);

    log.info(`Resolved authorization [${id}] -> ${status} by ${approved_by}`);
    recordAudit({ actor: approved_by, action: `authorization.${status.toLowerCase()}`, resourceType: 'authorization', resourceId: id });

    return getAuthorization(id);
}

module.exports = {
    registerAgentIdentity,
    getAgentIdentity,
    listAgentIdentities,
    requestAuthorization,
    getAuthorization,
    listPendingAuthorizations,
    resolveAuthorization,
    AUTONOMY_LEVELS,
    ensureIdentityTables
};
