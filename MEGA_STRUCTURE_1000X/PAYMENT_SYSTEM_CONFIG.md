# 💳 SISTEMA DE COBROS AUTOMATIZADO (MERCADO PAGO + PAYPAL + BANCO)

Este módulo permite al agente "Closer" generar links de pago y verificar transacciones automáticamente.

## 1. 🤝 MERCADO PAGO (Latam Power)
*   **Función:** Generar Links de Cobro / QR.
*   **Integración en n8n:**
    *   Usar nodo `HTTP Request` hacia la API de Mercado Pago (`https://api.mercadopago.com/checkout/preferences`).
    *   **Payload:**
        ```json
        {
          "items": [
            {
              "title": "Servicio de Desarrollo Bot IA",
              "quantity": 1,
              "currency_id": "MXN",
              "unit_price": 5000
            }
          ],
          "back_urls": { "success": "https://tusitio.com/gracias" }
        }
        ```
    *   **Respuesta:** El bot recibe `init_point` (Link de pago) y se lo envía al cliente por WhatsApp.

## 2. 🌎 PAYPAL (Clientes Internacionales)
*   **Función:** Links de pago en USD.
*   **Integración en n8n:**
    *   Usar nodo `PayPal` (Nativo en n8n) o `HTTP Request`.
    *   Generar una "Invoice" o un botón de pago rápido ("PayPal.Me/TuUsuario/500USD").
    *   **Verificación:** Webhook de PayPal -> n8n -> Notificación "Pago Recibido".

## 3. 🏦 TRANSFERENCIA BANCARIA (High Ticket)
*   **Función:** Para montos grandes donde las comisiones de pasarela duelen.
*   **Estrategia:**
    *   El bot no envía los datos bancarios en texto plano (se ve poco profesional).
    *   **Genera un PDF Pro:** Usando una plantilla HTML en n8n, genera un PDF con tu logo, datos bancarios (CLABE/IBAN) y monto exacto.
    *   **Envío:** "Aquí tienes la orden de pago formal en PDF. Avísame cuando realices la transferencia para iniciar."

---

## 🤖 FLUJO "CIERRE DE VENTA" (n8n Workflow)

1.  **Input:** Cliente dice "Ok, lo quiero".
2.  **Bot Pregunta:** "¿Prefieres Mercado Pago, PayPal o Transferencia?"
3.  **Switch (n8n):**
    *   **Caso MP:** Llama API MP -> Genera Link -> Envía.
    *   **Caso PP:** Genera Link PayPal -> Envía.
    *   **Caso Banco:** Rellena Plantilla PDF -> Envía documento.
4.  **Wait for Trigger:** Espera confirmación (Webhook de MP/PP o Foto de comprobante en WhatsApp).
5.  **Action:** Si paga -> Enviar acceso al servicio + Mensaje de bienvenida.
