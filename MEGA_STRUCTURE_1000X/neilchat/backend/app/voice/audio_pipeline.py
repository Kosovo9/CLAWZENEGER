"""Pipeline completo de audio - Joanna escucha Y habla (Versión 3000% NeilChat)"""
import asyncio
import base64
import io
import wave
import logging
import os
from typing import Optional
import httpx
import numpy as np

logger = logging.getLogger(__name__)

class AudioPipeline:
    def __init__(self):
        # Usar variables de entorno o fallbacks del búnker
        self.stt_url = os.getenv("WHISPER_URL", "http://whisper:9000")
        self.tts_url = os.getenv("XTTS_URL", "http://xtts:5002")
        self.sample_rate = 16000
        
    async def process_audio_input(self, audio_bytes: bytes) -> str:
        """Procesa audio entrante (voz del usuario) -> texto vía Whisper"""
        try:
            logger.info(f"🎤 Procesando audio para Whisper en {self.stt_url}...")
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"audio_file": ("audio.wav", audio_bytes, "audio/wav")}
                response = await client.post(f"{self.stt_url}/asr", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    text = result.get("text", "").strip()
                    logger.info(f"🎤 Whisper captó: {text}")
                    return text
                else:
                    logger.error(f"❌ Error STT: {response.status_code}")
                    return ""
        except Exception as e:
            logger.error(f"❌ Error fatal en proceso de audio: {e}")
            return ""
            
    async def generate_audio_output(self, text: str, voice: str = "Ana Florence") -> Optional[bytes]:
        """Genera audio de respuesta (voz de Joanna) vía XTTS"""
        try:
            logger.info(f"🔊 Sintetizando voz de Joanna para: '{text[:50]}...'")
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self.tts_url}/api/tts",
                    data={
                        "text": text,
                        "speaker_id": voice,
                        "language_id": "es"
                    }
                )
                if resp.status_code == 200:
                    return resp.content
                else:
                    logger.error(f"❌ Error TTS: {resp.status_code}")
                    return None
        except Exception as e:
            logger.error(f"❌ Error fatal generando voz: {e}")
            return None

audio_pipeline = AudioPipeline()
