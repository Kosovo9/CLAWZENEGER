Write-Host "🔥 Desplegando sistema automatizado de generación de leads (Clawzeneger Skill)..." -ForegroundColor Cyan

$basePath = "c:\CLAWZENEGER\MEGA_STRUCTURE_1000X\clawzeneger-skills\lead-generation-automation"

# Verificar red
docker network inspect hubzeneger-net > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    docker network create hubzeneger-net
}

# Levantar servicios usando el docker-compose de leadgen
docker-compose -f "$basePath\docker-compose.leadgen.yml" up -d --build

Write-Host "✅ Sistema desplegado 10X. Agentes activos:" -ForegroundColor Green
docker ps --filter "name=lead-" --format "table {{.Names}}\t{{.Status}}"