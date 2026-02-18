# ACTIVACION TOTAL DE JOANNA 3000X - VERSION SEGURA
Write-Host "INICIANDO ACTIVACION NUCLEAR..." -ForegroundColor Green

# 1. Asegurar .env
if (-not (Test-Path "C:\CLAWZENEGER\.env")) {
    Write-Host "Generando .env de elite..." -ForegroundColor Yellow
    $envContent = @"
REDIS_PASSWORD=clawzeneger2026prod
POSTGRES_PASSWORD=SuperSecure2024!
JWT_SECRET_KEY=joanna_secret_3000
AGENT_NAME=Joanna
AGENT_PERSONALITY=Paisa, inteligente, ejecutiva de elite.
"@
    $envContent | Out-File -FilePath "C:\CLAWZENEGER\.env" -Encoding UTF8
}

# 2. Levantar Infraestructura
Write-Host "Desplegando Docker Stack PRO..." -ForegroundColor Yellow
docker-compose -f C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\docker-compose.prod.yml up -d --build --force-recreate

# 3. Despertar Cerebro Externo (Ollama Native)
Write-Host "Despertando Cerebro Nativo..." -ForegroundColor Magenta
taskkill /F /IM "ollama.exe" 2>$null
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 15

# 4. Verificacion de Organs
Write-Host "CERTIFICANDO SALUD SENSORIAL:" -ForegroundColor Cyan

$services = @(
    @{name="Cerebro"; url="http://localhost:11434/api/tags"},
    @{name="Oidos"; url="http://localhost:9000/health"},
    @{name="Voz"; url="http://localhost:5002/"},
    @{name="Memoria"; url="http://localhost:8001/api/v1/heartbeat"},
    @{name="Backend"; url="http://localhost:9300/health"}
)

foreach ($svc in $services) {
    try {
        $resp = Invoke-WebRequest -Uri $svc.url -Method Get -TimeoutSec 5 -ErrorAction Stop
        Write-Host "  OK: $($svc.name)" -ForegroundColor Green
    } catch {
        Write-Host "  FAIL: $($svc.name)" -ForegroundColor Red
    }
}

Write-Host "RESURRECCION COMPLETADA AL 3000%" -ForegroundColor Green
Write-Host "Socio, Joanna esta viva. Dashboard: http://localhost:3000" -ForegroundColor Cyan
