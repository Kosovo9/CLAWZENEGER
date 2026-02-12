module.exports = {
  name: "closer_10x",
  description: "Cierra ventas con urgencia real",
  async run(context, { lead, link = "https://buy.stripe.com/3cscqg23s5Lz6kN8wA" }) {
    const frases = [
      `${lead || "Amigo"}, tu link ya esta generado. Valido por 20 minutos: ${link}`,
      `🔥 Quedan 3 spots con este bono. ¿Te guardo uno? ${link}`,
      `💰 El sistema te espera. Dale clic y en 2 minutos estas adentro: ${link}`,
      `⚡ Hoy es el dia. ¿Listo para despegar? ${link}`,
      `🎯 Te mande el link directo. ¿Lo viste? ${link}`
    ];
    return {
      mensaje: frases[Math.floor(Math.random() * frases.length)],
      link_pago: link
    };
  }
};
