
Write-Host "🔥 Desplegando HubZeneger - La fusión definitiva" -ForegroundColor Cyan
Write-Host "==================================================="

# 0. Verificar .env
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.hubzeneger.example") {
        Copy-Item ".env.hubzeneger.example" ".env"
        Write-Host "⚠️ Se ha creado .env desde ejemplo. Edítalo si es necesario." -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ No se encontró .env ni ejemplo." -ForegroundColor Red
        exit 1
    }
}

# 1. Verificar red
$netCheck = docker network inspect clawzeneger-net 2>&1
if ($netCheck -match "Error: No such network") {
    Write-Host "Creando red clawzeneger-net..." -ForegroundColor Yellow
    docker network create clawzeneger-net
}

# 2. Levantar servicios
Write-Host "Levantando Orquestador y Dashboard..." -ForegroundColor Yellow
docker-compose -f docker-compose.hubzeneger.yml up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Servicios HubZeneger levantados." -ForegroundColor Green
    Start-Sleep -Seconds 5
    
    Write-Host "`n📊 ESTADO DEL SISTEMA UNIFICADO" -ForegroundColor Cyan
    Write-Host "--------------------------------"
    Write-Host "🌐 Accesos:"
    Write-Host "  - 🖥️ Dashboard Central:   http://localhost:3000"
    Write-Host "  - 🔌 API Gateway Docs:    http://localhost:8000/docs"
    
    Write-Host "`n⚠️ Asegúrate de que los módulos Funnel, Scraper y Agentes estén corriendo (usa DEPLOY_EXTENSIONS.ps1 en la raiz)" -ForegroundColor Yellow
}
else {
    Write-Host "❌ Error al levantar docker-compose." -ForegroundColor Red
}
