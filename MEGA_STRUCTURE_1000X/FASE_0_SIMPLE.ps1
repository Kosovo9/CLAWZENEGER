# FASE 0 - PRE-FLIGHT CHECK (Simplified)
# Verificacion rapida del entorno

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CLAWZENEGER - PRE-FLIGHT CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# Check Docker
Write-Host "[1] Verificando Docker..." -NoNewline
try {
    $dockerVersion = docker version --format '{{.Server.Version}}' 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] v$dockerVersion" -ForegroundColor Green
    }
    else {
        Write-Host " [FAIL] Docker no esta corriendo" -ForegroundColor Red
        $ErrorCount++
    }
}
catch {
    Write-Host " [FAIL] Docker no instalado" -ForegroundColor Red
    $ErrorCount++
}

# Check archivos criticos
Write-Host "[2] Verificando archivos..." -NoNewline
$requiredFiles = @(
    "docker-compose.god_mode.FINAL.yml",
    ".env",
    "config/litellm/config.yaml"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host " [FAIL] Falta: $file" -ForegroundColor Red
        $allFilesExist = $false
        $ErrorCount++
    }
}
if ($allFilesExist) {
    Write-Host " [OK]" -ForegroundColor Green
}

# Check .env content
Write-Host "[3] Verificando HF_TOKEN..." -NoNewline
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "HF_TOKEN=hf_\w+") {
        Write-Host " [OK]" -ForegroundColor Green
    }
    else {
        Write-Host " [FAIL] HF_TOKEN no configurado" -ForegroundColor Red
        $ErrorCount++
    }
}
else {
    Write-Host " [FAIL] Archivo .env no existe" -ForegroundColor Red
    $ErrorCount++
}

# Check disk space
Write-Host "[4] Verificando espacio en disco..." -NoNewline
$disk = Get-PSDrive C
$freeSpaceGB = [math]::Round($disk.Free / 1GB, 2)
if ($freeSpaceGB -ge 30) {
    Write-Host " [OK] ${freeSpaceGB}GB libre" -ForegroundColor Green
}
else {
    Write-Host " [WARN] Solo ${freeSpaceGB}GB libre" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($ErrorCount -eq 0) {
    Write-Host "RESULTADO: LISTO PARA LANZAR" -ForegroundColor Green
    Write-Host "Ejecuta: .\LAUNCH_GOD_MODE_FINAL.ps1" -ForegroundColor Yellow
    exit 0
}
else {
    Write-Host "RESULTADO: $ErrorCount ERRORES ENCONTRADOS" -ForegroundColor Red
    Write-Host "Corrige los errores antes de continuar" -ForegroundColor Yellow
    exit 1
}
