# neilchat/backend/app/core/model_pool.py

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
import json
import redis.asyncio as redis
import httpx
import os
from litellm import acompletion

logger = logging.getLogger("JOANNA_MODEL_POOL")

class ModelPool:
    """Gestiona la precarga y el serving de modelos para Joanna 3000%"""
    
    def __init__(self):
        self.redis = None
        self.ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
        self.master_key = os.getenv("LITELLM_MASTER_KEY")
        self.default_model = "neilzeneger:latest" 
        self.loaded_models = set()

    async def initialize(self):
        """Conecta a Redis y arranca el warmup"""
        self.redis = await redis.from_url(
            f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST', 'redis')}:6379/0",
            decode_responses=True
        )
        logger.info("🔥 Synaptic ModelPool Online. Iniciando Warmup...")
        asyncio.create_task(self.warmup_models())

    async def warmup_models(self):
        """Precarga los modelos en GPU para Latencia 0"""
        models_to_warm = [self.default_model]
        async with httpx.AsyncClient(timeout=60.0) as client:
            for model in models_to_warm:
                try:
                    logger.info(f"🧠 Calentando neuronas para: {model}")
                    # Una llamada rápida para forzar la carga en VRAM
                    await acompletion(
                        model=f"ollama/{model}",
                        messages=[{"role": "user", "content": "ping"}],
                        max_tokens=1,
                        api_base=self.ollama_url,
                        api_key=self.master_key
                    )
                    self.loaded_models.add(model)
                    logger.info(f"✅ Modelo {model} listo para combate.")
                except Exception as e:
                    logger.warning(f"⚠️ Fallo en warmup de {model}: {e}")

    async def get_response(self, messages: List[Dict], user_id: str, stream: bool = False):
        """Gateway unificado para el cerebro de Joanna"""
        return await acompletion(
            model=f"ollama/{self.default_model}",
            messages=messages,
            stream=stream,
            api_base=self.ollama_url,
            api_key=self.master_key,
            user=user_id
        )

# Singleton
model_pool = ModelPool()
