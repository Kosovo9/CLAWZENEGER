import asyncio
import json
import os
import logging
import redis
import signal

class BaseAgent:
    def __init__(self, agent_name, config=None):
        self.agent_name = agent_name
        self.config = config or {}
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)
        self.queue_name = f"queue:{agent_name}"
        self.logger = logging.getLogger(agent_name)
        self.logger.setLevel(logging.INFO)
        
        # Handler to avoid duplicate logs if already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    async def listen(self, timeout=5):
        """Escucha la cola de Redis para nuevas tareas"""
        try:
            task_data = self.redis.blpop(self.queue_name, timeout=timeout)
            if task_data:
                return json.loads(task_data[1])
        except Exception as e:
            self.logger.error(f"Error listening to queue: {e}")
        return None

    async def send_task(self, target_queue, task):
        """Envía una tarea a otra cola"""
        try:
            self.redis.rpush(target_queue, json.dumps(task))
            return True
        except Exception as e:
            self.logger.error(f"Error sending task to {target_queue}: {e}")
        return False

    async def run(self):
        """Metodo principal a sobreescribir"""
        raise NotImplementedError("Subclasses must implement run()")
