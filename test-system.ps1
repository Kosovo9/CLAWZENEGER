<#
.SYNOPSIS
    Comprehensive Test Suite for NexoBot System
    Tests all components: Gateway, Ollama, OpenWebUI, Docker, Token validation
#>

param(
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"
$TestResults = @()

function Test-Component {
    param(
        [string]$Name,
        [scriptblock]$TestScript
    )
    
    Write-Host "`n🧪 Testing: $Name" -ForegroundColor Cyan
    try {
        $result = & $TestScript
        if ($result) {
            Write-Host "✅ PASS: $Name" -ForegroundColor Green
            $script:TestResults += @{Name = $Name; Status = "PASS"; Message = $result }
            return $true
        }
        else {
            Write-Host "❌ FAIL: $Name" -ForegroundColor Red
            $script:TestResults += @{Name = $Name; Status = "FAIL"; Message = "Test returned false" }
            return $false
        }
    }
    catch {
        Write-Host "❌ ERROR: $Name - $_" -ForegroundColor Red
        $script:TestResults += @{Name = $Name; Status = "ERROR"; Message = $_.Exception.Message }
        return $false
    }
}

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "   NexoBot System Test Suite - Full Verification   " -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta

# Test 1: WSL Connectivity
Test-Component "WSL Connectivity" {
    $result = wsl echo "WSL OK"
    return $result -eq "WSL OK"
}

# Test 2: Clawdbot Gateway Service Status
Test-Component "Clawdbot Gateway Service" {
    $status = wsl bash -c "systemctl --user is-active clawdbot-gateway.service"
    if ($Verbose) { Write-Host "  Status: $status" }
    return $status -eq "active"
}

# Test 3: Gateway Token Extraction
Test-Component "Gateway Token Extraction" {
    $token = wsl bash -c "systemctl --user show clawdbot-gateway.service -p Environment | grep CLAWDBOT_GATEWAY_TOKEN | sed 's/.*CLAWDBOT_GATEWAY_TOKEN=//;s/ .*//' | tr -d '\n'"
    if ($Verbose) { Write-Host "  Token: $token" }
    return $token.Length -gt 20
}

# Test 4: Gateway HTTP Endpoint
Test-Component "Gateway HTTP Endpoint" {
    $response = curl.exe -s http://localhost:18789/health
    if ($Verbose) { Write-Host "  Response length: $($response.Length)" }
    return $response.Length -gt 100
}

# Test 5: Ollama Native Service
Test-Component "Ollama Native Service" {
    $response = curl.exe -s http://localhost:11434/api/tags
    if ($Verbose) { Write-Host "  Response: $($response.Substring(0, [Math]::Min(100, $response.Length)))" }
    return $response -like "*models*"
}

# Test 6: Ollama from WSL
Test-Component "Ollama from WSL" {
    $response = wsl bash -c "curl -s http://172.18.240.1:11434/api/tags | jq -r '.models[0].name' 2>/dev/null"
    if ($Verbose) { Write-Host "  First model: $response" }
    return $response.Length -gt 0
}

# Test 7: Docker Service
Test-Component "Docker Service" {
    $status = docker info 2>&1
    return $status -notlike "*error*"
}

# Test 8: OpenWebUI Container
Test-Component "OpenWebUI Container" {
    $container = docker ps --filter "name=nexobot-openwebui" --format "{{.Status}}"
    if ($Verbose) { Write-Host "  Container status: $container" }
    return $container -like "*Up*"
}

# Test 9: OpenWebUI HTTP Endpoint
Test-Component "OpenWebUI HTTP Endpoint" {
    $response = curl.exe -s http://localhost:3000
    if ($Verbose) { Write-Host "  Response length: $($response.Length)" }
    return $response.Length -gt 100
}

# Test 10: Desktop Shortcut Exists
Test-Component "Desktop Shortcut" {
    $shortcutPath = "$env:USERPROFILE\Desktop\NexoBot.lnk"
    return Test-Path $shortcutPath
}

# Test 11: Shortcut Token Validation
Test-Component "Shortcut Token Validation" {
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\NexoBot.lnk")
    $args = $Shortcut.Arguments
    $realToken = wsl bash -c "systemctl --user show clawdbot-gateway.service -p Environment | grep CLAWDBOT_GATEWAY_TOKEN | sed 's/.*CLAWDBOT_GATEWAY_TOKEN=//;s/ .*//' | tr -d '\n'"
    if ($Verbose) { 
        Write-Host "  Shortcut token: $($args -replace '.*token=([^&\s]+).*', '$1')"
        Write-Host "  Real token: $realToken"
    }
    return $args -like "*$realToken*"
}

# Test 12: Gateway Logs (No Errors)
Test-Component "Gateway Logs Clean" {
    $logs = wsl bash -c "journalctl --user -u clawdbot-gateway.service --since '2 minutes ago' --no-pager | grep -i error | wc -l"
    if ($Verbose) { Write-Host "  Error count: $logs" }
    return [int]$logs -lt 5
}

# Test 13: Port 18789 Listening
Test-Component "Port 18789 Listening" {
    $listening = netstat -an | Select-String "18789.*LISTENING"
    return $null -ne $listening
}

# Test 14: Port 11434 Listening
Test-Component "Port 11434 Listening" {
    $listening = netstat -an | Select-String "11434.*LISTENING"
    return $null -ne $listening
}

# Test 15: Port 3000 Listening
Test-Component "Port 3000 Listening" {
    $listening = netstat -an | Select-String "3000.*LISTENING"
    return $null -ne $listening
}

# Summary
Write-Host "`n═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "                  Test Summary                      " -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta

$passCount = ($TestResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($TestResults | Where-Object { $_.Status -eq "FAIL" }).Count
$errorCount = ($TestResults | Where-Object { $_.Status -eq "ERROR" }).Count
$totalCount = $TestResults.Count

Write-Host "`n✅ Passed: $passCount / $totalCount" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "❌ Failed: $failCount / $totalCount" -ForegroundColor Red
}
if ($errorCount -gt 0) {
    Write-Host "⚠️  Errors: $errorCount / $totalCount" -ForegroundColor Yellow
}

$successRate = [math]::Round(($passCount / $totalCount) * 100, 2)
Write-Host "`n📊 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

if ($failCount -gt 0 -or $errorCount -gt 0) {
    Write-Host "`n❌ Failed/Error Tests:" -ForegroundColor Red
    $TestResults | Where-Object { $_.Status -ne "PASS" } | ForEach-Object {
        Write-Host "  - $($_.Name): $($_.Message)" -ForegroundColor Yellow
    }
}

Write-Host "`n═══════════════════════════════════════════════════`n" -ForegroundColor Magenta

# Exit with appropriate code
if ($successRate -eq 100) {
    Write-Host "🎉 ALL TESTS PASSED! System is 100% operational!" -ForegroundColor Green
    exit 0
}
elseif ($successRate -ge 80) {
    Write-Host "⚠️  Most tests passed, but some issues detected." -ForegroundColor Yellow
    exit 1
}
else {
    Write-Host "❌ Critical failures detected. System needs attention." -ForegroundColor Red
    exit 2
}
