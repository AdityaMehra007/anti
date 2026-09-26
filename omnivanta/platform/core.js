/**
 * OMNIVANTA PLATFORM CORE
 * 
 * Central module providing: configuration, module registry, event bus, and structured logging.
 * Every other Omnivanta module imports from this file.
 */

const { EventEmitter } = require('events');
const path = require('path');
const fs = require('fs');

// ─── Configuration ───────────────────────────────────────────────────────────

const OMNIVANTA_ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.join(OMNIVANTA_ROOT, 'data');
const DB_PATH = path.join(DATA_DIR, 'omnivanta.db');

const config = Object.freeze({
    name: 'OMNIVANTA',
    version: '1.0.0',
    description: 'AI-Native Enterprise Operating Platform',
    root: OMNIVANTA_ROOT,
    dataDir: DATA_DIR,
    dbPath: DB_PATH,
    port: parseInt(process.env.OMNIVANTA_PORT || '3000', 10),
    logLevel: process.env.OMNIVANTA_LOG_LEVEL || 'info',
    autonomyLevels: {
        0: 'OBSERVE',
        1: 'RECOMMEND',
        2: 'REVERSIBLE_ACTION',
        3: 'PRE_APPROVED_WORKFLOW',
        4: 'APPROVAL_REQUIRED',
        5: 'RESTRICTED',
    },
});

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// ─── Structured Logger ───────────────────────────────────────────────────────

const LOG_LEVELS = { error: 0, warn: 1, info: 2, debug: 3 };
const currentLogLevel = LOG_LEVELS[config.logLevel] ?? 2;

function createLogger(moduleName) {
    const log = (level, message, data = {}) => {
        if (LOG_LEVELS[level] > currentLogLevel) return;
        const entry = {
            ts: new Date().toISOString(),
            level,
            module: moduleName,
            msg: message,
            ...data,
        };
        const prefix = {
            error: '❌',
            warn: '⚠️',
            info: '→',
            debug: '🔍',
        }[level] || '→';

        console.log(`${prefix} [${moduleName}] ${message}`, Object.keys(data).length ? data : '');
    };

    return {
        error: (msg, data) => log('error', msg, data),
        warn: (msg, data) => log('warn', msg, data),
        info: (msg, data) => log('info', msg, data),
        debug: (msg, data) => log('debug', msg, data),
    };
}

// ─── Event Bus ───────────────────────────────────────────────────────────────

const eventBus = new EventEmitter();
eventBus.setMaxListeners(100);

// ─── Module Registry ─────────────────────────────────────────────────────────

const modules = new Map();

function registerModule(name, instance) {
    if (modules.has(name)) {
        throw new Error(`Module "${name}" is already registered`);
    }
    modules.set(name, instance);
    eventBus.emit('module:registered', { name, timestamp: new Date().toISOString() });
}

function getModule(name) {
    const mod = modules.get(name);
    if (!mod) throw new Error(`Module "${name}" is not registered`);
    return mod;
}

function listModules() {
    return Array.from(modules.keys());
}

// ─── Audit Logger ────────────────────────────────────────────────────────────
// Lightweight in-memory audit buffer that the DB module will persist

const auditBuffer = [];

function recordAudit(entry) {
    const record = {
        id: require('uuid').v4(),
        timestamp: new Date().toISOString(),
        actor: entry.actor || 'system',
        action: entry.action,
        resource_type: entry.resourceType || null,
        resource_id: entry.resourceId || null,
        details: typeof entry.details === 'string' ? entry.details : JSON.stringify(entry.details || {}),
        outcome: entry.outcome || 'success',
    };
    auditBuffer.push(record);
    eventBus.emit('audit:created', record);
    return record;
}

function drainAuditBuffer() {
    return auditBuffer.splice(0, auditBuffer.length);
}

// ─── Exports ─────────────────────────────────────────────────────────────────

module.exports = {
    config,
    createLogger,
    eventBus,
    registerModule,
    getModule,
    listModules,
    recordAudit,
    drainAuditBuffer,
};
