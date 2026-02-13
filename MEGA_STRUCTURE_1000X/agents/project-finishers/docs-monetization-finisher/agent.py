import asyncio
import json
import os
import logging
from pathlib import Path
import redis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DocsMonetizationFinisher")

class DocsMonetizationFinisher:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)
        self.hf_proxy_url = os.getenv("HF_PROXY_URL", "http://hf-proxy:4000/v1")
        self.queue_name = "queue:docs_monetization_finisher"
        self.results_queue = "queue:finisher_results"

    async def run(self):
        logger.info(f"✨ Backend Finisher Agent iniciado. Escuchando en {self.queue_name}")
        while True:
            try:
                task_data = self.redis.blpop(self.queue_name, timeout=5)
                if task_data:
                    task = json.loads(task_data[1])
                    logger.info(f"📥 Nueva tarea recibida: {task.get('action')}")
                    await self.process_task(task)
            except Exception as e:
                logger.error(f"❌ Error en el loop principal: {e}")
                await asyncio.sleep(5)

    async def process_task(self, task):
        action = task.get("action")
        project_id = task.get("project_id")
        project_path = task.get("project_path")
        task_id = task.get("task_id")

        result = {
            "task_id": task_id,
            "project_id": project_id,
            "agent": "docs_monetization_finisher",
            "status": "processing",
            "details": {}
        }

        try:
            if action == "analyze":
                report = await self.analyze_project(project_path)
                result["status"] = "completed"
                result["details"] = report
            elif action == "fix_auth":
                # Lógica para integrar Supabase o similar
                result["status"] = "completed"
                result["details"] = {"message": "Auth integration logic triggered (Mock)"}
            elif action == "deploy_escrow":
                result["status"] = "completed"
                result["details"] = {"message": "Escrow deployment logic triggered (Mock)"}
            else:
                result["status"] = "failed"
                result["details"] = {"error": f"Acción '{action}' no soportada"}
        except Exception as e:
            logger.error(f"❌ Error procesando tarea {task_id}: {e}")
            result["status"] = "failed"
            result["details"] = {"error": str(e)}

        self.redis.rpush(self.results_queue, json.dumps(result))
        logger.info(f"📤 Resultado enviado para tarea {task_id}")

    async def analyze_project(self, path):
        # Escaneo básico de archivos backend
        p = Path(path)
        if not p.exists():
            return {"error": "Ruta no existe"}
        
        stubs = []
        for file in p.rglob("*"):
            if file.suffix in ['.py', '.ts', '.js', '.go']:
                try:
                    content = file.read_text(errors='ignore')
                    if "TODO" in content or "FIXME" in content or "mock" in content.lower() or "stub" in content.lower():
                        stubs.append(str(file.relative_to(p)))
                except:
                    continue
        
        return {
            "files_analyzed": len(list(p.rglob("*"))),
            "potential_stubs": stubs,
            "backend_tech": "Detected Tech Stack Info"
        }

if __name__ == "__main__":
    agent = DocsMonetizationFinisher()
    asyncio.run(agent.run())
