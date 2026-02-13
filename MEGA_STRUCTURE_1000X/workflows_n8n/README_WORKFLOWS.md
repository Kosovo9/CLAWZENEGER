# 🤖 Workflows de Automatización Clawzeneger (n8n)

Este directorio contiene los flujos de automatización JSON listos para importar en n8n.

## ✅ Workflows Confirmados

| Workflow | Descripción | Trigger | IA Model |
|----------|-------------|---------|----------|
| **`whatsapp_ai_responder.json`** | Chatbot de ventas inteligente | Mensaje WhatsApp | Llama-3.2-3b |
| **`sales_pipeline.json`** | Pipeline de ventas automático | Cron (30 min) | DeepSeek-R1 |
| **`payment_generator.json`** | Generador de pagos y emails | Webhook | N/A |
| **`scraper_pipeline.json`** | Pipeline de scraping YouTube | Cron (6h) | N/A |
| **`affiliate_tracker.json`** | Tracking de afiliados | Webhook | N/A |
| **`email_campaign.json`** | Secuencias de email marketing | Cron (24h) | Llama-3.2-3b |
| **`telegram_hunter.json`** | Captura de leads en Telegram | Mensaje Telegram | N/A |

## 🚀 Cómo Importar

1. Abre tu panel de n8n (`http://localhost:5678`)
2. Ve a **Workflows** -> **Import from File**
3. Selecciona cualquiera de los archivos `.json` de esta carpeta.
4. Configura las credenciales (SMTP, WhatsApp, Telegram, etc.)
5. Activa el workflow.

## 🔐 Credenciales Requeridas

- **SMTP**: Para envío de emails (`email_campaign`, `payment_generator`)
- **Evolution API**: Para WhatsApp (`whatsapp_ai_responder`)
- **Telegram API**: Para Telegram (`telegram_hunter`)
- **Clawzeneger API Key**: Para todos los workflows que usan la API interna.
