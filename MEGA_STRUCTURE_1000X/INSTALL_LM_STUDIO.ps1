# ========================================
# INSTALL LM STUDIO - Local LLM Platform
# ========================================
# Instala LM Studio via Chocolatey o descarga directa
# y lo integra con Clawzeneger God Mode

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CLAWZENEGER - LM STUDIO INSTALLER" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar si Chocolatey está instalado
$chocoInstalled = $null -ne (Get-Command choco -ErrorAction SilentlyContinue)

if (-not $chocoInstalled) {
    Write-Host "[i] Chocolatey no encontrado. Instalando..." -ForegroundColor Yellow
    
    # Instalar Chocolatey
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refrescar PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    Write-Host "[OK] Chocolatey instalado" -ForegroundColor Green
}

# Descargar LM Studio
Write-Host "`n[i] Descargando LM Studio..." -ForegroundColor Cyan
$lmStudioUrl = "https://lmstudio.ai/download/windows"
$downloadPath = "$env:TEMP\LMStudioSetup.exe"

try {
    # Obtener la URL de descarga real (redirección)
    $response = Invoke-WebRequest -Uri $lmStudioUrl -MaximumRedirection 0 -ErrorAction SilentlyContinue
    $actualUrl = $response.Headers.Location
    
    if (-not $actualUrl) {
        $actualUrl = "https://s3.amazonaws.com/releases.lmstudio.ai/windows/0.3.8/LM%20Studio-0.3.8%20Setup.exe"
    }
    
    Write-Host "[+] Descargando desde: $actualUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $actualUrl -OutFile $downloadPath
    
    Write-Host "[OK] Descarga completa" -ForegroundColor Green
    
    # Ejecutar instalador
    Write-Host "`n[i] Instalando LM Studio..." -ForegroundColor Cyan
    Write-Host "    (Wizard de instalacion se abrira - acepta los defaults)" -ForegroundColor Yellow
    
    Start-Process -FilePath $downloadPath -Wait
    
    Write-Host "[OK] LM Studio instalado" -ForegroundColor Green
    
}
catch {
    Write-Host "[X] Error en descarga/instalacion: $_" -ForegroundColor Red
    Write-Host "`n[i] Visita manualmente: https://lmstudio.ai" -ForegroundColor Yellow
    exit 1
}

# Crear archivo de configuración para LM Studio
Write-Host "`n[i] Configurando integracion con Clawzeneger..." -ForegroundColor Cyan

$lmStudioConfig = @"
# LM Studio Configuration for Clawzeneger
# API Endpoint: http://localhost:1234/v1

{
  "serverPort": 1234,
  "enableCors": true,
  "models": [
    "llama-2-7b",
    "mistral-7b-instruct",
    "phi-2",
    "deepseek-coder-6.7b"
  ]
}
"@

$configPath = "C:\CLAWZENEGER\config\lm_studio.json"
New-Item -ItemType Directory -Force -Path "C:\CLAWZENEGER\config" | Out-Null
Set-Content -Path $configPath -Value $lmStudioConfig

Write-Host "[OK] Config creada en: $configPath" -ForegroundColor Green

# Actualizar LiteLLM config para incluir LM Studio
Write-Host "`n[i] Agregando LM Studio a LiteLLM config..." -ForegroundColor Cyan

$litellmConfigPath = "C:\CLAWZENEGER\config\litellm\config.yaml"

if (Test-Path $litellmConfigPath) {
    $litellmConfig = Get-Content $litellmConfigPath -Raw
    
    # Verificar si ya existe LM Studio
    if ($litellmConfig -notmatch "lmstudio") {
        
        $lmStudioEntry = @"

  # ========== LM STUDIO (Local OpenAI-compatible) ==========
  - model_name: lmstudio-default
    litellm_params:
      model: openai/lmstudio
      api_base: http://host.docker.internal:1234/v1
      api_key: dummy  # LM Studio no requiere key
"@
        
        # Insertar antes de la sección de OpenAI
        $litellmConfig = $litellmConfig -replace "  # ========== OPENAI", "$lmStudioEntry`n`n  # ========== OPENAI"
        
        Set-Content -Path $litellmConfigPath -Value $litellmConfig
        
        Write-Host "[OK] LM Studio agregado a LiteLLM" -ForegroundColor Green
    }
    else {
        Write-Host "[i] LM Studio ya esta en LiteLLM config" -ForegroundColor Yellow
    }
}
else {
    Write-Host "[!] LiteLLM config no encontrado: $litellmConfigPath" -ForegroundColor Yellow
}

# Crear script de inicio rapido
$quickStartScript = @"
# Quick Start LM Studio + Clawzeneger

Write-Host "Iniciando LM Studio..." -ForegroundColor Cyan
Start-Process "C:\Users\$env:USERNAME\AppData\Local\Programs\LMStudio\LM Studio.exe"

Write-Host "`n[i] Instrucciones:" -ForegroundColor Yellow
Write-Host "  1. En LM Studio, descarga un modelo (ej: mistral-7b-instruct)" -ForegroundColor Gray
Write-Host "  2. Click en 'Start Server' (puerto 1234)" -ForegroundColor Gray
Write-Host "  3. El modelo estara disponible en HF-Proxy como 'lmstudio-default'" -ForegroundColor Gray
Write-Host "`n[i] Endpoint: http://localhost:1234/v1" -ForegroundColor Cyan
"@

$quickStartPath = "C:\CLAWZENEGER\START_LM_STUDIO.ps1"
Set-Content -Path $quickStartPath -Value $quickStartScript

Write-Host "[OK] Quick start creado: $quickStartPath" -ForegroundColor Green

# Resumen
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  INSTALACION COMPLETA" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "[OK] LM Studio instalado" -ForegroundColor Green
Write-Host "[OK] Config integrada con Clawzeneger" -ForegroundColor Green
Write-Host "[OK] Modelo agregado a LiteLLM (lmstudio-default)" -ForegroundColor Green

Write-Host "`n[NEXT STEPS]" -ForegroundColor Yellow
Write-Host "  1. Ejecuta: .\START_LM_STUDIO.ps1" -ForegroundColor Gray
Write-Host "  2. Descarga un modelo en LM Studio" -ForegroundColor Gray
Write-Host "  3. Inicia el servidor local (puerto 1234)" -ForegroundColor Gray
Write-Host "  4. Usa 'lmstudio-default' en tus apps" -ForegroundColor Gray

Write-Host "`n[i] LM Studio UI: http://localhost:1234" -ForegroundColor Cyan
Write-Host "[i] Docs: https://lmstudio.ai/docs" -ForegroundColor Cyan
