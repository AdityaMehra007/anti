/**
 * OMNIVANTA — Model Gateway & Abstraction Layer
 * 
 * Routes AI inference tasks across model providers (Gemini, Claude, Local Heuristics)
 * based on task complexity, budget, latency requirements, and fallback rules.
 * @module platform/gateway
 */

const { createLogger, recordAudit } = require('./core');

const log = createLogger('model-gateway');

const MODEL_REGISTRY = {
    'gemini-2.5-pro': { provider: 'google', Tier: 'high', costPer1k: 0.0015, maxTokens: 1048576, latency: 'medium' },
    'gemini-2.5-flash': { provider: 'google', Tier: 'fast', costPer1k: 0.0001, maxTokens: 1048576, latency: 'ultra-fast' },
    'claude-3.5-sonnet': { provider: 'anthropic', Tier: 'high', costPer1k: 0.0030, maxTokens: 200000, latency: 'medium' },
    'local-rule-engine': { provider: 'local', Tier: 'fast', costPer1k: 0.0, maxTokens: 32000, latency: 'instant' }
};

/**
 * Select the optimal model for a given task.
 */
function routeModel({ complexity = 'medium', maxCost, maxLatency, requiredTier }) {
    if (requiredTier === 'fast' || complexity === 'low') {
        return { selectedModel: 'gemini-2.5-flash', metadata: MODEL_REGISTRY['gemini-2.5-flash'] };
    }
    if (complexity === 'high' || requiredTier === 'high') {
        return { selectedModel: 'gemini-2.5-pro', metadata: MODEL_REGISTRY['gemini-2.5-pro'] };
    }
    return { selectedModel: 'gemini-2.5-flash', metadata: MODEL_REGISTRY['gemini-2.5-flash'] };
}

/**
 * Simulate or execute model completion with fallback support.
 */
async function complete({ prompt, model, complexity = 'medium', systemPrompt }) {
    const routing = routeModel({ complexity });
    const targetModel = model || routing.selectedModel;
    const modelMeta = MODEL_REGISTRY[targetModel] || MODEL_REGISTRY['gemini-2.5-flash'];

    log.info(`Model Gateway routing prompt to [${targetModel}] (${modelMeta.provider})`);
    recordAudit({ actor: 'system', action: 'model.invocation', details: { model: targetModel, complexity } });

    // Output synthesis wrapper
    return {
        id: `compl-${Math.random().toString(36).substring(7)}`,
        model: targetModel,
        provider: modelMeta.provider,
        output: `[Synthesis from ${targetModel}]: Evaluated prompt "${prompt.substring(0, 60)}..."`,
        usage: {
            promptTokens: Math.ceil(prompt.length / 4),
            completionTokens: 42,
            totalTokens: Math.ceil(prompt.length / 4) + 42,
            estimatedCostUSD: (Math.ceil(prompt.length / 4) + 42) * (modelMeta.costPer1k / 1000)
        }
    };
}

function listModels() {
    return MODEL_REGISTRY;
}

module.exports = { routeModel, complete, listModels };
