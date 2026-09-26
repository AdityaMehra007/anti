/**
 * OMNIVANTA — Context Engine / Ontology
 * 
 * Relational ontology layer: CUSTOMER → ACCOUNT → PRODUCT → CONTRACT → OUTCOME
 * Uses better-sqlite3 (synchronous API).
 * @module context/ontology
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('ontology');

// ─── Customers ───────────────────────────────────────────────────────────────

function createCustomer({ orgId = 'org-default', name, industry, size, healthScore }) {
    const db = getDb();
    const id = uuid();
    db.prepare('INSERT INTO customers (id, org_id, name, industry, size, health_score) VALUES (?, ?, ?, ?, ?, ?)').run(id, orgId, name, industry || null, size || null, healthScore || null);
    recordAudit({ actor: 'system', action: 'customer.created', resourceType: 'customer', resourceId: id });
    log.info('Created customer: ' + name);
    return db.prepare('SELECT * FROM customers WHERE id = ?').get(id);
}

function getCustomer(id) {
    return getDb().prepare('SELECT * FROM customers WHERE id = ?').get(id) || null;
}

function listCustomers({ orgId, industry, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conds = []; const params = [];
    if (orgId) { conds.push('org_id = ?'); params.push(orgId); }
    if (industry) { conds.push('industry = ?'); params.push(industry); }
    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM customers ' + where).get(...params).count;
    const customers = db.prepare('SELECT * FROM customers ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);
    return { customers, total };
}

function updateCustomer(id, updates) {
    const db = getDb();
    const fields = { name: 'name', industry: 'industry', size: 'size', healthScore: 'health_score' };
    const set = []; const params = [];
    for (const [js, col] of Object.entries(fields)) {
        if (updates[js] !== undefined) { set.push(col + ' = ?'); params.push(updates[js]); }
    }
    if (set.length === 0) return getCustomer(id);
    params.push(id);
    db.prepare('UPDATE customers SET ' + set.join(', ') + ' WHERE id = ?').run(...params);
    recordAudit({ actor: 'system', action: 'customer.updated', resourceType: 'customer', resourceId: id });
    return getCustomer(id);
}

// ─── Accounts ────────────────────────────────────────────────────────────────

function createAccount({ customerId, name, type, status = 'active' }) {
    const db = getDb();
    const id = uuid();
    db.prepare('INSERT INTO accounts (id, customer_id, name, type, status) VALUES (?, ?, ?, ?, ?)').run(id, customerId, name, type || null, status);
    recordAudit({ actor: 'system', action: 'account.created', resourceType: 'account', resourceId: id });
    return db.prepare('SELECT * FROM accounts WHERE id = ?').get(id);
}

function getAccount(id) {
    return getDb().prepare('SELECT * FROM accounts WHERE id = ?').get(id) || null;
}

function listAccounts({ customerId, status, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conds = []; const params = [];
    if (customerId) { conds.push('customer_id = ?'); params.push(customerId); }
    if (status) { conds.push('status = ?'); params.push(status); }
    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM accounts ' + where).get(...params).count;
    const accounts = db.prepare('SELECT * FROM accounts ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);
    return { accounts, total };
}

// ─── Products ────────────────────────────────────────────────────────────────

function createProduct({ orgId = 'org-default', name, description, category, price, status = 'active' }) {
    const db = getDb();
    const id = uuid();
    db.prepare('INSERT INTO products (id, org_id, name, description, category, price, status) VALUES (?, ?, ?, ?, ?, ?, ?)').run(id, orgId, name, description || '', category || null, price || null, status);
    recordAudit({ actor: 'system', action: 'product.created', resourceType: 'product', resourceId: id });
    return db.prepare('SELECT * FROM products WHERE id = ?').get(id);
}

function getProduct(id) {
    return getDb().prepare('SELECT * FROM products WHERE id = ?').get(id) || null;
}

function listProducts({ orgId, category, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conds = []; const params = [];
    if (orgId) { conds.push('org_id = ?'); params.push(orgId); }
    if (category) { conds.push('category = ?'); params.push(category); }
    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM products ' + where).get(...params).count;
    const products = db.prepare('SELECT * FROM products ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);
    return { products, total };
}

// ─── Contracts ───────────────────────────────────────────────────────────────

function createContract({ accountId, productId, startDate, endDate, value, status = 'active', terms }) {
    const db = getDb();
    const id = uuid();
    db.prepare('INSERT INTO contracts (id, account_id, product_id, start_date, end_date, value, status, terms) VALUES (?, ?, ?, ?, ?, ?, ?, ?)').run(id, accountId, productId, startDate || null, endDate || null, value || null, status, terms || null);
    recordAudit({ actor: 'system', action: 'contract.created', resourceType: 'contract', resourceId: id });
    return db.prepare('SELECT * FROM contracts WHERE id = ?').get(id);
}

function getContract(id) {
    return getDb().prepare('SELECT * FROM contracts WHERE id = ?').get(id) || null;
}

function listContracts({ accountId, productId, status, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conds = []; const params = [];
    if (accountId) { conds.push('account_id = ?'); params.push(accountId); }
    if (productId) { conds.push('product_id = ?'); params.push(productId); }
    if (status) { conds.push('status = ?'); params.push(status); }
    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM contracts ' + where).get(...params).count;
    const contracts = db.prepare('SELECT * FROM contracts ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);
    return { contracts, total };
}

// ─── Outcomes ────────────────────────────────────────────────────────────────

function createOutcome({ taskId, agentId, result, evidence, metrics, verified = 0 }) {
    const db = getDb();
    const id = uuid();
    db.prepare('INSERT INTO outcomes (id, task_id, agent_id, result, evidence, metrics, verified) VALUES (?, ?, ?, ?, ?, ?, ?)').run(id, taskId || null, agentId || null, JSON.stringify(result || null), JSON.stringify(evidence || null), JSON.stringify(metrics || null), verified ? 1 : 0);
    recordAudit({ actor: 'system', action: 'outcome.created', resourceType: 'outcome', resourceId: id });
    return db.prepare('SELECT * FROM outcomes WHERE id = ?').get(id);
}

function getOutcome(id) {
    return getDb().prepare('SELECT * FROM outcomes WHERE id = ?').get(id) || null;
}

function listOutcomes({ taskId, agentId, verified, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conds = []; const params = [];
    if (taskId) { conds.push('task_id = ?'); params.push(taskId); }
    if (agentId) { conds.push('agent_id = ?'); params.push(agentId); }
    if (verified !== undefined) { conds.push('verified = ?'); params.push(verified ? 1 : 0); }
    const where = conds.length > 0 ? 'WHERE ' + conds.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM outcomes ' + where).get(...params).count;
    const outcomes = db.prepare('SELECT * FROM outcomes ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);
    return { outcomes, total };
}

// ─── Graph Traversal ─────────────────────────────────────────────────────────

function getCustomerGraph(customerId) {
    const customer = getCustomer(customerId);
    if (!customer) return null;

    const accounts = getDb().prepare('SELECT * FROM accounts WHERE customer_id = ?').all(customerId);
    for (const account of accounts) {
        account.contracts = getDb().prepare('SELECT * FROM contracts WHERE account_id = ?').all(account.id);
        for (const contract of account.contracts) {
            contract.product = getProduct(contract.product_id);
        }
    }

    return { customer, accounts };
}

// ─── Stats ───────────────────────────────────────────────────────────────────

function getOntologyStats(orgId) {
    const db = getDb();
    const customers = db.prepare('SELECT COUNT(*) as count FROM customers').get().count;
    const accounts = db.prepare('SELECT COUNT(*) as count FROM accounts').get().count;
    const products = db.prepare('SELECT COUNT(*) as count FROM products').get().count;
    const contracts = db.prepare('SELECT COUNT(*) as count FROM contracts').get().count;
    const outcomes = db.prepare('SELECT COUNT(*) as count FROM outcomes').get().count;
    return { customers, accounts, products, contracts, outcomes };
}

module.exports = {
    createCustomer, getCustomer, listCustomers, updateCustomer,
    createAccount, getAccount, listAccounts,
    createProduct, getProduct, listProducts,
    createContract, getContract, listContracts,
    createOutcome, getOutcome, listOutcomes,
    getCustomerGraph, getOntologyStats,
};
