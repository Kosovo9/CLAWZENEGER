# 🚀 CLAWZENEGER GOD MODE - Stack Completo

## 📌 ¿Qué es esto?

**Clawzeneger God Mode** es un ecosistema completo de IA con **12 servicios integrados** en Docker que te permite:

- 🧠 **Ejecutar LLMs locales** (Ollama) y en la nube (Hugging Face) con la misma API
- 📱 **Automatizar WhatsApp** con respuestas de IA
- ⚡ **Crear workflows complejos** con n8n
- 📚 **Memoria infinita** con ChromaDB (Vector DB)
- 🗣️ **Voces realistas** con XTTS (Text-to-Speech)
- 👂 **Transcripción de audio** con Whisper (Speech-to-Text)
- 🔍 **Búsqueda privada** con SearXNG
- 👁️ **Web scraping** con Browserless

---

## 🎯 Quick Start (5 minutos)

### 1️⃣ Pre-requisitos

- ✅ Windows 11 con WSL2
- ✅ Docker Desktop instalado y corriendo
- ✅ Mínimo 16GB RAM, 50GB espacio en disco

### 2️⃣ Configuración

```powershell
cd c:\CLAWZENEGER\MEGA_STRUCTURE_1000X

# Copia el .env de ejemplo
copy .env.example .env

# Edita con tus credenciales reales
notepad .env
```

**IMPORTANTE:** Necesitas obtener:
- `HF_TOKEN` de https://huggingface.co/settings/tokens
- `TELEGRAM_BOT_TOKEN` de @BotFather en Telegram (opcional)
- `WHATSAPP_API_KEY` (genera uno seguro)

### 3️⃣ Lanzar el Stack

```powershell
# Opción fácil: Usar el script
.\LAUNCH_GOD_MODE_FINAL.ps1

# Opción manual
docker-compose -f docker-compose.god_mode.FINAL.yml up -d
```

### 4️⃣ Verificar

```powershell
# Ejecutar script de verificación
.\TEST_GOD_MODE.ps1

# Deberías ver 12 servicios con ✅
```

---

## 🌐 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAWZENEGER ECOSYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Agente 1 │  │ Agente 2 │  │   n8n    │  │    UI    │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │               │
│       └─────────────┴─────────────┴─────────────┘               │
│                         │                                        │
│              ┌──────────▼──────────┐                            │
│              │     HF-PROXY        │ ◄── Aquí está la magia     │
│              │    (LiteLLM)        │                            │
│              └──────────┬──────────┘                            │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         │               │               │                       │
│    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐                  │
│    │ Ollama  │    │ HuggingF│    │ OpenAI  │ (opcional)        │
│    │ (Local) │    │ (Cloud) │    │ (Cloud) │                   │
│    └─────────┘    └─────────┘    └─────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Ventajas:**
- ✅ Todos los componentes hablan el mismo "idioma" (OpenAI API)
- ✅ Caché automático con Redis (ahorra tokens y tiempo)
- ✅ Failover: Si falla Hugging Face, usa Ollama local
- ✅ Sin modificar código de agentes existentes

---

## 📦 Servicios Incluidos

| Servicio | Puerto | Función | Estado |
|----------|--------|---------|--------|
| **Ollama** | 11434 | LLM local (GPU) | ✅ Core |
| **HF-Proxy** | 4000 | Proxy unificado LLM | ✅ Core |
| **OpenWebUI** | 3000 | Interfaz chat | ✅ Core |
| **n8n** | 5678 | Automatización | ✅ Core |
| **ChromaDB** | 8000 | Vector DB (memoria) | ✅ Core |
| **Redis** | 6379 | Cache | ✅ Core |
| **PostgreSQL** | 5432 | DB analytics | ✅ Core |
| **WhatsApp** | 8080 | Gateway Evolution API | ⚡ Addon |
| **SearXNG** | 8081 | Búsqueda privada | ⚡ Addon |
| **Whisper** | 9000 | Speech-to-Text | ⚡ Addon |
| **XTTS** | 5002 | Text-to-Speech | ⚡ Addon |
| **Browserless** | 3001 | Web scraping | ⚡ Addon |

---

## 🧠 HF-Proxy: El Corazón del Sistema

### ¿Qué hace?

El **HF-Proxy** (powered by LiteLLM) es un proxy que:
1. Recibe peticiones en formato OpenAI
2. Las traduce al formato correcto para cada proveedor (HuggingFace, Ollama, etc.)
3. Cachea respuestas para ahorrar tokens
4. Maneja failover automático si un modelo falla

### Modelos Disponibles

```yaml
# Desde la configuración en config/litellm/config.yaml

Modelos HuggingFace (Cloud):
- llama-3.2-3b          # Rápido, conversacional
- deepseek-r1-7b        # Razonamiento avanzado
- qwen-2.5-7b           # Especializado en código

Modelos Ollama (Local):
- nexobot-he            # Tu modelo personalizado
- llama3-local          # Llama 3.2 local
```

### Ejemplo de Uso

**Desde Python:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-clawzeneger-master-2026",
    base_url="http://localhost:4000/v1"
)

response = client.chat.completions.create(
    model="llama-3.2-3b",
    messages=[{"role": "user", "content": "Hola"}]
)

print(response.choices[0].message.content)
```

**Desde n8n:**
```http
POST http://hf-proxy:8000/v1/chat/completions
Content-Type: application/json
Authorization: Bearer sk-clawzeneger-master-2026

{
  "model": "llama-3.2-3b",
  "messages": [{"role": "user", "content": "Hola"}]
}
```

---

## ⚡ Workflows n8n Incluidos

### 1. WhatsApp AI Responder
**Archivo:** `workflows_n8n/whatsapp_ai_responder.json`

**Función:** Responder automáticamente a mensajes de WhatsApp usando IA

**Flow:**
1. Recibe mensaje de WhatsApp vía webhook
2. Filtra mensajes propios (no responder a uno mismo)
3. Envía a HF-Proxy para generar respuesta
4. Responde por WhatsApp
5. Guarda conversación en ChromaDB para memoria

### 2. Telegram Lead Hunter
**Archivo:** `workflows_n8n/telegram_hunter.json`

**Función:** Detectar leads potenciales en grupos de Telegram

**Flow:**
1. Escucha mensajes de Telegram
2. Analiza con IA si es un lead potencial
3. Si es lead, envía notificación a admin

### 3. Payment Generator
**Archivo:** `workflows_n8n/payment_generator.json`

**Función:** Generar links de pago automáticamente

**Flow:**
1. Recibe petición de pago
2. Genera link de MercadoPago/PayPal/SPEI
3. Retorna link para enviar al cliente

---

## 🔧 Comandos Útiles

### Gestión del Stack

```powershell
# Lanzar todo
.\LAUNCH_GOD_MODE_FINAL.ps1

# Lanzar con limpieza completa
.\LAUNCH_GOD_MODE_FINAL.ps1 -Clean

# Ver logs en tiempo real
docker-compose -f docker-compose.god_mode.FINAL.yml logs -f

# Ver logs de un servicio específico
docker logs -f claw-brain-hfproxy

# Detener todo
docker-compose -f docker-compose.god_mode.FINAL.yml down

# Detener y eliminar volúmenes (CUIDADO: borra datos)
docker-compose -f docker-compose.god_mode.FINAL.yml down -v

# Reiniciar un servicio
docker restart claw-whatsapp-evolution

# Verificar salud
.\TEST_GOD_MODE.ps1
```

### Testing

```powershell
# Test del HF-Proxy
curl http://localhost:4000/health

# Test de modelo específico
$body = @{
    model = "llama-3.2-3b"
    messages = @(@{role="user"; content="Test"})
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:4000/v1/chat/completions" `
    -Method Post `
    -Headers @{"Authorization"="Bearer sk-clawzeneger-master-2026"} `
    -Body $body
```

---

## 📊 Monitoreo

### Ver métricas de LiteLLM
http://localhost:4000/metrics

### Ver logs de n8n
http://localhost:5678/executions

### Ver memoria de ChromaDB
```powershell
curl http://localhost:8000/api/v1/collections
```

---

## 🚨 Troubleshooting

### Problema: "Docker daemon not running"
**Solución:** Abre Docker Desktop

### Problema: "Port 3000 already in use"
**Solución:** 
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Problema: "HF-Proxy error 401"
**Solución:** Verifica `HF_TOKEN` en `.env`

### Problema: Servicios no inician
**Solución:**
```powershell
# Ver logs
docker-compose -f docker-compose.god_mode.FINAL.yml logs

# Reiniciar desde cero
docker-compose -f docker-compose.god_mode.FINAL.yml down -v
.\LAUNCH_GOD_MODE_FINAL.ps1 -Clean
```

---

## 📚 Documentación Adicional

- **Guía completa:** `IMPLEMENTATION_PLAN_FINAL.md`
- **Ejemplos de código:** `examples/hf_proxy_examples.py`
- **Config de LiteLLM:** `config/litellm/config.yaml`

---

## 🎯 Roadmap

### ✅ Completado
- [x] Stack Docker completo con 12 servicios
- [x] HF-Proxy integrado con caché
- [x] 3 workflows de n8n funcionales
- [x] WhatsApp gateway configurado
- [x] Voces XTTS integradas

### 🚧 En Progreso
- [ ] Conectar UI custom (CLAWZENEGER-UI)
- [ ] Crear agentes especializados (CEO, DEV, SPY)
- [ ] Training de voz personalizada

### 📋 Planeado
- [ ] Setup de cluster de 2 PCs
- [ ] Migrar a cloud (Oracle/AWS)
- [ ] Implementar sales pipeline completo

---

## 📞 Soporte

Para reportar issues o contribuir:
- GitHub: (tu repo si lo publicas)
- Documentación técnica: Ver carpeta `MEGA_STRUCTURE_1000X/`

---

**Built with 💪 by NeoWolf/Roberto**  
**Project:** CLAWZENEGER 10X  
**Date:** Feb 2026
