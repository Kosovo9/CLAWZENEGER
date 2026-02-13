# tests/TEST_CEREBRO_3000.py

import asyncio
import time
import httpx
import os

API_URL = "http://localhost:9300/chat"
MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-clawzeneger-master-2026-prod-secret")

async def test_brain_performance():
    print("INICIANDO TEST DE CEREBRO 3000 (ModelPool)...")
    
    headers = {
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": "¿Cuál es tu estrategia de ROI para Neil?",
        "user_id": "test_boss_01"
    }
    
    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                latency = time.time() - start_time
                data = response.json()
                print(f"Respuesta Recibida en {latency:.2f}s")
                print(f"Joanna: {data.get('response', '')[:100]}...")
                
                if latency < 1.0:
                    print("EXCELENCIA: Latencia sub-segundo (Warmup OK)")
                else:
                    print(f"AVISO: Latencia de {latency:.2f}s - Revisar ModelPool")
            else:
                print(f"ERROR: Status {response.status_code} - {response.text}")
    except Exception as e:
        print(f"FALLO CRITICO: {e}")

if __name__ == "__main__":
    asyncio.run(test_brain_performance())
