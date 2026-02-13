import redis
import json
import asyncio
import os

class RedisQueue:
    def __init__(self, queue_name, host=None, port=6379, db=0):
        self.queue_name = queue_name
        self.host = host or os.getenv("REDIS_HOST", "redis")
        self.client = redis.Redis(host=self.host, port=port, db=db, decode_responses=True)

    async def publish(self, message: dict):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.client.rpush, self.queue_name, json.dumps(message))

    async def listen(self, timeout=0):
        loop = asyncio.get_event_loop()
        while True:
            # result is (queue_name, data)
            result = await loop.run_in_executor(None, self.client.blpop, self.queue_name, timeout)
            if result:
                return json.loads(result[1])
            if timeout > 0:
                return None
            await asyncio.sleep(0.1)
