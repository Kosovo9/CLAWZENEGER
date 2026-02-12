$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'D:\Neil Virtual Tests\NexoBot'

# Check Docker
try { docker info | Out-Null } catch {
  Write-Host 'Docker Desktop no está corriendo. Ábrelo y vuelve a intentar.' -ForegroundColor Yellow
  exit 1
}

Write-Host 'Levantando NexoBot (Ollama + OpenWebUI) ...'
docker compose -f 'D:\Neil Virtual Tests\NexoBot\docker-compose.nexobot.yml' up -d | Out-Null

# Wait until OpenWebUI responds (and is not "Cannot GET /")
$ok = $false
for ($i=0; $i -lt 60; $i++) {
  try {
    $r = Invoke-WebRequest -Uri 'http://localhost:3000/' -UseBasicParsing -TimeoutSec 2
    if ($r.StatusCode -eq 200 -and $r.Content -notmatch 'Cannot GET') { $ok = $true; break }
  } catch {}
  Start-Sleep -Seconds 2
}

# Get best LAN IP for mobile
function Get-BestIPv4 {
  try {
    $route = Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Sort-Object RouteMetric | Select-Object -First 1
    if ($route) {
      $ip = Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $route.InterfaceIndex -ErrorAction SilentlyContinue |
        Where-Object { $_.IPAddress -notlike '169.254*' -and $_.IPAddress -notlike '127.*' } |
        Select-Object -First 1 -ExpandProperty IPAddress
      if ($ip) { return $ip }
    }
  } catch {}
  return (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '169.254*' -and $_.IPAddress -notlike '127.*' } | Select-Object -First 1 -ExpandProperty IPAddress)
}

$ip = Get-BestIPv4

if (-not $ok) {
  Write-Host 'OpenWebUI no respondió bien. Muestro estado y logs (últimas 80 líneas):' -ForegroundColor Yellow
  docker compose -f 'D:\Neil Virtual Tests\NexoBot\docker-compose.nexobot.yml' ps
  docker logs --tail 80 nexobot-openwebui
  Write-Host 'Aun así, intento abrir el navegador...' -ForegroundColor Yellow
}

Write-Host ''
Write-Host '✅ Panel local:  http://localhost:3000' -ForegroundColor Green
if ($ip) { Write-Host ("✅ En Android (misma red/hotspot):  http://{0}:3000" -f $ip) -ForegroundColor Green }
Write-Host 'Tip: si estás sin internet, igual funciona mientras ambos estén en la misma red.' -ForegroundColor Cyan
Write-Host ''

Start-Process 'http://localhost:3000/'
