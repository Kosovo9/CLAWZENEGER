/**
 * @name Pricing Calculator
 * @description Dynamic pricing calculator for NexoBot services.
 * @version 1.0.0
 */

function calculate_pricing(params) {
    const basePrice = 500;
    const complexityMultiplier = params.complexity === 'pro' ? 2 : 1.5;
    const agentCount = params.agents || 1;
    const supportLevel = params.support === 'priority' ? 250 : 0;

    const total = (basePrice * complexityMultiplier * agentCount) + supportLevel;

    return {
        basePrice,
        complexity: params.complexity,
        agents: agentCount,
        support: params.support,
        total: `$${total.toLocaleString()} USD`,
        summary: `Cotización de NexoBot: ${agentCount} agente(s) nivel ${params.complexity} con soporte ${params.support}. TOTAL: $${total}`
    };
}

module.exports = { calculate_pricing };
