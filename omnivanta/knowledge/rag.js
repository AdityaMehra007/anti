/**
 * OMNIVANTA — Knowledge Base & Document RAG Engine
 * 
 * Provides chunking, indexing, provenance citation, and semantic/lexical
 * search over enterprise documents, policies, runbooks, and candidate assets.
 * 
 * @module knowledge/rag
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('rag-engine');

function ensureKnowledgeTables() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS knowledge_documents (
            id TEXT PRIMARY KEY,
            org_id TEXT DEFAULT 'org-default',
            title TEXT NOT NULL,
            source_uri TEXT,
            doc_type TEXT NOT NULL, -- 'POLICY', 'RUNBOOK', 'DATASET', 'REPORT', 'MANUAL'
            content TEXT NOT NULL,
            chunk_count INTEGER DEFAULT 0,
            metadata TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS knowledge_chunks (
            id TEXT PRIMARY KEY,
            doc_id TEXT REFERENCES knowledge_documents(id),
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            tokens_estimate INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_chunks_doc ON knowledge_chunks(doc_id);
    `);
}

/**
 * Ingest and chunk a document into the knowledge base
 */
function ingestDocument({ title, content, sourceUri = null, docType = 'POLICY', metadata = {}, chunkSize = 400 }) {
    ensureKnowledgeTables();
    const db = getDb();
    const docId = uuid();
    const now = new Date().toISOString();

    // Simple robust sliding-window chunking
    const words = content.split(/\s+/);
    const chunks = [];
    let currentChunk = [];

    for (let i = 0; i < words.length; i++) {
        currentChunk.push(words[i]);
        if (currentChunk.length >= chunkSize) {
            chunks.push(currentChunk.join(' '));
            currentChunk = [];
        }
    }
    if (currentChunk.length > 0) {
        chunks.push(currentChunk.join(' '));
    }

    db.prepare(`
        INSERT INTO knowledge_documents (id, title, source_uri, doc_type, content, chunk_count, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(docId, title, sourceUri, docType, content, chunks.length, JSON.stringify(metadata), now);

    const insertChunk = db.prepare(`
        INSERT INTO knowledge_chunks (id, doc_id, chunk_index, content, tokens_estimate, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    `);

    chunks.forEach((chunkText, idx) => {
        const chunkId = uuid();
        insertChunk.run(chunkId, docId, idx, chunkText, Math.ceil(chunkText.length / 4), now);
    });

    log.info(`Ingested document "${title}" -> ${chunks.length} chunks`);
    recordAudit({ actor: 'system', action: 'knowledge.doc_ingested', resourceType: 'knowledge_doc', resourceId: docId, details: { title, chunkCount: chunks.length } });

    return {
        id: docId,
        title,
        docType,
        chunkCount: chunks.length,
        created_at: now
    };
}

/**
 * Retrieve relevant document chunks with relevance scoring and provenance citation
 */
function queryKnowledge(query, { limit = 5, docType = null } = {}) {
    ensureKnowledgeTables();
    const db = getDb();
    const terms = query.toLowerCase().split(/\s+/).filter(t => t.length > 2);

    if (terms.length === 0) return { query, matches: [], total: 0 };

    const conds = [];
    const params = [];

    terms.forEach(term => {
        conds.push('LOWER(kc.content) LIKE ?');
        params.push(`%${term}%`);
    });

    let whereClause = conds.join(' OR ');
    if (docType) {
        whereClause = `(${whereClause}) AND kd.doc_type = ?`;
        params.push(docType);
    }

    const querySql = `
        SELECT kc.id, kc.doc_id, kc.chunk_index, kc.content, kd.title as doc_title, kd.source_uri, kd.doc_type
        FROM knowledge_chunks kc
        JOIN knowledge_documents kd ON kc.doc_id = kd.id
        WHERE ${whereClause}
        LIMIT ?
    `;

    const rows = db.prepare(querySql).all(...params, limit);

    const matches = rows.map(r => {
        // Calculate term frequency score
        const contentLower = r.content.toLowerCase();
        let score = 0;
        terms.forEach(t => {
            if (contentLower.includes(t)) score += 1;
        });
        const relevance = Math.min(1.0, score / terms.length);

        return {
            chunkId: r.id,
            docId: r.doc_id,
            docTitle: r.doc_title,
            docType: r.doc_type,
            sourceUri: r.source_uri,
            relevanceScore: parseFloat(relevance.toFixed(2)),
            snippet: r.content,
            citation: `Source: "${r.doc_title}" (Section chunk ${r.chunk_index + 1})`
        };
    }).sort((a, b) => b.relevanceScore - a.relevanceScore);

    return {
        query,
        total: matches.length,
        matches
    };
}

function getKnowledgeStats() {
    ensureKnowledgeTables();
    const db = getDb();
    const totalDocs = db.prepare('SELECT COUNT(*) as count FROM knowledge_documents').get().count;
    const totalChunks = db.prepare('SELECT COUNT(*) as count FROM knowledge_chunks').get().count;
    const byType = db.prepare('SELECT doc_type, COUNT(*) as count FROM knowledge_documents GROUP BY doc_type').all();

    return { totalDocs, totalChunks, byType };
}

module.exports = {
    ingestDocument,
    queryKnowledge,
    getKnowledgeStats,
    ensureKnowledgeTables
};
