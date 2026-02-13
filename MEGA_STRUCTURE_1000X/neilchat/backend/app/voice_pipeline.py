# neilchat/backend/app/voice_pipeline.py

import os
import httpx
import logging
import base64
import hashlib
import redis.asyncio as redis
from typing import Optional

logger = logging.getLogger("JOANNA_VOICE_3000")

class VoicePipeline:
    """Pipeline de voz con caché de nivel industrial"""
    
    def __init__(self, whisper_url: str, xtts_url: str):
        self.whisper_url = whisper_url.rstrip("/")
        self.xtts_url = xtts_url.rstrip("/")
        self.redis = None
        self.speaker_id = "Ana Florence" # Voz estable en español
        self.language = "es"

    async def initialize(self):
        """Conecta a Redis para el caché de audio"""
        self.redis = await redis.from_url(
            f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST', 'redis')}:6379/0"
        )
        logger.info("🎤 Voice Pipeline 3000% Online.")

    async def text_to_speech(self, text: str) -> Optional[bytes]:
        """Convierte texto a voz con optimización de caché"""
        if not text.strip(): return None
        
        # 1. Generar Hash para el caché
        text_hash = hashlib.md5(f"{text}:{self.speaker_id}".encode()).hexdigest()
        cache_key = f"tts_cache:{text_hash}"
        
        # 2. Verificar en Redis
        if self.redis:
            cached_audio = await self.redis.get(cache_key)
            if cached_audio:
                logger.info(f"💎 Cache Hit para: {text[:20]}...")
                return cached_audio

        # 3. Síntesis Real si no hay caché
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                logger.info(f"🗣️ Sintetizando (Real): {text[:20]}...")
                response = await client.post(
                    f"{self.xtts_url}/api/tts",
                    data={
                        "text": text,
                        "speaker_id": self.speaker_id,
                        "language_id": self.language
                    }
                )
                if response.status_code == 200:
                    audio_bytes = response.content
                    # Guardar en caché (Expira en 24h para no saturar Redis)
                    if self.redis:
                        await self.redis.setex(cache_key, 86400, audio_bytes)
                    return audio_bytes
                else:
                    logger.error(f"❌ Error en XTTS: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            logger.error(f"🔥 Fallo crítico de voz: {e}")
            return None

    async def speech_to_text(self, audio_data: bytes) -> Optional[str]:
        """Transcripción ultra-rápida vía Whisper"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"audio_file": ("audio.wav", audio_data, "audio/wav")}
                response = await client.post(f"{self.whisper_url}/asr", files=files)
                if response.status_code == 200:
                    return response.json().get("text", "").strip()
                return None
        except Exception as e:
            logger.error(f"👂 Error de audición: {e}")
            return None
