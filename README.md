# 🤖 NexoBot - Micro-SaaS Offline Platform

Sistema de IA autónomo y offline para desarrollo de Micro-SaaS, basado en Clawdbot, Ollama y OpenWebUI.

## 🎯 Descripción

NexoBot es una plataforma completa de IA que combina:
- **Clawdbot Gateway**: Motor de conversación con soporte multi-canal (WhatsApp, Web)
- **Ollama**: Servidor de modelos de IA locales
- **OpenWebUI**: Interfaz web moderna para interactuar con los modelos
- **Docker**: Orquestación de servicios
- **WSL2**: Entorno Linux en Windows

## 🚀 Características

- ✅ **100% Offline**: Funciona sin conexión a internet
- ✅ **Modelo Optimizado**: `nexobot-he` (3.6 GB) para respuestas rápidas
- ✅ **Multi-Canal**: WhatsApp, Web Dashboard, API
- ✅ **Backups Automáticos**: Protección de configuración y datos
- ✅ **Gestión Unificada**: Script PowerShell para control total
- ✅ **Skills Extensibles**: Sistema de plugins para funcionalidades

## 📋 Requisitos

- Windows 11 con WSL2 (Ubuntu)
- Docker Desktop
- PowerShell 7+
- 8GB RAM mínimo (16GB recomendado)
- GPU NVIDIA con 6GB VRAM (para aceleración)

## 🛠️ Instalación

### 1. Clonar el Repositorio

```bash
git clone <tu-repo-url>
cd NexoBot
```

### 2. Configurar Docker

Asegúrate de que Docker Desktop esté corriendo y WSL2 esté habilitado.

### 3. Iniciar el Sistema

```powershell
.\NexoBot-Pro.ps1 -Action Start
```

## 📖 Uso

### Comandos Principales

```powershell
# Iniciar todos los servicios
.\NexoBot-Pro.ps1 -Action Start

# Detener todos los servicios
.\NexoBot-Pro.ps1 -Action Stop

# Reiniciar (con limpieza y backup)
.\NexoBot-Pro.ps1 -Action Restart

# Ver estado
.\NexoBot-Pro.ps1 -Action Status

# Ver logs en tiempo real
.\NexoBot-Pro.ps1 -Action Logs

# Reparar configuración
.\NexoBot-Pro.ps1 -Action Fix
```

### Accesos Web

- **OpenWebUI**: http://localhost:3000
- **Clawdbot Dashboard**: http://localhost:18789/chat?token=iRCX5FU2Uqur6O7IUyOYvAbuqO9Q_BHniF-sCVKkG6I
- **Ollama API**: http://localhost:11434

### Launchers de Escritorio

En la carpeta `launchers/` hay scripts para acceso rápido:
- `Launch-NexoBot.ps1`: Abre solo Clawdbot
- `Launch-NexoBot-n8n.ps1`: Abre Clawdbot + n8n
- `Launch-All.ps1`: Abre todas las interfaces

## 🧠 Modelos Disponibles

### nexobot-he:latest (Recomendado)
- **Tamaño**: 3.6 GB
- **Base**: Qwen 7B (q3_K_S)
- **Uso**: Conversación general, respuestas rápidas
- **VRAM**: ~2-3 GB

### Otros Modelos
- `qwen:7b-chat-q4_K_M`: 4.9 GB
- `deepseek-coder:6.7b`: 4.1 GB
- `llama3.1:8b`: 4.9 GB

## 📁 Estructura del Proyecto

```
NexoBot/
├── config/
│   └── ollama/
│       └── hyper-efficient.Modelfile    # Configuración del modelo optimizado
├── launchers/
│   ├── Launch-NexoBot.ps1               # Launcher principal
│   ├── Launch-NexoBot-n8n.ps1           # Con n8n
│   └── Launch-All.ps1                   # Todas las interfaces
├── skills/
│   ├── archivist.py                     # Gestión de conocimiento
│   └── monitoring_workflow.json         # Workflow de monitoreo
├── docker-compose.yml                   # Orquestación de servicios
├── NexoBot-Manager.ps1                  # Manager legacy
├── NexoBot-Pro.ps1                      # Manager unificado (USAR ESTE)
├── ESTADO_SISTEMA.md                    # Documentación de estado
└── README.md                            # Este archivo
```

## 🔧 Solución de Problemas

### Dashboard Estático

Si la interfaz carga pero no responde:

```powershell
.\NexoBot-Pro.ps1 -Action Restart
```

### WSL Colgado

```powershell
wsl --shutdown
timeout /t 10
.\NexoBot-Pro.ps1 -Action Start
```

### Puerto Ocupado

```bash
# En WSL
lsof -i :18789
kill -9 <PID>
```

### Limpiar Todo y Empezar de Cero

```powershell
.\NexoBot-Pro.ps1 -Action Stop
wsl --shutdown
docker system prune -a
.\NexoBot-Pro.ps1 -Action Start
```

## 🎯 Roadmap

### Fase 1: Estabilización ✅
- [x] Crear modelo optimizado `nexobot-he`
- [x] Script de gestión unificado
- [x] Backups automáticos
- [x] Documentación completa

### Fase 2: Alineación (En Progreso)
- [ ] Cargar skills desde directorio consolidado
- [ ] Implementar allowlist de WhatsApp
- [ ] Inyectar directiva principal en el modelo
- [ ] Sistema RAG para base de conocimiento

### Fase 3: Producción
- [ ] Migración a Oracle Cloud Free Tier
- [ ] Implementar Tailscale para acceso remoto
- [ ] Hardening de seguridad
- [ ] Monitoreo y alertas

## 📝 Notas Importantes

### Configuración de WhatsApp

Para vincular WhatsApp:
1. Abre el dashboard de Clawdbot
2. Ve a "Channels" → "WhatsApp"
3. Escanea el código QR con tu teléfono
4. Envía un mensaje de prueba

### Backups

Los backups se crean automáticamente en `Backups/` cada vez que ejecutas `Start` o `Restart`.

**Ubicación**: `D:\Neil Virtual Tests\NexoBot\Backups\`

### Seguridad

- El token de autenticación está incluido en los launchers para acceso directo
- Para producción, considera implementar autenticación más robusta
- Los archivos sensibles están excluidos en `.gitignore`

## 🤝 Contribuir

Este es un proyecto personal, pero las sugerencias son bienvenidas.

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

## 👤 Autor

**Roberto (NeoWolf)**
- Proyecto: NexoBot Micro-SaaS Platform
- Fecha de inicio: Enero 2026

---

**🚀 ¡Construyendo el futuro del Micro-SaaS offline!**
