
Write-Host "🔥 Desplegando Extensiones Clawzeneger (Funnel, Scraper, Agentes)..." -ForegroundColor Cyan

# Ensure network exists
docker network inspect clawzeneger-net > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creando red clawzeneger-net..." -ForegroundColor Yellow
    docker network create clawzeneger-net
}

# Go to skills directory
cd "$PSScriptRoot\clawzeneger-skills"

# Build and Up
docker-compose -f docker-compose.agents.yml up -d --build

Write-Host "✅ Extensiones desplegadas:" -ForegroundColor Green
Write-Host "   - Funnel Editor: http://localhost:3002"
Write-Host "   - Funnel API:    http://localhost:8002"
Write-Host "   - Scraper API:   http://localhost:8001"
Write-Host "   - Market Agent:  Running in background"
Write-Host ""
Write-Host "📌 Logs: docker logs -f claw-agent-market"
