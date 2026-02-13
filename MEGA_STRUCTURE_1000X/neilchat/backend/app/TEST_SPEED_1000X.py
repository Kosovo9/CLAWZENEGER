import asyncio
import websockets
import json
import time

async def test_joanna_speed():
    uri = "ws://localhost:9300/ws/speed_socio"
    print(f"🔗 Conectando a Joanna Speed-1000X en {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            # Saludo inicial
            greeting = await websocket.recv()
            print(f"👋 Greeting: {json.loads(greeting)['text']}")
            
            test_msg = "Joanna, dame una estrategia rápida para monetizar $100 hoy mismo."
            print(f"\n👤 Socio: {test_msg}")
            
            start_time = time.time()
            
            await websocket.send(json.dumps({
                "type": "text",
                "content": test_msg
            }))
            
            first_token_time = None
            full_text = ""
            
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                
                if data["type"] == "partial_response":
                    if first_token_time is None:
                        first_token_time = time.time()
                        latency = first_token_time - start_time
                        print(f"⚡ LATENCIA PRIMER TOKEN: {latency:.2f}s")
                    
                    full_text += data["text"]
                    # print(data["text"], end="", flush=True) # Silenciamos para el reporte
                
                    if data.get('audio'):
                        print(f"🗣️ Voz: Generada (Base64 length: {len(data['audio'])})")

                elif data["type"] == "audio":
                    print(f"🗣️ Voz: RECIBIDA (Base64 length: {len(data['data'])})")
                    break

                elif data["type"] == "response" and data.get("is_final"):
                    end_time = time.time()
                    print(f"\n\n✅ RESPUESTA FINAL RECIBIDA.")
                    print(f"⏱️ Tiempo total: {end_time - start_time:.2f}s")
                    print(f"🧠 Joanna: {data['text'][:100]}...")
                    # Continue waiting for audio
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_joanna_speed())
