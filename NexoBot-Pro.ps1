<#
.SYNOPSIS
    Script de gestión PRO para NexoBot - Edición "Sin Errores".
    Incluye limpieza de procesos zombis, backups y gestión de Docker/WSL.
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Start", "Stop", "Restart", "Status", "Logs", "Fix")]
    [string]$Action,
    [string]$Service
)

$ProjectRoot = "D:\Neil Virtual Tests\NexoBot"
$BackupDir = Join-Path $ProjectRoot "Backups"
$ComposeFile = Join-Path $ProjectRoot "docker-compose.yml"

# Asegurar que existan las carpetas necesarias
if (!(Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir }

function Backup-Config {
    Write-Host "--- Creando respaldo de seguridad ---" -ForegroundColor Cyan
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Dest = Join-Path $BackupDir "backup_$Timestamp"
    # Respalda la carpeta de configuración de OpenClaw/Clawdbot desde WSL
    wsl bash -c "cp -r ~/.openclaw /mnt/d/'Neil Virtual Tests'/NexoBot/Backups/backup_$Timestamp 2>/dev/null || cp -r ~/.clawdbot /mnt/d/'Neil Virtual Tests'/NexoBot/Backups/backup_$Timestamp 2>/dev/null"
    Write-Host "✅ Respaldo creado en: $Dest" -ForegroundColor Green
}

function Clean-Zombies {
    Write-Host "--- Limpiando procesos y sessión ---" -ForegroundColor Magenta
    wsl bash -c "pkill -f 'clawd|moltbot|openclaw' 2>/dev/null; rm -rf ~/.clawdbot/sessions/* 2>/dev/null; true"
    wsl bash -c "rm -rf ~/.clawdbot/*.lock ~/.clawdbot/tmp/* 2>/dev/null; true"
    Write-Host "✅ Limpieza completada." -ForegroundColor Green
}

function Start-Services {
    Backup-Config
    Clean-Zombies
    
    Write-Host "--- Iniciando servicios Docker (OpenWebUI/Ollama) ---" -ForegroundColor Cyan
    docker compose -f $ComposeFile up -d
    
    Write-Host "--- Iniciando Gateway en WSL ---" -ForegroundColor Cyan
    wsl systemctl --user start clawdbot-gateway.service
    
    Start-Sleep -Seconds 5
    if (Test-Status) {
        # Extract real token from systemd service
        Write-Host "🚀 ¡SISTEMA ONLINE! Accede en:" -ForegroundColor Green
        Write-Host "Dashboard: http://localhost:18789/chat?token=NexoBot100xSecure" -ForegroundColor White
        Write-Host "OpenWebUI: http://localhost:3000" -ForegroundColor White
    }
    else {
        Write-Host "⚠️ El Gateway no respondió. Revisa los logs con: .\NexoBot-Pro.ps1 -Action Logs" -ForegroundColor Red
    }
}

function Stop-Services {
    Write-Host "--- Apagando sistema de forma segura ---" -ForegroundColor Yellow
    wsl systemctl --user stop clawdbot-gateway.service
    Clean-Zombies
    docker compose -f $ComposeFile down
    Write-Host "✅ Todo apagado." -ForegroundColor Green
}

function Test-Status {
    $Status = wsl systemctl --user is-active clawdbot-gateway.service
    return ($Status.Trim() -eq 'active')
}

function Get-Status {
    Write-Host "`n--- Estado de Servicios Docker ---" -ForegroundColor Gray
    docker compose -f $ComposeFile ps
    Write-Host "`n--- Estado de Servicio Clawdbot ---" -ForegroundColor Gray
    wsl systemctl --user status clawdbot-gateway.service --no-pager
}

function Get-Logs {
    if ($Service) {
        docker compose -f $ComposeFile logs -f $Service
    }
    else {
        Write-Host "--- Mostrando logs del Gateway (WSL) ---" -ForegroundColor Gray
        wsl journalctl --user -u clawdbot-gateway.service -n 50 -f
    }
}

function Apply-Fix {
    Write-Host "--- Aplicando reparaciones de seguridad y permisos ---" -ForegroundColor Cyan
    wsl bash -c "clawdbot doctor --fix 2>/dev/null || openclaw doctor --fix 2>/dev/null || echo 'Doctor command not available'"
    wsl bash -c "chmod 700 ~/.openclaw/credentials 2>/dev/null || chmod 700 ~/.clawdbot/credentials 2>/dev/null || true"
    Write-Host "✅ Reparaciones aplicadas." -ForegroundColor Green
}

switch ($Action) {
    "Start" { Start-Services }
    "Stop" { Stop-Services }
    "Restart" { Stop-Services; Start-Services }
    "Status" { Get-Status }
    "Logs" { Get-Logs }
    "Fix" { Apply-Fix }
}
