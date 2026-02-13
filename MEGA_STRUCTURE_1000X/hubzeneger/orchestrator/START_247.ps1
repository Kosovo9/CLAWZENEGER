# 🦁 HUZENEGER ORCHESTRATOR 24/7 - AUTO-HEALER
# Autor: Huzeneger Omni-OS

$ORCHESTRATOR_PATH = "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\hubzeneger\orchestrator\orchestrator.py"

Write-Host "🚀 INICIANDO ORQUESTADOR HUZENEGER EN MODO 24/7..." -ForegroundColor Cyan

while ($true) {
    Write-Host "[$(Get-Date)] Despertando al Orquestador..." -ForegroundColor Green
    
    # Ejecutar el orquestador y esperar a que termine (si falla)
    python $ORCHESTRATOR_PATH
    
    Write-Host "[$(Get-Date)] ⚠️  El Orquestador se detuvo o falló. Reiniciando en 5 segundos..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}
