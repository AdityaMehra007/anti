/**
 * OMNIVANTA OMEGA — Four-Layer Truth Model & Universal Evidence Engine
 * 
 * Classifies all platform actions into 5 empirical states:
 * - LOCAL: Internal computation only
 * - SIMULATED: External operation represented/mocked
 * - SANDBOX: Legitimate external test environment
 * - LIVE: Production external connection exists
 * - LIVE_VERIFIED: Production operation occurred with independently verifiable proof
 * 
 * Every action produces a cryptographically hashed Universal Evidence Record.
 * No evidence = UNVERIFIED.
 * 
 * @module omega/truth_model
 */

const crypto = require('crypto');
const { getDb } = require('../platform/db');
const { createLogger, recordAudit } = require('../platform/core');
const { v4: uuid } = require('uuid');

const log = createLogger('truth-model');

const TRUTH_LEVELS = {
    LOCAL: 'LOCAL',
    SIMULATED: 'SIMULATED',
    SANDBOX: 'SANDBOX',
    LIVE: 'LIVE',
    LIVE_VERIFIED: 'LIVE_VERIFIED'
};

function ensureEvidenceTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS universal_evidence (
            evidence_id TEXT PRIMARY KEY,
            trace_id TEXT NOT NULL,
            mission_id TEXT,
            task_id TEXT,
            agent_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            environment TEXT NOT NULL CHECK(environment IN ('LOCAL', 'SIMULATED', 'SANDBOX', 'LIVE', 'LIVE_VERIFIED')),
            provider TEXT,
            request TEXT,
            response TEXT,
            external_reference TEXT,
            evidence_hash TEXT NOT NULL,
            reconciliation TEXT,
            verification_status TEXT NOT NULL CHECK(verification_status IN ('VERIFIED', 'UNVERIFIED', 'FAILED_RECONCILIATION', 'PENDING_AUDIT'))
        );
        CREATE INDEX IF NOT EXISTS idx_evidence_trace ON universal_evidence(trace_id);
        CREATE INDEX IF NOT EXISTS idx_evidence_status ON universal_evidence(verification_status);
        CREATE INDEX IF NOT EXISTS idx_evidence_env ON universal_evidence(environment);
    `);
}

/**
 * Generate SHA-256 hash of evidence payload
 */
function computeEvidenceHash(payload) {
    const raw = JSON.stringify({
        agent_id: payload.agent_id,
        action: payload.action,
        timestamp: payload.timestamp,
        request: payload.request,
        response: payload.response,
        external_reference: payload.external_reference
    });
    return crypto.createHash('sha256').update(raw).digest('hex');
}

/**
 * Record a Universal Evidence Record for an action
 */
function recordEvidence({
    trace_id = uuid(),
    mission_id = null,
    task_id = null,
    agent_id = 'system',
    action,
    environment = TRUTH_LEVELS.LOCAL,
    provider = 'internal',
    request = {},
    response = {},
    external_reference = null,
    reconciliation = null,
    verification_status = null
}) {
    ensureEvidenceTable();
    const db = getDb();
    const evidence_id = `ev-${uuid()}`;
    const timestamp = new Date().toISOString();

    const reqStr = typeof request === 'object' ? JSON.stringify(request) : String(request);
    const resStr = typeof response === 'object' ? JSON.stringify(response) : String(response);
    const recStr = reconciliation ? (typeof reconciliation === 'object' ? JSON.stringify(reconciliation) : String(reconciliation)) : null;

    // Automatic truth status determination
    let status = verification_status;
    if (!status) {
        if (environment === TRUTH_LEVELS.LIVE_VERIFIED && external_reference) {
            status = 'VERIFIED';
        } else if (environment === TRUTH_LEVELS.LOCAL || environment === TRUTH_LEVELS.SANDBOX) {
            status = 'VERIFIED';
        } else {
            status = 'UNVERIFIED';
        }
    }

    const payload = {
        agent_id,
        action,
        timestamp,
        request: reqStr,
        response: resStr,
        external_reference
    };
    const evidence_hash = computeEvidenceHash(payload);

    db.prepare(`
        INSERT INTO universal_evidence (
            evidence_id, trace_id, mission_id, task_id, agent_id, timestamp, action,
            environment, provider, request, response, external_reference, evidence_hash,
            reconciliation, verification_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
        evidence_id, trace_id, mission_id, task_id, agent_id, timestamp, action,
        environment, provider, reqStr, resStr, external_reference, evidence_hash,
        recStr, status
    );

    log.info(`Recorded evidence [${evidence_id.substring(0,10)}] (${environment}) -> ${status}`);
    recordAudit({
        actor: agent_id,
        action: 'evidence.recorded',
        resourceType: 'evidence',
        resourceId: evidence_id,
        details: { action, environment, status, evidence_hash }
    });

    return getEvidenceById(evidence_id);
}

function getEvidenceById(evidence_id) {
    ensureEvidenceTable();
    const db = getDb();
    const row = db.prepare('SELECT * FROM universal_evidence WHERE evidence_id = ?').get(evidence_id);
    if (!row) return null;
    return {
        ...row,
        request: JSON.parse(row.request || '{}'),
        response: JSON.parse(row.response || '{}'),
        reconciliation: JSON.parse(row.reconciliation || 'null')
    };
}

function listEvidence({ limit = 50, environment, verification_status, trace_id } = {}) {
    ensureEvidenceTable();
    const db = getDb();
    const conds = [];
    const params = [];

    if (environment) { conds.push('environment = ?'); params.push(environment); }
    if (verification_status) { conds.push('verification_status = ?'); params.push(verification_status); }
    if (trace_id) { conds.push('trace_id = ?'); params.push(trace_id); }

    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const rows = db.prepare(`SELECT * FROM universal_evidence ${where} ORDER BY timestamp DESC LIMIT ?`).all(...params, limit);
    return rows.map(r => ({
        ...r,
        request: JSON.parse(r.request || '{}'),
        response: JSON.parse(r.response || '{}'),
        reconciliation: JSON.parse(r.reconciliation || 'null')
    }));
}

function getTruthSummary() {
    ensureEvidenceTable();
    const db = getDb();
    const total = db.prepare('SELECT COUNT(*) as count FROM universal_evidence').get().count;
    const byEnv = db.prepare('SELECT environment, COUNT(*) as count FROM universal_evidence GROUP BY environment').all();
    const byStatus = db.prepare('SELECT verification_status, COUNT(*) as count FROM universal_evidence GROUP BY verification_status').all();

    const envMap = { LOCAL: 0, SIMULATED: 0, SANDBOX: 0, LIVE: 0, LIVE_VERIFIED: 0 };
    byEnv.forEach(r => { envMap[r.environment] = r.count; });

    const statusMap = { VERIFIED: 0, UNVERIFIED: 0, FAILED_RECONCILIATION: 0, PENDING_AUDIT: 0 };
    byStatus.forEach(r => { statusMap[r.verification_status] = r.count; });

    return {
        totalEvidenceRecords: total,
        environments: envMap,
        verificationStatuses: statusMap
    };
}

module.exports = {
    recordEvidence,
    getEvidenceById,
    listEvidence,
    getTruthSummary,
    computeEvidenceHash,
    TRUTH_LEVELS,
    ensureEvidenceTable
};
