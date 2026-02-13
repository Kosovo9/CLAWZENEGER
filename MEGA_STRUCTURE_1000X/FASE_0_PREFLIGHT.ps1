# ========================================================
# CLAWZENEGER - FASE 0: PRE-VUELO (PRE-FLIGHT CHECK)
# ========================================================
# Verifica que el entorno está listo para despliegue
# Autor: VP Global de Ingeniería
# Duración estimada: 30 minutos

param(
    [switch]$Fix,  # Intenta arreglar problemas automáticamente
    [switch]$SkipCredentials  # Skip credential checks (para testing)
)

$ErrorActionPreference = "Continue"
$script:FailCount = 0
$script:WarnCount = 0
$script:PassCount = 0

function Write-Check {
    param([string]$Message, [string]$Status, [string]$Details = "")
    
    $color = switch ($Status) {
        "PASS" { "Green"; $script:PassCount++ }
        "FAIL" { "Red"; $script:FailCount++ }
        "WARN" { "Yellow"; $script:WarnCount++ }
        default { "White" }
    }
    
    $icon = switch ($Status) {
        "PASS" { "[OK]" }
        "FAIL" { "[X]" }
        "WARN" { "[!]" }
        default { "[i]" }
    }
    
    Write-Host "$icon $Message" -NoNewline
    Write-Host " [$Status]" -ForegroundColor $color
    if ($Details) {
        Write-Host "   └─ $Details" -ForegroundColor Gray
    }
}

Write-Host @"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🚀 CLAWZENEGER FASE 0: PRE-FLIGHT CHECK 🚀          ║
║                                                          ║
║     Verificación de entorno para producción             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""
Write-Host "⏰ Duración estimada: 30 minutos" -ForegroundColor Yellow
Write-Host ""

# ========================================================
# CHECK 1: SISTEMA OPERATIVO Y WSL2
# ========================================================
Write-Host "📋 SISTEMA OPERATIVO Y WSL2" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────" -ForegroundColor Gray

# Verificar Windows 11
$osInfo = Get-CimInstance -ClassName Win32_OperatingSystem
$buildNumber = [int]$osInfo.BuildNumber

if ($buildNumber -ge 22000) {
    Write-Check "Windows 11 detectado (Build: $buildNumber)" "PASS"
}
elseif ($buildNumber -ge 19041) {
    Write-Check "Windows 10 detectado (Build: $buildNumber)" "WARN" "Windows 11 recomendado"
}
else {
    Write-Check "Windows $($osInfo.Version)" "FAIL" "Requiere Windows 10 20H1+ o Windows 11"
}

# Verificar WSL2
try {
    $wslList = wsl -l -v 2>&1
    if ($wslList -match "Ubuntu.*Running.*2") {
        Write-Check "WSL2 con Ubuntu corriendo" "PASS"
    }
    elseif ($wslList -match "Ubuntu") {
        Write-Check "WSL Ubuntu encontrado" "WARN" "Verifica que esté en versión 2"
        if ($Fix) {
            Write-Host "   └─ Intentando convertir a WSL2..." -ForegroundColor Yellow
            wsl --set-version Ubuntu 2
        }
    }
    else {
        Write-Check "WSL2" "FAIL" "Ejecuta: wsl --install -d Ubuntu"
    }
}
catch {
    Write-Check "WSL2" "FAIL" "WSL no está instalado"
}

Write-Host ""

# ========================================================
# CHECK 2: DOCKER DESKTOP
# ========================================================
Write-Host "🐳 DOCKER DESKTOP" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────" -ForegroundColor Gray

try {
    $dockerVersion = docker version --format '{{.Server.Version}}' 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Check "Docker Server corriendo (v$dockerVersion)" "PASS"
    }
    else {
        Write-Check "Docker Server" "FAIL" "Docker Desktop no está corriendo"
        if ($Fix) {
            Write-Host "   └─ Intentando iniciar Docker Desktop..." -ForegroundColor Yellow
            Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
            Write-Host "   └─ Espera 30 segundos..." -ForegroundColor Yellow
            Start-Sleep -Seconds 30
        }
    }
}
catch {
    Write-Check "Docker" "FAIL" "Docker no está instalado. Descarga: https://www.docker.com/products/docker-desktop/"
}

# Verificar Docker Compose
try {
    $composeVersion = docker-compose version --short 2>&1
    Write-Check "Docker Compose (v$composeVersion)" "PASS"
}
catch {
    Write-Check "Docker Compose" "FAIL" "Incluido en Docker Desktop"
}

# Verificar WSL Integration
try {
    $wslDocker = wsl -d Ubuntu docker --version 2>&1
    if ($wslDocker -match "Docker version") {
        Write-Check "Docker WSL Integration" "PASS"
    }
    else {
        Write-Check "Docker WSL Integration" "FAIL" "Activar en Docker Desktop → Settings → Resources → WSL Integration"
    }
}
catch {
    Write-Check "Docker WSL Integration" "WARN" "Verifica configuración"
}

Write-Host ""

# ========================================================
# CHECK 3: RECURSOS DEL SISTEMA
# ========================================================
Write-Host "💻 RECURSOS DEL SISTEMA" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────" -ForegroundColor Gray

# RAM
$totalRAM = [math]::Round($osInfo.TotalVisibleMemorySize / 1MB, 2)
if ($totalRAM -ge 16) {
    Write-Check "RAM Total: ${totalRAM}GB" "PASS"
}
elseif ($totalRAM -ge 8) {
    Write-Check "RAM Total: ${totalRAM}GB" "WARN" "16GB recomendado para producción"
}
else {
    Write-Check "RAM Total: ${totalRAM}GB" "FAIL" "Mínimo 8GB requerido"
}

# Espacio en disco
$disk = Get-PSDrive C
$freeSpaceGB = [math]::Round($disk.Free / 1GB, 2)
if ($freeSpaceGB -ge 50) {
    Write-Check "Espacio libre en C: ${freeSpaceGB}GB" "PASS"
}
elseif ($freeSpaceGB -ge 30) {
    Write-Check "Espacio libre en C: ${freeSpaceGB}GB" "WARN" "50GB recomendado"
}
else {
    Write-Check "Espacio libre en C: ${freeSpaceGB}GB" "FAIL" "Mínimo 30GB requerido"
}

# CPU
$cpu = Get-CimInstance -ClassName Win32_Processor
$cores = $cpu.NumberOfLogicalProcessors
if ($cores -ge 8) {
    Write-Check "CPU Cores: $cores" "PASS"
}
elseif ($cores -ge 4) {
    Write-Check "CPU Cores: $cores" "WARN" "8+ cores recomendado"
}
else {
    Write-Check "CPU Cores: $cores" "FAIL" "Mínimo 4 cores requerido"
}

Write-Host ""

# ========================================================
# CHECK 4: ARCHIVOS DEL PROYECTO
# ========================================================
Write-Host "📁 ARCHIVOS DEL PROYECTO" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────" -ForegroundColor Gray

$projectPath = "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X"
Set-Location $projectPath -ErrorAction SilentlyContinue

$requiredFiles = @(
    "docker-compose.god_mode.FINAL.yml",
    "LAUNCH_GOD_MODE_FINAL.ps1",
    "TEST_GOD_MODE.ps1",
    ".env.example",
    "config/litellm/config.yaml",
    "workflows_n8n/whatsapp_ai_responder.json"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Check "Archivo: $file" "PASS"
    }
    else {
        Write-Check "Archivo: $file" "FAIL" "Archivo crítico faltante"
    }
}

Write-Host ""

# ========================================================
# CHECK 5: CREDENCIALES (si no se skippea)
# ========================================================
if (-not $SkipCredentials) {
    Write-Host "🔐 CREDENCIALES" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────────────────" -ForegroundColor Gray

    if (Test-Path ".env") {
        Write-Check "Archivo .env encontrado" "PASS"
        
        $envContent = Get-Content ".env" -Raw
        
        # Verificar variables críticas
        $criticalVars = @(
            @{Name = "HF_TOKEN"; Pattern = "HF_TOKEN=hf_[a-zA-Z0-9]{30}" },
            @{Name = "LITELLM_MASTER_KEY"; Pattern = "LITELLM_MASTER_KEY=sk-" },
            @{Name = "WHATSAPP_API_KEY"; Pattern = "WHATSAPP_API_KEY=\w{20}" },
            @{Name = "REDIS_PASSWORD"; Pattern = "REDIS_PASSWORD=\w+" }
        )
        
        foreach ($var in $criticalVars) {
            if ($envContent -match $var.Pattern) {
                Write-Check "Variable: $($var.Name)" "PASS"
            }
            elseif ($envContent -match "$($var.Name)=CHANGE_THIS") {
                Write-Check "Variable: $($var.Name)" "FAIL" "Contiene valor de ejemplo 'CHANGE_THIS'"
            }
            else {
                Write-Check "Variable: $($var.Name)" "FAIL" "No encontrada o formato inválido"
            }
        }
    }
    else {
        Write-Check "Archivo .env" "FAIL" "Copia .env.example a .env y configura"
        if ($Fix) {
            Write-Host "   └─ Creando .env desde .env.example..." -ForegroundColor Yellow
            Copy-Item ".env.example" ".env"
            Write-Host "   └─ ⚠️  IMPORTANTE: Edita .env con tus credenciales reales" -ForegroundColor Yellow
        }
    }
}

Write-Host ""

# ========================================================
# CHECK 6: CONECTIVIDAD
# ========================================================
Write-Host "🌐 CONECTIVIDAD" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────" -ForegroundColor Gray

# Test HuggingFace
try {
    $hfTest = Invoke-WebRequest -Uri "https://huggingface.co" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Check "HuggingFace accesible" "PASS"
}
catch {
    Write-Check "HuggingFace accesible" "WARN" "Verifica firewall/proxy"
}

# Test Docker Hub
try {
    $dockerTest = Invoke-WebRequest -Uri "https://hub.docker.com" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Check "Docker Hub accesible" "PASS"
}
catch {
    Write-Check "Docker Hub accesible" "WARN" "Necesario para descargar imágenes"
}

Write-Host ""

# ========================================================
# RESUMEN FINAL
# ========================================================
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                   RESUMEN PRE-VUELO                      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ✅ Checks pasados:  $script:PassCount" -ForegroundColor Green
Write-Host "  ⚠️  Warnings:        $script:WarnCount" -ForegroundColor Yellow
Write-Host "  ❌ Checks fallidos: $script:FailCount" -ForegroundColor Red
Write-Host ""

if ($script:FailCount -eq 0) {
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║         ✅ SISTEMA LISTO PARA FASE 1 ✅                  ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximo paso:" -ForegroundColor Yellow
    Write-Host "  .\LAUNCH_GOD_MODE_FINAL.ps1" -ForegroundColor White
    Write-Host ""
    exit 0
}
elseif ($script:FailCount -le 2 -and $script:WarnCount -le 3) {
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║      ⚠️  SISTEMA CASI LISTO - REVISA WARNINGS ⚠️        ║" -ForegroundColor Yellow
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Puedes continuar bajo tu propio riesgo con:" -ForegroundColor Yellow
    Write-Host "  .\LAUNCH_GOD_MODE_FINAL.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}
else {
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║         ❌ SISTEMA NO LISTO - CORRIGE ERRORES ❌        ║" -ForegroundColor Red
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "Acciones recomendadas:" -ForegroundColor Yellow
    Write-Host "  1. Revisa los checks con ❌ arriba" -ForegroundColor White
    Write-Host "  2. Ejecuta con: .\FASE_0_PREFLIGHT.ps1 -Fix" -ForegroundColor White
    Write-Host "  3. Vuelve a ejecutar: .\FASE_0_PREFLIGHT.ps1" -ForegroundColor White
    Write-Host ""
    exit 2
}
