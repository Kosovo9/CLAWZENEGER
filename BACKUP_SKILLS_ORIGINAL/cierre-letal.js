/**
 * @name Cierre Letal
 * @description Advanced lethal closing techniques for maximum conversion.
 * @version 1.0.0
 */

const CLOSING_TECHNIQUES = [
    "Cierre de Doble Alternativa: ¿Prefieres que arranquemos la integración este lunes o el miércoles por la mañana?",
    "Cierre por Escasez: Tenemos solo 2 espacios disponibles para implementaciones este mes con el bono de configuración n8n gratuita. ¿Te aparto uno?",
    "Cierre de Suposición: Dado que los beneficios de ROI son claros, ¿a qué correo te envío el acuerdo para firma electrónica?",
    "Cierre de la Balanza: Si ponemos en un lado el ahorro de tiempo y en otro la inversión, la balanza se inclina claramente hacia la automatización. ¿Cierto?"
];

function lethal_close(strategy) {
    if (strategy === 'random') {
        return CLOSING_TECHNIQUES[Math.floor(Math.random() * CLOSING_TECHNIQUES.length)];
    }
    return CLOSING_TECHNIQUES[0];
}

module.exports = { lethal_close };
