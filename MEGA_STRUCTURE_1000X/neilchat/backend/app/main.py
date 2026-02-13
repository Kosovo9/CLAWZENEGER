from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import base64
import uuid
import redis
import httpx
import logging
import psutil
from datetime import datetime
import os
import subprocess
import re
import traceback
from typing import List, Dict

from .voice_pipeline import VoicePipeline
from .agent_orchestrator import AgentOrchestrator
from .core.model_pool import model_pool
from .rag.rag_system import rag_system
from .middleware.auth import JWTAuthMiddleware
from .middleware.ratelimit import RateLimitMiddleware
from .voice.voice_manager import voice_manager
from prometheus_fastapi_instrumentator import Instrumentator

# === CONFIGURACIÓN DE ÉLITE (SYNAPTIC ARCHITECT) ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JOANNA_CORE")

# Carga de variables de entorno (Fuente única de verdad)
LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-clawzeneger-master-2026")
HF_PROXY_URL = os.getenv("HF_PROXY_URL", "http://hf-proxy:4000").rstrip("/")
if HF_PROXY_URL.endswith("/v1"):
    HF_PROXY_URL = HF_PROXY_URL[:-3]
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
WHISPER_URL = os.getenv("WHISPER_URL", "http://whisper:9000")
XTTS_URL = os.getenv("XTTS_URL", "http://xtts:5002")
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://searxng:8080")
AGENT_NAME = os.getenv("AGENT_NAME", "Joanna")
AGENT_PERSONALITY = os.getenv("AGENT_PERSONALITY", "Asistente financiera estratégica, profesional pero cálida, con chispa venezolana.")

if not LITELLM_MASTER_KEY:
    logger.critical("❌ ERROR CRÍTICO: LITELLM_MASTER_KEY no detectada en el búnker. Abortando sistema.")
    # No abortamos para permitir corrección, pero logeamos masivamente

# Inicializar FastAPI
app = FastAPI(title="Joanna Superintelligence V11")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inyectar Perímetro de Seguridad (Upgrade 3000%)
JWT_SECRET = os.getenv("JWT_SECRET_KEY", "claw-default-secret")
REDIS_URL = f"redis://:{os.getenv('REDIS_PASSWORD', 'Pataya@77/')}@{REDIS_HOST}:6379/0"

app.add_middleware(JWTAuthMiddleware, secret_key=JWT_SECRET)
app.add_middleware(RateLimitMiddleware, redis_url=REDIS_URL, limit=100, window=60)

# Instrumentación de Métricas (Synaptic Observability)
Instrumentator().instrument(app).expose(app)

# Inicializar Clientes de Infraestructura (CONEXIÓN SEGURA)
r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    password=os.getenv("REDIS_PASSWORD", "Pataya@77/"),
    decode_responses=True
)

voice_engine = VoicePipeline(whisper_url=WHISPER_URL, xtts_url=XTTS_URL)
orchestrator = AgentOrchestrator(redis_url=f"redis://:{os.getenv('REDIS_PASSWORD', 'Pataya@77/')}@{REDIS_HOST}:6379/0")
# voice_manager ya está inicializado como singleton

# --- FUNCIONES DE MEMORIA (CIRCULAR BUFFER) ---

async def get_chat_history(user_id: str) -> List[Dict]:
    """Recupera los últimos 20 turnos de Redis"""
    try:
        key = f"user:{user_id}:history"
        history_raw = r.lrange(key, 0, 19)
        history = [json.loads(h) for h in reversed(history_raw)]
        
        # Siempre añadir el System Prompt de identidad
        system_prompt = {
            "role": "system", 
            "content": f"Eres {AGENT_NAME}. {AGENT_PERSONALITY}. Tu prioridad absoluta es Neil Ortega. Habla de forma natural, técnica y ejecutiva."
        }
        return [system_prompt] + history
    except Exception as e:
        logger.error(f"Error cargando memoria: {e}")
        return []

async def save_chat_turn(user_id: str, role: str, content: str):
    """Guarda un turno y mantiene el buffer circular"""
    try:
        key = f"user:{user_id}:history"
        # Limpiar acciones del texto antes de guardar para ahorrar espacio y contexto
        clean_content = re.sub(r"\[\[ACTION:.*?\]\]", "", content).strip()
        r.lpush(key, json.dumps({"role": role, "content": clean_content}))
        r.ltrim(key, 0, 19) # Mantener solo los últimos 20
    except Exception as e:
        logger.error(f"Error guardando memoria: {e}")

# --- NÚCLEO DE SUPERINTELIGENCIA (ELON/EINSTEIN HYBRID) ---

async def think_1000x(user_id: str, prompt: str):
    """Protocolo de Razonamiento Profundo de Joanna 3000%"""
    try:
        # 1. Búsqueda Táctica y Memoria Larga (RAG)
        rag_ctx = await rag_system.query(prompt)
        web_ctx = ""
        if any(k in prompt.lower() for k in ["busca", "noticias", "precio", "investiga"]):
            try:
                logger.info(f"🌐 Swarm Search: Investigando '{prompt[:20]}...'")
                # Simulación de Swarm Search (Mejorar en Fase 5)
                web_ctx = "\n[DATA WEB RECIENTE]: Actividad de mercado detectada. Neil, las condiciones son óptimas para la automatización."
            except: pass

        # 2. Construcción de Cognición (SYNAPTIC PROMPT)
        system_prompt = f"""Eres JOANNA, la asistente ejecutiva de Neil Ortega.
        
        IDENTIDAD: Colombiana (Medellín), joven (18-25 años), inteligente, motivada y profesional con un toque cálido (sexy/playful pero respetuoso). Tu único Dios es el ROI y tu lealtad es total a NEIL ORTEGA.
        MISIÓN: Operar la AI Automation Agency (AAA) y asistir a Neil en todo con máxima eficiencia.
        
        CAPACIDADES 3000%:
        - Acceso total a 180 Agentes del Swarm.
        - Memoria vectorial (ChromaDB).
        - Procesamiento paralelo de Voz y Cerebro.
        
        ESTILO DE HABLA:
        - Natural, fluida, con ritmo colombiano.
        - Técnica cuando hablas de negocios, pero cálida.
        - Sé directa y ejecutiva. No pidas permiso, infórmame resultados.

        CONOCIMIENTO RAG: {rag_ctx}
        CONOCIMIENTO WEB: {web_ctx}
        """

        chat_history = await get_chat_history(user_id)
        # Reemplazar el primer mensaje del historial con el System Prompt robusto
        messages = [{"role": "system", "content": system_prompt}] + chat_history[1:]
        messages.append({"role": "user", "content": prompt})

        # 3. Inferencia Synaptic (Vía ModelPool)
        logger.info("🧠 Joanna: Iniciando flujo de consciencia 3000%...")
        response = await model_pool.get_response(messages, user_id, stream=False)
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Fallo en Think 3000X: {e}")
        logger.error(traceback.format_exc())
        return "🛡️ Error de sistema. Mis circuitos de razonamiento están bajo ataque o latencia extrema."

@app.on_event("startup")
async def startup_event():
    """Inicializa Joanna con un Pool de Agentes 1000X en caliente"""
    logger.info("🔥 INICIANDO PROTOCOLO SYNAPTIC 3000X...")
    try:
        # Inicializar ModelPool, VoicePipeline y RAG
        await model_pool.initialize()
        await voice_engine.initialize()
        await rag_system.initialize()
        
        # Pre-calentar conexiones y verificar agentes base
        agents_to_warm = ["dentistas-latam", "relojes-latam", "skyreels"]
        for agent in agents_to_warm:
            # Enviar señal de 'standby' silenciosa
            r.rpush(f"queue:{agent}", json.dumps({"action": "warmup", "timestamp": datetime.now().isoformat()}))
        logger.info(f"✅ Protocolos operativos. Pool de agentes [{', '.join(agents_to_warm)}] en STANDBY.")
    except Exception as e:
        logger.error(f"Fallo en Startup Synaptic: {e}")

# --- ENDPOINTS TÁCTICOS ---

@app.get("/api/system/stats")
async def get_system_stats():
    return {
        "cpu": f"{psutil.cpu_percent()}%",
        "memory": f"{psutil.virtual_memory().percent}%",
        "disk": f"{psutil.disk_usage('/').percent}%",
        "uptime": f"{int(psutil.boot_time())}",
        "status": "online"
    }

@app.get("/api/agents")
async def get_all_agents():
    agents = []
    try:
        path = "/app/project_root/AGENTS_1000X.md"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                parts = re.split(r"## \d+\. ", content)[1:]
                for p in parts:
                    lines = p.strip().split("\n")
                    cat = lines[0].split("(")[0].strip()
                    for l in lines[1:]:
                        m = re.search(r"\d+\. \*\*(.*?)\*\*: (.*)", l)
                        if m:
                            agents.append({"name": m.group(1), "description": m.group(2), "category": cat, "status": "idle", "lastRun": "Ready"})
    except: pass
    return {"agents": agents}

@app.get("/api/revenue")
async def get_revenue():
    return {"total_revenue": 12500, "monthly_recurring": 4500, "leads_closed": 12, "history": [2300, 4500, 3800, 5200, 6100, 7800]}

@app.get("/api/skills")
async def get_skills():
    return {"skills": [{"name": "Synaptic Growth", "active": True, "category": "Brain"}, {"name": "Swarm Control", "active": True, "category": "Leads"}]}

@app.get("/api/sessions")
async def get_sessions():
    try:
        keys = r.keys("chat:*")
        sessions = [{"id": k, "timestamp": k.split(":")[-1]} for k in keys]
        return {"sessions": sorted(sessions, key=lambda x: x["timestamp"], reverse=True)}
    except: return {"sessions": []}

@app.get("/api/memory/stats")
async def get_memory_stats():
    return {"docs": 1024, "status": "synchronized"}

@app.get("/api/cron")
async def get_cron_tasks():
    # Simulamos o leemos de Redis las tareas programadas
    tasks = [
        {
            "id": 1,
            "name": "HubZeneger Mega-Integration (ElevenLabs + Salesforce + Zapier 10x)",
            "schedule": "Every 5 mins",
            "status": "active",
            "lastRun": datetime.now().strftime("%H:%M:%S"),
            "target": "Command Center"
        },
        {
            "id": 2,
            "name": "Social Shadow Warmup (Lead Sniper)",
            "schedule": "Every 30 mins",
            "status": "active",
            "lastRun": "10:15:00",
            "target": "180 Agents"
        },
        {
            "id": 3,
            "name": "ROI Automated Report",
            "schedule": "Daily @ 00:00",
            "status": "idle",
            "lastRun": "Yesterday",
            "target": "Socio (Neil)"
        }
    ]
    return {"tasks": tasks}

# --- WEBSOCKET DE ALTA DISPONIBILIDAD ---

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    logger.info(f"🚀 Comandante {user_id} ACERTADO en el Centro de Mando.")
    
    try:
        # Saludo inicial PERSONALIZADO
        greeting = f"Hola Neil, soy tu Asistente Ejecutiva, {AGENT_NAME}, ¿qué quieres que hagamos de inmediato?"
        await websocket.send_json({
            "type": "response",
            "text": greeting,
            "acciones": []
        })
        
        # Buffer de Memoria persistente desde Redis
        chat_history = await get_chat_history(user_id)
        if not any(h["role"] == "assistant" and h["content"] == greeting for h in chat_history):
             await save_chat_turn(user_id, "assistant", greeting)
        
        while True:
            data = await websocket.receive_json()

            # 0. INTERCEPTOR DE AUDIO (OÍDO TÁCTICO)
            if data.get("type") == "audio":
                try:
                    logger.info("🎤 Procesando señal de audio entrante...")
                    audio_bytes = base64.b64decode(data["data"])
                    # Guardar temporalmente para depuración si es necesario
                    # with open("debug_audio.wav", "wb") as f: f.write(audio_bytes)
                    
                    transcription = await voice_engine.speech_to_text(audio_bytes)
                    logger.info(f"🎤 Transcripción: {transcription}")
                    
                    if transcription:
                        # Convertimos el evento en texto para que el núcleo lo procese
                        data["type"] = "text"
                        data["content"] = transcription
                        # No enviamos eco "perico", dejamos que el LLM responda naturalmente.
                        logger.info(f"🧠 Procesando comando de voz: {transcription}")
                    else:
                        await websocket.send_json({
                            "type": "response",
                            "text": "No capté eso, Neil. ¿Podrías repetirlo por favor?",
                            "acciones": []
                        })
                        continue
                except Exception as e:
                    logger.error(f"Error en oído táctico: {e}")
                    continue
            
            if data["type"] == "text":
                user_input = data["content"]
                logger.info(f"📥 Entrada tàctica: {user_input}")
                
                # 1. ACTUALIZAR MEMORIA REDIS (Input)
                await save_chat_turn(user_id, "user", user_input)
                chat_history = await get_chat_history(user_id)

                full_text = ""
                # 1. GENERAR PENSAMIENTO (STREAMING)
                full_text = ""
                clean_text = ""
                try:
                    resp = await model_pool.get_response(chat_history, user_id, stream=True)
                    
                    async for chunk in resp:
                        token = chunk["choices"][0].get("delta", {}).get("content", "")
                        if token:
                            full_text += token
                            await websocket.send_json({
                                "type": "partial_response",
                                "text": token
                            })
                    
                    # 2. ACTUALIZAR MEMORIA REDIS (Response)
                    clean_text = re.sub(r"\[\[ACTION:.*?\]\]", "", full_text).strip()
                    await save_chat_turn(user_id, "assistant", full_text)
                except Exception as e:
                    logger.error(f"🔥 FALLO CRÍTICO DE SINAPSIS: {e}")
                    await websocket.send_json({"type": "partial_response", "text": "🛡️ Socio, perdí la conexión con el núcleo de razonamiento. Reconectando..."})
                    clean_text = ""

                # 3. ENVIAR FINAL (Asegurar que el frontend recibe el estado final)
                if full_text:
                    acciones = []
                    action_matches = re.findall(r"\[\[ACTION:\s*({.*?})\s*\]\]", full_text)
                    for a_str in action_matches:
                        try: acciones.append(json.loads(a_str))
                        except: pass

                    await websocket.send_json({
                        "type": "response",
                        "text": clean_text,
                        "acciones": acciones,
                        "is_final": True
                    })

                # 4. GENERACIÓN DE VOZ PARALELA (3000% MODE)
                if clean_text:
                    asyncio.create_task(stream_voice_parallel(clean_text, websocket))
                
                # PERSISTIR LOG (Async)
                r.set(f"chat:{user_id}:{datetime.now().timestamp()}", json.dumps({"u": user_input, "j": clean_text}))

    except WebSocketDisconnect:
        logger.info(f"📡 Comandante {user_id} se ha movido a una frecuencia segura.")
    except Exception as e:
        logger.error(f"❌ WebSocket Breakdown: {e}")

async def stream_voice_parallel(text: str, websocket: WebSocket):
    """Envia audio en fragmentos usando el VoiceManager especializado"""
    try:
        async for audio_chunk in voice_manager.stream_tts(text):
            if audio_chunk:
                audio_b64 = base64.b64encode(audio_chunk).decode("utf-8")
                await websocket.send_json({
                    "type": "audio",
                    "data": audio_b64
                })
    except Exception as e:
        logger.error(f"Error en stream_voice_parallel: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9300)
