/**
 * OMNIVANTA — Clean Fast Launcher
 */
const { initDb } = require('./platform/db');
const { registerModule } = require('./platform/core');
const agentRegistry = require('./agents/registry');
const workflowEngine = require('./workflows/engine');
const ontology = require('./context/ontology');
const connectorRegistry = require('./integrations/connector');
const { startServer } = require('./platform/server');

initDb();
try { registerModule('agentRegistry', agentRegistry); } catch (e) {}
try { registerModule('workflowEngine', workflowEngine); } catch (e) {}
try { registerModule('ontology', ontology); } catch (e) {}
try { registerModule('connectorRegistry', connectorRegistry); } catch (e) {}

const server = startServer({ agentRegistry, workflowEngine, ontology, connectorRegistry });
console.log('OMNIVANTA_SERVER_READY_ON_PORT_3000');
