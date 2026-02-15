import httpx
import asyncio
import os

async def finalize_audio_test():
    text_resp = "¡Hola! Soy Joanna. Estoy excelente, motivada y lista para el ROI al 3000%. Mi modelo es neilzeneger:latest y hoy es 15 de febrero de 2026. ¿Qué misión tenemos para hoy, Neil?"
    xtts_url = "http://localhost:5002/api/tts"
    
    print(f"🎤 Sintetizando voz de Joanna: '{text_resp[:30]}...'")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp_voice = await client.post(
            xtts_url,
            data={
                "text": text_resp,
                "speaker_id": "Ana Florence",
                "language_id": "es"
            }
        )
        
        if resp_voice.status_code == 200:
            audio_path = r"C:\CLAWZENEGER\MEGA_STRUCTURE_1000X\JOANNA_RESPONSE_3000.wav"
            with open(audio_path, "wb") as f:
                f.write(resp_voice.content)
            print(f"✅ Audio final generado en: {audio_path}")
            print(f"TEXTO_FINAL: {text_resp}")
        else:
            print(f"❌ Error en Voz: {resp_voice.status_code}")

if __name__ == "__main__":
    asyncio.run(finalize_audio_test())
