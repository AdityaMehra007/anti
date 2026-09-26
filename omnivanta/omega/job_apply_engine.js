/**
 * OMNIVANTA OMEGA — Job Application Engine & Dispatcher
 * Manages the complete lifecycle of job applications across the 61 Bangalore MNC pipeline:
 * Dossier compilation, ATS resume extraction, cover letters, referral matching,
 * status transitions, and cryptographic proof receipt logging.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { getDb } = require('../platform/db');
const { createLogger, eventBus, recordAudit } = require('../platform/core');
const { recordEvidence, verifyEvidence } = require('./truth_model');
const { commitLedgerBlock } = require('./ledger');

const logger = createLogger('job-apply-engine');

const CSV_PIPELINE_PATH = path.resolve(__dirname, '../../BBA_IB_Bengaluru_61_Job_Pipeline.csv');
const CSV_MATCHES_PATH = path.resolve(__dirname, '../../job_to_connection_matches.csv');
const DOSSIERS_DIR = path.resolve(__dirname, '../../application_packages');

/**
 * Ensures the `job_applications` table exists in SQLite.
 */
function ensureJobApplicationsTable() {
    const db = getDb();
    db.exec(`
        CREATE TABLE IF NOT EXISTS job_applications (
            job_id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            fit_score REAL,
            fit_band TEXT,
            priority TEXT,
            portal_url TEXT,
            status TEXT DEFAULT 'PREPARED' CHECK(status IN ('PREPARED', 'AUTHORIZED', 'QUEUED', 'SUBMITTED', 'LIVE_VERIFIED', 'REJECTED')),
            cover_letter TEXT,
            resume_text TEXT,
            outreach_pitch TEXT,
            referral_name TEXT,
            referral_title TEXT,
            referral_url TEXT,
            referral_message TEXT,
            star_bullets TEXT,
            receipt_id TEXT,
            evidence_hash TEXT,
            applied_at TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_job_app_status ON job_applications(status);
        CREATE INDEX IF NOT EXISTS idx_job_app_company ON job_applications(company);
    `);
}

/**
 * Parses a dossier markdown file (e.g. BLR-JOB-001_Accenture.md)
 */
function parseDossierFile(filePath) {
    if (!fs.existsSync(filePath)) return null;
    const content = fs.readFileSync(filePath, 'utf-8');

    let coverLetter = '';
    let resumeText = '';
    let outreachPitch = '';
    let starBullets = '';

    // Split sections by ##
    const sections = content.split(/\n##\s+/);
    for (const sec of sections) {
        if (sec.includes('Cover Letter')) {
            coverLetter = sec.replace(/^.*?Cover Letter\s*\n+/, '').trim();
        } else if (sec.includes('Resume Extract')) {
            const match = sec.match(/```([\s\S]*?)```/);
            resumeText = match ? match[1].trim() : sec.trim();
        } else if (sec.includes('Outreach') || sec.includes('Referral Template')) {
            outreachPitch = sec.replace(/^.*?(Outreach|Referral Template).*?\n+/, '').trim();
        } else if (sec.includes('STAR Interview') || sec.includes('Role Defense')) {
            starBullets = sec.replace(/^.*?(STAR Interview|Role Defense).*?\n+/, '').trim();
        }
    }

    return { coverLetter, resumeText, outreachPitch, starBullets, fullContent: content };
}

/**
 * Initializes and seeds the 61 job applications from CSVs and application dossiers.
 */
function seedJobApplications() {
    ensureJobApplicationsTable();
    const db = getDb();

    if (!fs.existsSync(CSV_PIPELINE_PATH)) {
        logger.warn(`Pipeline CSV not found at ${CSV_PIPELINE_PATH}`);
        return { count: 0 };
    }

    // Load referral contacts index from CSV_MATCHES_PATH
    const referralMap = new Map();
    if (fs.existsSync(CSV_MATCHES_PATH)) {
        const matchLines = fs.readFileSync(CSV_MATCHES_PATH, 'utf-8').split('\n').filter(l => l.trim());
        for (let i = 1; i < matchLines.length; i++) {
            const cols = matchLines[i].split(',');
            if (cols.length >= 8) {
                const jId = cols[0]?.trim();
                if (!referralMap.has(jId)) {
                    referralMap.set(jId, {
                        name: cols[5]?.trim(),
                        title: cols[6]?.trim(),
                        url: cols[7]?.trim()
                    });
                }
            }
        }
    }

    // Load dossiers available on disk
    const dossierFiles = fs.existsSync(DOSSIERS_DIR) ? fs.readdirSync(DOSSIERS_DIR) : [];
    const dossierMap = new Map();
    for (const f of dossierFiles) {
        if (f.startsWith('BLR-JOB-') && f.endsWith('.md')) {
            const jobId = f.split('_')[0];
            dossierMap.set(jobId, path.join(DOSSIERS_DIR, f));
        }
    }

    const raw = fs.readFileSync(CSV_PIPELINE_PATH, 'utf-8');
    const lines = raw.split('\n').filter(l => l.trim());
    let inserted = 0;

    const insertStmt = db.prepare(`
        INSERT INTO job_applications (
            job_id, company, role, location, fit_score, fit_band, priority, portal_url,
            status, cover_letter, resume_text, outreach_pitch, referral_name, referral_title,
            referral_url, referral_message, star_bullets, updated_at
        ) VALUES (
            @job_id, @company, @role, @location, @fit_score, @fit_band, @priority, @portal_url,
            @status, @cover_letter, @resume_text, @outreach_pitch, @referral_name, @referral_title,
            @referral_url, @referral_message, @star_bullets, datetime('now')
        )
        ON CONFLICT(job_id) DO UPDATE SET
            company = excluded.company,
            role = excluded.role,
            location = excluded.location,
            fit_score = excluded.fit_score,
            fit_band = excluded.fit_band,
            priority = excluded.priority,
            portal_url = excluded.portal_url,
            cover_letter = COALESCE(excluded.cover_letter, job_applications.cover_letter),
            resume_text = COALESCE(excluded.resume_text, job_applications.resume_text),
            outreach_pitch = COALESCE(excluded.outreach_pitch, job_applications.outreach_pitch),
            referral_name = COALESCE(excluded.referral_name, job_applications.referral_name),
            referral_title = COALESCE(excluded.referral_title, job_applications.referral_title),
            referral_url = COALESCE(excluded.referral_url, job_applications.referral_url),
            referral_message = COALESCE(excluded.referral_message, job_applications.referral_message),
            star_bullets = COALESCE(excluded.star_bullets, job_applications.star_bullets),
            updated_at = datetime('now')
    `);

    db.transaction(() => {
        for (let i = 1; i < lines.length; i++) {
            const cols = lines[i].split(',').map(c => c.trim().replace(/^"|"$/g, ''));
            if (cols.length >= 7) {
                const jobId = cols[0];
                const company = cols[1];
                const role = cols[2];
                const fitScore = parseFloat(cols[3]) || 9.5;
                const fitBand = cols[4] || '9.5–10.0';
                const priority = cols[5] || 'Apply immediately';
                const location = cols[6] || 'Bengaluru';
                const portalUrl = cols[7] || '';

                const dossierPath = dossierMap.get(jobId);
                const dossier = dossierPath ? parseDossierFile(dossierPath) : null;
                const referral = referralMap.get(jobId) || {};

                const referralMsg = referral.name
                    ? `Hi ${referral.name}, I noticed your role at ${company}. I am actively applying for the ${role} opening (${jobId}) and given my background in BBA International Business and logistics operations (Aero India 2025), I would love to connect and see if you'd be open to sharing advice or an internal referral.`
                    : `Hi Hiring Team, I am actively applying for the ${role} position at ${company}.`;

                insertStmt.run({
                    job_id: jobId,
                    company,
                    role,
                    location,
                    fit_score: fitScore,
                    fit_band: fitBand,
                    priority,
                    portal_url: portalUrl,
                    status: 'PREPARED',
                    cover_letter: dossier?.coverLetter || `Tailored cover letter for ${role} at ${company}.`,
                    resume_text: dossier?.resumeText || `Tailored ATS resume for ${role} at ${company}.`,
                    outreach_pitch: dossier?.outreachPitch || `InMail outreach pitch for ${company}.`,
                    referral_name: referral.name || null,
                    referral_title: referral.title || null,
                    referral_url: referral.url || null,
                    referral_message: referralMsg,
                    star_bullets: dossier?.starBullets || `STAR interview defense for ${role}.`
                });
                inserted++;
            }
        }
    })();

    logger.info(`Seeded / Synced ${inserted} job applications into database`);
    return { count: inserted };
}

/**
 * Lists job applications with optional status and search filtering.
 */
function listJobApplications({ status, search, minFit = 0, limit = 100, offset = 0 } = {}) {
    ensureJobApplicationsTable();
    const db = getDb();

    let query = `SELECT * FROM job_applications WHERE fit_score >= ?`;
    const params = [minFit];

    if (status && status !== 'ALL') {
        query += ` AND status = ?`;
        params.push(status);
    }

    if (search) {
        query += ` AND (company LIKE ? OR role LIKE ? OR location LIKE ?)`;
        const s = `%${search}%`;
        params.push(s, s, s);
    }

    query += ` ORDER BY fit_score DESC, job_id ASC LIMIT ? OFFSET ?`;
    params.push(limit, offset);

    const rows = db.prepare(query).all(...params);
    const total = db.prepare(`SELECT COUNT(*) as count FROM job_applications`).get().count;
    
    // Stats by status
    const statusCounts = db.prepare(`
        SELECT status, COUNT(*) as count FROM job_applications GROUP BY status
    `).all();

    return {
        applications: rows,
        total,
        statusBreakdown: Object.fromEntries(statusCounts.map(r => [r.status, r.count]))
    };
}

/**
 * Gets the complete dossier and details for a single job application.
 */
function getJobApplication(jobId) {
    ensureJobApplicationsTable();
    const db = getDb();
    const app = db.prepare(`SELECT * FROM job_applications WHERE job_id = ?`).get(jobId);
    if (!app) return null;

    // Check if there is an immutable ledger block or evidence record
    let ledgerTx = null;
    if (app.receipt_id) {
        ledgerTx = db.prepare(`SELECT * FROM omega_ledger WHERE tx_id = ? OR payload LIKE ?`).get(app.receipt_id, `%${jobId}%`);
    }

    return { ...app, ledgerTransaction: ledgerTx };
}

/**
 * Marks an application as applied and logs a cryptographic receipt.
 * Enforces the 5-tier Epistemic Truth Model:
 * If a valid external receipt ID is provided -> LIVE_VERIFIED
 * If no external receipt ID is provided -> SUBMITTED (LOCAL)
 */
function logApplicationSubmission(jobId, { receiptId, notes = '', channel = 'PORTAL' } = {}) {
    ensureJobApplicationsTable();
    const db = getDb();
    const app = db.prepare(`SELECT * FROM job_applications WHERE job_id = ?`).get(jobId);
    if (!app) throw new Error(`Job application not found: ${jobId}`);

    const newStatus = receiptId ? 'LIVE_VERIFIED' : 'SUBMITTED';
    const epistemicTier = receiptId ? 'LIVE_VERIFIED' : 'LOCAL';
    const evidenceHash = crypto.createHash('sha256')
        .update(`${jobId}:${app.company}:${app.role}:${receiptId || 'DIRECT_SUBMIT'}:${Date.now()}`)
        .digest('hex');

    // 1. Record evidence in universal_evidence
    const evidence = recordEvidence({
        source: `career_app:${jobId}`,
        claim: `Applied for ${app.role} at ${app.company} via ${channel}`,
        tier: epistemicTier,
        data: { jobId, company: app.company, role: app.role, receiptId, channel, notes }
    });

    // 2. Commit to Merkle ledger
    const ledgerBlock = commitLedgerBlock({
        txType: 'JOB_APPLICATION_SUBMIT',
        actor: 'aditya_mehra',
        payload: {
            jobId,
            company: app.company,
            role: app.role,
            receiptId,
            channel,
            evidenceId: evidence.evidenceId,
            evidenceHash
        }
    });

    // 3. Update job_applications table
    db.prepare(`
        UPDATE job_applications
        SET status = ?, receipt_id = ?, evidence_hash = ?, applied_at = datetime('now'), updated_at = datetime('now')
        WHERE job_id = ?
    `).run(newStatus, receiptId || null, evidenceHash, jobId);

    // 4. Record audit log
    recordAudit({
        actor: 'aditya_mehra',
        action: 'job_application_applied',
        resourceType: 'job_application',
        resourceId: jobId,
        details: JSON.stringify({ company: app.company, role: app.role, newStatus, receiptId })
    });

    eventBus.emit('career:application_submitted', { jobId, company: app.company, status: newStatus });
    logger.info(`Job [${jobId}] at ${app.company} updated to status [${newStatus}] with evidence [${evidence.evidenceId}]`);

    return {
        success: true,
        jobId,
        status: newStatus,
        receiptId: receiptId || null,
        evidenceId: evidence.evidenceId,
        evidenceHash,
        ledgerIndex: ledgerBlock.index,
        blockHash: ledgerBlock.blockHash
    };
}

module.exports = {
    ensureJobApplicationsTable,
    seedJobApplications,
    listJobApplications,
    getJobApplication,
    logApplicationSubmission
};
