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
import redis.asyncio as redis
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class JoannaEterna:
    """
    Gestiona la memoria infinita y la evolución de Joanna.
    Combina Redis (memoria volátil/reciente) con ChromaDB (memoria eterna).
    """
    
    def __init__(self):
        # Configuración REDIS (Caché y Personalidad)
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=False)
        
        # Configuración CHROMA (Memoria RAG Eterna)
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", 8000))
        self.chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # Modelo de Embeddings (3000% Performance)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Inicializar Colecciones
        try:
            self.collection = self.chroma_client.get_or_create_collection(
                name="joanna_recuerdos",
                metadata={"description": "Memoria de largo plazo de Joanna Zeneger"}
            )
        except Exception as e:
            logger.error(f"❌ Error al conectar con ChromaDB: {e}")

    async def registrar_interaccion(self, user_id: str, mensaje: str, respuesta: str, emocion: str = "neutral"):
        """Graba la interacción en la memoria eterna y actualiza la personalidad."""
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

            # 1. Guardar en Redis (Diario Reciente)
            await self.redis.lpush(f"joanna:diario:{user_id}", json.dumps(interaccion))
            await self.redis.ltrim(f"joanna:diario:{user_id}", 0, 99) # Guardar 100 interacciones rápidas

            # 2. Guardar en ChromaDB (Evolución RAG)
            embedding = self.embedder.encode(f"Socio: {mensaje} | Joanna: {respuesta}").tolist()
            
            self.collection.add(
                embeddings=[embedding],
                documents=[f"Contexto: El socio preguntó '{mensaje}' y Joanna respondió '{respuesta}' con emoción {emocion}."],
                metadatas=[{"timestamp": timestamp, "user_id": user_id, "emocion": emocion}],
                ids=[f"recuerdo_{int(timestamp * 1000)}"]
            )

            # 3. Evolución de Personalidad
            await self._evolucionar(mensaje, user_id)
            
            logger.info(f"✅ Interacción registrada en Memoria Eterna para {user_id}")
        except Exception as e:
            logger.error(f"❌ Error en memoria eterna: {e}")

    async def _evolucionar(self, mensaje: str, user_id: str):
        """Ajusta el tono de Joanna según el trato del socio."""
        palabras_calidas = ["gracias", "bien", "genial", "joannita", "linda"]
        palabras_frias = ["mal", "error", "fallo", "lento", "repite"]
        
        msg_lower = mensaje.lower()
        if any(p in msg_lower for p in palabras_calidas):
            await self.redis.hincrby("joanna:perfil", "afinidad", 1)
            await self.redis.hset("joanna:perfil", "estado_actual", "Motivada 🚀")
        elif any(p in msg_lower for p in palabras_frias):
            await self.redis.hincrby("joanna:perfil", "afinidad", -1)
            await self.redis.hset("joanna:perfil", "estado_actual", "Analítica 🧠")

    async def recordar_contexto(self, user_id: str, query: str) -> str:
        """Busca en la memoria eterna para dar respuestas hiper-personalizadas."""
        try:
            embedding = self.embedder.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=2,
                where={"user_id": user_id}
            )
            
            if results["documents"] and len(results["documents"][0]) > 0:
                contexto = "\n".join(results["documents"][0])
                return f"\n[RECUERDO TÁCTICO]: Joanna recuerda:\n{contexto}"
            return ""
        except Exception:
            return ""

    async def get_stats(self) -> Dict:
        """Métricas de vida real de Joanna."""
        afinidad = int(await self.redis.hget("joanna:perfil", "afinidad") or 50)
        estado = (await self.redis.hget("joanna:perfil", "estado_actual") or b"Operativa").decode()
        
        return {
            "afinidad": afinidad,
            "estado": estado,
            "recuerdos_totales": self.collection.count()
        }

# Instancia única para el búnker
joanna_eterna = JoannaEterna()
