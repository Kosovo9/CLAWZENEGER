# 💣 OPERACION DESTRUCCION CONTROLADA 100X
Write-Host "💣 INICIANDO PURGA TOTAL DEL BUNKER..." -ForegroundColor Red

# 1. Matar procesos
Write-Host "Matando procesos y contenedores..." -ForegroundColor Yellow
docker-compose -f C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\docker-compose.god_mode.ULTIMATE.yml down --volumes --remove-orphans
taskkill /F /IM "ollama.exe" 2>$null
taskkill /F /IM "python.exe" 2>$null
taskkill /F /IM "node.exe" 2>$null

# 2. Limpiar Docker
Write-Host "Limpiando Docker (Prune)..." -ForegroundColor Yellow
docker system prune -a -f --volumes

# 3. Borrar carpetas de datos corruptos
Write-Host "Quemando datos viejos..." -ForegroundColor Yellow
$folders = @(
    "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\data\redis",
    "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\data\chroma",
    "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\data\postgres",
    "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\models\ollama",
    "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\temp",
    "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\logs"
)

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Remove-Item -Path $folder -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  OK: Eliminado $folder"
    }
}

# 4. Recrear estructura
Write-Host "Recreando cimientos..." -ForegroundColor Yellow
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "  OK: Creado $folder"
}

Write-Host "PURGA COMPLETADA. SISTEMA LIMPIO AL 100%" -ForegroundColor Green
