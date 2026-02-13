import redis
import json
import os

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

def publish(queue, message):
    redis_client.rpush(queue, json.dumps(message))

def subscribe(queue, block=True):
    if block:
        msg = redis_client.blpop(queue)
        if msg:
            return json.loads(msg[1])
    else:
        msg = redis_client.lpop(queue)
        if msg:
            return json.loads(msg)
    return None