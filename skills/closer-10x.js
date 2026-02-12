module.exports = {
  name: "closer_10x",
  description: "Cierra ventas con urgencia",
  async run(context, { lead, link }) {
    const frases = [
      (lead || "Compa") + ", tu link ya esta generado. Valido por 20 minutos: " + link,
      "Quedan 3 spots con este bono. Te guardo uno? " + link,
      "El sistema te espera. Dale clic y en 2 minutos estas adentro: " + link,
      "Hoy es el dia. Listo para despegar? " + link
    ];
    return { mensaje: frases[Math.floor(Math.random() * frases.length)], link_pago: link };
  }
};
