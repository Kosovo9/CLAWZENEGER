import asyncio
import logging
from abc import ABC, abstractmethod
from shared.memory.chroma_client import ChromaMemory
from shared.messaging.redis_client import RedisQueue
from shared.personality import get_personality_instruction

class BaseAgent(ABC):
    def __init__(self, agent_name: str, config: dict = None):
        self.name = agent_name
        self.config = config or {}
        self.soul = get_personality_instruction(agent_name)
        self.memory = ChromaMemory(collection_name=f"agent_{agent_name}")
        self.queue = RedisQueue(f"queue:{agent_name}")
        self.logger = logging.getLogger(agent_name)
        self.logger.info(f"✨ Agente {agent_name} cargado con Soul de NEIL 1000X.")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    @abstractmethod
    async def run(self):
        pass

    async def remember(self, key: str, data: dict):
        self.memory.add(key, data)

    async def recall(self, query: str, n=5):
        return self.collection.query(query_texts=[query], n_results=n)

    async def send_task(self, target_agent: str, task: dict):
        # We assume queue name is formatted as queue:target_agent
        target_queue = RedisQueue(f"queue:{target_agent}")
        await target_queue.publish(task)
