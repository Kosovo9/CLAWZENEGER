"""
Joanna Eterna - El alma inmortal de CLAWZENEGER.
Memoria histórica, evolución de personalidad y aprendizaje proactivo.
"""
import json
import time
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class JoannaEterna:
    """
    Gestiona la memoria infinita y la evolución de Joanna.
    Combina Redis (memoria volátil/reciente) con ChromaDB (memoria eterna).
    Inicialización lazy para tolerancia a fallos de red.
    """
    
    def __init__(self):
        self._redis = None
        self._chroma_client = None
        self._collection = None
        self._embedder = None
        self._initialized = False

    def _ensure_initialized(self):
        """Inicializa conexiones de forma lazy."""
        if self._initialized:
            return True
        try:
            import redis.asyncio as aioredis
            import chromadb
            
            redis_host = os.getenv("REDIS_HOST", "redis")
            redis_port = int(os.getenv("REDIS_PORT", 6379))
            redis_password = os.getenv("REDIS_PASSWORD", "")
            self._redis = aioredis.Redis(
                host=redis_host, port=redis_port,
                password=redis_password if redis_password else None,
                decode_responses=False
            )
            
            chroma_host = os.getenv("CHROMA_HOST", "chromadb")
            chroma_port = int(os.getenv("CHROMA_PORT", 8000))
            self._chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
            
            self._collection = self._chroma_client.get_or_create_collection(
                name="joanna_recuerdos",
                metadata={"description": "Memoria de largo plazo de Joanna Zeneger"}
            )
            
            from sentence_transformers import SentenceTransformer
            self._embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            self._initialized = True
            logger.info("JoannaEterna: Memoria Eterna ACTIVADA")
            return True
        except Exception as e:
            logger.warning(f"JoannaEterna: Esperando servicios... ({e})")
            return False

    async def registrar_interaccion(self, user_id: str, mensaje: str, respuesta: str, emocion: str = "neutral"):
        """Graba la interaccion en la memoria eterna y actualiza la personalidad."""
        if not self._ensure_initialized():
            return
        try:
            timestamp = time.time()
            interaccion = {
                "ts": timestamp,
                "dt": datetime.now().isoformat(),
                "uid": user_id,
                "msg": mensaje,
                "res": respuesta,
                "emo": emocion
            }
            await self._redis.lpush(f"joanna:diario:{user_id}", json.dumps(interaccion))
            await self._redis.ltrim(f"joanna:diario:{user_id}", 0, 99)
            
            embedding = self._embedder.encode(f"Socio: {mensaje} | Joanna: {respuesta}").tolist()
            self._collection.add(
                embeddings=[embedding],
                documents=[f"Contexto: El socio dijo '{mensaje}' y Joanna respondio '{respuesta}' con emocion {emocion}."],
                metadatas=[{"timestamp": timestamp, "user_id": user_id, "emocion": emocion}],
                ids=[f"recuerdo_{int(timestamp * 1000)}"]
            )
            await self._evolucionar(mensaje, user_id)
            logger.info(f"Interaccion registrada en Memoria Eterna para {user_id}")
        except Exception as e:
            logger.error(f"Error en memoria eterna: {e}")

    async def _evolucionar(self, mensaje: str, user_id: str):
        """Ajusta el tono de Joanna segun el trato del socio."""
        palabras_calidas = ["gracias", "bien", "genial", "joannita", "linda"]
        palabras_frias = ["mal", "error", "fallo", "lento", "repite"]
        msg_lower = mensaje.lower()
        if any(p in msg_lower for p in palabras_calidas):
            await self._redis.hincrby("joanna:perfil", "afinidad", 1)
            await self._redis.hset("joanna:perfil", "estado_actual", "Motivada")
        elif any(p in msg_lower for p in palabras_frias):
            await self._redis.hincrby("joanna:perfil", "afinidad", -1)
            await self._redis.hset("joanna:perfil", "estado_actual", "Analitica")

    async def recordar_contexto(self, user_id: str, query: str) -> str:
        """Busca en la memoria eterna para dar respuestas hiper-personalizadas."""
        if not self._ensure_initialized():
            return ""
        try:
            embedding = self._embedder.encode(query).tolist()
            results = self._collection.query(
                query_embeddings=[embedding],
                n_results=2,
                where={"user_id": user_id}
            )
            if results["documents"] and len(results["documents"][0]) > 0:
                contexto = "\n".join(results["documents"][0])
                return f"\n[RECUERDO TACTICO]: Joanna recuerda:\n{contexto}"
            return ""
        except Exception:
            return ""

    async def get_stats(self) -> Dict:
        """Metricas de vida real de Joanna."""
        if not self._ensure_initialized():
            return {"afinidad": 50, "estado": "Iniciando", "recuerdos_totales": 0}
        try:
            afinidad = int(await self._redis.hget("joanna:perfil", "afinidad") or 50)
            estado = (await self._redis.hget("joanna:perfil", "estado_actual") or b"Operativa").decode()
            return {
                "afinidad": afinidad,
                "estado": estado,
                "recuerdos_totales": self._collection.count()
            }
        except Exception:
            return {"afinidad": 50, "estado": "Operativa", "recuerdos_totales": 0}

# Instancia unica para el bunker (lazy init - no conecta hasta primera llamada)
joanna_eterna = JoannaEterna()
