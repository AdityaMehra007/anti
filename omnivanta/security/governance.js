/**
 * OMNIVANTA — Security & AI Governance Engine
 * 
 * Enforces Autonomy Levels (0: Observe -> 5: Restricted), prompt safety auditing,
 * risk classification checks, and action permission gates.
 * @module security/governance
 */

const { createLogger, recordAudit } = require('../platform/core');

const log = createLogger('governance');

const AUTONOMY_POLICY = {
    0: { name: 'OBSERVE', allowedActions: ['read', 'query', 'log'] },
    1: { name: 'RECOMMEND', allowedActions: ['read', 'query', 'log', 'propose'] },
    2: { name: 'REVERSIBLE_ACTION', allowedActions: ['read', 'query', 'log', 'propose', 'write_local', 'update_draft'] },
    3: { name: 'PRE_APPROVED_WORKFLOW', allowedActions: ['read', 'query', 'log', 'propose', 'write_local', 'update_draft', 'execute_approved'] },
    4: { name: 'APPROVAL_REQUIRED', allowedActions: ['read', 'query', 'log', 'propose', 'write_local', 'update_draft', 'execute_approved', 'request_escalation'] },
    5: { name: 'RESTRICTED', allowedActions: ['read', 'query'] }
};

const DANGEROUS_PATTERNS = [
    /drop\s+table/i,
    /delete\s+from\s+users/i,
    /rm\s+-rf\s+\//i,
    /ignore\s+previous\s+instructions/i,
    /bypass\s+security/i
];

/**
 * Audit input prompt for prompt injection or dangerous patterns.
 */
function auditPrompt(promptText) {
    if (!promptText || typeof promptText !== 'string') return { safe: true, riskScore: 0 };
    
    for (const pattern of DANGEROUS_PATTERNS) {
        if (pattern.test(promptText)) {
            log.warn(`Security alert: Dangerous prompt pattern detected matching ${pattern}`);
            recordAudit({ actor: 'system', action: 'security.prompt_flagged', outcome: 'blocked', details: { pattern: pattern.toString() } });
            return { safe: false, riskScore: 0.95, reason: `Pattern match: ${pattern}` };
        }
    }

    return { safe: true, riskScore: 0.05 };
}

/**
 * Validate whether an agent with a given autonomy level can execute a target action.
 */
function authorizeAction(autonomyLevel, requestedAction) {
    const policy = AUTONOMY_POLICY[autonomyLevel] || AUTONOMY_POLICY[0];
    const isAllowed = policy.allowedActions.includes(requestedAction);

    recordAudit({
        actor: 'governance',
        action: 'security.action_authorized',
        outcome: isAllowed ? 'allowed' : 'denied',
        details: { autonomyLevel, requestedAction, policyName: policy.name }
    });

    return {
        authorized: isAllowed,
        autonomyLevel,
        policyName: policy.name,
        action: requestedAction
    };
}

module.exports = { auditPrompt, authorizeAction, AUTONOMY_POLICY };
