import hashlib
import base64
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from .config import settings

def generate_referral_code(user_id: str) -> str:
    """Genera un código de 8 caracteres basado en el user_id"""
    hash_obj = hashlib.sha256(user_id.encode())
    code = base64.urlsafe_b64encode(hash_obj.digest()[:6]).decode().rstrip("=")
    return f"CLAW_{code.upper()}"

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        # Para desarrollo, si no hay token, devolvemos un ID de prueba
        # TODO: En producción, requerir token real
        return "test-user-uuid"
        # raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
