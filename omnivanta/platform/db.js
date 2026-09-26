/**
 * Omnivanta SQLite Database Layer
 * @module platform/db
 */

const Database = require('better-sqlite3');
const { config, createLogger, eventBus, drainAuditBuffer } = require('./core');

const logger = createLogger('db');
let dbInstance = null;

/**
 * Initializes the database tables.
 * @param {Database} db 
 */
function createTables(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS organizations (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      org_id TEXT REFERENCES organizations(id),
      name TEXT NOT NULL,
      email TEXT,
      role TEXT DEFAULT 'member',
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS agents (
      id TEXT PRIMARY KEY,
      org_id TEXT REFERENCES organizations(id),
      name TEXT NOT NULL,
      description TEXT,
      model TEXT,
      autonomy_level INTEGER DEFAULT 0 CHECK(autonomy_level BETWEEN 0 AND 5),
      tools TEXT,
      knowledge TEXT,
      permissions TEXT,
      memory_config TEXT,
      status TEXT DEFAULT 'inactive',
      owner TEXT,
      risk_class TEXT DEFAULT 'low',
      version INTEGER DEFAULT 1,
      eval_score REAL,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS workflows (
      id TEXT PRIMARY KEY,
      org_id TEXT REFERENCES organizations(id),
      name TEXT NOT NULL,
      description TEXT,
      trigger_type TEXT,
      trigger_config TEXT,
      steps TEXT,
      status TEXT DEFAULT 'draft',
      owner TEXT,
      sla_seconds INTEGER,
      retry_policy TEXT DEFAULT '{"maxRetries":3}',
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS tasks (
      id TEXT PRIMARY KEY,
      workflow_id TEXT REFERENCES workflows(id),
      agent_id TEXT REFERENCES agents(id),
      name TEXT NOT NULL,
      input TEXT,
      output TEXT,
      status TEXT DEFAULT 'pending' CHECK(status IN ('pending','running','completed','failed','cancelled')),
      priority INTEGER DEFAULT 5,
      attempt INTEGER DEFAULT 0,
      error TEXT,
      started_at TEXT,
      completed_at TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS customers (
      id TEXT PRIMARY KEY,
      org_id TEXT REFERENCES organizations(id),
      name TEXT NOT NULL,
      industry TEXT,
      size TEXT,
      health_score REAL,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS accounts (
      id TEXT PRIMARY KEY,
      customer_id TEXT REFERENCES customers(id),
      name TEXT NOT NULL,
      type TEXT,
      status TEXT DEFAULT 'active',
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS products (
      id TEXT PRIMARY KEY,
      org_id TEXT REFERENCES organizations(id),
      name TEXT NOT NULL,
      description TEXT,
      category TEXT,
      price REAL,
      status TEXT DEFAULT 'active',
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS contracts (
      id TEXT PRIMARY KEY,
      account_id TEXT REFERENCES accounts(id),
      product_id TEXT REFERENCES products(id),
      start_date TEXT,
      end_date TEXT,
      value REAL,
      status TEXT DEFAULT 'active',
      terms TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS outcomes (
      id TEXT PRIMARY KEY,
      task_id TEXT REFERENCES tasks(id),
      agent_id TEXT REFERENCES agents(id),
      result TEXT,
      evidence TEXT,
      metrics TEXT,
      verified INTEGER DEFAULT 0,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS events (
      id TEXT PRIMARY KEY,
      type TEXT NOT NULL,
      source TEXT,
      data TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS audit_log (
      id TEXT PRIMARY KEY,
      timestamp TEXT NOT NULL,
      actor TEXT,
      action TEXT NOT NULL,
      resource_type TEXT,
      resource_id TEXT,
      details TEXT,
      outcome TEXT DEFAULT 'success'
    );

    CREATE TABLE IF NOT EXISTS connectors (
      id TEXT PRIMARY KEY,
      org_id TEXT REFERENCES organizations(id),
      name TEXT NOT NULL,
      type TEXT,
      config TEXT,
      status TEXT DEFAULT 'inactive',
      health TEXT DEFAULT 'unknown',
      last_check TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    );
  `);
}

/**
 * Gets the singleton database instance.
 * @returns {Database} The better-sqlite3 database instance
 */
function getDb() {
  if (!dbInstance) {
    throw new Error('Database not initialized. Call initDb() first.');
  }
  return dbInstance;
}

/**
 * Initializes the database connection, creates tables, and sets up pragmas/listeners.
 * @returns {Database}
 */
function initDb() {
  if (dbInstance) {
    logger.warn('Database already initialized');
    return dbInstance;
  }

  logger.info('Initializing database at ' + config.dbPath);
  
  try {
    dbInstance = new Database(config.dbPath);
    
    // Set pragmas
    dbInstance.pragma('journal_mode = WAL');
    dbInstance.pragma('foreign_keys = ON');

    // Create tables
    createTables(dbInstance);

    // Seed default organization
    const insertOrg = dbInstance.prepare(`
      INSERT INTO organizations (id, name)
      VALUES (@id, @name)
      ON CONFLICT(id) DO UPDATE SET name = excluded.name
    `);
    
    insertOrg.run({ id: 'org-default', name: 'Omnivanta' });
    logger.info('Default organization seeded successfully.');

    // Setup audit log event listener to drain buffer
    eventBus.on('audit:created', () => {
      const logs = drainAuditBuffer();
      if (logs && logs.length > 0) {
        const insertAudit = dbInstance.prepare(`
          INSERT INTO audit_log (id, timestamp, actor, action, resource_type, resource_id, details, outcome)
          VALUES (@id, @timestamp, @actor, @action, @resource_type, @resource_id, @details, @outcome)
        `);
        
        const insertMany = dbInstance.transaction((auditLogs) => {
          for (const entry of auditLogs) {
            insertAudit.run({
              id: entry.id || Math.random().toString(36).substring(7),
              timestamp: entry.timestamp || new Date().toISOString(),
              actor: entry.actor || 'system',
              action: entry.action,
              resource_type: entry.resource_type || null,
              resource_id: entry.resource_id || null,
              details: typeof entry.details === 'object' ? JSON.stringify(entry.details) : (entry.details || null),
              outcome: entry.outcome || 'success'
            });
          }
        });

        try {
          insertMany(logs);
        } catch (err) {
          logger.error('Failed to insert audit logs:', err);
        }
      }
    });

    logger.info('Database initialization complete.');
    return dbInstance;
  } catch (error) {
    logger.error('Failed to initialize database:', error);
    throw error;
  }
}

/**
 * Closes the database connection safely.
 */
function closeDb() {
  if (dbInstance) {
    dbInstance.close();
    dbInstance = null;
    logger.info('Database connection closed.');
  }
}

module.exports = {
  getDb,
  initDb,
  closeDb
};
