/**
 * OMNIVANTA — Workflow Engine
 * 
 * Real workflow execution engine with state machine, task queue, and audit trail.
 * Uses better-sqlite3 (synchronous API).
 * @module workflows/engine
 */

const { createLogger, eventBus, recordAudit } = require('../platform/core');
const { getDb } = require('../platform/db');
const { v4: uuid } = require('uuid');

const log = createLogger('workflow-engine');

// ─── Valid state transitions ─────────────────────────────────────────────────
const VALID_TRANSITIONS = {
    pending: ['running', 'cancelled'],
    running: ['completed', 'failed'],
    failed: ['pending'], // retry
};

/** Parse JSON fields from a workflow row */
function parseWorkflow(row) {
    if (!row) return null;
    return {
        ...row,
        steps: JSON.parse(row.steps || '[]'),
        trigger_config: JSON.parse(row.trigger_config || '{}'),
        retry_policy: JSON.parse(row.retry_policy || '{"maxRetries":3}'),
    };
}

/** Parse JSON fields from a task row */
function parseTask(row) {
    if (!row) return null;
    return {
        ...row,
        input: JSON.parse(row.input || '{}'),
        output: JSON.parse(row.output || 'null'),
    };
}

// ─── Workflow CRUD ───────────────────────────────────────────────────────────

function createWorkflow({ orgId = 'org-default', name, description, triggerType = 'manual', triggerConfig = {}, steps = [], owner, slaSeconds }) {
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();

    db.prepare(`
        INSERT INTO workflows (id, org_id, name, description, trigger_type, trigger_config, steps, status, owner, sla_seconds, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, ?)
    `).run(id, orgId, name, description || '', triggerType, JSON.stringify(triggerConfig), JSON.stringify(steps), owner || 'system', slaSeconds || null, now, now);

    recordAudit({ actor: owner || 'system', action: 'workflow.created', resourceType: 'workflow', resourceId: id });
    log.info('Created workflow: ' + name + ' (' + id.substring(0, 8) + ')');

    return parseWorkflow(db.prepare('SELECT * FROM workflows WHERE id = ?').get(id));
}

function getWorkflow(id) {
    return parseWorkflow(getDb().prepare('SELECT * FROM workflows WHERE id = ?').get(id));
}

function listWorkflows({ orgId, status, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conditions = [];
    const params = [];

    if (orgId) { conditions.push('org_id = ?'); params.push(orgId); }
    if (status) { conditions.push('status = ?'); params.push(status); }

    const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM workflows ' + where).get(...params).count;
    const rows = db.prepare('SELECT * FROM workflows ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);

    return { workflows: rows.map(parseWorkflow), total };
}

function updateWorkflow(id, updates) {
    const db = getDb();
    const existing = db.prepare('SELECT id FROM workflows WHERE id = ?').get(id);
    if (!existing) throw new Error('Workflow not found: ' + id);

    const fieldMap = { name: 'name', description: 'description', triggerType: 'trigger_type', status: 'status', owner: 'owner', slaSeconds: 'sla_seconds' };
    const jsonFields = { steps: 'steps', triggerConfig: 'trigger_config', retryPolicy: 'retry_policy' };
    const setClauses = [];
    const params = [];

    for (const [jsKey, dbCol] of Object.entries(fieldMap)) {
        if (updates[jsKey] !== undefined) { setClauses.push(dbCol + ' = ?'); params.push(updates[jsKey]); }
    }
    for (const [jsKey, dbCol] of Object.entries(jsonFields)) {
        if (updates[jsKey] !== undefined) { setClauses.push(dbCol + ' = ?'); params.push(JSON.stringify(updates[jsKey])); }
    }
    if (setClauses.length === 0) return getWorkflow(id);

    setClauses.push("updated_at = ?");
    params.push(new Date().toISOString());
    params.push(id);

    db.prepare('UPDATE workflows SET ' + setClauses.join(', ') + ' WHERE id = ?').run(...params);
    return getWorkflow(id);
}

// ─── Task CRUD ───────────────────────────────────────────────────────────────

function createTask({ workflowId, agentId, name, input = {}, priority = 5 }) {
    const db = getDb();
    const id = uuid();
    const now = new Date().toISOString();

    db.prepare(`
        INSERT INTO tasks (id, workflow_id, agent_id, name, input, status, priority, attempt, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', ?, 0, ?)
    `).run(id, workflowId || null, agentId || null, name, JSON.stringify(input), priority, now);

    log.info('Created task: ' + name + ' (' + id.substring(0, 8) + ')');
    return parseTask(db.prepare('SELECT * FROM tasks WHERE id = ?').get(id));
}

function getTask(id) {
    return parseTask(getDb().prepare('SELECT * FROM tasks WHERE id = ?').get(id));
}

function listTasks({ workflowId, agentId, status, limit = 50, offset = 0 } = {}) {
    const db = getDb();
    const conditions = [];
    const params = [];

    if (workflowId) { conditions.push('workflow_id = ?'); params.push(workflowId); }
    if (agentId) { conditions.push('agent_id = ?'); params.push(agentId); }
    if (status) { conditions.push('status = ?'); params.push(status); }

    const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';
    const total = db.prepare('SELECT COUNT(*) as count FROM tasks ' + where).get(...params).count;
    const rows = db.prepare('SELECT * FROM tasks ' + where + ' ORDER BY created_at DESC LIMIT ? OFFSET ?').all(...params, limit, offset);

    return { tasks: rows.map(parseTask), total };
}

/**
 * Transition a task's status with state machine validation.
 */
function transitionTask(taskId, newStatus, { output, error } = {}) {
    const db = getDb();
    const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(taskId);
    if (!task) throw new Error('Task not found: ' + taskId);

    const allowed = VALID_TRANSITIONS[task.status];
    if (!allowed || !allowed.includes(newStatus)) {
        throw new Error('Invalid transition: ' + task.status + ' → ' + newStatus);
    }

    const now = new Date().toISOString();
    const updates = { status: newStatus };

    if (newStatus === 'running') {
        updates.started_at = now;
        updates.attempt = task.attempt + 1;
    }
    if (newStatus === 'completed' || newStatus === 'failed') {
        updates.completed_at = now;
    }
    if (output !== undefined) updates.output = JSON.stringify(output);
    if (error !== undefined) updates.error = error;

    const setClauses = Object.entries(updates).map(([k]) => k + ' = ?');
    const params = Object.values(updates);
    params.push(taskId);

    db.prepare('UPDATE tasks SET ' + setClauses.join(', ') + ' WHERE id = ?').run(...params);

    eventBus.emit('task:' + newStatus, { taskId, newStatus });
    return parseTask(db.prepare('SELECT * FROM tasks WHERE id = ?').get(taskId));
}

// ─── Workflow Execution ──────────────────────────────────────────────────────

/**
 * Execute a workflow end-to-end: create tasks for each step and run them.
 */
function executeWorkflow(workflowId, { input, executedBy } = {}) {
    const workflow = getWorkflow(workflowId);
    if (!workflow) throw new Error('Workflow not found: ' + workflowId);

    const startTime = Date.now();
    log.info('Executing workflow: ' + workflow.name);

    // Set workflow to active
    updateWorkflow(workflowId, { status: 'active' });
    eventBus.emit('workflow:started', { workflowId });
    recordAudit({ actor: executedBy || 'system', action: 'workflow.executed', resourceType: 'workflow', resourceId: workflowId });

    const taskResults = [];
    let overallStatus = 'completed';

    for (const step of workflow.steps) {
        const task = createTask({
            workflowId,
            agentId: step.agentId || null,
            name: step.name,
            input: { ...step.input, workflowInput: input },
            priority: 5,
        });

        // Transition to running
        transitionTask(task.id, 'running');

        // Simulate execution (real agent execution would happen here)
        try {
            const result = {
                stepName: step.name,
                action: step.action || 'execute',
                executedAt: new Date().toISOString(),
                simulatedOutput: 'Step completed successfully',
            };
            const completedTask = transitionTask(task.id, 'completed', { output: result });
            taskResults.push(completedTask);
        } catch (err) {
            const failedTask = transitionTask(task.id, 'failed', { error: err.message });
            taskResults.push(failedTask);
            overallStatus = 'failed';
            log.error('Step failed: ' + step.name, { error: err.message });
            break;
        }
    }

    // Update workflow status
    updateWorkflow(workflowId, { status: overallStatus });
    eventBus.emit('workflow:' + overallStatus, { workflowId });

    const duration = Date.now() - startTime;
    log.info('Workflow ' + overallStatus + ' in ' + duration + 'ms');

    return {
        workflowId,
        workflowName: workflow.name,
        status: overallStatus,
        tasks: taskResults,
        duration,
        executedBy: executedBy || 'system',
    };
}

// ─── Stats ───────────────────────────────────────────────────────────────────

function getWorkflowStats(orgId) {
    const db = getDb();
    const base = orgId ? ' WHERE org_id = ?' : '';
    const p = orgId ? [orgId] : [];

    const total = db.prepare('SELECT COUNT(*) as count FROM workflows' + base).get(...p).count;
    const rows = db.prepare('SELECT status, COUNT(*) as count FROM workflows' + base + ' GROUP BY status').all(...p);

    const stats = { total, draft: 0, active: 0, completed: 0, failed: 0 };
    rows.forEach(r => { stats[r.status] = r.count; });
    return stats;
}

module.exports = {
    createWorkflow, getWorkflow, listWorkflows, updateWorkflow,
    createTask, getTask, listTasks, transitionTask,
    executeWorkflow, getWorkflowStats,
};
