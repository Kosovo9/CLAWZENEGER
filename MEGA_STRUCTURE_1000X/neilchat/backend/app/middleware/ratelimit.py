# neilchat/backend/app/middleware/ratelimit.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
import os
import time
import logging

logger = logging.getLogger("JOANNA_LIMIT")

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, limit: int = 60, window: int = 60):
        super().__init__(app)
        self.redis = redis.from_url(redis_url)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        try:
            count = await self.redis.incr(key)
            if count == 1:
                await self.redis.expire(key, self.window)
            
            if count > self.limit:
                logger.warning(f"🔥 Rate limit excedido para: {client_ip}")
                raise HTTPException(status_code=429, detail="Latencia de Seguridad: Demasiadas peticiones.")
        except HTTPException: raise
        except Exception as e:
            logger.error(f"⚠️ Error en Rate Limit: {e}")
            
        return await call_next(request)
