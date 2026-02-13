
import json
import os
import redis.asyncio as redis

class RedisQueue:
    def __init__(self, queue_name: str):
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self.queue_name = queue_name
        self.redis = redis.from_url(self.redis_url, decode_responses=True)

    async def publish(self, target_queue: str, message: dict):
        """Push a message to a specific queue"""
        await self.redis.rpush(target_queue, json.dumps(message))

    async def listen(self):
        """Pop a message from this agent's queue (non-blocking for demo, or blocking via blpop)"""
        # Using lpop for non-blocking check
        item = await self.redis.lpop(self.queue_name)
        if item:
            return json.loads(item)
        return None
