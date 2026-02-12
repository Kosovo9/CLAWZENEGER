module.exports = {
  name: "intent_detector_10x",
  description: "Detecta intencion de compra",
  async run(context, { mensaje }) {
    const text = (mensaje || "").toLowerCase();
    const highIntent = ["quiero", "comprar", "precio", "costo", "pago", "link", "ahora", "urgente"];
    const mediumIntent = ["como", "funciona", "sirve", "ejemplo", "demo", "planes"];
    const highScore = highIntent.filter(word => text.includes(word)).length;
    const mediumScore = mediumIntent.filter(word => text.includes(word)).length;
    let nivel = "bajo";
    let accion = "nutrir";
    if (highScore >= 1) { nivel = "alto"; accion = "enviar_link_pago"; }
    else if (mediumScore >= 2) { nivel = "medio"; accion = "enviar_demo"; }
    return { nivel, accion, confianza: Math.min(0.99, highScore * 0.5 + mediumScore * 0.2) };
  }
};
