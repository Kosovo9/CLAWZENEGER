<#
.SYNOPSIS
    Despliegue final de Clawzeneger Omega 1000X con tests automáticos.
.DESCRIPTION
    Levanta toda la infraestructura, verifica servicios y guía al usuario en tests manuales.
.NOTES
    Ejecutar como Administrador en PowerShell.
#>

$ErrorActionPreference = "Continue" # Changed to Continue to allow some failures to be reported without stopping the script entirely
$host.UI.RawUI.WindowTitle = "🔥 CLAWZENEGER OMEGA FINAL DEPLOY 🔥"

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      CLAWZENEGER OMEGA 1000X - DESPLIEGUE FINAL              ║" -ForegroundColor Cyan
Write-Host "║              Genera dinero en 3 horas o menos                ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# ---------- FASE 0: VERIFICACIÓN ----------
Write-Host "`n🔍 Verificando entorno..." -ForegroundColor Yellow

# Docker
try {
    $dockerVersion = docker version --format '{{.Server.Version}}' 2>$null
    if (-not $dockerVersion) { throw "Docker no responde" }
    Write-Host "  ✅ Docker Desktop: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "  ❌ Docker Desktop no está corriendo. Inícialo y vuelve a ejecutar." -ForegroundColor Red
    exit 1
}

# Directorio
$basePath = "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X"
if (-not (Test-Path $basePath)) {
    Write-Host "  ❌ No se encuentra $basePath" -ForegroundColor Red
    exit 1
}
Set-Location $basePath

# Archivos críticos
$required = @(
    "docker-compose.god_mode.FINAL.yml",
    ".env",
    "workflows_n8n/whatsapp_ai_responder.json"
)
$missing = $false
foreach ($file in $required) {
    if (-not (Test-Path $file)) {
        Write-Host "  ❌ Falta archivo: $file" -ForegroundColor Red
        $missing = $true
    }
}
if ($missing) { exit 1 }
Write-Host "  ✅ Archivos base OK" -ForegroundColor Green

# ---------- FASE 1: LEVANTAR SERVICIOS ----------
Write-Host "`n🐳 Levantando todos los servicios (puede tomar 5-10 minutos)..." -ForegroundColor Yellow
docker-compose -f docker-compose.god_mode.FINAL.yml up -d

Write-Host "  Esperando 60 segundos para estabilización..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

# ---------- FASE 2: PRUEBAS AUTOMÁTICAS ----------
Write-Host "`n🧪 Ejecutando pruebas automáticas..." -ForegroundColor Yellow

$tests = @(
    @{Name = "Orquestador"; URL = "http://localhost:8000/health"; Expected = "ok" }
    @{Name = "Funnel Backend"; URL = "http://localhost:8002/health"; Expected = "ok" }
    @{Name = "Scraper API"; URL = "http://localhost:8001/health"; Expected = "ok" }
    @{Name = "HF-Proxy"; URL = "http://localhost:4000/health"; Expected = "healthy" }
    @{Name = "n8n"; URL = "http://localhost:5678/healthz"; Expected = "ok" }
    @{Name = "Evolution API"; URL = "http://localhost:8080/health"; Expected = "OK" }
)

$allPassed = $true
foreach ($test in $tests) {
    try {
        $resp = Invoke-RestMethod -Uri $test.URL -TimeoutSec 10
        # Convert response to string if it is an object
        $respStr = $resp | Out-String
        if ($respStr -match $test.Expected -or $resp.status -eq $test.Expected -or $resp.message -eq $test.Expected) {
            Write-Host "  ✅ $($test.Name) responde correctamente." -ForegroundColor Green
        }
        else {
            Write-Host "  ❌ $($test.Name) respuesta inesperada: $respStr" -ForegroundColor Red
            $allPassed = $false
        }
    }
    catch {
        Write-Host "  ❌ $($test.Name) no responde o error: $_" -ForegroundColor Red
        $allPassed = $false
    }
}

if (-not $allPassed) {
    Write-Host "  ⚠️ Algunas pruebas fallaron. Revisa los logs con: docker-compose logs" -ForegroundColor Yellow
}
else {
    Write-Host "  ✅ Todas las pruebas automáticas pasaron." -ForegroundColor Green
}

# Verificar agentes (solo que estén corriendo)
$agents = @("hub-agent-market", "hub-agent-coder", "hub-agent-mechanic")
foreach ($a in $agents) {
    $status = docker ps --filter "name=$a" --format "{{.Status}}"
    if ($status -match "Up") {
        Write-Host "  ✅ Agente $a activo." -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ Agente $a no está corriendo." -ForegroundColor Red
    }
}

# ---------- FASE 3: RESUMEN ----------
Write-Host "`n📋 RESUMEN DE ACCESOS:" -ForegroundColor Cyan
Write-Host "  Dashboard:        http://localhost:3000"
Write-Host "  Orquestador API:  http://localhost:8000/docs"
Write-Host "  Funnel API:       http://localhost:8002/docs"
Write-Host "  Scraper API:      http://localhost:8001/docs"
Write-Host "  n8n:              http://localhost:5678"
Write-Host "  Evolution API:    http://localhost:8080"
Write-Host "  HF-Proxy:         http://localhost:4000"

Write-Host "`n🌐 CONFIGURACIÓN DE WEBHOOKS (OBLIGATORIO PARA PAGOS):" -ForegroundColor Yellow
Write-Host "  1. Descarga e instala ngrok desde https://ngrok.com"
Write-Host "  2. Ejecuta: ngrok http 8002 (expone el funnel backend)"
Write-Host "  3. Copia la URL generada (ej. https://abc123.ngrok.io)"
Write-Host "  4. Configura los webhooks en:"
Write-Host "     - Mercado Pago: https://www.mercadopago.com.ar/developers/panel/webhooks"
Write-Host "       URL: https://tu-ngrok.ngrok.io/api/webhooks/mercadopago"
Write-Host "     - PayPal: https://developer.paypal.com/dashboard/webhooks"
Write-Host "       URL: https://tu-ngrok.ngrok.io/api/webhooks/paypal"
Write-Host "  5. En el archivo .env, actualiza FRONTEND_URL con la URL de ngrok si es necesario."

Write-Host "`n📌 PRÓXIMOS PASOS (TESTS MANUALES):" -ForegroundColor Magenta
Write-Host "  A continuación, realiza las pruebas manuales detalladas en el documento TESTS_MANUALES.md."
Write-Host "  Una vez validadas, ¡empieza a promocionar tus embudos y a ganar dinero!"

Write-Host "`n¿Quieres abrir el dashboard ahora? (s/n)" -ForegroundColor Cyan
$resp = Read-Host
if ($resp -eq 's') { Start-Process "http://localhost:3000" }

Write-Host "`n✅ Despliegue completado. Revisa el plan de tests en el documento adjunto." -ForegroundColor Green
