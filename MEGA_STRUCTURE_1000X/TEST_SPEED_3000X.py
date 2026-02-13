# TEST_SPEED_3000X.py

import asyncio
import websockets
import json
import time
import os

WS_URL = "ws://localhost:9300/chat/ws/neil_3000"

async def test_synaptic_performance():
    print("🚀 INICIANDO PRUEBA DE RENDIMIENTO SYNAPTIC 3000%...")
    
    async with websockets.connect(WS_URL) as websocket:
        # Test 1: Latencia de Razonamiento
        prompt = "¿Cuál es tu misión estratégica para el Swarm 3000%?"
        start_time = time.time()
        
        await websocket.send(json.dumps({
            "type": "text",
            "content": prompt
        }))
        
        first_token_received = False
        full_text = ""
        
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                data = json.loads(message)
                
                if data["type"] == "partial_response" and not first_token_received:
                    latency = time.time() - start_time
                    first_token_received = True
                    print(f"⏱️ LATENCIA PRIMER TOKEN: {latency:.2f}s")
                    if latency < 1.0:
                        print("✅ EXCELENCIA: Latencia sub-segundo alcanzada.")
                    else:
                        print("⚠️ ADVERTENCIA: Latencia superior a 1s.")
                
                elif data["type"] == "partial_response":
                    full_text += data["text"]
                
                elif data["type"] == "audio":
                    print(f"🗣️ VOZ DETECTADA: Segmento de audio recibido (Caché/Real)")
                
                elif data["type"] == "response" and data.get("is_final"):
                    print(f"🧠 JOANNA FINAL: {full_text[:50]}...")
                    break
            except asyncio.TimeoutError:
                print("❌ ERROR: Tiempo de espera agotado.")
                break

    print("\n🏁 PRUEBA COMPLETADA.")

if __name__ == "__main__":
    asyncio.run(test_synaptic_performance())
