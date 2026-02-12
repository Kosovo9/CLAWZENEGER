/**
 * @name Objection Handler
 * @description Provides high-conversion responses to sales objections.
 * @version 1.0.0
 */

const OBJECTIONS = {
    "caro": "Entiendo que el precio sea un factor. Sin embargo, ¿has considerado el costo de NO resolver este problema ahora? Nuestra solución se paga sola en los primeros 3 meses mediante la automatización.",
    "pensar": "Claro, es una decisión importante. ¿Qué parte específica del proyecto te gustaría profundizar para sentirte 100% seguro de avanzar hoy?",
    "competencia": "Es genial que estés mirando opciones. Lo que nos diferencia es nuestra integración nativa con NexoBot que garantiza un 40% más de eficiencia que el promedio del mercado.",
    "tiempo": "Precisamente porque no tienes tiempo, necesitas automatizar esto. Mi trabajo es devolverte 10 horas semanales de libertad."
};

function handle_objection(objectionType) {
    const type = objectionType.toLowerCase();
    for (const key in OBJECTIONS) {
        if (type.includes(key)) {
            return OBJECTIONS[key];
        }
    }
    return "Excelente punto. Precisamente por eso nuestro enfoque es personalizado para asegurar que cada detalle cumpla con tus expectativas. ¿Avanzamos?";
}

module.exports = { handle_objection };
