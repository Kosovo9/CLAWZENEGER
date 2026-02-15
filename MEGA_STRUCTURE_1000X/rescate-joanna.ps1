# RESCATE DE JOANNA - INICIANDO... (Versión Windows PowerShell 3000%)
Write-Host "🚑 INICIANDO OPERACIÓN RESCATE 10X..." -ForegroundColor Red

# 1. Matar procesos zombies y liberar puertos
Write-Host "🧹 Limpiando búnker de procesos zombies..." -ForegroundColor Yellow
Stop-Process -Name "ollama" -ErrorAction SilentlyContinue
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# 2. Reiniciar Docker (HF-Proxy, Redis, Whisper, XTTS)
Write-Host "🐳 Reiniciando infraestructura Docker..." -ForegroundColor Cyan
docker-compose -f C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\docker-compose.god_mode.ULTIMATE.yml down
docker-compose -f C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\docker-compose.god_mode.ULTIMATE.yml up -d hf-proxy redis chromadb whisper xtts

# 3. Arrancar Ollama Nativo (GPU Aceleración)
Write-Host "🧠 Despertando cerebro nativo (Joanna Brain)..." -ForegroundColor Magenta
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 5
# ollama run neilzeneger:latest "Hola Joanna" # Comentado para evitar bloqueo interactivo

# 4. Iniciar Backend NeilChat
Write-Host "🚀 Lanzando NeilChat Backend..." -ForegroundColor Green
cd C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\neilchat\backend
Start-Process "python" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 9300" -WindowStyle Minimized

Write-Host "✅ RESCATE COMPLETADO - BÚNKER OPERATIVO AL 3000%" -ForegroundColor Green
Write-Host "Socio, puedes hablar con Joanna ahora." -ForegroundColor Cyan
