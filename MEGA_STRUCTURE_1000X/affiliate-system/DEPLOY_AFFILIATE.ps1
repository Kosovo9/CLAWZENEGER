# 🎯 DESPLIEGUE DEL SISTEMA DE AFILIADOS - CLAWZENEGER OMEGA 1000X

Write-Host "Iniciando despliegue de Afiliados (30% comisión)..." -ForegroundColor Cyan

# 1. Crear Base de Datos si no existe
Write-Host "Verificando base de datos en Postgres..." -ForegroundColor Yellow
docker exec -i claw-postgres psql -U litellm -c "CREATE DATABASE affiliate;" 2>$null

# 2. Levantar Servicios
Write-Host "Levantando Backend y Frontend de Afiliados..." -ForegroundColor Yellow
docker-compose -f c:\CLAWZENEGER\MEGA_STRUCTURE_1000X\affiliate-system\docker-compose.affiliate.yml up -d --build

# 3. Mostrar Estatus
Write-Host "`n✅ Sistema de Afiliados Desplegado!" -ForegroundColor Green
Write-Host "  - Panel de Afiliado: http://localhost:9201" -ForegroundColor Gray
Write-Host "  - API Backend Docs: http://localhost:9200/docs" -ForegroundColor Gray
Write-Host "  - Comisión: 30% (Automática por Webhook)" -ForegroundColor Gray

Write-Host "`n📌 NOTA: Para integrar con el funnel, asegúrate de enviar los pagos a:" -ForegroundColor White
Write-Host "  http://affiliate-backend:9200/api/v1/webhooks/payment-success" -ForegroundColor Cyan
