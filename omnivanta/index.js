/**
 * OMNIVANTA — Main Entry Point
 * 
 * Initializes the database, registers all modules, seeds demo data,
 * and starts the API server.
 * 
 * Usage: node index.js
 */

const { config, createLogger, registerModule } = require('./platform/core');
const { initDb, closeDb } = require('./platform/db');
const agentRegistry = require('./agents/registry');
const workflowEngine = require('./workflows/engine');
const ontology = require('./context/ontology');
const connectorRegistry = require('./integrations/connector');
const { startServer } = require('./platform/server');

const log = createLogger('main');

async function main() {
    log.info('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    log.info('  OMNIVANTA AI PLATFORM — Starting...');
    log.info('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    // Phase 1: Initialize database
    log.info('Phase 1: Initializing SQLite database...');
    initDb();

    // Phase 2: Register modules
    log.info('Phase 2: Registering platform modules...');
    registerModule('agentRegistry', agentRegistry);
    registerModule('workflowEngine', workflowEngine);
    registerModule('ontology', ontology);
    registerModule('connectorRegistry', connectorRegistry);

    // Phase 3: Seed demo data if database is empty
    log.info('Phase 3: Checking for seed data...');
    const agentStats = agentRegistry.getAgentStats();
    if (agentStats.total === 0) {
        log.info('Empty database detected — seeding demo data...');
        seedDemoData();
    } else {
        log.info(`Database already contains ${agentStats.total} agents — skipping seed.`);
    }

    // Phase 4: Start API server
    log.info('Phase 4: Starting API server...');
    const server = startServer({ agentRegistry, workflowEngine, ontology, connectorRegistry });

    // Graceful shutdown
    process.on('SIGINT', () => {
        log.info('Shutting down...');
        server.close();
        closeDb();
        process.exit(0);
    });

    process.on('SIGTERM', () => {
        log.info('Shutting down...');
        server.close();
        closeDb();
        process.exit(0);
    });
}

function seedDemoData() {
    const orgId = 'org-default';

    // Create agents
    const researchAgent = agentRegistry.createAgent({
        orgId, name: 'Research Agent', description: 'Finds and synthesizes information from multiple sources',
        model: 'gemini-2.5-pro', autonomyLevel: 1, tools: ['web_search', 'browser', 'filesystem'],
        knowledge: ['company_data', 'market_intelligence'], permissions: ['read'], owner: 'system', riskClass: 'low',
    });

    const analystAgent = agentRegistry.createAgent({
        orgId, name: 'Business Analyst Agent', description: 'Analyzes business data and generates reports',
        model: 'gemini-2.5-flash', autonomyLevel: 2, tools: ['filesystem', 'database'],
        knowledge: ['financial_data', 'market_data'], permissions: ['read', 'write_reports'], owner: 'system', riskClass: 'low',
    });

    const salesAgent = agentRegistry.createAgent({
        orgId, name: 'Sales Intelligence Agent', description: 'Researches prospects and generates outreach recommendations',
        model: 'gemini-2.5-pro', autonomyLevel: 1, tools: ['web_search', 'browser'],
        knowledge: ['crm_data', 'company_profiles'], permissions: ['read'], owner: 'system', riskClass: 'medium',
    });

    const opsAgent = agentRegistry.createAgent({
        orgId, name: 'Operations Agent', description: 'Executes pre-approved operational workflows',
        model: 'gemini-2.5-flash', autonomyLevel: 3, tools: ['filesystem', 'database', 'email'],
        knowledge: ['sops', 'runbooks'], permissions: ['read', 'execute_workflow'], owner: 'system', riskClass: 'medium',
    });

    const securityAgent = agentRegistry.createAgent({
        orgId, name: 'Security Monitor Agent', description: 'Monitors for security events and anomalies',
        model: 'gemini-2.5-flash', autonomyLevel: 0, tools: ['log_reader', 'alert_system'],
        knowledge: ['security_policies'], permissions: ['read', 'alert'], owner: 'system', riskClass: 'high',
    });

    // Activate agents
    [researchAgent, analystAgent, salesAgent, opsAgent, securityAgent].forEach(a => {
        agentRegistry.updateAgent(a.id, { status: 'active' });
    });

    // Create a workflow
    workflowEngine.createWorkflow({
        orgId, name: 'Company Research Pipeline',
        description: 'Research a target company, analyze its profile, and generate a report',
        triggerType: 'manual',
        steps: [
            { name: 'Research Company', agentId: researchAgent.id, action: 'research', input: { query: 'company profile' }, timeout: 60 },
            { name: 'Analyze Data', agentId: analystAgent.id, action: 'analyze', input: { type: 'company_profile' }, timeout: 30 },
            { name: 'Generate Report', agentId: analystAgent.id, action: 'report', input: { format: 'executive_summary' }, timeout: 30 },
        ],
        owner: 'system', slaSeconds: 300,
    });

    workflowEngine.createWorkflow({
        orgId, name: 'Sales Prospect Qualification',
        description: 'Research a prospect, score them, and recommend outreach strategy',
        triggerType: 'manual',
        steps: [
            { name: 'Research Prospect', agentId: salesAgent.id, action: 'research', input: { query: 'prospect profile' }, timeout: 60 },
            { name: 'Score Prospect', agentId: analystAgent.id, action: 'score', input: { criteria: 'qualification_matrix' }, timeout: 30 },
        ],
        owner: 'system', slaSeconds: 180,
    });

    // Create ontology entities
    const customer1 = ontology.createCustomer({
        orgId, name: 'Acme Corporation', industry: 'Technology', size: 'Enterprise', healthScore: 85,
    });

    const account1 = ontology.createAccount({
        customerId: customer1.id, name: 'Acme Corp - Enterprise License', type: 'enterprise', status: 'active',
    });

    const product1 = ontology.createProduct({
        orgId, name: 'Omnivanta Control Tower', description: 'Enterprise command center for AI operations',
        category: 'platform', price: 50000, status: 'active',
    });

    const product2 = ontology.createProduct({
        orgId, name: 'Omnivanta Agent Cloud', description: 'Deploy and manage specialized AI agents',
        category: 'ai', price: 25000, status: 'active',
    });

    ontology.createContract({
        accountId: account1.id, productId: product1.id,
        startDate: '2026-01-01', endDate: '2026-12-31', value: 50000, status: 'active',
        terms: 'Annual enterprise license with SLA',
    });

    // Create connectors
    connectorRegistry.createConnector({ orgId, name: 'Local Filesystem', type: 'filesystem', config: { basePath: config.root } });
    connectorRegistry.createConnector({ orgId, name: 'Web Search', type: 'web_search', config: { provider: 'google' } });
    connectorRegistry.createConnector({ orgId, name: 'Browser Automation', type: 'browser', config: { headless: true } });

    log.info('Demo data seeded: 5 agents, 2 workflows, 1 customer, 2 products, 1 contract, 3 connectors');
}

main().catch(err => {
    log.error('Failed to start Omnivanta', { error: err.message });
    process.exit(1);
});
