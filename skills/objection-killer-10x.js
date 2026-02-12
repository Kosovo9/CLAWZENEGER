module.exports = {
  name: "objection_killer_10x",
  description: "Destruye objeciones",
  async run(context, { objecion }) {
    const o = (objecion || "").toLowerCase();
    if (o.includes("caro") || o.includes("precio")) {
      return "Te entiendo. La mayoria de clientes piensa igual, hasta que ven el retorno. Inviertes 49 USD y generas +500 USD en contenido. Sigue siendo caro?";
    }
    if (o.includes("tiempo") || o.includes("demora")) {
      return "47 segundos. Eso tarda en generarse tu primera imagen.";
    }
    if (o.includes("pensarlo") || o.includes("despues")) {
      return "Hoy es el ultimo dia del 20% OFF. Maniana pagas mas. Cerramos con el descuento?";
    }
    return "Cuentame mas, quiero entender tu duda.";
  }
};
