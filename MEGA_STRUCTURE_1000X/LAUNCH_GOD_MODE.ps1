
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "   🚀 INICIANDO PROTOCOLO CLAWZENEGER GOD MODE 🚀   " -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan

# 1. Verificar Docker
if (!(Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Error "CRITICAL: Docker no está instalado o no está en el PATH."
    exit
}

# 2. Crear carpetas de datos
Write-Host "`n[1/3] Creando búnker de datos..." -ForegroundColor White
$dirs = @(
    "data\ollama",
    "data\openwebui",
    "data\n8n",
    "data\chroma",
    "config\searxng"
)
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  + Creado: $dir" -ForegroundColor Gray
    }
}

# 3. Lanzar la Bestia
Write-Host "`n[2/3] Levantando la infraestructura (Esto puede tardar)..." -ForegroundColor White
docker-compose -f docker-compose.god_mode.yml up -d

# 4. Resumen
Write-Host "`n[3/3] ¡SISTEMA ONLINE!" -ForegroundColor Green
Write-Host "---------------------------------------------------"
Write-Host "🧠 CEREBRO (Ollama):   http://localhost:11434"
Write-Host "🖥️ UI (OpenWebUI):     http://localhost:3000"
Write-Host "⚡ AUTOMATION (n8n):   http://localhost:5678"
Write-Host "🌐 SEARCH (SearXNG):   http://localhost:8081"
Write-Host "---------------------------------------------------"
Write-Host "👉 Accede a la UI para comenzar el entrenamiento de los agentes." -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan
Pause
