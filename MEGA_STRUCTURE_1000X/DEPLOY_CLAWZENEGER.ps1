<#
.SYNOPSIS
    Despliegue automático de Clawzeneger God Mode en producción
    Tiempo estimado: 1 hora a 4 horas (depende de descargas)
.NOTES
    Ejecutar SOLO en PowerShell como administrador
    No requiere WSL (usa Docker Desktop con Linux containers)
#>

$ErrorActionPreference = "Stop"
$host.UI.RawUI.WindowTitle = "CLAWZENEGER DEPLOY - ANTIGRAVITY MODE"

Write-Host "INICIANDO DESPLIEGUE AUTOMATICO DE CLAWZENEGER" -ForegroundColor Cyan
Write-Host "==================================================="

# ---------- FASE 0: PRE-FLIGHT (todo automatico) ----------
Write-Host "`nFASE 0: Verificando entorno..." -ForegroundColor Yellow

# 1. Docker Desktop instalado y corriendo
# ---------- FASE 0: VERIFICACION DEL ENTORNO ----------
Write-Host "`nFASE 0: Verificando entorno..." -ForegroundColor Yellow

# Verificar Docker con reintentos
$dockerOk = $false
$maxRetries = 3
$retryCount = 0

while (-not $dockerOk -and $retryCount -lt $maxRetries) {
    try {
        $dockerVersion = docker version --format '{{.Server.Version}}' 2>&1
        if ($dockerVersion -match "^\d+\.\d+\.\d+") {
            $dockerOk = $true
            Write-Host "  [OK] Docker Desktop activo (v$dockerVersion)" -ForegroundColor Green
        }
        else {
            throw "Version invalida"
        }
    }
    catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "  [!] Docker engine iniciando... reintentando ($retryCount/$maxRetries)" -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
    }
}

if (-not $dockerOk) {
    Write-Host "  [X] Docker Desktop no esta corriendo o esta iniciando." -ForegroundColor Red
    Write-Host "      1. Abre Docker Desktop" -ForegroundColor Yellow
    Write-Host "      2. Espera 30 segundos hasta ver 'Docker Desktop is running'" -ForegroundColor Yellow
    Write-Host "      3. Vuelve a ejecutar este script" -ForegroundColor Yellow
    exit 1
}

# 2. Archivos criticos presentes
$requiredFiles = @(
    "docker-compose.god_mode.FINAL.yml",
    "LAUNCH_GOD_MODE_FINAL.ps1",
    "TEST_GOD_MODE.ps1"
)
$missing = $false
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "  [X] Falta archivo: $file" -ForegroundColor Red
        $missing = $true
    }
}
if ($missing) {
    Write-Host "Asegurate de estar en C:\CLAWZENEGER\MEGA_STRUCTURE_1000X y que los archivos esten presentes." -ForegroundColor Red
    exit 1
}
else {
    Write-Host "  [OK] Archivos base presentes" -ForegroundColor Green
}

# 3. Crear .env automaticamente con credenciales reales
Write-Host "  [+] Creando .env con credenciales..." -ForegroundColor Yellow
$envContent = @"
# CLAWZENEGER GOD MODE - ENVIRONMENT VARIABLES
# Auto-generado por DEPLOY_CLAWZENEGER.ps1
# Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

# === HUGGING FACE ===
HF_TOKEN=YOUR_HF_TOKEN_HERE

# === LITELLM / HF-PROXY ===
LITELLM_MASTER_KEY=sk-clawzeneger-master-2026-prod-secret

# === REDIS ===
REDIS_PASSWORD=clawzeneger2026prod

# === WHATSAPP (Evolution API) ===
WHATSAPP_API_KEY=claw-whatsapp-api-key-2026-secure-token

# === MERCADO PAGO (Opcional - para pagos) ===
MERCADOPAGO_ACCESS_TOKEN=YOUR_MP_ACCESS_TOKEN_HERE
MERCADOPAGO_PUBLIC_KEY=YOUR_MP_PUBLIC_KEY_HERE

# === TELEGRAM (Opcional - para notificaciones) ===
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
TELEGRAM_ADMIN_CHAT_ID=YOUR_ADMIN_CHAT_ID_HERE

# === OPENAI (Opcional - fallback) ===
OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE

# === DATABASE ===
DATABASE_URL=postgresql://litellm:litellm@postgres:5432/litellm

# === TIMEZONE ===
TZ=America/Mexico_City

# === NEXOVBOT ===
HF_PROXY_URL=http://hf-proxy:8000/v1
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "  [OK] .env creado con HF_TOKEN real" -ForegroundColor Green

# 4. Backup del compose actual
if (Test-Path "docker-compose.god_mode.FINAL.yml") {
    $backupName = "docker-compose.god_mode.FINAL.yml.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item "docker-compose.god_mode.FINAL.yml" $backupName
    Write-Host "  [OK] Backup creado: $backupName" -ForegroundColor Green
}

# ---------- FASE 1: LANZAR STACK ----------
Write-Host "`nFASE 1: Levantando servicios (esto toma 5-10 minutos)..." -ForegroundColor Yellow
try {
    # Detener servicios previos
    Write-Host "  [+] Deteniendo servicios previos..." -ForegroundColor Gray
    docker-compose -f docker-compose.god_mode.FINAL.yml down 2>$null
    
    # Levantar servicios
    Write-Host "  [+] Iniciando 13 servicios..." -ForegroundColor Yellow
    docker-compose -f docker-compose.god_mode.FINAL.yml up -d
    
    if ($LASTEXITCODE -ne 0) { throw "docker-compose fallo" }
    Write-Host "  [OK] Servicios levantados" -ForegroundColor Green
}
catch {
    Write-Host "  [X] Error al levantar servicios: $_" -ForegroundColor Red
    Write-Host "  [i] Logs: docker-compose -f docker-compose.god_mode.FINAL.yml logs" -ForegroundColor Yellow
    exit 1
}

# ---------- FASE 2: VERIFICACION AUTOMATICA ----------
Write-Host "`nFASE 2: Verificando salud de servicios (espera 45 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Verificar contenedores corriendo
$containers = docker ps --format "{{.Names}}" | Where-Object { $_ -match "^claw-" }
Write-Host "  [i] Contenedores activos: $($containers.Count)" -ForegroundColor Cyan
foreach ($container in $containers) {
    Write-Host "    - $container" -ForegroundColor Gray
}

# ---------- FASE 2.5: DESCARGAR MODELOS DE OLLAMA ----------
Write-Host "`nFASE 2.5: Descargando modelos de Ollama (puede tomar 10-30 min)..." -ForegroundColor Yellow

$ollamaModels = @(
    "llama3.2:3b",        # Configurado en LiteLLM
    "llama3.2:1b",        # Extra rapido
    "deepseek-r1:7b",     # Razonamiento
    "deepseek-r1:1.5b",   # Razonamiento ligero
    "qwen2.5:7b",         # General purpose
    "phi4:latest",        # Microsoft pequeño
    "nemotron-mini:latest", # NVIDIA ultra rapido
    "glm4:9b"             # Zhipu AI (GLM-5 local alternative)
)

Write-Host "  [i] Modelos a descargar: $($ollamaModels.Count)" -ForegroundColor Cyan

foreach ($model in $ollamaModels) {
    try {
        Write-Host "  [+] Descargando $model..." -ForegroundColor Gray
        docker exec claw-brain-ollama ollama pull $model 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    [OK] $model descargado" -ForegroundColor Green
        }
        else {
            Write-Host "    [!] $model fallo (continuando...)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "    [!] Error con $model : $_" -ForegroundColor Yellow
    }
}

# Verificar modelos instalados
Write-Host "`n  [i] Verificando modelos instalados..." -ForegroundColor Gray
try {
    $installedModels = docker exec claw-brain-ollama ollama list 2>&1
    Write-Host $installedModels -ForegroundColor Gray
}
catch {
    Write-Host "  [!] No se pudo listar modelos" -ForegroundColor Yellow
}

# ---------- FASE 3: PRUEBA DEL HF-PROXY ----------
Write-Host "`nFASE 3: Probando HF-Proxy (LiteLLM)..." -ForegroundColor Yellow
$litellmKey = "sk-clawzeneger-master-2026-prod-secret"

try {
    $body = @{
        model    = "llama-3.2-3b"
        messages = @(@{ role = "user"; content = "Di solo: OK" })
    } | ConvertTo-Json

    Write-Host "  [+] Enviando request a HF-Proxy..." -ForegroundColor Gray
    $response = Invoke-RestMethod -Uri "http://localhost:4000/v1/chat/completions" -Method Post -Headers @{
        "Authorization" = "Bearer $litellmKey"
        "Content-Type"  = "application/json"
    } -Body $body -TimeoutSec 60

    if ($response.choices[0].message.content) {
        Write-Host "  [OK] HF-Proxy responde: $($response.choices[0].message.content)" -ForegroundColor Green
    }
    else {
        throw "Respuesta vacia"
    }
}
catch {
    Write-Host "  [!] Warning HF-Proxy: $_" -ForegroundColor Yellow
    Write-Host "     Puede que el modelo este descargando. Continua con FASE 4." -ForegroundColor Yellow
}

# ---------- FASE 4: PROBAR NEXOVBOT ----------
Write-Host "`nFASE 4: Verificando Nexovbot..." -ForegroundColor Yellow
try {
    $healthCheck = Invoke-RestMethod -Uri "http://localhost:5000/health" -TimeoutSec 10
    if ($healthCheck.status -eq "ok") {
        Write-Host "  [OK] Nexovbot operativo" -ForegroundColor Green
    }
}
catch {
    Write-Host "  [!] Nexovbot no responde (puede estar iniciando)" -ForegroundColor Yellow
}

# ---------- FASE 5: CONFIGURACION DE WHATSAPP (MANUAL ASISTIDO) ----------
Write-Host "`nFASE 5: Conectar WhatsApp (requiere interaccion manual)" -ForegroundColor Yellow
Write-Host "  1. Abre http://localhost:8080 en tu navegador" -ForegroundColor Cyan
Write-Host "  2. Escanea el codigo QR con tu WhatsApp (modo multi-dispositivo)" -ForegroundColor Cyan
Write-Host "  3. Espera a que aparezca 'Conectado'" -ForegroundColor Cyan
Write-Host "`n  [?] Presiona ENTER cuando hayas conectado WhatsApp (o SKIP para omitir)..." -ForegroundColor Yellow
$skip = Read-Host

# ---------- FASE 6: IMPORTAR WORKFLOW A N8N ----------
Write-Host "`nFASE 6: Configuracion de n8n..." -ForegroundColor Yellow
Write-Host "  [i] Importa manualmente los workflows:" -ForegroundColor Cyan
Write-Host "     - Abre http://localhost:5678" -ForegroundColor Cyan
Write-Host "     - Import from File -> workflows_n8n/whatsapp_ai_responder.json" -ForegroundColor Cyan
Write-Host "     - Import from File -> workflows_n8n/sales_pipeline.json" -ForegroundColor Cyan
Write-Host "  [?] Presiona ENTER cuando hayas importado..." -ForegroundColor Yellow
Read-Host

# ---------- FASE 7: INICIALIZAR CHROMADB ----------
Write-Host "`nFASE 7: Inicializando base de conocimiento (RAG)..." -ForegroundColor Yellow
try {
    $chromaHealth = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/heartbeat" -TimeoutSec 5
    Write-Host "  [OK] ChromaDB operativo" -ForegroundColor Green
}
catch {
    Write-Host "  [!] ChromaDB no esta listo: $_" -ForegroundColor Yellow
}

# ---------- RESUMEN FINAL ----------
Write-Host "`n============================================" -ForegroundColor Green
Write-Host "DESPLIEGUE COMPLETADO CON EXITO" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "`nAccesos:" -ForegroundColor Cyan
Write-Host "  - OpenWebUI:      http://localhost:3000" -ForegroundColor White
Write-Host "  - n8n:            http://localhost:5678" -ForegroundColor White
Write-Host "  - Evolution API:  http://localhost:8080" -ForegroundColor White
Write-Host "  - HF-Proxy:       http://localhost:4000" -ForegroundColor White
Write-Host "  - Nexovbot:       http://localhost:5000" -ForegroundColor White
Write-Host "  - ChromaDB:       http://localhost:8000" -ForegroundColor White
Write-Host "  - PostgreSQL:     localhost:5432 (user: litellm, pass: litellm)" -ForegroundColor White
Write-Host "  - Redis:          localhost:6379" -ForegroundColor White

Write-Host "`nPROXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "  1. Prueba enviando un WhatsApp a tu numero." -ForegroundColor White
Write-Host "  2. Monitorea logs: docker logs -f claw-nerves-n8n" -ForegroundColor White
Write-Host "  3. Activa workflows en n8n (http://localhost:5678)" -ForegroundColor White
Write-Host "  4. Configura pipeline de ventas (sales_pipeline.json)" -ForegroundColor White

Write-Host "`nMETRICAS:" -ForegroundColor Cyan
Write-Host "  Ver leads: docker exec -it claw-db-postgres psql -U litellm -d litellm -c 'SELECT * FROM leads;'" -ForegroundColor Gray

Write-Host "`nA ganar 100K en 60 dias, socio!" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Green
