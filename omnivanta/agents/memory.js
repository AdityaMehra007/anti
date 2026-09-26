/**
 * OMNIVANTA — Multi-Tier Agent Memory Engine
 * 
 * Implements 7-tier memory architecture (Section 15):
 * - Session: ephemeral current conversation
 * - Task: active objective context
 * - Project: ongoing project artifacts & state
 * - Org: enterprise knowledge & facts
 * - Agent: specialized procedural knowledge
 * - Decision: recorded decisions & rationales
 * - Failure: past failures, exceptions, and fixes
 * 
 * @module agents/memory
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('agent-memory');

/**
 * Ensure memory table exists in SQLite database
 */
function ensureMemoryTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS agent_memory (
            id TEXT PRIMARY KEY,
            agent_id TEXT,
            tier TEXT NOT NULL CHECK(tier IN ('session', 'task', 'project', 'org', 'agent', 'decision', 'failure')),
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            tags TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_memory_agent_tier ON agent_memory(agent_id, tier);
        CREATE INDEX IF NOT EXISTS idx_memory_key ON agent_memory(key);
    `);
}

/**
 * Store or update a memory item.
 */
function storeMemory({ agentId = null, tier = 'agent', key, value, tags = [] }) {
    ensureMemoryTable();
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();
    const valString = typeof value === 'object' ? JSON.stringify(value) : String(value);
    const tagsString = JSON.stringify(tags);

    // Check existing
    const existing = db.prepare('SELECT id FROM agent_memory WHERE (agent_id = ? OR (agent_id IS NULL AND ? IS NULL)) AND tier = ? AND key = ?')
        .get(agentId, agentId, tier, key);

    if (existing) {
        db.prepare('UPDATE agent_memory SET value = ?, tags = ?, updated_at = ? WHERE id = ?')
            .run(valString, tagsString, now, existing.id);
        recordAudit({ actor: 'system', action: 'memory.updated', resourceType: 'memory', resourceId: existing.id, details: { tier, key } });
        return getMemoryById(existing.id);
    }

    db.prepare(`
        INSERT INTO agent_memory (id, agent_id, tier, key, value, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(id, agentId, tier, key, valString, tagsString, now, now);

    recordAudit({ actor: 'system', action: 'memory.created', resourceType: 'memory', resourceId: id, details: { tier, key } });
    log.info(`Stored [${tier}] memory: "${key}" for agent ${agentId || 'global'}`);

    return getMemoryById(id);
}

function parseMemory(row) {
    if (!row) return null;
    let parsedValue = row.value;
    try { parsedValue = JSON.parse(row.value); } catch (e) {}
    let parsedTags = [];
    try { parsedTags = JSON.parse(row.tags || '[]'); } catch (e) {}
    return {
        ...row,
        value: parsedValue,
        tags: parsedTags
    };
}

function getMemoryById(id) {
    ensureMemoryTable();
    return parseMemory(getDb().prepare('SELECT * FROM agent_memory WHERE id = ?').get(id));
}

/**
 * Retrieve memory items for an agent or globally across a tier.
 */
function retrieveMemory({ agentId = null, tier, key, tag, limit = 50 }) {
    ensureMemoryTable();
    const db = getDb();
    const conds = [];
    const params = [];

    if (agentId) {
        conds.push('(agent_id = ? OR agent_id IS NULL)');
        params.push(agentId);
    }
    if (tier) {
        conds.push('tier = ?');
        params.push(tier);
    }
    if (key) {
        conds.push('key LIKE ?');
        params.push(`%${key}%`);
    }
    if (tag) {
        conds.push('tags LIKE ?');
        params.push(`%${tag}%`);
    }

    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const rows = db.prepare(`SELECT * FROM agent_memory ${where} ORDER BY updated_at DESC LIMIT ?`).all(...params, limit);
    return rows.map(parseMemory);
}

/**
 * Get memory statistics across tiers
 */
function getMemoryStats() {
    ensureMemoryTable();
    const db = getDb();
    const rows = db.prepare('SELECT tier, COUNT(*) as count FROM agent_memory GROUP BY tier').all();
    const total = db.prepare('SELECT COUNT(*) as count FROM agent_memory').get().count;
    const byTier = { session: 0, task: 0, project: 0, org: 0, agent: 0, decision: 0, failure: 0 };
    rows.forEach(r => { byTier[r.tier] = r.count; });
    return { total, byTier };
}

module.exports = {
    storeMemory,
    retrieveMemory,
    getMemoryById,
    getMemoryStats,
    ensureMemoryTable
};
