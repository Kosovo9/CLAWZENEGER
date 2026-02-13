import requests
import time
import subprocess
import os

# 🔧 SUPER-BOT MECÁNICO 24/7 - AUTO-HEALER & OPTIMIZER
# Autor: Huzeneger Omni-OS
# Misión: Monitorear el estado del sistema y autoreparar fallos de conexión o procesos caídos.

SERVICES_TO_CHECK = {
    "ORCHESTRATOR": "http://localhost:54321/",
    "UI": "http://localhost:44444/",
    "XTTS": "http://localhost:5002/",
    "CHAT": "http://localhost:56789/"
}

def repair_orchestrator():
    print("🔧 [MECÁNICO] Detectado fallo en Orquestador. Reiniciando proceso...")
    ps_command = r'powershell -WindowStyle Minimized -File "C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\hubzeneger\orchestrator\START_247.ps1"'
    subprocess.Popen(ps_command, shell=True)
    time.sleep(5)

def repair_ui():
    print("🌐 [MECÁNICO] Detectado fallo en UI Server. Reiniciando...")
    cmd = r'powershell -WindowStyle Minimized -Command "python C:\CLAWZENEGER\CLAWZENEGER-UI\ui_server.py"'
    subprocess.Popen(cmd, shell=True)
    time.sleep(3)

def check_and_fix():
    print("🦁 [SUPER-BOT] Iniciando ronda de inspección...")
    
    for service, url in SERVICES_TO_CHECK.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service}: LÍNEA")
            else:
                print(f"⚠️ {service}: STATUS {response.status_code}")
        except Exception as e:
            print(f"❌ {service}: OFFLINE. Iniciando protocolo de reparación...")
            if service == "ORCHESTRATOR":
                repair_orchestrator()
            elif service == "UI":
                repair_ui()
            else:
                print(f"💡 Sugerencia: Revisa los contenedores Docker para {service}")

if __name__ == "__main__":
    while True:
        check_and_fix()
        # VIGILANCIA CONTINUA - SIN DESCANSOS
