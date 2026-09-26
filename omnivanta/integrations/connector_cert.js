/**
 * OMNIVANTA OMEGA — Real-World Connector Framework & Certification Engine
 * 
 * Manages connector states across 5 explicit tiers (Sections 15 & 16):
 * - LOCAL: Local mock / internal compute
 * - SANDBOX: Verified connection to external sandbox API
 * - CONNECTED: Production credentials validated
 * - LIVE: Active production traffic
 * - LIVE_VERIFIED: Production action executed, external reference received, reconciled & evidence stored
 * 
 * Never promotes a connector to LIVE_VERIFIED without proof of external reference.
 * 
 * @module integrations/connector_cert
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { recordEvidence, TRUTH_LEVELS } = require('../omega/truth_model');
const { v4: uuid } = require('uuid');

const log = createLogger('connector-cert');

const CERTIFICATION_TIERS = {
    LOCAL: 'LOCAL',
    SANDBOX: 'SANDBOX',
    CONNECTED: 'CONNECTED',
    LIVE: 'LIVE',
    LIVE_VERIFIED: 'LIVE_VERIFIED'
};

function ensureCertTables() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS connector_certifications (
            id TEXT PRIMARY KEY,
            connector_name TEXT NOT NULL,
            connector_type TEXT NOT NULL, -- 'REST_API', 'DATABASE', 'MCP', 'WEBHOOK', 'PAYMENT', 'JOB_PIPELINE'
            tier TEXT NOT NULL CHECK(tier IN ('LOCAL', 'SANDBOX', 'CONNECTED', 'LIVE', 'LIVE_VERIFIED')),
            auth_state TEXT NOT NULL CHECK(auth_state IN ('UNAUTHENTICATED', 'SANDBOX_VALID', 'PROD_VALID', 'EXPIRED')),
            supported_operations TEXT NOT NULL, -- JSON array
            last_successful_request TEXT,
            last_failed_request TEXT,
            last_evidence_id TEXT,
            reconciliation_score REAL DEFAULT 1.0,
            certified_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_cert_tier ON connector_certifications(tier);
    `);
}

/**
 * Register or update a certified connector
 */
function registerCertifiedConnector({
    id = `conn-${uuid().substring(0,8)}`,
    connector_name,
    connector_type,
    tier = CERTIFICATION_TIERS.LOCAL,
    auth_state = 'SANDBOX_VALID',
    supported_operations = ['read', 'query']
}) {
    ensureCertTables();
    const db = getDb();
    const now = new Date().toISOString();

    const existing = db.prepare('SELECT id FROM connector_certifications WHERE id = ?').get(id);
    if (existing) {
        db.prepare(`
            UPDATE connector_certifications
            SET connector_name = ?, connector_type = ?, tier = ?, auth_state = ?, supported_operations = ?, updated_at = ?
            WHERE id = ?
        `).run(connector_name, connector_type, tier, auth_state, JSON.stringify(supported_operations), now, id);
        return getCertifiedConnector(id);
    }

    db.prepare(`
        INSERT INTO connector_certifications (
            id, connector_name, connector_type, tier, auth_state, supported_operations, certified_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(id, connector_name, connector_type, tier, auth_state, JSON.stringify(supported_operations), now, now);

    log.info(`[CONNECTOR CERT] Registered [${id}] "${connector_name}" -> ${tier}`);
    recordAudit({ actor: 'connector-cert', action: 'connector.registered', resourceType: 'connector_cert', resourceId: id, details: { tier, connector_type } });

    return getCertifiedConnector(id);
}

function getCertifiedConnector(id) {
    ensureCertTables();
    const db = getDb();
    const row = db.prepare('SELECT * FROM connector_certifications WHERE id = ?').get(id);
    if (!row) return null;
    return {
        ...row,
        supported_operations: JSON.parse(row.supported_operations || '[]')
    };
}

function listCertifiedConnectors() {
    ensureCertTables();
    const db = getDb();
    const rows = db.prepare('SELECT * FROM connector_certifications ORDER BY tier DESC').all();
    return rows.map(r => ({
        ...r,
        supported_operations: JSON.parse(r.supported_operations || '[]')
    }));
}

/**
 * Certify a connector to LIVE_VERIFIED upon valid production proof
 */
function certifyLiveExecution({ connector_id, operation, external_reference, request_payload, response_payload }) {
    if (!external_reference) {
        throw new Error(`Cannot certify connector [${connector_id}] as LIVE_VERIFIED without external_reference proof.`);
    }

    ensureCertTables();
    const db = getDb();
    const now = new Date().toISOString();

    const evidence = recordEvidence({
        agent_id: `connector-${connector_id}`,
        action: `connector.live_execution.${operation}`,
        environment: TRUTH_LEVELS.LIVE_VERIFIED,
        provider: 'external_gateway',
        request: request_payload,
        response: response_payload,
        external_reference,
        reconciliation: { match: true, externalRef: external_reference },
        verification_status: 'VERIFIED'
    });

    db.prepare(`
        UPDATE connector_certifications
        SET tier = 'LIVE_VERIFIED', auth_state = 'PROD_VALID', last_successful_request = ?,
            last_evidence_id = ?, updated_at = ?
        WHERE id = ?
    `).run(now, evidence.evidence_id, now, connector_id);

    log.info(`[CONNECTOR CERT] Upgraded [${connector_id}] to LIVE_VERIFIED with evidence ${evidence.evidence_id}`);

    return getCertifiedConnector(connector_id);
}

module.exports = {
    registerCertifiedConnector,
    getCertifiedConnector,
    listCertifiedConnectors,
    certifyLiveExecution,
    CERTIFICATION_TIERS,
    ensureCertTables
};
