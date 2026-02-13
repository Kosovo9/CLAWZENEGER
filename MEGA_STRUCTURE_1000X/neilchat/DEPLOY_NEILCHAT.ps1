$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           🎯 ACTIVANDO CANAL PRIVADO NEILCHAT           ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Crear directorios de persistencia
$dataDir = Join-Path $PSScriptRoot "backend/data"
if (!(Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host " ✅ Directorio de datos creado" -ForegroundColor Green
}

# 2. Verificar red clawzeneger-net
$network = docker network ls --filter name=clawzeneger-net -q
if (!$network) {
    Write-Host " ❌ Error: La red 'clawzeneger-net' no existe." -ForegroundColor Red
    Write-Host " Por favor lanza el sistema principal primero." -ForegroundColor Yellow
    exit 1
}

# 3. Lanzar stack
Write-Host " 🚀 Construyendo y lanzando NeilChat (Backend + Frontend)..." -ForegroundColor Blue
docker-compose -f docker-compose.neilchat.yml up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ ¡NEILCHAT ESTÁ ONLINE!" -ForegroundColor Green
    Write-Host "----------------------------------------------------" -ForegroundColor Gray
    Write-Host " 🌐 Interfaz de Chat:   http://localhost:9301" -ForegroundColor White
    Write-Host " 🧠 Documentación API:  http://localhost:9300/docs" -ForegroundColor White
    Write-Host "----------------------------------------------------" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 Instrucciones:" -ForegroundColor Cyan
    Write-Host " 1. Habla con Neil pulsando el icono del Micrófono." -ForegroundColor White
    Write-Host " 2. Dale órdenes directas como: 'Analiza el mercado inmobiliario'." -ForegroundColor White
    Write-Host " 3. Neil enviará las órdenes a los agentes automáticamente." -ForegroundColor White
}
else {
    Write-Host " ❌ Hubo un error al lanzar NeilChat." -ForegroundColor Red
}
