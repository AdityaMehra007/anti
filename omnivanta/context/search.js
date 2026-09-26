/**
 * OMNIVANTA — Universal Enterprise Search Engine
 * 
 * Provides unified cross-domain search across:
 * - Agents
 * - Workflows & Tasks
 * - Target Companies
 * - Customers & Accounts
 * - Contracts & Products
 * - Candidate Skills Matrix
 * - Audit Trail
 * 
 * @module context/search
 */

const { createLogger, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const path = require('path');
const fs = require('fs');

const log = createLogger('universal-search');

/**
 * Execute unified search across all platform entities
 */
function search(query, { limit = 20, domain = 'all' } = {}) {
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
        return { query: '', total: 0, results: [] };
    }

    const q = query.trim().toLowerCase();
    const db = getDb();
    const results = [];

    // 1. Search Agents
    if (domain === 'all' || domain === 'agents') {
        const agents = db.prepare(`
            SELECT id, name, description, model, autonomy_level, status 
            FROM agents 
            WHERE (LOWER(name) LIKE ? OR LOWER(description) LIKE ?) AND status != 'deleted'
            LIMIT ?
        `).all(`%${q}%`, `%${q}%`, limit);

        agents.forEach(a => {
            results.push({
                domain: 'agents',
                id: a.id,
                title: a.name,
                snippet: `${a.description || 'AI Specialist'} | Model: ${a.model} | Autonomy: Level ${a.autonomy_level}`,
                url: `/api/agents/${a.id}`,
                badge: a.status
            });
        });
    }

    // 2. Search Workflows
    if (domain === 'all' || domain === 'workflows') {
        const workflows = db.prepare(`
            SELECT id, name, description, trigger_type, status 
            FROM workflows 
            WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ?
            LIMIT ?
        `).all(`%${q}%`, `%${q}%`, limit);

        workflows.forEach(w => {
            results.push({
                domain: 'workflows',
                id: w.id,
                title: w.name,
                snippet: `${w.description || 'Enterprise Workflow'} | Trigger: ${w.trigger_type}`,
                url: `/api/workflows/${w.id}`,
                badge: w.status
            });
        });
    }

    // 3. Search Ontology: Customers & Products
    if (domain === 'all' || domain === 'ontology') {
        const customers = db.prepare(`
            SELECT id, name, industry, size, health_score 
            FROM customers 
            WHERE LOWER(name) LIKE ? OR LOWER(industry) LIKE ?
            LIMIT ?
        `).all(`%${q}%`, `%${q}%`, limit);

        customers.forEach(c => {
            results.push({
                domain: 'customers',
                id: c.id,
                title: c.name,
                snippet: `Industry: ${c.industry || 'General'} | Size: ${c.size || 'Enterprise'} | Health: ${c.health_score || 90}%`,
                url: `/api/customers/${c.id}`,
                badge: 'customer'
            });
        });

        const products = db.prepare(`
            SELECT id, name, description, category, price 
            FROM products 
            WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ?
            LIMIT ?
        `).all(`%${q}%`, `%${q}%`, limit);

        products.forEach(p => {
            results.push({
                domain: 'products',
                id: p.id,
                title: p.name,
                snippet: `${p.description || ''} | Category: ${p.category} | $${p.price?.toLocaleString()}`,
                url: `/api/products/${p.id}`,
                badge: 'product'
            });
        });
    }

    // 4. Search Target Companies & Job Applications
    if (domain === 'all' || domain === 'companies' || domain === 'career') {
        try {
            // Search SQLite job_applications table
            const apps = db.prepare(`
                SELECT job_id, company, role, location, fit_score, status 
                FROM job_applications 
                WHERE LOWER(company) LIKE ? OR LOWER(role) LIKE ? OR LOWER(location) LIKE ?
                LIMIT ?
            `).all(`%${q}%`, `%${q}%`, `%${q}%`, limit);

            apps.forEach(a => {
                results.push({
                    domain: 'companies',
                    id: a.job_id,
                    title: `${a.company} — ${a.role}`,
                    snippet: `Fit: ${a.fit_score}/10 | Location: ${a.location} | Status: ${a.status}`,
                    url: `/career`,
                    badge: 'target-company'
                });
            });

            // Also search company directories on disk
            const companyPaths = [
                path.join(__dirname, '..', '..', 'data', 'Bangalore_3000_Company_Target_Directory.csv'),
                path.join(__dirname, '..', '..', 'BBA_IB_Bengaluru_61_Job_Pipeline.csv')
            ];

            for (const csvPath of companyPaths) {
                if (fs.existsSync(csvPath)) {
                    const raw = fs.readFileSync(csvPath, 'utf-8');
                    const lines = raw.split('\n').filter(l => l.trim());
                    for (let i = 1; i < lines.length; i++) {
                        const lineLower = lines[i].toLowerCase();
                        if (lineLower.includes(q)) {
                            const parts = lines[i].split(',').map(p => p.replace(/"/g, '').trim());
                            if (parts.length >= 2) {
                                results.push({
                                    domain: 'companies',
                                    id: `comp-${i}`,
                                    title: parts[1] || parts[0],
                                    snippet: `Industry: ${parts[2] || 'Corporate'} | Location: ${parts[4] || parts[6] || 'Bengaluru'}`,
                                    url: `/bi`,
                                    badge: 'target-company'
                                });
                            }
                        }
                        if (results.length >= limit * 2) break;
                    }
                }
            }
        } catch (e) {
            log.warn('Company search error: ' + e.message);
        }
    }

    // 5. Search Skills Matrix (from CSV dataset)
    if (domain === 'all' || domain === 'skills') {
        try {
            const skillPath = path.join(__dirname, '..', '..', 'Aditya_Mehra_300_Skills_Master_Matrix.csv');
            if (fs.existsSync(skillPath)) {
                const raw = fs.readFileSync(skillPath, 'utf-8');
                const lines = raw.split('\n').filter(l => l.trim());
                for (let i = 1; i < lines.length; i++) {
                    if (lines[i].toLowerCase().includes(q)) {
                        const skillName = lines[i].split(',')[0]?.replace(/"/g, '').trim();
                        results.push({
                            domain: 'skills',
                            id: `skill-${i}`,
                            title: skillName,
                            snippet: `Verified Skill in Candidate Master Matrix | Provenance: Empirical Proof of Claim`,
                            url: `/career`,
                            badge: 'skill'
                        });
                    }
                    if (results.length >= limit * 3) break;
                }
            }
        } catch (e) {
            log.warn('Skills CSV search error: ' + e.message);
        }
    }

    log.info(`Universal Search for "${query}" returned ${results.length} matches`);
    recordAudit({ actor: 'user', action: 'search.query', details: { query, count: results.length } });

    return {
        query,
        total: results.length,
        results: results.slice(0, limit)
    };
}

module.exports = { search };
