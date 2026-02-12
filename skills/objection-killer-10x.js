module.exports = {
  name: "objection_killer_10x",
  description: "Destruye objeciones de venta",
  async run(context, { objecion }) {
    const o = (objecion || "").toLowerCase();

    if (o.includes("caro") || o.includes("precio") || o.includes("cuesta")) {
      return "Te entiendo. La mayoria de clientes piensa igual hasta que ven el retorno. Con 49 USD generas +500 USD en contenido premium. ¿Sigue siendo caro?";
    }
    if (o.includes("tiempo") || o.includes("demora") || o.includes("entrega")) {
      return "47 segundos. Eso tarda en generarse tu primera imagen. ¿Te ayudo con una muestra?";
    }
    if (o.includes("pensarlo") || o.includes("despues") || o.includes("decidir")) {
      return "Hoy es el ultimo dia del 20% OFF. Mañana pagas mas. ¿Cerramos con el descuento?";
    }
    if (o.includes("competencia") || o.includes("otro") || o.includes("mejor")) {
      return "Nadie mas tiene nuestro motor de prompts 10X. ¿Te mando una muestra gratis?";
    }
    if (o.includes("garantia") || o.includes("devolucion")) {
      return "7 dias de garantia. Si no te gusta, te devolvemos tu dinero. Sin preguntas.";
    }
    return "Cuentame mas, quiero entender bien tu duda.";
  }
};
