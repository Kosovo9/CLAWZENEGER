$ErrorActionPreference="Stop"
$Base = "D:\Neil Virtual Tests\NexoBot"
Set-Location $Base
docker compose down
Write-Host "OK. Contenedores abajo." -ForegroundColor Yellow
