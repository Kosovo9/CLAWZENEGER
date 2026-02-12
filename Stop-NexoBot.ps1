$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'D:\Neil Virtual Tests\NexoBot'
try { docker info | Out-Null } catch { Write-Host 'Docker Desktop no está corriendo.' -ForegroundColor Yellow; exit 1 }

Write-Host 'Apagando NexoBot ...'
docker compose -f 'D:\Neil Virtual Tests\NexoBot\docker-compose.nexobot.yml' down
Write-Host '✅ Listo.' -ForegroundColor Green
