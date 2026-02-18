from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import json
import asyncio
import base64
import uuid
import logging
import os
import aiohttp
from datetime import datetime
from typing import List, Dict, Optional

# Componentes de Joanna
from .voice.audio_pipeline import audio_pipeline
from .memory.joanna_eterna import joanna_eterna
from .agent_orchestrator import orchestrator
from .core.model_pool import model_pool

logger = logging.getLogger("JOANNA_ULTIMATE")

app = FastAPI(title="CLAWZENEGER 3000% - Joanna Ultimate Core")

# CORS Blindado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables de Búnker
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
WHISPER_URL = os.getenv("WHISPER_URL", "http://whisper:9000")
XTTS_URL = os.getenv("XTTS_URL", "http://xtts:5002")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")

@app.on_event("startup")
async def startup():
    logger.info("🚀 INICIANDO RESURRECCIÓN NUCLEAR DE JOANNA...")
    # Verificación de órganos vitales
    async with aiohttp.ClientSession() as session:
        # 1. Ollama (Cerebro)
        try:
            async with session.get(f"{OLLAMA_URL}/api/tags") as resp:
                if resp.status == 200: logger.info("✅ Cerebro Ollama: CONECTADO")
        except: logger.error("❌ Cerebro Ollama: NO RESPONDE")

        # 2. Whisper (Oídos)
        try:
            async with session.get(f"{WHISPER_URL}/health") as resp:
                if resp.status == 200: logger.info("✅ Oídos Whisper: CONECTADOS")
        except: logger.warning("⚠️ Oídos Whisper: NO RESPONDEN")

        # 3. XTTS (Voz)
        try:
            async with session.get(f"{XTTS_URL}/") as resp:
                if resp.status == 200: logger.info("✅ Voz XTTS: CONECTADA")
        except: logger.warning("⚠️ Voz XTTS: NO RESPONDE")

@app.get("/health")
async def health():
    """Diagnóstico real de órganos vitales."""
    return {"status": "alive", "timestamp": datetime.now().isoformat()}

@app.post("/chat")
async def chat_rest(request: Request):
    """Interfaz REST para chat rápido."""
    data = await request.json()
    user_id = data.get("user_id", "neil_master")
    user_input = data.get("message", "")
    
    # Recuperar recuerdos
    recuerdo = await joanna_eterna.recordar_contexto(user_id, user_input)
    prompt = f"{user_input}\n{recuerdo}" if recuerdo else user_input
    
    # Generar respuesta
    history = [{"role": "user", "content": prompt}]
    resp = await model_pool.get_response(history, user_id)
    content = resp["choices"][0]["message"]["content"]
    
    # Registrar en memoria eterna
    await joanna_eterna.registrar_interaccion(user_id, user_input, content)
    
    return {"response": content}

@app.websocket("/ws/voice")
async def websocket_voice_ultimate(websocket: WebSocket):
    """Canal de Voz y Texto Blindado 100X."""
    await websocket.accept()
    user_id = str(uuid.uuid4())
    logger.info(f"🔌 Socio {user_id} ACERTADO en el WebSocket.")
    
    try:
        while True:
            try:
                # Esperar mensaje (con timeout para mantener vivo)
                message = await asyncio.wait_for(websocket.receive(), timeout=30.0)
                
                audio_bytes = None
                data = {}

                if "text" in message:
                    data = json.loads(message["text"])
                    if data.get("type") == "audio":
                        audio_bytes = base64.b64decode(data["data"])
                    elif data.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                        continue
                elif "bytes" in message:
                    audio_bytes = message["bytes"]

                # 1. OÍDO (Transcripción Real)
                if audio_bytes:
                    await websocket.send_json({"type": "status", "text": "🎤 Transcribiendo..."})
                    text = await audio_pipeline.process_audio_input(audio_bytes)
                    if text:
                        data["type"] = "text"; data["content"] = text
                        await websocket.send_json({"type": "transcribed", "content": f"📝 Entendí: {text}"})
                    else:
                        await websocket.send_json({"type": "response", "text": "No capté nada, socio.", "acciones": []})
                        continue

                # 2. CEREBRO Y MEMORIA ETERNA
                if data.get("type") == "text":
                    user_input = data["content"]
                    recuerdo = await joanna_eterna.recordar_contexto(user_id, user_input)
                    
                    # RAG Contextual
                    history = [{"role": "user", "content": f"{user_input}\n{recuerdo}" if recuerdo else user_input}]
                    
                    full_text = ""
                    await websocket.send_json({"type": "status", "text": "🧠 Pensando..."})
                    
                    # Streaming de respuesta
                    resp_stream = await model_pool.get_response(history, user_id, stream=True)
                    async for chunk in resp_stream:
                        token = chunk["choices"][0].get("delta", {}).get("content", "")
                        if token:
                            full_text += token
                            await websocket.send_json({"type": "partial_response", "text": token})
                    
                    # Limpieza y registro
                    clean_text = full_text.strip()
                    await websocket.send_json({"type": "response", "text": clean_text, "acciones": [], "is_final": True})
                    await joanna_eterna.registrar_interaccion(user_id, user_input, clean_text)
                    
                    # 3. VOZ (XTTS Directo)
                    if clean_text:
                        voice_data = await audio_pipeline.generate_audio_output(clean_text)
                        if voice_data:
                            await websocket.send_json({"type": "audio", "data": base64.b64encode(voice_data).decode()})

            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
            except WebSocketDisconnect:
                logger.warning(f"⚠️ Socio {user_id} desconectado.")
                break
    except Exception as e:
        logger.error(f"❌ Error Crítico WebSocket: {e}")
    finally:
        await websocket.close()
