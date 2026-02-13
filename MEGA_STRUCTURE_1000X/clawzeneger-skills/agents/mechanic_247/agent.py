
import asyncio
import docker
from ..base_agent import BaseAgent

class MechanicAgent(BaseAgent):
    def __init__(self, config):
        super().__init__("mechanic_247", config)
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            self.logger.error(f"Failed to connect to Docker: {e}")
            self.docker_client = None

    async def run(self):
        self.logger.info("Mecánico Todólogo 24/7 iniciado")
        while True:
            if self.docker_client:
                try:
                    containers = self.docker_client.containers.list()
                    self.logger.info(f"Monitoring {len(containers)} containers...")
                    for c in containers:
                        if c.status != 'running':
                            self.logger.warning(f"Container {c.name} is {c.status}")
                except Exception as e:
                     self.logger.error(f"Error monitoring docker: {e}")
            
            await asyncio.sleep(60)

if __name__ == "__main__":
    agent = MechanicAgent({})
    asyncio.run(agent.run())
