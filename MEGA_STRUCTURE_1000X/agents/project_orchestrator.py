import json
import os
import redis
import logging
import uuid
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProjectOrchestrator")

class ProjectOrchestrator:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)
        self.projects_config_path = "projects_config.json"
        self.agents = {
            "backend": "queue:backend_finisher",
            "frontend": "queue:frontend_finisher",
            "devops": "queue:devops_finisher",
            "qa": "queue:qa_finisher",
            "docs": "queue:docs_metodization_finisher"
        }

    def load_projects(self):
        if Path(self.projects_config_path).exists():
            with open(self.projects_config_path, 'r') as f:
                return json.load(f)
        return []

    def dispatch_full_pipeline(self, project):
        project_id = project.get("id")
        project_path = project.get("path")
        
        logger.info(f"🚀 Iniciando pipeline completo para: {project.get('name')}")
        
        for agent_name, queue in self.agents.items():
            task = {
                "task_id": str(uuid.uuid4()),
                "project_id": project_id,
                "project_path": project_path,
                "action": "analyze_and_fix",
                "metadata": project.get("metadata", {})
            }
            self.redis.rpush(queue, json.dumps(task))
            logger.info(f"  - Tarea enviada a {agent_name} ({queue})")

    def run(self):
        projects = self.load_projects()
        if not projects:
            logger.warning("⚠️ No se encontraron proyectos para procesar en projects_config.json")
            return

        for project in projects:
            if project.get("status") == "pending":
                self.dispatch_full_pipeline(project)
                # Opcional: marcar como 'processing' en la config
                
if __name__ == "__main__":
    orchestrator = ProjectOrchestrator()
    orchestrator.run()
