=== INSTRUCCIONES DE DESPLIEGUE NEXOBOT v1.0-Stable ===
Fecha: 2 Feb 2026

Este paquete contiene la configuración estabilizada y herramientas para el despliegue de NexoBot.

CONTENIDO:
1. clawdbot.json          -> Configuración maestra (Gateway, Auth, Plugins).
2. docker-compose.yml     -> servicios Ollama y OpenWebUI.
3. NexoBot-Pro.ps1        -> Script de gestión automatizada.
4. TECHNICAL_REPORT_10X.md -> Documentación técnica detallada.

INSTALACIÓN RÁPIDA:
1. Copia `clawdbot.json` a tu directorio de configuración en WSL:
   wsl cp clawdbot.json ~/.clawdbot/

2. Inicia el sistema completo usando el script maestro:
   .\NexoBot-Pro.ps1

NOTAS IMPORTANTES:
- El token de acceso ya está configurado en clawdbot.json.
- WhatsApp está habilitado en modo 'allowlist' (solo números permitidos).
- Puerto del Gateway: 18789 (Loopback).

SOPORTE:
Ver TECHNICAL_REPORT_10X.md para resolución de problemas.
