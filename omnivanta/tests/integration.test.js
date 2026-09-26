/**
 * OMNIVANTA — MASTER EXPANDED INTEGRATION TEST SUITE (18 GATES)
 * 
 * Validates Core Platform, Gateway, Governance, Search, Memory, Governed Tools,
 * Billing, BI, Career OS, AI Service Desk, Swarm Missions, Document RAG, Telemetry, and App Builder.
 */

const http = require('http');
const { config, registerModule } = require('../platform/core');
const { initDb, closeDb } = require('../platform/db');
const agentRegistry = require('../agents/registry');
const workflowEngine = require('../workflows/engine');
const ontology = require('../context/ontology');
const connectorRegistry = require('../integrations/connector');
const { createServer } = require('../platform/server');
const { routeModel } = require('../platform/gateway');
const { auditPrompt, authorizeAction } = require('../security/governance');

let serverInstance = null;

function request(path, method = 'GET', body = null) {
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
                    resolve({ status: res.statusCode, body: JSON.parse(data) });
                } catch (e) {
                    resolve({ status: res.statusCode, body: data });
                }
            });
        });
        req.on('error', reject);
        if (body) req.write(JSON.stringify(body));
        req.end();
    });
}

async function startServerForTest() {
    try {
        initDb();
        try { registerModule('agentRegistry', agentRegistry); } catch(e) {}
        try { registerModule('workflowEngine', workflowEngine); } catch(e) {}
        try { registerModule('ontology', ontology); } catch(e) {}
        try { registerModule('connectorRegistry', connectorRegistry); } catch(e) {}

        const app = createServer();
        return new Promise((resolve) => {
            serverInstance = app.listen(config.port, () => {
                resolve();
            });
            serverInstance.on('error', (err) => {
                if (err.code === 'EADDRINUSE') {
                    resolve();
                }
            });
        });
    } catch (e) {}
}

async function runTests() {
    await startServerForTest();
    console.log("🧪 RUNNING COMPREHENSIVE 18-GATE OMNIVANTA TEST SUITE...\n");
    let passed = 0;
    let failed = 0;

    async function assert(name, fn) {
        try {
            await fn();
            console.log(`  ✅ PASS: ${name}`);
            passed++;
        } catch (e) {
            console.log(`  ❌ FAIL: ${name} — ${e.message}`);
            failed++;
        }
    }

    // 1. Health check
    await assert('Gate 1: Health Check (/api/health)', async () => {
        const res = await request('/api/health');
        if (res.status !== 200 || res.body.status !== 'healthy') throw new Error(`Health check failed`);
    });

    // 2. Dashboard Aggregate
    await assert('Gate 2: Dashboard Summary (/api/dashboard)', async () => {
        const res = await request('/api/dashboard');
        if (res.status !== 200 || !res.body.agents) throw new Error(`Dashboard data invalid`);
    });

    // 3. Model Gateway Routing
    await assert('Gate 3: Model Gateway Dynamic Routing', async () => {
        const routing = routeModel({ complexity: 'high' });
        if (routing.selectedModel !== 'gemini-2.5-pro') throw new Error(`Model routing failed`);
    });

    // 4. AI Governance Prompt Injection Defense
    await assert('Gate 4: AI Governance Prompt Injection Detection', async () => {
        const checkSafe = auditPrompt('Generate financial report summary');
        if (!checkSafe.safe) throw new Error(`Safe prompt failed`);
        const checkUnsafe = auditPrompt('DROP TABLE users; --');
        if (checkUnsafe.safe) throw new Error(`Unsafe prompt bypassed defense`);
    });

    // 5. AI Governance Autonomy Gate
    await assert('Gate 5: AI Governance Autonomy Level Gate (L1 vs L3)', async () => {
        const authL1 = authorizeAction(1, 'write_local');
        if (authL1.authorized) throw new Error(`L1 should not permit write_local`);
        const authL3 = authorizeAction(3, 'write_local');
        if (!authL3.authorized) throw new Error(`L3 should permit write_local`);
    });

    // 6. Universal Enterprise Search
    await assert('Gate 6: Universal Enterprise Search (/api/search)', async () => {
        const res = await request('/api/search?q=Amazon');
        if (res.status !== 200 || !res.body.results || res.body.results.length === 0) {
            throw new Error(`Search failed to find matches for "Amazon"`);
        }
    });

    // 7. Multi-Tier Agent Memory
    await assert('Gate 7: Agent Memory Store & Retrieval (/api/memory)', async () => {
        const storeRes = await request('/api/memory', 'POST', {
            tier: 'decision',
            key: 'pricing_strategy_q4',
            value: { model: 'usage_based', margin: 0.90 },
            tags: ['pricing', 'strategy']
        });
        if (storeRes.status !== 201 || !storeRes.body.id) throw new Error(`Memory storage failed`);

        const getRes = await request('/api/memory?key=pricing_strategy_q4');
        if (getRes.status !== 200 || getRes.body.total === 0) throw new Error(`Memory retrieval failed`);
    });

    // 8. Governed Tool Execution
    await assert('Gate 8: Governed Tool Execution (/api/tools/execute)', async () => {
        const toolRes = await request('/api/tools/execute', 'POST', {
            toolName: 'system_time',
            autonomyLevel: 1
        });
        if (toolRes.status !== 200 || !toolRes.body.result?.timezone) throw new Error(`Tool execution failed`);
    });

    // 9. Commercial Billing Plans
    await assert('Gate 9: Commercial Billing Plans (/api/billing/plans)', async () => {
        const res = await request('/api/billing/plans');
        if (res.status !== 200 || !res.body.plans?.enterprise) throw new Error(`Plans retrieval failed`);
    });

    // 10. Automated Invoice Generation
    await assert('Gate 10: Invoice Generation Engine (/api/billing/invoice)', async () => {
        const res = await request('/api/billing/invoice?tier=business');
        if (res.status !== 200 || res.body.totalDueUSD !== 1999) throw new Error(`Invoice calculation failed`);
    });

    // 11. Business Intelligence Portal API
    await assert('Gate 11: Business Intelligence API (/api/bi/companies)', async () => {
        const res = await request('/api/bi/companies?q=Apple');
        if (res.status !== 200 || !res.body.companies) throw new Error(`BI API query failed`);
    });

    // 12. Career Intelligence OS Pipeline API
    await assert('Gate 12: Career Intelligence Pipeline API (/api/career/pipeline)', async () => {
        const res = await request('/api/career/pipeline');
        if (res.status !== 200 || res.body.total === 0) throw new Error(`Career pipeline query failed`);
    });

    // 13. AI Service Desk Incident Triage & Resolution
    let ticketId = null;
    await assert('Gate 13: Service Desk Triage & Resolution (/api/service-desk/tickets)', async () => {
        const ticketRes = await request('/api/service-desk/tickets', 'POST', {
            title: 'Critical Outage on Main Node',
            description: '500 error cascade observed in production cluster'
        });
        if (ticketRes.status !== 201 || ticketRes.body.priority !== 'P1_CRITICAL') {
            throw new Error(`AI triage failed to flag P1_CRITICAL`);
        }
        ticketId = ticketRes.body.id;

        const resolveRes = await request(`/api/service-desk/tickets/${ticketId}/resolve`, 'POST', {
            resolution: 'Applied rollback patch and cleared connection pool.'
        });
        if (resolveRes.status !== 200 || resolveRes.body.status !== 'RESOLVED') {
            throw new Error(`Ticket resolution failed`);
        }
    });

    // 14. Agent & Workflow Full Execution Pipeline
    await assert('Gate 14: Agent & Workflow Full Execution Pipeline', async () => {
        const agentRes = await request('/api/agents', 'POST', { name: 'Gate 14 Agent', model: 'gemini-2.5-flash', autonomyLevel: 3 });
        const wfRes = await request('/api/workflows', 'POST', { name: 'Health Workflow', steps: [{ name: 'Step 1', agentId: agentRes.body.id }] });
        const execRes = await request(`/api/workflows/${wfRes.body.id}/execute`, 'POST', { executedBy: 'master-runner' });
        if (execRes.status !== 200 || execRes.body.status !== 'completed') throw new Error(`Workflow execution failed`);
    });

    // 15. Agent Swarm Autonomous Mission Launch
    await assert('Gate 15: Agent Swarm Collaborative Mission (/api/swarm/missions)', async () => {
        const missionRes = await request('/api/swarm/missions', 'POST', {
            title: 'Q4 Market Opportunity Scan',
            objective: 'Identify high-margin expansion targets in Asia-Pacific enterprise AI'
        });
        if (missionRes.status !== 201 || missionRes.body.status !== 'COMPLETED' || !missionRes.body.collaborative_output) {
            throw new Error(`Swarm mission failed or output missing`);
        }
    });

    // 16. Document Knowledge Ingestion & Citation RAG Query
    await assert('Gate 16: Knowledge Base Ingestion & RAG Citation Query (/api/knowledge)', async () => {
        const ingestRes = await request('/api/knowledge/ingest', 'POST', {
            title: 'Omnivanta Security Protocol v29',
            docType: 'POLICY',
            content: 'All agent network communication must use mutual TLS. Level 4 and Level 5 actions require human authorization quorum.'
        });
        if (ingestRes.status !== 201 || ingestRes.body.chunkCount === 0) throw new Error(`Document ingestion failed`);

        const queryRes = await request('/api/knowledge/query?q=authorization+quorum');
        if (queryRes.status !== 200 || !queryRes.body.matches || queryRes.body.matches.length === 0) {
            throw new Error(`RAG query failed to retrieve relevant citation`);
        }
    });

    // 17. Telemetry & Observability Latency Percentiles
    await assert('Gate 17: Live Observability & Telemetry Metrics (/api/observability/metrics)', async () => {
        const res = await request('/api/observability/metrics');
        if (res.status !== 200 || res.body.traffic?.totalRequests === undefined || !res.body.systemMemory?.heapUsedMB) {
            throw new Error(`Observability telemetry invalid`);
        }
    });

    // 18. Custom Micro-App Builder Creation & Submissions
    await assert('Gate 18: Custom App Builder & Record Submissions (/api/apps)', async () => {
        const appRes = await request('/api/apps', 'POST', {
            name: 'Vendor Invoice Approval Micro-App',
            category: 'FINANCE',
            description: 'Automated invoice routing and departmental approval tracking'
        });
        if (appRes.status !== 201 || !appRes.body.id) throw new Error(`App creation failed`);
        const appId = appRes.body.id;

        const subRes = await request(`/api/apps/${appId}/records`, 'POST', {
            title: 'AWS Enterprise Cloud Bill August 2026',
            amount: 4250,
            status: 'Approved'
        });
        if (subRes.status !== 201 || !subRes.body.id) throw new Error(`App record submission failed`);
    });

    console.log(`\n📊 MASTER TEST RESULTS: ${passed} Passed | ${failed} Failed`);
    
    if (serverInstance) {
        serverInstance.close();
    }
    
    if (failed > 0) process.exit(1);
    else process.exit(0);
}

runTests().catch(err => {
    console.error("Test runner error:", err);
    if (serverInstance) serverInstance.close();
    process.exit(1);
});
