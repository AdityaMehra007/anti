/**
 * OMNIVANTA OMEGA — Unified Memory 2.0 & Knowledge Trust Engine
 * 
 * Provides verifiable epistemic tagging (Sections 13 & 14):
 * - FACT: Empirical, independently verified data point
 * - INFERENCE: Logically derived conclusion from verified facts
 * - ASSUMPTION: Unverified hypothesis or default expectation
 * - UNKNOWN: Acknowledged absence of verifiable data
 * 
 * Tracks 8 unified memory domains with confidence scoring and provenance citations.
 * 
 * @module knowledge/memory2
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('memory2');

const EPISTEMIC_TYPES = {
    FACT: 'FACT',
    INFERENCE: 'INFERENCE',
    ASSUMPTION: 'ASSUMPTION',
    UNKNOWN: 'UNKNOWN'
};

const MEMORY_DOMAINS = [
    'global_knowledge',
    'project_knowledge',
    'agent_memory',
    'decision_memory',
    'failure_memory',
    'workflow_memory',
    'user_approved_preferences',
    'experiment_memory'
];

function ensureMemory2Table() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS unified_memory (
            id TEXT PRIMARY KEY,
            domain TEXT NOT NULL CHECK(domain IN ('global_knowledge', 'project_knowledge', 'agent_memory', 'decision_memory', 'failure_memory', 'workflow_memory', 'user_approved_preferences', 'experiment_memory')),
            epistemic_type TEXT NOT NULL CHECK(epistemic_type IN ('FACT', 'INFERENCE', 'ASSUMPTION', 'UNKNOWN')),
            subject TEXT NOT NULL,
            claim TEXT NOT NULL,
            confidence REAL NOT NULL CHECK(confidence BETWEEN 0.0 AND 1.0),
            provenance_source TEXT NOT NULL,
            citation TEXT,
            version INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_unified_mem_domain ON unified_memory(domain);
        CREATE INDEX IF NOT EXISTS idx_unified_mem_type ON unified_memory(epistemic_type);
        CREATE INDEX IF NOT EXISTS idx_unified_mem_subject ON unified_memory(subject);
    `);
}

/**
 * Store a verified statement in Unified Memory 2.0
 */
function recordMemoryItem({
    domain = 'global_knowledge',
    epistemic_type = EPISTEMIC_TYPES.FACT,
    subject,
    claim,
    confidence = 1.0,
    provenance_source,
    citation = null
}) {
    ensureMemory2Table();
    const db = getDb();
    const id = `mem-${uuid()}`;
    const now = new Date().toISOString();

    const verifiedCitation = citation || `Provenance: ${provenance_source} (Recorded: ${now})`;

    db.prepare(`
        INSERT INTO unified_memory (
            id, domain, epistemic_type, subject, claim, confidence, provenance_source, citation, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(id, domain, epistemic_type, subject, claim, confidence, provenance_source, verifiedCitation, now, now);

    log.info(`[MEMORY 2.0] Stored [${epistemic_type}] in ${domain}: "${subject}" (Conf: ${confidence})`);
    recordAudit({ actor: 'memory2', action: 'memory.item_stored', resourceType: 'unified_memory', resourceId: id, details: { epistemic_type, domain, subject } });

    return getMemoryItem(id);
}

function getMemoryItem(id) {
    ensureMemory2Table();
    return getDb().prepare('SELECT * FROM unified_memory WHERE id = ?').get(id) || null;
}

/**
 * Query unified memory with epistemic transparency
 */
function queryTrustedMemory(query, { domain = null, epistemic_type = null, minConfidence = 0.5, limit = 10 } = {}) {
    ensureMemory2Table();
    const db = getDb();
    const conds = ['confidence >= ?'];
    const params = [minConfidence];

    if (query) {
        conds.push('(LOWER(subject) LIKE ? OR LOWER(claim) LIKE ?)');
        params.push(`%${query.toLowerCase()}%`, `%${query.toLowerCase()}%`);
    }
    if (domain) {
        conds.push('domain = ?');
        params.push(domain);
    }
    if (epistemic_type) {
        conds.push('epistemic_type = ?');
        params.push(epistemic_type);
    }

    const where = 'WHERE ' + conds.join(' AND ');
    const items = db.prepare(`SELECT * FROM unified_memory ${where} ORDER BY confidence DESC, updated_at DESC LIMIT ?`).all(...params, limit);

    return {
        query,
        total: items.length,
        items
    };
}

function getMemory2Stats() {
    ensureMemory2Table();
    const db = getDb();
    const total = db.prepare('SELECT COUNT(*) as count FROM unified_memory').get().count;
    const byEpistemic = db.prepare('SELECT epistemic_type, COUNT(*) as count FROM unified_memory GROUP BY epistemic_type').all();
    const byDomain = db.prepare('SELECT domain, COUNT(*) as count FROM unified_memory GROUP BY domain').all();

    const epistemicMap = { FACT: 0, INFERENCE: 0, ASSUMPTION: 0, UNKNOWN: 0 };
    byEpistemic.forEach(r => { epistemicMap[r.epistemic_type] = r.count; });

    const domainMap = {};
    byDomain.forEach(r => { domainMap[r.domain] = r.count; });

    return {
        totalRecords: total,
        byEpistemicType: epistemicMap,
        byDomain: domainMap
    };
}

module.exports = {
    recordMemoryItem,
    getMemoryItem,
    queryTrustedMemory,
    getMemory2Stats,
    EPISTEMIC_TYPES,
    MEMORY_DOMAINS,
    ensureMemory2Table
};
