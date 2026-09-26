/**
 * OMNIVANTA OMEGA — Disaster Recovery & Snapshot Engine
 * 
 * Provides automated database backup, point-in-time snapshotting,
 * and live restore verification tests (Section 28).
 * 
 * @module omega/disaster_recovery
 */

const fs = require('fs');
const path = require('path');
const { getDb } = require('../platform/db');
const { createLogger, recordAudit } = require('../platform/core');
const Database = require('better-sqlite3');

const log = createLogger('disaster-recovery');

const BACKUP_DIR = path.join(__dirname, '..', 'data', 'backups');

function ensureBackupDir() {
    if (!fs.existsSync(BACKUP_DIR)) {
        fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }
}

/**
 * Create a validated point-in-time backup snapshot of the SQLite database
 */
async function createSnapshot(tag = 'scheduled') {
    ensureBackupDir();
    const db = getDb();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFileName = `omnivanta_backup_${tag}_${timestamp}.db`;
    const backupPath = path.join(BACKUP_DIR, backupFileName);

    log.info(`[DISASTER RECOVERY] Creating snapshot at ${backupPath}...`);

    // Use better-sqlite3 native backup API
    await db.backup(backupPath);

    const stats = fs.statSync(backupPath);
    log.info(`[DISASTER RECOVERY] Snapshot complete (${stats.size} bytes)`);

    recordAudit({
        actor: 'disaster-recovery',
        action: 'backup.snapshot_created',
        details: { backupPath, sizeBytes: stats.size, tag }
    });

    return {
        backupFileName,
        backupPath,
        sizeBytes: stats.size,
        tag,
        createdAt: new Date().toISOString()
    };
}

/**
 * Execute an automated restore verification test
 * Verifies that the backup can be mounted, queried, and matches record integrity.
 */
async function runRestoreVerificationTest() {
    log.info('[DISASTER RECOVERY] Starting automated restore verification test...');
    const snapshot = await createSnapshot('restore_test');

    // Mount backup file in temporary read-only test mode
    const testDb = new Database(snapshot.backupPath, { readonly: true });
    try {
        // Query critical tables
        const agentCount = testDb.prepare('SELECT COUNT(*) as count FROM agents').get().count;
        const workflowCount = testDb.prepare('SELECT COUNT(*) as count FROM workflows').get().count;
        const integrityCheck = testDb.pragma('quick_check', { simple: true });

        testDb.close();

        const verified = integrityCheck === 'ok' && agentCount > 0;
        log.info(`[DISASTER RECOVERY] Restore Test Result: ${verified ? 'SUCCESS' : 'FAILED'} (Integrity: ${integrityCheck}, Agents: ${agentCount})`);

        recordAudit({
            actor: 'disaster-recovery',
            action: 'backup.restore_verified',
            details: { snapshot: snapshot.backupFileName, integrityCheck, agentCount, verified }
        });

        return {
            status: verified ? 'RESTORE_TEST_PASSED' : 'RESTORE_TEST_FAILED',
            backupTested: snapshot.backupFileName,
            integrityCheck,
            verifiedRecords: {
                agents: agentCount,
                workflows: workflowCount
            },
            verifiedAt: new Date().toISOString()
        };
    } catch (e) {
        testDb.close();
        log.error(`[DISASTER RECOVERY] Restore test error: ${e.message}`);
        throw e;
    }
}

function listSnapshots() {
    ensureBackupDir();
    const files = fs.readdirSync(BACKUP_DIR).filter(f => f.endsWith('.db'));
    return files.map(f => {
        const fullPath = path.join(BACKUP_DIR, f);
        const st = fs.statSync(fullPath);
        return {
            fileName: f,
            sizeBytes: st.size,
            createdAt: st.mtime.toISOString()
        };
    });
}

module.exports = {
    createSnapshot,
    runRestoreVerificationTest,
    listSnapshots
};
