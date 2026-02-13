
# 💸 PIPELINE DE VENTAS AUTOMATIZADO 1000X

**Objetivo:** Convertir CLAWZENEGER en una **Máquina de Ventas Autónoma**.
**Misión:** Prospectar -> Contactar -> Negociar -> Cerrar ($$$).

## 🧩 Componentes del Embudo "Killer Sales"

### 1. 🕵️ Generación de Leads (Hunter Agent)
*   **Fuente:** Telegram (Grupos), LinkedIn (via Scraping) y Google Maps.
*   **Acción:** El agente "Hunter" escanea grupos de Telegram y perfiles públicos buscando palabras clave ("necesito bot", "busco desarrollo", "urgente").
*   **Filtro:** Usa `Llama3` para clasificar si el lead es "Caliente" (tiene dinero/urgencia) o "Frío".

### 2. 🎣 Primer Contacto (Outreach)
*   **Canales:** WhatsApp y Email (Gmail SMTP).
*   **Estrategia:** "Hyper-Personalization".
    *   *No:* "Hola vendo bots".
    *   *Sí:* "Hola [Nombre], vi que preguntaste en [Grupo] sobre automatización. Mi sistema [Clawzeneger] puede resolver eso en 2 horas. ¿Te muestro?"
*   **Automatización:** n8n envía el mensaje 3 minutos después de detectar el lead (para no parecer robot spam).

### 3. 🧠 El Negociador (Closer Agent)
*   **Modelo:** Llama 3 (Prompt "Lobo de Wall Street").
*   **Habilidad:** Manejo de objeciones.
    *   *Cliente:* "Es muy caro".
    *   *Bot:* "Entiendo que busques precio, pero Clawzeneger te ahorra 20h semanales. Si valoras tu hora a $10, se paga solo en 3 días."
*   **Cierre:** Envía link de pago (**Mercado Pago / PayPal**) o genera PDF con datos de **Transferencia Bancaria**.

---

## 🛠️ Configuración para MAÑANA (Ready-to-Deploy)

### A. Flujo de n8n: "Telegram Hunter"
1.  **Trigger:** `Telegram Trigger` (Mensaje nuevo en grupos monitoreados).
2.  **AI Filter:** El mensaje pasa por un nodo de `Ollama`.
    *   *Prompt:* "Analiza si este mensaje es una oportunidad de venta. Responde solo SI o NO".
3.  **Action:** Si es SI -> Guardar en `Google Sheets` (CRM temporal) -> Notificarme por Audio.

### B. Flujo de n8n: "Auto-Responder WhatsApp"
1.  **Trigger:** Mensaje entrante de WhatsApp (WPPConnect).
2.  **RAG Check:** Busca en `ChromaDB` si ya conocemos al cliente.
3.  **AI Response:** Genera respuesta persuasiva usando contexto previo.
4.  **Wait:** Espera 10-30 seg (simula escritura humana).
5.  **Send:** Envía respuesta.

### C. La UI "Nuclear Sales"
En el Dashboard de React (que ya tienes), añadiremos un Tab de "CRM EN VIVO":
*   Gráfico de Torta: Leads detectados vs. Cerrados.
*   Lista en tiempo real: "Negociando con Juan Pérez... Probabilidad 80%".
*   Botón de Pánico: "Tomar Control Manual" (si el bot se lía).

---

## 🚀 ¿Cómo activarlo mañana a mediodía?
Simplemente configura el `Launch_God_Mode.ps1`. La infraestructura ya incluye `n8n` y `Ollama`. Solo faltará importar los JSONs de los workflows de ventas (que generaré para ti).
