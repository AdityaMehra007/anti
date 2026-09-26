/**
 * OMNIVANTA — App Builder & Automation Engine
 * 
 * Enables low-code / AI micro-app generation, custom data schemas,
 * dynamic forms, and trigger-action automation pipelines (Sections 33, 44 & 54).
 * 
 * @module applications/app-builder/service
 */

const { createLogger, recordAudit } = require('../../platform/core');
const { getDb } = require('../../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('app-builder');

function ensureAppsTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS custom_apps (
            id TEXT PRIMARY KEY,
            org_id TEXT DEFAULT 'org-default',
            name TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL, -- 'OPERATIONS', 'FINANCE', 'HR', 'SALES', 'ANALYTICS'
            schema_fields TEXT NOT NULL, -- JSON array of field definitions
            automation_trigger TEXT, -- JSON trigger definition
            status TEXT DEFAULT 'PUBLISHED',
            submissions_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS app_records (
            id TEXT PRIMARY KEY,
            app_id TEXT REFERENCES custom_apps(id),
            data TEXT NOT NULL, -- JSON payload
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_records_app ON app_records(app_id);
    `);
}

/**
 * Create or generate a custom micro-application
 */
function createApp({ name, description, category = 'OPERATIONS', fields = [], automationTrigger = null, orgId = 'org-default' }) {
    ensureAppsTable();
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();

    // Default sample fields if empty
    const schemaFields = fields.length ? fields : [
        { name: 'title', label: 'Title', type: 'text', required: true },
        { name: 'amount', label: 'Amount / Value', type: 'number', required: false },
        { name: 'status', label: 'Approval Status', type: 'select', options: ['Pending', 'Approved', 'Rejected'], required: true }
    ];

    db.prepare(`
        INSERT INTO custom_apps (id, org_id, name, description, category, schema_fields, automation_trigger, status, submissions_count, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'PUBLISHED', 0, ?, ?)
    `).run(id, orgId, name, description || '', category, JSON.stringify(schemaFields), JSON.stringify(automationTrigger), now, now);

    log.info(`Created Custom App [${id.substring(0,8)}] "${name}" (${category})`);
    recordAudit({ actor: 'user', action: 'app.created', resourceType: 'app', resourceId: id, details: { name, category } });

    return getApp(id);
}

function getApp(id) {
    ensureAppsTable();
    const db = getDb();
    const app = db.prepare('SELECT * FROM custom_apps WHERE id = ?').get(id);
    if (!app) return null;
    return {
        ...app,
        schema_fields: JSON.parse(app.schema_fields || '[]'),
        automation_trigger: JSON.parse(app.automation_trigger || 'null')
    };
}

function listApps({ category, orgId = 'org-default' } = {}) {
    ensureAppsTable();
    const db = getDb();
    const conds = ['org_id = ?'];
    const params = [orgId];
    if (category) { conds.push('category = ?'); params.push(category); }

    const apps = db.prepare(`SELECT * FROM custom_apps WHERE ${conds.join(' AND ')} ORDER BY created_at DESC`).all(...params);
    return apps.map(a => ({
        ...a,
        schema_fields: JSON.parse(a.schema_fields || '[]'),
        automation_trigger: JSON.parse(a.automation_trigger || 'null')
    }));
}

/**
 * Submit data record to custom micro-app
 */
function submitRecord(appId, data) {
    ensureAppsTable();
    const db = getDb();
    const recordId = uuid();
    const now = new Date().toISOString();

    db.prepare(`
        INSERT INTO app_records (id, app_id, data, created_at)
        VALUES (?, ?, ?, ?)
    `).run(recordId, appId, JSON.stringify(data), now);

    db.prepare(`UPDATE custom_apps SET submissions_count = submissions_count + 1, updated_at = ? WHERE id = ?`)
        .run(now, appId);

    recordAudit({ actor: 'user', action: 'app.record_submitted', resourceType: 'app', resourceId: appId });
    return { id: recordId, appId, data, created_at: now };
}

function getAppRecords(appId, { limit = 50 } = {}) {
    ensureAppsTable();
    const db = getDb();
    const rows = db.prepare('SELECT * FROM app_records WHERE app_id = ? ORDER BY created_at DESC LIMIT ?').all(appId, limit);
    return rows.map(r => ({
        ...r,
        data: JSON.parse(r.data || '{}')
    }));
}

module.exports = {
    createApp,
    getApp,
    listApps,
    submitRecord,
    getAppRecords,
    ensureAppsTable
};
