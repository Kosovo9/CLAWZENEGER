import json
import os
import redis
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ResultListener")

class ResultListener:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)
        self.results_queue = "queue:finisher_results"

    def run(self):
        logger.info(f"👂 Escuchando resultados de agentes en {self.results_queue}...")
        while True:
            try:
                result_data = self.redis.blpop(self.results_queue, timeout=5)
                if result_data:
                    result = json.loads(result_data[1])
                    agent = result.get("agent")
                    status = result.get("status")
                    project_id = result.get("project_id")
                    
                    if status == "completed":
                        logger.info(f"✅ [{agent}] Proyecto {project_id} procesado con éxito.")
                    elif status == "failed":
                        logger.error(f"❌ [{agent}] Proyecto {project_id} falló: {result.get('details', {}).get('error')}")
                    else:
                        logger.info(f"⏳ [{agent}] Proyecto {project_id} en estado: {status}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"❌ Error en listener: {e}")

if __name__ == "__main__":
    listener = ResultListener()
    listener.run()
