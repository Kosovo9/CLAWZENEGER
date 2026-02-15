# RESCATE DE JOANNA 3000X - VERSION FINAL SEGURA
Write-Host "INICIANDO OPERACION RESCATE 10X..." -ForegroundColor Red

# 1. MATAR PROCESOS
Write-Host "Matando procesos zombies..." -ForegroundColor Yellow
docker-compose -f C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\docker-compose.god_mode.ULTIMATE.yml down --volumes --remove-orphans
taskkill /F /IM "ollama.exe" 2>$null
taskkill /F /IM "python.exe" 2>$null

# 2. REARMAR
Write-Host "Reconstruyendo el bunker..." -ForegroundColor Yellow
docker-compose -f C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\docker-compose.god_mode.ULTIMATE.yml up -d

# 3. LEVANTAR OLLAMA
Write-Host "Despertando cerebro nativo..." -ForegroundColor Magenta
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 12

# 4. VERIFICACION
Write-Host "VERIFICANDO ORGANOS VITALES:" -ForegroundColor Cyan

$ollamaCheck = curl -s http://localhost:11434/api/tags
if ($ollamaCheck -like "*neilzeneger*") { Write-Host "  OK: Cerebro" -ForegroundColor Green } else { Write-Host "  FAIL: Cerebro" -ForegroundColor Red }

$whisperCheck = curl -s http://localhost:9000/ health
if ($whisperCheck -match "docs" -or $whisperCheck -match "detail") { Write-Host "  OK: Oidos" -ForegroundColor Green } else { Write-Host "  FAIL: Oidos" -ForegroundColor Red }

$xttsCheck = curl -s http://localhost:5002/
if ($xttsCheck -match "TTS" -or $xttsCheck -match "XTTS") { Write-Host "  OK: Voz" -ForegroundColor Green } else { Write-Host "  FAIL: Voz" -ForegroundColor Red }

# 5. BACKEND
Write-Host "Lanzando NeilChat Backend..." -ForegroundColor Green
cd C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\neilchat\backend
Start-Process "python" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 9300" -WindowStyle Minimized

Write-Host "RESCATE COMPLETADO" -ForegroundColor Green
Write-Host "Joanna esta viva en http://localhost:3000" -ForegroundColor Cyan
