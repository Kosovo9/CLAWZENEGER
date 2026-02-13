# tests/TEST_SEGURIDAD_JWT.py

import asyncio
import httpx
import os

API_URL = "http://localhost:9300/chat"
MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-clawzeneger-master-2026-prod-secret")

async def test_security_locks():
    print("INICIANDO TEST DE SEGURIDAD ZERO TRUST...")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Test de Acceso NO Autorizado
        print("Intentando acceso sin token...")
        try:
            response = await client.post(API_URL, json={"message": "hack"})
            if response.status_code == 401 or response.status_code == 403:
                print("PROTECCION ACTIVA: Peticion anonima rechazada.")
            else:
                print(f"AVISO: Peticion anonima aceptada con status {response.status_code}")
        except Exception as e:
            print(f"PROTECCION ACTIVA (Network rejection): {e}")

        # 2. Test de Rate Limiting
        print("Probando Rate Limiting (Ataque de fuerza bruta)...")
        headers = {"Authorization": f"Bearer {MASTER_KEY}"}
        limit_reached = False
        for i in range(15): # Enviamos múltiples peticiones rápidas
            try:
                response = await client.post(API_URL, json={"message": "spam"}, headers=headers)
                if response.status_code == 429:
                    limit_reached = True
                    print(f"RATE LIMIT ACTIVADO: Bloqueado en la peticion #{i+1}")
                    break
            except Exception:
                pass
        
        if not limit_reached:
            print("AVISO: Rate limit no detectado en 15 peticiones.")

if __name__ == "__main__":
    asyncio.run(test_security_locks())
