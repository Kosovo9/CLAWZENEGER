@echo off
echo ==================================================
echo   CLAWZENEGER OMEGA 1000X - PROJECT FINISHER
echo ==================================================
echo.
echo 1. Levantando agentes especializados (Docker)...
docker-compose -f docker-compose.finishers.yml up -d

echo.
echo 2. Iniciando Orquestador...
python project_orchestrator.py

echo.
echo 3. Escuchando resultados (Ctrl+C para salir)...
python result_listener.py
pause
