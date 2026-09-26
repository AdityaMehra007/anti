/**
 * OMNIVANTA — Agent Registry
 * 
 * CRUD operations for AI agents, backed by better-sqlite3 (synchronous).
 * @module agents/registry
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('agent-registry');

/** Helper: parse JSON fields from a DB row */
function parseAgent(row) {
    if (!row) return null;
    return {
        ...row,
        tools: JSON.parse(row.tools || '[]'),
        knowledge: JSON.parse(row.knowledge || '{}'),
        permissions: JSON.parse(row.permissions || '[]'),
    };
}

/**
 * Create a new agent.
 * @param {Object} params
 * @returns {Object} The created agent
 */
function createAgent({ orgId = 'org-default', name, description, model, autonomyLevel = 0, tools = [], knowledge = {}, permissions = [], owner, riskClass = 'low' }) {
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();

    db.prepare(`
        INSERT INTO agents (id, org_id, name, description, model, autonomy_level, tools, knowledge, permissions, owner, risk_class, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'inactive', ?, ?)
    `).run(id, orgId, name, description || '', model || '', autonomyLevel, JSON.stringify(tools), JSON.stringify(knowledge), JSON.stringify(permissions), owner || 'system', riskClass, now, now);

    recordAudit({ actor: owner || 'system', action: 'agent.created', resourceType: 'agent', resourceId: id });
    log.info('Created agent: ' + name + ' (' + id.substring(0, 8) + ')');

    return parseAgent(db.prepare('SELECT * FROM agents WHERE id = ?').get(id));
}

/**
 * Get agent by ID.
 * @param {string} id
 * @returns {Object|null}
 */
function getAgent(id) {
    return parseAgent(getDb().prepare('SELECT * FROM agents WHERE id = ?').get(id));
}

/**
 * List agents with optional filters and pagination.
 * @param {Object} options
 * @returns {{ agents: Object[], total: number }}
 */
function listAgents({ orgId, status, autonomyLevel, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conditions = ["status != 'deleted'"];
    const params = [];

    if (orgId) { conditions.push('org_id = ?'); params.push(orgId); }
    if (status) { conditions.push('status = ?'); params.push(status); }
    if (autonomyLevel != null) { conditions.push('autonomy_level = ?'); params.push(autonomyLevel); }

    const where = 'WHERE ' + conditions.join(' AND ');
    const total = db.prepare('SELECT COUNT(*) as count FROM agents ' + where).get(...params).count;
    const rows = db.prepare('SELECT * FROM agents ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);

    return { agents: rows.map(parseAgent), total };
}

/**
 * Update agent fields.
 * @param {string} id
 * @param {Object} updates
 * @returns {Object} Updated agent
 */
function updateAgent(id, updates) {
    const db = getDb();
    const existing = db.prepare('SELECT id FROM agents WHERE id = ?').get(id);
    if (!existing) throw new Error('Agent not found: ' + id);

    const fieldMap = {
        name: 'name', description: 'description', model: 'model',
        autonomyLevel: 'autonomy_level', status: 'status',
        owner: 'owner', riskClass: 'risk_class',
    };
    const jsonFields = { tools: 'tools', knowledge: 'knowledge', permissions: 'permissions' };

    const setClauses = [];
    const params = [];

    for (const [jsKey, dbCol] of Object.entries(fieldMap)) {
        if (updates[jsKey] !== undefined) {
            setClauses.push(dbCol + ' = ?');
            params.push(updates[jsKey]);
        }
    }
    for (const [jsKey, dbCol] of Object.entries(jsonFields)) {
        if (updates[jsKey] !== undefined) {
            setClauses.push(dbCol + ' = ?');
            params.push(JSON.stringify(updates[jsKey]));
        }
    }

    if (setClauses.length === 0) return getAgent(id);

    setClauses.push("updated_at = ?");
    params.push(new Date().toISOString());
    params.push(id);

    db.prepare('UPDATE agents SET ' + setClauses.join(', ') + ' WHERE id = ?').run(...params);
    recordAudit({ actor: 'system', action: 'agent.updated', resourceType: 'agent', resourceId: id, details: updates });
    return getAgent(id);
}

/**
 * Soft-delete an agent.
 * @param {string} id
 * @returns {boolean}
 */
function deleteAgent(id) {
    const result = getDb().prepare("UPDATE agents SET status = 'deleted', updated_at = ? WHERE id = ?").run(new Date().toISOString(), id);
    if (result.changes > 0) {
        recordAudit({ actor: 'system', action: 'agent.deleted', resourceType: 'agent', resourceId: id });
        return true;
    }
    return false;
}

/**
 * Get agent statistics.
 * @param {string} [orgId]
 * @returns {Object}
 */
function getAgentStats(orgId) {
    const db = getDb();
    const base = orgId ? " WHERE org_id = ? AND status != 'deleted'" : " WHERE status != 'deleted'";
    const p = orgId ? [orgId] : [];

    const total = db.prepare("SELECT COUNT(*) as count FROM agents" + base).get(...p).count;
    const active = db.prepare("SELECT COUNT(*) as count FROM agents" + (orgId ? " WHERE org_id = ? AND status = 'active'" : " WHERE status = 'active'")).get(...p).count;
    const inactive = db.prepare("SELECT COUNT(*) as count FROM agents" + (orgId ? " WHERE org_id = ? AND status = 'inactive'" : " WHERE status = 'inactive'")).get(...p).count;
    const autonomyRows = db.prepare("SELECT autonomy_level, COUNT(*) as count FROM agents" + base + " GROUP BY autonomy_level").all(...p);

    const byAutonomy = {};
    autonomyRows.forEach(r => { byAutonomy[r.autonomy_level] = r.count; });

    return { total, active, inactive, byAutonomy };
}

module.exports = { createAgent, getAgent, listAgents, updateAgent, deleteAgent, getAgentStats };
