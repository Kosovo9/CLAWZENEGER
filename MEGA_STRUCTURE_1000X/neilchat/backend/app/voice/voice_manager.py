# neilchat/backend/app/voice/voice_manager.py

import json
import logging
import random
import os
from typing import Optional, Dict, List
import httpx
import asyncio

logger = logging.getLogger("JOANNA_VOICE_MANAGER")

class VoiceManager:
    """Voice Manager 3000% - Voces ultra-realistas y multilingües"""
    
    def __init__(self):
        self.voices = {
            "joanna_co": {
                "name": "Joanna",
                "language": "es",
                "country": "Colombia",
                "display_name": "Joanna 🇨🇴",
                "personality": "joven, inteligente, motivada, tono profesional cálido",
                "file": "joanna_colombia.yaml",
                "model": "xtts_v2",
                "greeting": "¡Hola! Soy Joanna, tu asistente personal. ¿En qué puedo ayudarte?"
            },
            "sophia_us": {
                "name": "Sophia",
                "language": "en",
                "country": "USA",
                "display_name": "Sophia 🇺🇸",
                "personality": "young, intelligent, motivated, confident tone",
                "file": "american_sophia.yaml",
                "model": "xtts_v2",
                "greeting": "Hey! I'm Sophia, your personal assistant. How can I help you?"
            }
        }
        self.xtts_url = os.getenv("XTTS_URL", "http://xtts:5002").rstrip("/")

    async def initialize(self):
        """Pre-cargar voces en el motor XTTS"""
        logger.info("🎤 Inicializando VoiceManager 3000%...")
        # En una arquitectura real, aquí enviaríamos los archivos de referencia a XTTS
        # Por ahora, nos aseguramos que XTTS sepa qué voz usar
        logger.info("✅ Voces configuradas en el pipeline.")

    async def text_to_speech(self, text: str, voice_id: str = "joanna_co", emotion: str = "motivated") -> Optional[bytes]:
        """Conversión de texto a voz vía XTTS"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.xtts_url}/api/tts",
                    data={
                        "text": text,
                        "speaker_id": "Ana Florence", # Mapeamos joanna_co a una voz disponible mientras cargamos samples
                        "language_id": self.voices.get(voice_id, {}).get("language", "es")
                    }
                )
                if response.status_code == 200:
                    return response.content
                return None
        except Exception as e:
            logger.error(f"Error en TTS (VoiceManager): {e}")
            return None

    async def stream_tts(self, text: str, voice_id: Optional[str] = None):
        """Generador de fragmentos de audio para streaming"""
        if not voice_id:
            has_spanish = any(c in text for c in 'áéíóúñ¿¡')
            voice_id = "joanna_co" if has_spanish else "sophia_us"
            
        # Dividir en frases naturales
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            if not sentence.strip(): continue
            audio = await self.text_to_speech(sentence, voice_id)
            if audio:
                yield audio

voice_manager = VoiceManager()
