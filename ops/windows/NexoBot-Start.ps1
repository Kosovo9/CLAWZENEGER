$ErrorActionPreference="Stop"
$Base = "D:\Neil Virtual Tests\NexoBot"
Set-Location $Base

# Levanta OpenWebUI + Ollama
docker compose up -d --pull always

# Si quieres n8n también, descomenta:
# docker compose --profile automation up -d

Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"   # OpenWebUI
Start-Process "http://localhost:18789"  # Clawdbot Dashboard
# Start-Process "http://localhost:5678" # n8n (si lo levantaste)

Write-Host "`nOK. URLs:" -ForegroundColor Green
Write-Host "OpenWebUI: http://localhost:3000"
Write-Host "Clawdbot : http://localhost:18789"
