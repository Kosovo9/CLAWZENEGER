import psutil
import time
import docker
import os
import logging
import socket

# 🔧 JOANNA GUARDIAN V2 (SYNAPTIC ARCHITECT EDITION)
# Misión: Inmortalidad sistémica. Monitorización real vía Docker Socket.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GUARDIAN_1000X")

# Configuración de contenedores por nombre de servicio en la red
SERVICES = {
    "neilchat-backend": {"port": 9300, "container": "claw-neilchat-backend"},
    "ollama": {"port": 11434, "container": "claw-brain-ollama"},
    "hf-proxy": {"port": 4000, "container": "claw-brain-hfproxy"},
    "redis": {"port": 6379, "container": "claw-cache-redis"},
}

try:
    client = docker.from_env()
    logger.info("✅ Conexión con Docker Engine establecida.")
except Exception as e:
    logger.critical(f"❌ Fallo al conectar con Docker Socket: {e}")
    client = None

def check_service(host: str, port: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            return s.connect_ex((host, port)) == 0
    except:
        return False

def protect_the_bunker():
    while True:
        if not client:
            logger.error("Cierre del Guardian: No hay acceso a Docker.")
            break
            
        for name, cfg in SERVICES.items():
            # 1. Chequeo de Puerto (Red Interna)
            is_up = check_service(name, cfg["port"])
            
            if not is_up:
                logger.warning(f"⚠️ {name} no responde en el puerto {cfg['port']}. Verificando estado del contenedor...")
                try:
                    container = client.containers.get(cfg["container"])
                    if container.status != "running":
                        logger.info(f"🔄 Reiniciando contenedor {cfg['container']} (Status: {container.status})...")
                        container.restart()
                        logger.info(f"✅ {name} restaurado.")
                    else:
                        logger.warning(f"🧟 {name} está 'running' pero no responde. Reinicio forzado...")
                        container.restart()
                except Exception as e:
                    logger.error(f"Fallo al sanar {name}: {e}")
        
        # 2. Gestión de Recursos (Synaptic Level)
        mem = psutil.virtual_memory().percent
        if mem > 95:
            logger.critical(f"🚨 MEMORIA CRÍTICA: {mem}%. Ejecutando protocolo de purga...")
            client.containers.prune()
            client.images.prune(filters={'dangling': True})
            
        time.sleep(15)

if __name__ == "__main__":
    logger.info("🛡️ THE SYNAPTIC GUARDIAN: Iniciando vigilancia eterna.")
    protect_the_bunker()
