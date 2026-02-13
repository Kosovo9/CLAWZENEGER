import logging
import asyncio
from agents.base_agent import BaseAgent

class CodeGenerator:
    async def generate(self, prompt, language="python"):
        # Integration with LiteLLM/HF-Proxy would go here
        return f"# Generated {language} code for: {prompt}\nprint('Hello World 10X')"

class ProjectScaffolder:
    async def create_scaffold(self, project_name):
        return f"Scaffold for {project_name} ready."

class CoderAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("coder_10000x", config)
        self.code_gen = CodeGenerator()
        self.scaffolder = ProjectScaffolder()

    async def run(self):
        self.logger.info("Coder 10000X iniciado. Esperando tareas...")
        while True:
            try:
                task = await self.queue.listen(timeout=5)
                if task:
                    await self.process_task(task)
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                self.logger.error(f"Error en CoderAgent: {e}")
                await asyncio.sleep(5)

    async def process_task(self, task):
        action = task.get("action")
        self.logger.info(f"Procesando tarea: {action}")
        
        if action == "generate_code":
            code = await self.code_gen.generate(
                prompt=task.get("prompt", ""),
                language=task.get("language", "python")
            )
            task_id = task.get("id", "unknown")
            await self.remember(f"code_{task_id}", {"code": code, "task": task})
            
            if "requester" in task:
                await self.send_task(task["requester"], {"action": "code_ready", "result": code, "task_id": task_id})
        
        elif action == "scaffold_project":
            result = await self.scaffolder.create_scaffold(task.get("project_name", "new_project"))
            self.logger.info(result)

if __name__ == "__main__":
    agent = CoderAgent()
    asyncio.run(agent.run())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
