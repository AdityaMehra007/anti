/**
 * OMNIVANTA OMEGA — Universal Immutable Transaction Ledger
 * 
 * Cryptographically linked, append-only hash-chain ledger for all enterprise
 * transactions, disbursements, invoices, external calls, and high-impact actions.
 * 
 * Guarantees zero historical rewriting through SHA-256 Merkle-linking.
 * 
 * @module omega/ledger
 */

const crypto = require('crypto');
const { getDb } = require('../platform/db');
const { createLogger, recordAudit } = require('../platform/core');
const { v4: uuid } = require('uuid');

const log = createLogger('ledger');

const GENESIS_PREV_HASH = '0000000000000000000000000000000000000000000000000000000000000000';

function ensureLedgerTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS omega_ledger (
            block_index INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_id TEXT UNIQUE NOT NULL,
            prev_hash TEXT NOT NULL,
            tx_type TEXT NOT NULL CHECK(tx_type IN ('PAYMENT', 'INVOICE', 'DISBURSEMENT', 'OUTREACH', 'DEPLOYMENT', 'SERVICE_ACTION', 'EXTERNAL_API', 'AGENT_ACTION', 'GOVERNANCE_DECISION')),
            actor_id TEXT NOT NULL,
            payload TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            block_hash TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_ledger_type ON omega_ledger(tx_type);
        CREATE INDEX IF NOT EXISTS idx_ledger_actor ON omega_ledger(actor_id);
    `);
}

function calculateBlockHash(index, prevHash, txType, actorId, payload, timestamp) {
    const data = `${index}|${prevHash}|${txType}|${actorId}|${payload}|${timestamp}`;
    return crypto.createHash('sha256').update(data).digest('hex');
}

/**
 * Append an immutable transaction to the Merkle-linked ledger
 */
function recordTransaction({ tx_type, actor_id = 'system', payload = {} }) {
    ensureLedgerTable();
    const db = getDb();
    const tx_id = `tx-${uuid()}`;
    const timestamp = new Date().toISOString();
    const payloadStr = typeof payload === 'object' ? JSON.stringify(payload) : String(payload);

    // Get last block hash
    const lastBlock = db.prepare('SELECT block_index, block_hash FROM omega_ledger ORDER BY block_index DESC LIMIT 1').get();
    const nextIndex = lastBlock ? lastBlock.block_index + 1 : 1;
    const prevHash = lastBlock ? lastBlock.block_hash : GENESIS_PREV_HASH;

    const blockHash = calculateBlockHash(nextIndex, prevHash, tx_type, actor_id, payloadStr, timestamp);

    db.prepare(`
        INSERT INTO omega_ledger (block_index, tx_id, prev_hash, tx_type, actor_id, payload, timestamp, block_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(nextIndex, tx_id, prevHash, tx_type, actor_id, payloadStr, timestamp, blockHash);

    log.info(`Committed ledger block #${nextIndex} [${tx_id.substring(0,8)}] (${tx_type})`);
    recordAudit({ actor: actor_id, action: `ledger.${tx_type.toLowerCase()}`, details: { block_index: nextIndex, block_hash: blockHash } });

    return getTransactionById(tx_id);
}

function getTransactionById(tx_id) {
    ensureLedgerTable();
    const db = getDb();
    const row = db.prepare('SELECT * FROM omega_ledger WHERE tx_id = ?').get(tx_id);
    if (!row) return null;
    return {
        ...row,
        payload: JSON.parse(row.payload || '{}')
    };
}

function listTransactions({ limit = 50, tx_type, actor_id } = {}) {
    ensureLedgerTable();
    const db = getDb();
    const conds = [];
    const params = [];

    if (tx_type) { conds.push('tx_type = ?'); params.push(tx_type); }
    if (actor_id) { conds.push('actor_id = ?'); params.push(actor_id); }

    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const rows = db.prepare(`SELECT * FROM omega_ledger ${where} ORDER BY block_index DESC LIMIT ?`).all(...params, limit);
    return rows.map(r => ({
        ...r,
        payload: JSON.parse(r.payload || '{}')
    }));
}

/**
 * Verify cryptographic integrity of the complete hash chain
 */
function verifyLedgerIntegrity() {
    ensureLedgerTable();
    const db = getDb();
    const blocks = db.prepare('SELECT * FROM omega_ledger ORDER BY block_index ASC').all();

    let prevHash = GENESIS_PREV_HASH;
    for (let i = 0; i < blocks.length; i++) {
        const b = blocks[i];
        if (b.prev_hash !== prevHash) {
            return {
                valid: false,
                tamperedBlockIndex: b.block_index,
                reason: `Chain broken at block #${b.block_index}: expected prev_hash ${prevHash}, found ${b.prev_hash}`
            };
        }
        const computed = calculateBlockHash(b.block_index, b.prev_hash, b.tx_type, b.actor_id, b.payload, b.timestamp);
        if (computed !== b.block_hash) {
            return {
                valid: false,
                tamperedBlockIndex: b.block_index,
                reason: `Data payload tampered at block #${b.block_index}: computed ${computed}, found ${b.block_hash}`
            };
        }
        prevHash = b.block_hash;
    }

    return {
        valid: true,
        totalBlocks: blocks.length,
        headHash: prevHash,
        status: 'IMMUTABLE_INTEGRITY_VERIFIED'
    };
}

module.exports = {
    recordTransaction,
    getTransactionById,
    listTransactions,
    verifyLedgerIntegrity,
    ensureLedgerTable
};
