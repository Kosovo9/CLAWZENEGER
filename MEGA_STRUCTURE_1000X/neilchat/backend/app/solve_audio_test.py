import httpx
import asyncio
import os
import json
from datetime import datetime

async def solve_audio_test():
    prompt = "Hola Joanna, ¿cómo estás? Dime cuál es tu modelo y qué fecha es el día de hoy, por favor."
    print(f"📥 Procesando comando del Socio: '{prompt}'")
    
    # 1. RAZONAMIENTO (Joanna Brain)
    litellm_url = "http://localhost:4000/v1/chat/completions"
    api_key = "sk-clawzeneger-master-2026-prod-secret"
    
    print("🧠 Joanna está pensando...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            litellm_url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "ollama/neilzeneger:latest",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        
        if response.status_code == 200:
            text_resp = response.json()['choices'][0]['message']['content']
        else:
            print(f"⚠️ LiteLLM Falló ({response.status_code}). Intentando conexión directa con Ollama...")
            # Fallback directo a Ollama
            ollama_url = "http://localhost:11434/api/generate"
            async with httpx.AsyncClient(timeout=60.0) as client_ollama:
                resp_ollama = await client_ollama.post(
                    ollama_url,
                    json={
                        "model": "neilzeneger:latest",
                        "prompt": prompt,
                        "stream": False
                    }
                )
                if resp_ollama.status_code == 200:
                    text_resp = resp_ollama.json().get('response', '')
                else:
                    print(f"❌ Error Crítico en Ollama: {resp_ollama.status_code}")
                    return
        
        print(f"🧠 Respuesta Joanna: {text_resp}")

    # 2. VOZ (XTTS Synthesis)
    xtts_url = "http://localhost:5002/api/tts"
    print("🎤 Sintetizando voz de Joanna (Paisa 3000%)...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # XTTS espera 'text', 'speaker_id' y 'language_id' en form-data según los logs previos
        resp_voice = await client.post(
            xtts_url,
            data={
                "text": text_resp,
                "speaker_id": "Ana Florence",
                "language_id": "es"
            }
        )
        
        if resp_voice.status_code == 200:
            audio_path = r"C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\temp_audio_test.wav"
            with open(audio_path, "wb") as f:
                f.write(resp_voice.content)
            print(f"✅ Audio generado en: {audio_path}")
            print(f"TEXTO_FINAL: {text_resp}")
        else:
            print(f"❌ Error en Voz: {resp_voice.status_code} - {resp_voice.text}")

if __name__ == "__main__":
    asyncio.run(solve_audio_test())
