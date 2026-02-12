<#
.SYNOPSIS
    Script de gestión unificado para el ecosistema NexoBot.
    Optimizada para persistencia (Linger) y robustez con Systemd.
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Start", "Stop", "Restart", "Status", "Logs")]
    [string]$Action,

    [string]$Service
)

$ProjectRoot = "D:\Neil Virtual Tests\NexoBot"
$ComposeFile = Join-Path $ProjectRoot "docker-compose.yml"

# Asegurar que lingering esté habilitado para persistencia
# Fundamental para que servicios de usuario persistan sin sesión activa
wsl -e loginctl enable-linger neocwolf 2>$null

function Start-Services {
    Write-Host "Iniciando servicios Docker..." -ForegroundColor Cyan
    docker compose -f $ComposeFile up -d
    Write-Host "Iniciando servicio Clawdbot en WSL..." -ForegroundColor Cyan
    wsl -e systemctl --user start clawdbot-gateway.service
    
    Start-Sleep -Seconds 3
    if (Test-Status) {
        Write-Host "✅ Servicios iniciados y verificados." -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ Advertencia: Clawdbot puede no estar respondiendo." -ForegroundColor Yellow
        Get-Status
    }
}

function Stop-Services {
    Write-Host "Deteniendo servicio Clawdbot en WSL..." -ForegroundColor Yellow
    wsl -e systemctl --user stop clawdbot-gateway.service
    Write-Host "Deteniendo servicios Docker..." -ForegroundColor Yellow
    docker compose -f $ComposeFile down
}

function Test-Status {
    $Status = wsl -e systemctl --user is-active clawdbot-gateway.service
    return ($Status.Trim() -eq 'active')
}

function Get-Status {
    Write-Host "--- Estado de Servicios Docker ---" -ForegroundColor Gray
    docker compose -f $ComposeFile ps
    Write-Host "`n--- Estado de Servicio Clawdbot ---" -ForegroundColor Gray
    wsl -e systemctl --user status clawdbot-gateway.service --no-pager
}

function Get-Logs {
    if ($Service) {
        Write-Host "Mostrando logs para $Service..."
        docker compose -f $ComposeFile logs -f $Service
    }
    else {
        Write-Host "Mostrando logs del sistema para Clawdbot..."
        wsl -e journalctl -u clawdbot-gateway.service --no-pager -n 50 -f
    }
}

switch ($Action) {
    "Start" { Start-Services }
    "Stop" { Stop-Services }
    "Restart" { Stop-Services; Start-Services }
    "Status" { Get-Status }
    "Logs" { Get-Logs }
}
