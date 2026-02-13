# tests/TEST_VOZ_JOANNA.py

import asyncio
import time
import httpx
import os
import base64

API_TTS_URL = "http://localhost:9300/voice/tts" # Puerto del backend orchestrator
MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-clawzeneger-master-2026-prod-secret")

async def test_joanna_voice():
    print("INICIANDO TEST DE VOZ JOANNA (Paisa Mode)...")
    
    headers = {
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    }
    
    phrase = "Hola Socio! Estoy lista para cerrar estas ventas por ti. Hacemos plata hoy o que?"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Prueba 1: Generación Fría
        print(f"Generando audio (Cold Start): '{phrase[:30]}...'")
        start_time = time.time()
        response = await client.post(API_TTS_URL, json={"text": phrase, "voice_id": "joanna_co"}, headers=headers)
        
        if response.status_code == 200:
            cold_latency = time.time() - start_time
            print(f"Audio generado en {cold_latency:.2f}s")
            
            # Prueba 2: Generación desde Caché Redis
            print("Probando Cache de Voz (Redis)...")
            start_time = time.time()
            response_cached = await client.post(API_TTS_URL, json={"text": phrase, "voice_id": "joanna_co"}, headers=headers)
            
            if response_cached.status_code == 200:
                warm_latency = time.time() - start_time
                print(f"Respuesta desde CACHE en {warm_latency:.2f}s")
                
                if warm_latency < 0.1:
                    print("EXCELENCIA: Cache de Voz operando a baja latencia.")
                else:
                    print(f"Aviso: Latencia de cache mejorable: {warm_latency:.2f}s")
        else:
            print(f"ERROR VOZ: {response.status_code} - {response.text}")

if __name__ == "__main__":
    asyncio.run(test_joanna_voice())
