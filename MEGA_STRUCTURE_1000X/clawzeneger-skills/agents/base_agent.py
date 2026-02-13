
import asyncio
import logging
from abc import ABC, abstractmethod
import os

class BaseAgent(ABC):
    def __init__(self, agent_name: str, config: dict):
        self.name = agent_name
        self.config = config
        self.logger = logging.getLogger(agent_name)
        logging.basicConfig(level=logging.INFO)

    @abstractmethod
    async def run(self):
        """Bucle principal del agente"""
        pass

    async def remember(self, key: str, data: dict):
        """Guardar en memoria a largo plazo (Mock)"""
        self.logger.info(f"[{self.name}] Remembering {key}: {str(data)[:50]}...")
        # In real impl, call ChromaDB here

    async def send_task(self, target_agent: str, task: dict):
        """Enviar tarea a otro agente (Mock)"""
        self.logger.info(f"[{self.name}] Sending task to {target_agent}: {task}")
        # In real impl, publish to Redis here
