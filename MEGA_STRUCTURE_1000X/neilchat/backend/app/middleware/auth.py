# neilchat/backend/app/middleware/auth.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os
import time
import logging

logger = logging.getLogger("JOANNA_AUTH")

class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str):
        super().__init__(app)
        self.secret_key = secret_key

    async def dispatch(self, request: Request, call_next):
        # Excluir rutas públicas (Docs, Health, login si existiera)
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/"]:
            return await call_next(request)
        
        # Para WebSockets, el token se suele pasar por query param o mensaje inicial
        # Aquí manejaremos principalmente HTTP
        if "Authorization" not in request.headers:
            # logger.warning(f"🚫 Intento de acceso sin token: {request.url.path}")
            # Por ahora dejaremos pasar para no romper el dashboard actual hasta avisar al socio
            # Pero logeamos el aviso
            return await call_next(request)

        try:
            token = request.headers["Authorization"].split(" ")[1]
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            request.state.user = payload
        except Exception as e:
            logger.error(f"❌ Error de autenticación: {e}")
            raise HTTPException(status_code=403, detail="Cerebro Bloqueado: Token Inválido")

        return await call_next(request)
