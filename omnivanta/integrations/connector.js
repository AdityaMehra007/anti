/**
 * OMNIVANTA — Integration Connector Registry
 * 
 * Manages connectors for external system integrations.
 * Uses better-sqlite3 (synchronous API).
 * @module integrations/connector
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('connector-registry');

function createConnector({ orgId = 'org-default', name, type, config = {} }) {
    const db = getDb();
    const id = uuid();
    db.prepare('INSERT INTO connectors (id, org_id, name, type, config, status, health) VALUES (?, ?, ?, ?, ?, ?, ?)').run(id, orgId, name, type, JSON.stringify(config), 'inactive', 'unknown');
    recordAudit({ actor: 'system', action: 'connector.created', resourceType: 'connector', resourceId: id });
    log.info('Created connector: ' + name + ' (' + type + ')');
    return parseConnector(db.prepare('SELECT * FROM connectors WHERE id = ?').get(id));
}

function parseConnector(row) {
    if (!row) return null;
    return { ...row, config: JSON.parse(row.config || '{}') };
}

function getConnector(id) {
    return parseConnector(getDb().prepare('SELECT * FROM connectors WHERE id = ?').get(id));
}

function listConnectors({ orgId, type, status, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conds = []; const params = [];
    if (orgId) { conds.push('org_id = ?'); params.push(orgId); }
    if (type) { conds.push('type = ?'); params.push(type); }
    if (status) { conds.push('status = ?'); params.push(status); }
    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM connectors ' + where).get(...params).count;
    const connectors = db.prepare('SELECT * FROM connectors ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset).map(parseConnector);
    return { connectors, total };
}

function updateConnector(id, updates) {
    const db = getDb();
    const fields = { name: 'name', type: 'type', status: 'status', health: 'health' };
    const set = []; const params = [];
    for (const [js, col] of Object.entries(fields)) {
        if (updates[js] !== undefined) { set.push(col + ' = ?'); params.push(updates[js]); }
    }
    if (updates.config !== undefined) { set.push('config = ?'); params.push(JSON.stringify(updates.config)); }
    if (set.length === 0) return getConnector(id);
    params.push(id);
    db.prepare('UPDATE connectors SET ' + set.join(', ') + ' WHERE id = ?').run(...params);
    return getConnector(id);
}

function enableConnector(id) {
    const now = new Date().toISOString();
    getDb().prepare("UPDATE connectors SET status = 'active', last_check = ? WHERE id = ?").run(now, id);
    recordAudit({ actor: 'system', action: 'connector.enabled', resourceType: 'connector', resourceId: id });
    return getConnector(id);
}

function disableConnector(id) {
    getDb().prepare("UPDATE connectors SET status = 'inactive' WHERE id = ?").run(id);
    recordAudit({ actor: 'system', action: 'connector.disabled', resourceType: 'connector', resourceId: id });
    return getConnector(id);
}

function checkHealth(id) {
    const now = new Date().toISOString();
    // In production, this would actually ping the connector
    getDb().prepare("UPDATE connectors SET health = 'healthy', last_check = ? WHERE id = ?").run(now, id);
    return getConnector(id);
}

function getConnectorStats(orgId) {
    const db = getDb();
    const typeRows = db.prepare('SELECT type, COUNT(*) as count FROM connectors GROUP BY type').all();
    const statusRows = db.prepare('SELECT status, COUNT(*) as count FROM connectors GROUP BY status').all();
    const total = db.prepare('SELECT COUNT(*) as count FROM connectors').get().count;

    const byType = {}; typeRows.forEach(r => { byType[r.type] = r.count; });
    const byStatus = {}; statusRows.forEach(r => { byStatus[r.status] = r.count; });

    return { total, byType, byStatus };
}

module.exports = {
    createConnector, getConnector, listConnectors, updateConnector,
    enableConnector, disableConnector, checkHealth, getConnectorStats,
};
