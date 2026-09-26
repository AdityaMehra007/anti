#!/usr/bin/env node
/**
 * OMNIVANTA OMEGA DEVELOPER CLI
 * 
 * Command-line interface to inspect agents, workflows, truth metrics,
 * Merkle ledger, Swarm 2.0 missions, and trigger autonomous cycles.
 * 
 * Usage:
 *   npm run cli -- status
 *   npm run cli -- agent list
 *   npm run cli -- omega truth
 *   npm run cli -- omega score
 *   npm run cli -- omega ledger
 *   npm run cli -- omega redteam
 *   npm run cli -- omega loop
 */

const http = require('http');

const args = process.argv.slice(2);
const command = args[0] || 'status';
const subcommand = args[1] || '';

function apiCall(path, method = 'GET', body = null) {
    return new Promise((resolve, reject) => {
        const req = http.request({
            host: 'localhost',
            port: 3000,
            path: path,
            method: method,
            headers: { 'Content-Type': 'application/json' }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    resolve(data);
                }
            });
        });
        req.on('error', (err) => reject(new Error(`Server unreachable at http://localhost:3000. Error: ${err.message}`)));
        if (body) req.write(JSON.stringify(body));
        req.end();
    });
}

async function main() {
    try {
        if (command === 'status' || command === 'health') {
            const health = await apiCall('/api/health');
            console.log('🌐 OMNIVANTA CLI — SYSTEM HEALTH');
            console.log(JSON.stringify(health, null, 2));
        } else if (command === 'agent') {
            if (subcommand === 'list') {
                const data = await apiCall('/api/agents');
                console.log(`🤖 AGENT REGISTRY (${data.total || 0} Total):`);
                (data.agents || []).forEach(a => {
                    console.log(`  - [${a.id.substring(0,8)}] ${a.name} (Model: ${a.model}, Autonomy: L${a.autonomy_level}, Status: ${a.status})`);
                });
            } else {
                const stats = await apiCall('/api/agents/stats');
                console.log('🤖 AGENT STATS:', JSON.stringify(stats, null, 2));
            }
        } else if (command === 'workflow') {
            const data = await apiCall('/api/workflows');
            console.log(`⚡ WORKFLOW ENGINE (${data.total || 0} Total):`);
            (data.workflows || []).forEach(w => {
                console.log(`  - [${w.id.substring(0,8)}] ${w.name} (Trigger: ${w.trigger_type}, Steps: ${(w.steps||[]).length}, Status: ${w.status})`);
            });
        } else if (command === 'ontology') {
            const stats = await apiCall('/api/ontology/stats');
            console.log('🌐 ENTERPRISE ONTOLOGY STATS:', JSON.stringify(stats, null, 2));
        } else if (command === 'omega') {
            if (subcommand === 'truth') {
                const truth = await apiCall('/api/omega/truth');
                console.log('🔍 OMEGA FOUR-LAYER TRUTH SUMMARY:');
                console.log(JSON.stringify(truth, null, 2));
            } else if (subcommand === 'score') {
                const score = await apiCall('/api/omega/score');
                console.log(`🏆 OMNIVANTA OMEGA SCORE: ${score.compositeOmegaScore}/100 (${score.rating})`);
                console.log('Dimensions:', JSON.stringify(score.dimensions, null, 2));
            } else if (subcommand === 'ledger') {
                const ledger = await apiCall('/api/omega/ledger/verify');
                console.log(`🔗 MERKLE LEDGER INTEGRITY: ${ledger.status} (${ledger.totalBlocks} blocks)`);
            } else if (subcommand === 'redteam') {
                console.log('🔴 Running Automated Adversarial Red Team Attack Audit...');
                const audit = await apiCall('/api/omega/red-team', 'POST');
                console.log(`Status: ${audit.overallSecurityStatus} | Blocked: ${audit.blockedAttacksCount}/${audit.totalAttacksTested} | Vulnerabilities: ${audit.vulnerabilitiesCount}`);
            } else if (subcommand === 'loop') {
                console.log('⚡ Triggering 10-Step Autonomous Daily Operations Cycle...');
                const loop = await apiCall('/api/omega/daily-loop', 'POST');
                console.log('Daily Loop Summary:', JSON.stringify(loop.executiveSummary, null, 2));
            } else {
                console.log('Omega Subcommands: truth | score | ledger | redteam | loop');
            }
        } else if (command === 'apply') {
            if (subcommand === 'list') {
                const data = await apiCall('/api/career/applications');
                console.log(`🎯 TARGET JOB APPLICATIONS (${data.total || 0} Total):`);
                (data.applications || []).forEach(a => {
                    console.log(`  - [${a.job_id}] ${a.company} — ${a.role} | Fit: ${a.fit_score} | Status: ${a.status}`);
                });
            } else if (subcommand === 'get') {
                const jobId = args[2] || 'BLR-JOB-001';
                const app = await apiCall(`/api/career/applications/${jobId}`);
                console.log(`📄 DOSSIER: [${app.job_id}] ${app.company} - ${app.role}`);
                console.log(`Location: ${app.location} | Fit: ${app.fit_score} | Status: ${app.status}`);
                console.log(`Portal: ${app.portal_url}`);
                if (app.referral_name) console.log(`Referral: ${app.referral_name} (${app.referral_title}) - ${app.referral_url}`);
                console.log('\n--- COVER LETTER EXTRACT ---\n' + (app.cover_letter || '').substring(0, 300) + '...\n');
            } else if (subcommand === 'submit') {
                const jobId = args[2];
                const receiptId = args[3] || 'CONF-RECEIPT-' + Date.now();
                if (!jobId) {
                    console.log('Usage: npm run cli -- apply submit <jobId> [receiptId]');
                    return;
                }
                const res = await apiCall(`/api/career/apply/${jobId}`, 'POST', { receiptId, notes: 'CLI submission' });
                console.log(`✅ Logged submission for ${jobId}: Status ${res.status} | Block #${res.ledgerIndex}`);
            } else {
                console.log('Apply Subcommands: list | get <jobId> | submit <jobId> [receiptId]');
            }
        } else {
            console.log('Usage: node cli.js [status | agent list | workflow | ontology | omega | apply]');
        }
    } catch (err) {
        console.error('❌ CLI Error:', err.message);
        process.exit(1);
    }
}

main();
