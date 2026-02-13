import psutil
import logging
import os

logger = logging.getLogger(__name__)

def get_host_stats():
    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "process_count": len(psutil.pids())
        }
    except Exception as e:
        logger.error(f"Error getting host stats: {e}")
        return {}

def get_container_info():
    # En entornos Docker, podemos intentar leer /proc o usar el socket si está mapeado
    # Por ahora devolvemos info básica de entorno
    return {
        "node_name": os.getenv("HOSTNAME", "unknown"),
        "env": "production"
    }
