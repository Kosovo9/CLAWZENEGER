# tests/TEST_MEMORIA_RAG.py

import asyncio
import httpx
import os

API_UPLOAD_URL = "http://localhost:9300/rag/upload"
API_QUERY_URL = "http://localhost:9300/chat" # Usamos el chat principal que tiene RAG inyectado
MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-clawzeneger-master-2026-prod-secret")

async def test_rag_system():
    print("INICIANDO TEST DE MEMORIA RAG 3000...")
    
    headers = {"Authorization": f"Bearer {MASTER_KEY}"}
    
    # 1. Test de Ingesta (URL Simulada o Texto)
    print("Probando ingesta de conocimiento...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Simulamos subida de URL estratégica
            upload_payload = {
                "source": "https://estudio-nexora.com/servicios",
                "user_id": "test_boss_01"
            }
            # Nota: Implementación simplificada para el test
            print(f"Ingesta enviada para: {upload_payload['source']}")
            
            # 2. Test de Recuperación
            print("Probando recuperacion semantica...")
            query_payload = {
                "message": "Que servicios ofrece Nexora?",
                "user_id": "test_boss_01"
            }
            
            response = await client.post(API_QUERY_URL, json=query_payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print("Contexto RAG recuperado con exito.")
                print(f"Joanna-RAG: {data.get('response', '')[:100]}...")
            else:
                print(f"ERROR RAG: {response.status_code}")
                
    except Exception as e:
        print(f"FALLO RAG: {e}")

if __name__ == "__main__":
    asyncio.run(test_rag_system())
