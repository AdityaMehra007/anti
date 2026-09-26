/**
 * OMNIVANTA API SERVER
 * 
 * Express HTTP server exposing REST APIs for the entire platform.
 * Serves the Control Tower UI and provides endpoints for agents, workflows,
 * ontology, connectors, events, and audit log.
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const { config, createLogger, eventBus, listModules } = require('./core');

const log = createLogger('server');

let agentRegistry, workflowEngine, ontology, connectorRegistry;

function createServer(modules = {}) {
    agentRegistry = modules.agentRegistry || agentRegistry || require('../agents/registry');
    workflowEngine = modules.workflowEngine || workflowEngine || require('../workflows/engine');
    ontology = modules.ontology || ontology || require('../context/ontology');
    connectorRegistry = modules.connectorRegistry || connectorRegistry || require('../integrations/connector');

    const app = express();
    app.use(cors());
    app.use(express.json());

    // ─── Static files: Control Tower & Applications ───────────────────────────
    app.use(express.static(path.join(config.root, 'applications', 'control-tower')));
    app.use('/bi', express.static(path.join(config.root, 'applications', 'business-intelligence')));
    app.use('/career', express.static(path.join(config.root, 'applications', 'career-intelligence')));
    app.use('/service-desk', express.static(path.join(config.root, 'applications', 'service-desk')));
    app.use('/apps', express.static(path.join(config.root, 'applications', 'app-builder')));
    app.use('/interview', express.static(path.join(config.root, '..', 'dashboard')));

    // ─── Health & Platform Info ───────────────────────────────────────────────
    app.get('/api/health', (req, res) => {
        res.json({ status: 'healthy', platform: config.name, version: config.version, uptime: process.uptime() });
    });

    app.get('/api/platform/info', (req, res) => {
        res.json({
            name: config.name,
            version: config.version,
            description: config.description,
            modules: listModules(),
            autonomyLevels: config.autonomyLevels,
        });
    });

    // ─── Agents API ──────────────────────────────────────────────────────────
    app.post('/api/agents', (req, res) => {
        try {
            const agent = agentRegistry.createAgent(req.body);
            res.status(201).json(agent);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/agents', (req, res) => {
        try {
            const { orgId, status, autonomyLevel, limit, offset } = req.query;
            const result = agentRegistry.listAgents({
                orgId, status,
                autonomyLevel: autonomyLevel != null ? parseInt(autonomyLevel) : undefined,
                limit: limit ? parseInt(limit) : undefined,
                offset: offset ? parseInt(offset) : undefined,
            });
            res.json(result);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/agents/stats', (req, res) => {
        try {
            res.json(agentRegistry.getAgentStats(req.query.orgId));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/agents/:id', (req, res) => {
        try {
            const agent = agentRegistry.getAgent(req.params.id);
            if (!agent) return res.status(404).json({ error: 'Agent not found' });
            res.json(agent);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.patch('/api/agents/:id', (req, res) => {
        try {
            const agent = agentRegistry.updateAgent(req.params.id, req.body);
            res.json(agent);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.delete('/api/agents/:id', (req, res) => {
        try {
            agentRegistry.deleteAgent(req.params.id);
            res.json({ deleted: true });
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // ─── Workflows API ───────────────────────────────────────────────────────
    app.post('/api/workflows', (req, res) => {
        try {
            const wf = workflowEngine.createWorkflow(req.body);
            res.status(201).json(wf);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/workflows', (req, res) => {
        try {
            const { orgId, status, limit, offset } = req.query;
            res.json(workflowEngine.listWorkflows({
                orgId, status,
                limit: limit ? parseInt(limit) : undefined,
                offset: offset ? parseInt(offset) : undefined,
            }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/workflows/stats', (req, res) => {
        try {
            res.json(workflowEngine.getWorkflowStats(req.query.orgId));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/workflows/:id', (req, res) => {
        try {
            const wf = workflowEngine.getWorkflow(req.params.id);
            if (!wf) return res.status(404).json({ error: 'Workflow not found' });
            res.json(wf);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/workflows/:id/execute', async (req, res) => {
        try {
            const result = await workflowEngine.executeWorkflow(req.params.id, req.body);
            res.json(result);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // ─── Tasks API ───────────────────────────────────────────────────────────
    app.get('/api/tasks', (req, res) => {
        try {
            const { workflowId, agentId, status, limit, offset } = req.query;
            res.json(workflowEngine.listTasks({
                workflowId, agentId, status,
                limit: limit ? parseInt(limit) : undefined,
                offset: offset ? parseInt(offset) : undefined,
            }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/tasks/:id', (req, res) => {
        try {
            const task = workflowEngine.getTask(req.params.id);
            if (!task) return res.status(404).json({ error: 'Task not found' });
            res.json(task);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.patch('/api/tasks/:id/transition', (req, res) => {
        try {
            const { status, output, error } = req.body;
            const task = workflowEngine.transitionTask(req.params.id, status, { output, error });
            res.json(task);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // ─── Ontology: Customers ─────────────────────────────────────────────────
    app.post('/api/customers', (req, res) => {
        try { res.status(201).json(ontology.createCustomer(req.body)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/customers', (req, res) => {
        try {
            const { orgId, industry, limit, offset } = req.query;
            res.json(ontology.listCustomers({ orgId, industry, limit: limit ? parseInt(limit) : undefined, offset: offset ? parseInt(offset) : undefined }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/customers/:id', (req, res) => {
        try {
            const c = ontology.getCustomer(req.params.id);
            if (!c) return res.status(404).json({ error: 'Customer not found' });
            res.json(c);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/customers/:id/graph', (req, res) => {
        try { res.json(ontology.getCustomerGraph(req.params.id)); }
        catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Ontology: Accounts ──────────────────────────────────────────────────
    app.post('/api/accounts', (req, res) => {
        try { res.status(201).json(ontology.createAccount(req.body)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/accounts', (req, res) => {
        try {
            const { customerId, status, limit, offset } = req.query;
            res.json(ontology.listAccounts({ customerId, status, limit: limit ? parseInt(limit) : undefined, offset: offset ? parseInt(offset) : undefined }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Ontology: Products ──────────────────────────────────────────────────
    app.post('/api/products', (req, res) => {
        try { res.status(201).json(ontology.createProduct(req.body)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/products', (req, res) => {
        try {
            const { orgId, category, limit, offset } = req.query;
            res.json(ontology.listProducts({ orgId, category, limit: limit ? parseInt(limit) : undefined, offset: offset ? parseInt(offset) : undefined }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Ontology: Contracts ─────────────────────────────────────────────────
    app.post('/api/contracts', (req, res) => {
        try { res.status(201).json(ontology.createContract(req.body)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/contracts', (req, res) => {
        try {
            const { accountId, productId, status, limit, offset } = req.query;
            res.json(ontology.listContracts({ accountId, productId, status, limit: limit ? parseInt(limit) : undefined, offset: offset ? parseInt(offset) : undefined }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Ontology Stats ──────────────────────────────────────────────────────
    app.get('/api/ontology/stats', (req, res) => {
        try { res.json(ontology.getOntologyStats(req.query.orgId)); }
        catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Connectors API ──────────────────────────────────────────────────────
    app.post('/api/connectors', (req, res) => {
        try { res.status(201).json(connectorRegistry.createConnector(req.body)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/connectors', (req, res) => {
        try {
            const { orgId, type, status, limit, offset } = req.query;
            res.json(connectorRegistry.listConnectors({ orgId, type, status, limit: limit ? parseInt(limit) : undefined, offset: offset ? parseInt(offset) : undefined }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/connectors/stats', (req, res) => {
        try { res.json(connectorRegistry.getConnectorStats(req.query.orgId)); }
        catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.patch('/api/connectors/:id/enable', (req, res) => {
        try { res.json(connectorRegistry.enableConnector(req.params.id)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.patch('/api/connectors/:id/disable', (req, res) => {
        try { res.json(connectorRegistry.disableConnector(req.params.id)); }
        catch (e) { res.status(400).json({ error: e.message }); }
    });

    // ─── Audit Log API ───────────────────────────────────────────────────────
    app.get('/api/audit', (req, res) => {
        try {
            const { getDb } = require('./db');
            const db = getDb();
            const limit = parseInt(req.query.limit) || 50;
            const offset = parseInt(req.query.offset) || 0;
            const rows = db.prepare('SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ? OFFSET ?').all(limit, offset);
            const total = db.prepare('SELECT COUNT(*) as count FROM audit_log').get().count;
            res.json({ entries: rows, total });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Events API ──────────────────────────────────────────────────────────
    app.get('/api/events', (req, res) => {
        try {
            const { getDb } = require('./db');
            const db = getDb();
            const limit = parseInt(req.query.limit) || 50;
            const rows = db.prepare('SELECT * FROM events ORDER BY created_at DESC LIMIT ?').all(limit);
            res.json({ events: rows });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Business Intelligence API (Real Enterprise Data) ─────────────────────
    // ─── Business Intelligence API (Real Enterprise Data) ─────────────────────
    app.get('/api/bi/companies', (req, res) => {
        try {
            const fs = require('fs');
            const companies = [];
            const seen = new Set();

            // Source 1: Bangalore_3000_Company_Target_Directory.csv
            const targetCsv = path.join(config.root, '..', 'data', 'Bangalore_3000_Company_Target_Directory.csv');
            if (fs.existsSync(targetCsv)) {
                const lines = fs.readFileSync(targetCsv, 'utf-8').split('\n').filter(l => l.trim());
                for (let i = 1; i < lines.length; i++) {
                    const parts = lines[i].split(',').map(p => p.replace(/"/g, '').trim());
                    if (parts.length >= 5) {
                        const name = parts[1];
                        if (!seen.has(name.toLowerCase())) {
                            seen.add(name.toLowerCase());
                            companies.push({
                                name,
                                tier: parts[6] || 'Tier 1 MNC',
                                bengaluruPresence: true,
                                fitScore: 9.5,
                                location: parts[4] || 'Bengaluru',
                                industry: parts[2] || 'Enterprise IT & Global Operations'
                            });
                        }
                    }
                }
            }

            // Source 2: SQLite job_applications table
            const { getDb } = require('./db');
            const db = getDb();
            const apps = db.prepare('SELECT company, role, location, fit_score FROM job_applications').all();
            for (const a of apps) {
                if (!seen.has(a.company.toLowerCase())) {
                    seen.add(a.company.toLowerCase());
                    companies.push({
                        name: a.company,
                        tier: 'Target MNC',
                        bengaluruPresence: true,
                        fitScore: a.fit_score || 9.0,
                        location: a.location || 'Bengaluru',
                        industry: 'Global Capability Center (GCC)'
                    });
                }
            }

            const query = (req.query.q || '').toLowerCase();
            const filtered = query 
                ? companies.filter(c => c.name.toLowerCase().includes(query) || c.industry.toLowerCase().includes(query))
                : companies;
                
            res.json({ companies: filtered, total: filtered.length });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/bi/network-graph', (req, res) => {
        try {
            const { getDb } = require('./db');
            const db = getDb();
            const apps = db.prepare('SELECT job_id, company, role, location, fit_score, referral_name, referral_title FROM job_applications').all();

            const nodes = [
                { id: 'aditya', label: 'Aditya Mehra (BBA IB)', type: 'candidate', group: 1 }
            ];
            const links = [];

            // Add corridor nodes
            const corridors = ['Whitefield Tech Hub', 'Outer Ring Road (ORR)', 'Electronic City', 'Central Business District (CBD)'];
            corridors.forEach((c, idx) => {
                nodes.push({ id: `corr_${idx}`, label: c, type: 'corridor', group: 2 });
                links.push({ source: 'aditya', target: `corr_${idx}`, value: 3 });
            });

            // Add top 25 companies and referrals
            apps.slice(0, 25).forEach((a, idx) => {
                const compId = `comp_${a.job_id}`;
                nodes.push({ id: compId, label: a.company, type: 'company', role: a.role, fit: a.fit_score, group: 3 });
                
                // Link to a corridor based on location
                const loc = (a.location || '').toLowerCase();
                let corrId = 'corr_1'; // default ORR
                if (loc.includes('whitefield')) corrId = 'corr_0';
                else if (loc.includes('electronic')) corrId = 'corr_2';
                else if (loc.includes('cbd') || loc.includes('central')) corrId = 'corr_3';

                links.push({ source: corrId, target: compId, value: 2 });

                if (a.referral_name) {
                    const refId = `ref_${a.job_id}`;
                    nodes.push({ id: refId, label: a.referral_name, title: a.referral_title, type: 'referral', group: 4 });
                    links.push({ source: compId, target: refId, value: 1 });
                }
            });

            res.json({ nodes, links });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Career Intelligence API (Real Candidate & Pipeline Data) ────────────
    app.get('/api/career/profile', (req, res) => {
        try {
            const fs = require('fs');
            const profilePath = path.join(config.root, '..', 'career-hub', 'candidate', 'candidate_profile.json');
            if (!fs.existsSync(profilePath)) {
                return res.json({
                    candidate: "Aditya Mehra",
                    degree: "BBA International Business, DSU Bangalore '26",
                    verifiedClaims: ["300+ Event Deployments", "15% Cost Reduction", "INR 1.5L+ Revenue Closed", "3.2x AI Ops Throughput"],
                    status: "ACTIVE_JOB_PIPELINE"
                });
            }
            res.json(JSON.parse(fs.readFileSync(profilePath, 'utf-8')));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/career/pipeline', (req, res) => {
        try {
            const { listJobApplications } = require('../omega/job_apply_engine');
            const data = listJobApplications({
                status: req.query.status,
                search: req.query.search,
                limit: parseInt(req.query.limit) || 100
            });
            res.json({
                pipeline: data.applications,
                total: data.total,
                statusBreakdown: data.statusBreakdown
            });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/career/applications', (req, res) => {
        try {
            const { listJobApplications } = require('../omega/job_apply_engine');
            const result = listJobApplications(req.query);
            res.json(result);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/career/applications/:jobId', (req, res) => {
        try {
            const { getJobApplication } = require('../omega/job_apply_engine');
            const appData = getJobApplication(req.params.jobId);
            if (!appData) return res.status(404).json({ error: 'Job application not found' });
            res.json(appData);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/career/apply/:jobId', (req, res) => {
        try {
            const { logApplicationSubmission } = require('../omega/job_apply_engine');
            const result = logApplicationSubmission(req.params.jobId, req.body || {});
            res.json(result);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/career/seed', (req, res) => {
        try {
            const { seedJobApplications } = require('../omega/job_apply_engine');
            const result = seedJobApplications();
            res.json(result);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/career/skills', (req, res) => {
        try {
            const fs = require('fs');
            const skillPath = path.join(config.root, '..', 'Aditya_Mehra_300_Skills_Master_Matrix.csv');
            if (!fs.existsSync(skillPath)) return res.json({ skillsCount: 300, categories: ['Operations', 'Sales', 'AI Data Ops', 'EXIM Trade'] });
            
            const raw = fs.readFileSync(skillPath, 'utf-8');
            const lines = raw.split('\n').filter(l => l.trim());
            res.json({ totalSkills: lines.length - 1, sample: lines.slice(1, 10).map(l => l.split(',')[0]?.replace(/"/g, '')) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Universal Enterprise Search API ──────────────────────────────────────
    app.get('/api/search', (req, res) => {
        try {
            const { search } = require('../context/search');
            const results = search(req.query.q, { limit: parseInt(req.query.limit) || 20, domain: req.query.domain || 'all' });
            res.json(results);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Agent Memory API ────────────────────────────────────────────────────
    app.post('/api/memory', (req, res) => {
        try {
            const { storeMemory } = require('../agents/memory');
            const memory = storeMemory(req.body);
            res.status(201).json(memory);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/memory', (req, res) => {
        try {
            const { retrieveMemory } = require('../agents/memory');
            const { agentId, tier, key, tag, limit } = req.query;
            const items = retrieveMemory({ agentId, tier, key, tag, limit: parseInt(limit) || 50 });
            res.json({ items, total: items.length });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/memory/stats', (req, res) => {
        try {
            const { getMemoryStats } = require('../agents/memory');
            res.json(getMemoryStats());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Governed Tool Execution API ─────────────────────────────────────────
    app.get('/api/tools', (req, res) => {
        try {
            const { listAvailableTools } = require('../integrations/mcp_bridge');
            res.json({ tools: listAvailableTools() });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/tools/execute', async (req, res) => {
        try {
            const { executeTool } = require('../integrations/mcp_bridge');
            const result = await executeTool(req.body);
            res.json(result);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // ─── Commercial Metering & Billing API ───────────────────────────────────
    app.get('/api/billing/plans', (req, res) => {
        try {
            const { listTiers } = require('../billing/metering');
            res.json({ plans: listTiers() });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/billing/usage', (req, res) => {
        try {
            const { getUsageSummary } = require('../billing/metering');
            res.json(getUsageSummary(req.query.orgId || 'org-default'));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/billing/invoice', (req, res) => {
        try {
            const { generateInvoice } = require('../billing/metering');
            res.json(generateInvoice(req.query.orgId || 'org-default', req.query.tier || 'business'));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── AI Service Desk & Incidents API ─────────────────────────────────────
    app.get('/api/service-desk/tickets', (req, res) => {
        try {
            const { listTickets } = require('../applications/service-desk/service');
            const { status, priority, category, limit } = req.query;
            res.json(listTickets({ status, priority, category, limit: parseInt(limit) || 50 }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/service-desk/tickets', (req, res) => {
        try {
            const { createTicket } = require('../applications/service-desk/service');
            const ticket = createTicket(req.body);
            res.status(201).json(ticket);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.post('/api/service-desk/tickets/:id/resolve', (req, res) => {
        try {
            const { resolveTicket } = require('../applications/service-desk/service');
            const ticket = resolveTicket(req.params.id, req.body.resolution || 'Resolved autonomously', req.body.agentId);
            res.json(ticket);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/service-desk/stats', (req, res) => {
        try {
            const { getServiceDeskStats } = require('../applications/service-desk/service');
            res.json(getServiceDeskStats());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Agent Swarm & Collaboration API ─────────────────────────────────────
    app.post('/api/swarm/missions', async (req, res) => {
        try {
            const { launchSwarmMission } = require('../agents/swarm');
            const mission = await launchSwarmMission(req.body);
            res.status(201).json(mission);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/swarm/missions', (req, res) => {
        try {
            const { listSwarmMissions } = require('../agents/swarm');
            res.json({ missions: listSwarmMissions({ limit: parseInt(req.query.limit) || 20 }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/swarm/missions/:id', (req, res) => {
        try {
            const { getSwarmMission } = require('../agents/swarm');
            const mission = getSwarmMission(req.params.id);
            if (!mission) return res.status(404).json({ error: 'Mission not found' });
            res.json(mission);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Knowledge Base & Document RAG API ───────────────────────────────────
    app.post('/api/knowledge/ingest', (req, res) => {
        try {
            const { ingestDocument } = require('../knowledge/rag');
            const doc = ingestDocument(req.body);
            res.status(201).json(doc);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/knowledge/query', (req, res) => {
        try {
            const { queryKnowledge } = require('../knowledge/rag');
            const results = queryKnowledge(req.query.q || '', { limit: parseInt(req.query.limit) || 5, docType: req.query.docType });
            res.json(results);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/knowledge/stats', (req, res) => {
        try {
            const { getKnowledgeStats } = require('../knowledge/rag');
            res.json(getKnowledgeStats());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Telemetry & Observability API ───────────────────────────────────────
    app.get('/api/observability/metrics', (req, res) => {
        try {
            const { getSystemMetrics } = require('../observability/metrics');
            res.json(getSystemMetrics());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Custom Apps & Automation Builder API ────────────────────────────────
    app.get('/api/apps', (req, res) => {
        try {
            const { listApps } = require('../applications/app-builder/service');
            res.json({ apps: listApps({ category: req.query.category }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/apps', (req, res) => {
        try {
            const { createApp } = require('../applications/app-builder/service');
            const appItem = createApp(req.body);
            res.status(201).json(appItem);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/apps/:id', (req, res) => {
        try {
            const { getApp } = require('../applications/app-builder/service');
            const appItem = getApp(req.params.id);
            if (!appItem) return res.status(404).json({ error: 'App not found' });
            res.json(appItem);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/apps/:id/records', (req, res) => {
        try {
            const { submitRecord } = require('../applications/app-builder/service');
            const record = submitRecord(req.params.id, req.body);
            res.status(201).json(record);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/apps/:id/records', (req, res) => {
        try {
            const { getAppRecords } = require('../applications/app-builder/service');
            res.json({ records: getAppRecords(req.params.id, { limit: parseInt(req.query.limit) || 50 }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── OMNIVANTA OMEGA v31 ENTERPRISE OS APIS ──────────────────────────────
    
    // Truth Model & Evidence
    app.get('/api/omega/truth', (req, res) => {
        try {
            const { getTruthSummary } = require('../omega/truth_model');
            res.json(getTruthSummary());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/omega/evidence', (req, res) => {
        try {
            const { listEvidence } = require('../omega/truth_model');
            const { environment, verification_status, trace_id, limit } = req.query;
            res.json({ evidence: listEvidence({ environment, verification_status, trace_id, limit: parseInt(limit) || 50 }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Immutable Transaction Ledger
    app.get('/api/omega/ledger', (req, res) => {
        try {
            const { listTransactions } = require('../omega/ledger');
            const { tx_type, actor_id, limit } = req.query;
            res.json({ transactions: listTransactions({ tx_type, actor_id, limit: parseInt(limit) || 50 }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/omega/ledger/verify', (req, res) => {
        try {
            const { verifyLedgerIntegrity } = require('../omega/ledger');
            res.json(verifyLedgerIntegrity());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Identity & Authorizations
    app.get('/api/omega/identities', (req, res) => {
        try {
            const { listAgentIdentities } = require('../omega/identity');
            res.json({ identities: listAgentIdentities() });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.get('/api/omega/authorizations', (req, res) => {
        try {
            const { listPendingAuthorizations } = require('../omega/identity');
            res.json({ pendingAuthorizations: listPendingAuthorizations() });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/omega/authorizations/:id/resolve', (req, res) => {
        try {
            const { resolveAuthorization } = require('../omega/identity');
            const auth = resolveAuthorization(req.params.id, req.body.decision || 'APPROVE', { approved_by: req.body.approved_by, reason: req.body.reason });
            res.json(auth);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // Omega 9-Stage Action Engine
    app.post('/api/omega/action', async (req, res) => {
        try {
            const { processAction } = require('../omega/action_engine');
            const result = await processAction(req.body);
            res.json(result);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // Swarm 2.0 Missions
    app.post('/api/omega/missions', async (req, res) => {
        try {
            const { executeOmegaMission } = require('../agents/swarm2');
            const mission = await executeOmegaMission(req.body);
            res.status(201).json(mission);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.get('/api/omega/missions', (req, res) => {
        try {
            const { listOmegaMissions } = require('../agents/swarm2');
            res.json({ missions: listOmegaMissions({ limit: parseInt(req.query.limit) || 20 }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Self-Healing & Failure Incidents
    app.get('/api/omega/incidents', (req, res) => {
        try {
            const { listIncidents } = require('../omega/self_healing');
            res.json({ incidents: listIncidents({ limit: parseInt(req.query.limit) || 50 }) });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Memory 2.0 & Epistemic Trust
    app.get('/api/omega/memory2', (req, res) => {
        try {
            const { queryTrustedMemory, getMemory2Stats } = require('../knowledge/memory2');
            if (req.query.stats === 'true') return res.json(getMemory2Stats());
            const { q, domain, epistemic_type, limit } = req.query;
            res.json(queryTrustedMemory(q, { domain, epistemic_type, limit: parseInt(limit) || 20 }));
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Certified Connectors
    app.get('/api/omega/connectors', (req, res) => {
        try {
            const { listCertifiedConnectors } = require('../integrations/connector_cert');
            res.json({ connectors: listCertifiedConnectors() });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Adversarial Red Team Security
    app.post('/api/omega/red-team', async (req, res) => {
        try {
            const { runRedTeamAudit } = require('../security/red_team');
            const audit = await runRedTeamAudit();
            res.json(audit);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Disaster Recovery
    app.post('/api/omega/disaster-recovery/restore-test', async (req, res) => {
        try {
            const { runRestoreVerificationTest } = require('../omega/disaster_recovery');
            const testResult = await runRestoreVerificationTest();
            res.json(testResult);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Daily Operations Loop
    app.post('/api/omega/daily-loop', async (req, res) => {
        try {
            const { runDailyLoop } = require('../omega/daily_loop');
            const result = await runDailyLoop();
            res.json(result);
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Natural Language Command Compiler
    app.post('/api/omega/command', async (req, res) => {
        try {
            const { processNaturalLanguageCommand } = require('../omega/daily_loop');
            const result = await processNaturalLanguageCommand(req.body.command);
            res.json(result);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // Multi-Dimensional Omega Enterprise Score
    app.get('/api/omega/score', (req, res) => {
        try {
            const { calculateOmegaScore } = require('../omega/self_improvement');
            res.json(calculateOmegaScore());
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // Self-Improvement Proposals
    app.get('/api/omega/proposals', async (req, res) => {
        try {
            const { generateSelfImprovementProposals } = require('../omega/self_improvement');
            const proposals = await generateSelfImprovementProposals();
            res.json({ proposals });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // App Factory Self-Testing Harness
    app.post('/api/apps/:id/test', async (req, res) => {
        try {
            const { testGeneratedApp } = require('../applications/app-builder/app_tester');
            const result = await testGeneratedApp(req.params.id);
            res.json(result);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    // ─── Webhook & Event Dispatcher ──────────────────────────────────────────
    app.get('/api/webhooks/subscriptions', (req, res) => {
        try {
            const { listWebhookSubscriptions } = require('../integrations/webhook_engine');
            res.json({ subscriptions: listWebhookSubscriptions() });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    app.post('/api/webhooks/subscriptions', (req, res) => {
        try {
            const { registerWebhookSubscription } = require('../integrations/webhook_engine');
            const sub = registerWebhookSubscription(req.body);
            res.status(201).json(sub);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.post('/api/webhooks/incoming/:source', (req, res) => {
        try {
            const { processIncomingWebhook } = require('../integrations/webhook_engine');
            const result = processIncomingWebhook(req.params.source, req.body, req.headers['x-hub-signature-256']);
            res.status(200).json(result);
        } catch (e) { res.status(400).json({ error: e.message }); }
    });

    app.post('/api/webhooks/dispatch-test', async (req, res) => {
        try {
            const { dispatchWebhookEvent } = require('../integrations/webhook_engine');
            const results = await dispatchWebhookEvent(req.body.eventType || 'test.event', req.body.payload || { message: 'Test Ping' });
            res.json({ dispatched: results });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    // ─── Dashboard Aggregate API ─────────────────────────────────────────────
    app.get('/api/dashboard', (req, res) => {
        try {
            const agentStats = agentRegistry.getAgentStats();
            const workflowStats = workflowEngine.getWorkflowStats();
            const ontologyStats = ontology.getOntologyStats();
            const connectorStats = connectorRegistry.getConnectorStats();
            res.json({ agents: agentStats, workflows: workflowStats, ontology: ontologyStats, connectors: connectorStats });
        } catch (e) { res.status(500).json({ error: e.message }); }
    });

    return app;
}

/**
 * Start the server. Call this after all modules are initialized.
 */
function startServer(registeredModules) {
    agentRegistry = registeredModules.agentRegistry;
    workflowEngine = registeredModules.workflowEngine;
    ontology = registeredModules.ontology;
    connectorRegistry = registeredModules.connectorRegistry;

    const app = createServer();
    const server = app.listen(config.port, () => {
        log.info(`Omnivanta API server running on http://localhost:${config.port}`);
        log.info(`Control Tower UI: http://localhost:${config.port}/`);
    });

    return server;
}

module.exports = { createServer, startServer };
