$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'D:\Neil Virtual Tests\NexoBot'
docker compose -f 'D:\Neil Virtual Tests\NexoBot\docker-compose.nexobot.yml' --profile automation up -d
Start-Process 'http://localhost:3000/'
Start-Process 'http://localhost:5678/'
