# ==================================================
# CLAWZENEGER GOD MODE - VERIFICATION SCRIPT
# ==================================================
# Este script verifica que todos los servicios estén funcionando correctamente

Write-Host "🚀 CLAWZENEGER GOD MODE - VERIFICATION SYSTEM" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Función para verificar endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [int]$ExpectedStatus = 200
    )
    
    try {
        Write-Host "Testing $Name..." -NoNewline
        $response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-Host " ✅ OK" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host " ⚠️  Status: $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Función para verificar puerto
function Test-Port {
    param(
        [string]$Name,
        [string]$Host = "localhost",
        [int]$Port
    )
    
    Write-Host "Testing $Name (port $Port)..." -NoNewline
    try {
        $connection = Test-NetConnection -ComputerName $Host -Port $Port -WarningAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-Host " ✅ OK" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host " ❌ Port closed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        return $false
    }
}

Write-Host "📊 CHECKING DOCKER SERVICES..." -ForegroundColor Yellow
Write-Host ""

# Verificar que Docker esté corriendo
try {
    $dockerRunning = docker ps -q
    if ($dockerRunning) {
        Write-Host "Docker daemon: ✅ Running" -ForegroundColor Green
    }
    else {
        Write-Host "Docker daemon: ⚠️  No containers running" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Docker daemon: ❌ NOT RUNNING" -ForegroundColor Red
    Write-Host "Por favor, inicia Docker Desktop primero." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔍 TESTING CORE SERVICES..." -ForegroundColor Yellow
Write-Host ""

# Array de servicios a verificar
$services = @(
    @{Name = "Ollama API"; Url = "http://localhost:11434/api/tags"; Port = 11434 },
    @{Name = "OpenWebUI"; Url = "http://localhost:3000"; Port = 3000 },
    @{Name = "n8n Automation"; Url = "http://localhost:5678/healthz"; Port = 5678 },
    @{Name = "HF-Proxy (LiteLLM)"; Url = "http://localhost:4000/health"; Port = 4000 },
    @{Name = "ChromaDB Memory"; Url = "http://localhost:8000/api/v1/heartbeat"; Port = 8000 },
    @{Name = "SearXNG Search"; Url = "http://localhost:8081"; Port = 8081 },
    @{Name = "Whisper STT"; Url = "http://localhost:9000"; Port = 9000 },
    @{Name = "XTTS Voice"; Url = "http://localhost:5002"; Port = 5002 },
    @{Name = "WhatsApp Gateway"; Url = "http://localhost:8080"; Port = 8080 },
    @{Name = "Browserless"; Url = "http://localhost:3001/pressure"; Port = 3001 },
    @{Name = "Redis Cache"; Port = 6379 }
)

$results = @{Passed = 0; Failed = 0 }

foreach ($service in $services) {
    if ($service.Url) {
        $result = Test-Endpoint -Name $service.Name -Url $service.Url
    }
    else {
        $result = Test-Port -Name $service.Name -Port $service.Port
    }
    
    if ($result) {
        $results.Passed++
    }
    else {
        $results.Failed++
    }
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "📈 RESULTS: $($results.Passed) OK | $($results.Failed) FAILED" -ForegroundColor $(if ($results.Failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Test especial: HF-Proxy con modelo
if (Test-Endpoint -Name "HF-Proxy Health" -Url "http://localhost:4000/health") {
    Write-Host ""
    Write-Host "🧠 TESTING AI BRAIN (HF-Proxy)..." -ForegroundColor Yellow
    Write-Host ""
    
    $testBody = @{
        model      = "llama-3.2-3b"
        messages   = @(
            @{
                role    = "user"
                content = "Responde solo 'OK' si funcionas correctamente"
            }
        )
        max_tokens = 10
    } | ConvertTo-Json -Depth 4
    
    try {
        Write-Host "Sending test request to HF-Proxy..." -NoNewline
        $response = Invoke-RestMethod -Uri "http://localhost:4000/v1/chat/completions" `
            -Method Post `
            -Headers @{
            "Authorization" = "Bearer sk-clawzeneger-master-2026"
            "Content-Type"  = "application/json"
        } `
            -Body $testBody `
            -TimeoutSec 30
        
        Write-Host " ✅ SUCCESS" -ForegroundColor Green
        Write-Host "Response: $($response.choices[0].message.content)" -ForegroundColor Cyan
    }
    catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📱 QUICK ACCESS URLS:" -ForegroundColor Cyan
Write-Host "-------------------------------------------"
Write-Host "OpenWebUI:      http://localhost:3000" -ForegroundColor White
Write-Host "n8n:            http://localhost:5678" -ForegroundColor White
Write-Host "HF-Proxy:       http://localhost:4000" -ForegroundColor White
Write-Host "WhatsApp QR:    http://localhost:8080" -ForegroundColor White
Write-Host "ChromaDB:       http://localhost:8000" -ForegroundColor White
Write-Host "SearXNG:        http://localhost:8081" -ForegroundColor White
Write-Host "-------------------------------------------"
Write-Host ""

if ($results.Failed -eq 0) {
    Write-Host "✅ ALL SYSTEMS OPERATIONAL - CLAWZENEGER READY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Open OpenWebUI at http://localhost:3000" -ForegroundColor White
    Write-Host "2. Import workflows to n8n at http://localhost:5678" -ForegroundColor White
    Write-Host "3. Scan WhatsApp QR at http://localhost:8080" -ForegroundColor White
}
else {
    Write-Host "⚠️  SOME SERVICES FAILED - Check logs above" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To view logs:" -ForegroundColor Yellow
    Write-Host "docker-compose -f docker-compose.god_mode.FINAL.yml logs [service-name]" -ForegroundColor White
}

Write-Host ""
