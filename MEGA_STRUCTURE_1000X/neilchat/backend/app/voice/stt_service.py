"""Servicio de Transcripción (Oídos de Joanna)"""
import aiohttp
import asyncio
import logging
import os
import tempfile

logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        # Usar el host de docker interno o localhost si falla
        self.whisper_url = os.getenv("WHISPER_URL", "http://whisper:9000")
        
    async def transcribe(self, audio_bytes: bytes, language: str = "es") -> str:
        """
        Convierte audio a texto usando Whisper
        """
        temp_path = None
        try:
            # Guardar audio temporalmente
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
                f.write(audio_bytes)
                temp_path = f.name
                
            # Enviar a Whisper
            async with aiohttp.ClientSession() as session:
                with open(temp_path, 'rb') as audio_file:
                    form_data = aiohttp.FormData()
                    form_data.add_field('audio_file', 
                                       audio_file,
                                       filename='audio.webm',
                                       content_type='audio/webm')
                    form_data.add_field('language', language)
                    form_data.add_field('task', 'transcribe')
                    
                    async with session.post(
                        f"{self.whisper_url}/asr",
                        data=form_data,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            text = result.get('text', '')
                            logger.info(f"🎤 Transcripción Exitosa: {text[:50]}...")
                            return text
                        else:
                            resp_text = await response.text()
                            logger.error(f"Error Whisper ({response.status}): {resp_text}")
                            return ""
                            
        except Exception as e:
            logger.error(f"Error en transcripción STT: {e}")
            return ""
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except: pass

stt_service = STTService()
