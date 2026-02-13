# ⚡ CLAWZENEGER - DESPLIEGUE EJECUTIVO 4 HORAS
# De stack apagado → Primeros ingresos REALES
# NO SIMULACIONES. REAL MONEY.

## 📂 ARCHIVOS LISTOS (13 CRÍTICOS)
```
✅ docker-compose.god_mode.FINAL.yml (ACTUALIZADO con Nexovbot)
✅ LAUNCH_GOD_MODE_FINAL.ps1
✅ TEST_GOD_MODE.ps1
✅ FASE_0_PREFLIGHT.ps1
✅ .env.example
✅ config/litellm/config.yaml
✅ workflows_n8n/whatsapp_ai_responder.json
✅ workflows_n8n/sales_pipeline.json (NUEVO)
✅ nexovbot/app.py (NUEVO)
✅ nexovbot/Dockerfile (NUEVO)
✅ examples/hf_proxy_examples.py
✅ README_GOD_MODE.md
✅ REPORTE_SESION_FEB_2026.md
```

---

## ⏰ CRONÓMETRO: 240 MINUTOS → REVENUE

### FASE 0: PRE-VUELO (5 MIN) ⏱️ 14:32 - 14:37

```powershell
cd C:\CLAWZENEGER\MEGA_STRUCTURE_1000X
.\FASE_0_PREFLIGHT.ps1
```

**Esperamos:**
- ✅ Docker corriendo
- ✅ Archivos presentes
- ✅ .env configurado con HF_TOKEN

**Si falla:** `.\FASE_0_PREFLIGHT.ps1 -Fix`

---

### FASE 1: LEVANTAR STACK (15 MIN) ⏱️ 14:37 - 14:52

```powershell
# Editar .env primero
copy .env.example .env
notepad .env
# CRÍTICO: Agregar HF_TOKEN real desde https://huggingface.co/settings/tokens

# Lanzar
.\LAUNCH_GOD_MODE_FINAL.ps1
```

**Esperamos:**
```
Starting 13 services...
✅ ollama          http://localhost:11434
✅ hf-proxy        http://localhost:4000
✅ nexovbot-core   http://localhost:5000   ← NUEVO
✅ redis           tcp://localhost:6379
✅ postgres        tcp://localhost:5432
✅ openwebui       http://localhost:3000
✅ n8n             http://localhost:5678
✅ chromadb        http://localhost:8000
✅ searxng         http://localhost:8081
✅ whisper         http://localhost:9000
✅ xtts            http://localhost:5002
✅ browserless     http://localhost:3001
✅ whatsapp        http://localhost:8080
```

**Verificar:**
```powershell
.\TEST_GOD_MODE.ps1
```

**Si falla un servicio:**
```powershell
docker logs claw-<servicio>-<nombre>
docker-compose -f docker-compose.god_mode.FINAL.yml restart <servicio>
```

---

### FASE 2: VALIDAR HF-PROXY + NEXOVBOT (20 MIN) ⏱️ 14:52 - 15:12

#### Test 1: HF-Proxy Directo
```powershell
# Obtener LITELLM_MASTER_KEY del .env
$env:LITELLM_KEY = "sk-clawzeneger-master-2026"  # o tu valor

curl -X POST http://localhost:4000/v1/chat/completions `
  -H "Authorization: Bearer $env:LITELLM_KEY" `
  -H "Content-Type: application/json" `
  -d '{\"model\":\"llama-3.2-3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Di solo: ONLINE\"}]}'
```

**Esperamos:** JSON con `"content": "ONLINE"`

#### Test 2: Nexovbot API
```powershell
curl http://localhost:5000/health
```
**Esperamos:** `{"status":"ok","service":"nexovbot-core"}`

#### Test 3: Nexovbot Lead Qualifier
```powershell
curl -X POST http://localhost:5000/qualify-lead `
  -H "Content-Type: application/json" `
  -d '{\"message\":\"Hola necesito un bot para WhatsApp\",\"context\":{\"phone\":\"+525512345678\",\"source\":\"web\"}}'
```

**Esperamos:** JSON con `score`, `is_hot`, `suggested_response`

**Si falla:**
```powershell
docker logs claw-agent-nexovbot
docker logs claw-brain-hfproxy
```

---

### FASE 3: WHATSAPP + n8n (20 MIN) ⏱️ 15:12 - 15:32

#### 3.1 Evolution API - Escanear QR
1. Abre: http://localhost:8080
2. Busca QR code
3. Escanea con WhatsApp Business (Settings → Linked Devices)
4. Espera "Conectado"

#### 3.2 Importar Workflows n8n
1. Abre: http://localhost:5678
2. Click: **Import from File**
3. Sube: `workflows_n8n/sales_pipeline.json`
4. Sube: `workflows_n8n/whatsapp_ai_responder.json`
5. Click: **Activate** en ambos

#### 3.3 Configurar Credenciales n8n
En workflow **Sales Pipeline**:
- Nodo "WhatsApp - Enviar Oferta":
  - Authentication: HTTP Header Auth
  - Name: `apikey`
  - Value: `<tu_WHATSAPP_API_KEY del .env>`
  
- Nodo "PostgreSQL - Guardar Lead":
  - Host: `postgres`
  - Port: `5432`
  - Database: `litellm`
  - User: `litellm`
  - Password: `litellm`

#### 3.4 Test Workflow WhatsApp
```powershell
# Envía mensaje a tu WhatsApp desde otro número
# Mensaje: "Hola bot"
```

**Esperamos:** Respuesta automática del bot

**Si falla:**
```powershell
docker logs claw-nerves-n8n
docker logs claw-whatsapp-evolution
```

---

### FASE 4: PIPELINE DE VENTAS (120 MIN) ⏱️ 15:32 - 17:32

#### 4.1 Crear Tabla Leads en PostgreSQL (5 min)
```powershell
# Conectar a PostgreSQL
docker exec -it claw-db-postgres psql -U litellm -d litellm

# Crear tabla
CREATE TABLE IF NOT EXISTS leads (
  id SERIAL PRIMARY KEY,
  phone VARCHAR(20),
  email VARCHAR(100),
  message TEXT,
  score INT,
  is_hot BOOLEAN,
  source VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### 4.2 Webhook para Captura de Leads (10 min)
El workflow `sales_pipeline.json` ya tiene un webhook.

**URL del webhook:**
```
http://localhost:5678/webhook/lead-webhook
```

**Test manual:**
```powershell
curl -X POST http://localhost:5678/webhook/lead-webhook `
  -H "Content-Type: application/json" `
  -d '{\"message\":\"Necesito un chatbot para mi negocio\",\"phone\":\"+525512345678\",\"email\":\"cliente@example.com\",\"source\":\"landing_page\"}'
```

**Esperamos:**
1. n8n ejecuta workflow
2. Nexovbot califica lead
3. Si `is_hot=true`, envía WhatsApp
4. Guarda en PostgreSQL

#### 4.3 Landing Page Simple (30 min)
```html
<!-- C:\CLAWZENEGER\landing\index.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Clawzeneger - Bots IA</title>
  <style>
    body { font-family: Arial; max-width: 600px; margin: 50px auto; }
    input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
    button { background: #007bff; color: white; padding: 15px; border: none; cursor: pointer; }
  </style>
</head>
<body>
  <h1>🤖 Automatiza tu Negocio con IA</h1>
  <p>Chatbots para WhatsApp, atención 24/7, sin contratar personal.</p>
  
  <form id="leadForm">
    <input type="text" id="phone" placeholder="+52 55 1234 5678" required>
    <input type="email" id="email" placeholder="tu@email.com" required>
    <textarea id="message" placeholder="Cuéntanos tu necesidad..." required></textarea>
    <button type="submit">Solicitar Información</button>
  </form>
  
  <div id="result" style="margin-top: 20px;"></div>
  
  <script>
    document.getElementById('leadForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const data = {
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value,
        source: 'landing_page'
      };
      
      const response = await fetch('http://localhost:5678/webhook/lead-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      document.getElementById('result').innerHTML = 
        '<p style="color:green">✅ Recibido! Te contactaremos por WhatsApp pronto.</p>';
    });
  </script>
</body>
</html>
```

**Abrir:** `file:///C:/CLAWZENEGER/landing/index.html`

#### 4.4 Configurar Pago (30 min)
Opciones rápidas:

**Opción A - Stripe:**
```javascript
// En el mensaje de WhatsApp, incluir:
suggested_response = `${respuesta_ia}

💳 *Precio Especial HOY: $1,999 MXN*
Link de pago: https://buy.stripe.com/test_XXXXXX
`
```

**Opción B - MercadoPago:**
```javascript
// Usar API de preferencias
const MP = require('mercadopago');
MP.configure({ access_token: process.env.MERCADOPAGO_ACCESS_TOKEN });

const preference = {
  items: [{
    title: 'Bot WhatsApp IA',
    quantity: 1,
    currency_id: 'MXN',
    unit_price: 1999
  }]
};

const response = await MP.preferences.create(preference);
const paymentLink = response.body.init_point;
```

#### 4.5 Primera Venta de Prueba (45 min)
1. **Tú mismo eres el lead:**
   - Llena la landing page con tu email/WhatsApp
   
2. **Nexovbot califica:**
   - Revisa logs: `docker logs claw-agent-nexovbot`
   - Debe marcar `is_hot=true` (ajusta prompt si no)
   
3. **Recibe mensaje WhatsApp:**
   - Con oferta + link de pago
   
4. **Modo prueba de pago:**
   - Stripe Test: Tarjeta `4242 4242 4242 4242`
   - Confirma pago
   
5. **Webhook de confirmación:**
   - Cuando Stripe/MP confirma pago, envía webhook
   - n8n registra venta en PostgreSQL
   
**SQL para ver ventas:**
```sql
SELECT * FROM sales ORDER BY created_at DESC LIMIT 10;
```

---

### FASE 5: REPORTE FINAL (10 MIN) ⏱️ 17:32 - 17:42

**Checklist:**
- [ ] 13 servicios corriendo
- [ ] HF-Proxy responde
- [ ] Nexovbot califica leads
- [ ] WhatsApp conectado
- [ ] Workflow sales_pipeline activo
- [ ] Landing page funcional
- [ ] Link de pago generado
- [ ] Primera venta de prueba ejecutada

**Métricas:**
```powershell
# Leads capturados
docker exec -it claw-db-postgres psql -U litellm -d litellm -c "SELECT COUNT(*) FROM leads;"

# Leads calientes
docker exec -it claw-db-postgres psql -U litellm -d litellm -c "SELECT COUNT(*) FROM leads WHERE is_hot=true;"

# Ventas (si creaste tabla)
docker exec -it claw-db-postgres psql -U litellm -d litellm -c "SELECT SUM(amount) FROM sales;"
```

---

## 🚨 TROUBLESHOOTING RÁPIDO

### Servicio no inicia
```powershell
docker logs <container_name>
docker-compose -f docker-compose.god_mode.FINAL.yml restart <servicio>
```

### HF-Proxy falla
- Verifica HF_TOKEN válido
- Revisa límites de Hugging Face (rate limit)
- Fallback a Ollama editando `config/litellm/config.yaml`

### n8n workflow no ejecuta
- Verifica que esté **Activated**
- Revisa ejecuciones: http://localhost:5678/executions
- Logs: `docker logs claw-nerves-n8n`

### WhatsApp desconectado
- Re-escanea QR en http://localhost:8080
- Verifica que WhatsApp Business esté en tu teléfono

---

## 📊 PRÓXIMOS PASOS (DESPUÉS DE 4H)

1. **Escalar tráfico:**
   - Facebook Ads → Landing page
   - Google Ads con retargeting
   
2. **Doble Swarm:**
   - PC1 (Hunter): WhatsApp + n8n
   - PC2 (Maker): Ollama + HF-Proxy + Nexovbot
   
3. **Monitoreo:**
   - Prometheus + Grafana
   - Alertas de caídas
   
4. **Automatización completa:**
   - Onboarding automático de clientes
   - Bots pre-configurados entregables en 5 min

---

## ✅ ENTREGABLE FINAL

Al terminar 4 horas:
- ✅ Stack funcional (13 servicios)
- ✅ Pipeline de ventas operativo
- ✅ Primera transacción real confirmada (aunque sea en modo prueba)
- ✅ Dashboards de monitoreo básicos
- ✅ Documentación de escalado a producción

**OBJETIVO: $100K EN 60 DÍAS COMIENZA AHORA.**
