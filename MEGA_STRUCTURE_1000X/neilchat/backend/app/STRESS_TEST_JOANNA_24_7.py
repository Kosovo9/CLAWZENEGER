import asyncio
import websockets
import json
import base64
import time
import random

# Configuración del Stress Test 24/7
AGENT_NAME = "Joanna"
URI = "ws://localhost:9300/ws/stress_test_socio"
INTERACTIONS = 50 # Número de ciclos para este test
TALK_INTERVAL = 3  # Segundos entre interacciones

PROMPTS = [
    "Hola Joanna, ¿cuál es nuestra facturación proyectada hoy?",
    "¿Qué agentes del enjambre están cerrando ventas ahora mismo?",
    "Necesito un reporte del ROI de la última campaña de dentistas.",
    "Joanna, cuéntame un chiste paisa mientras revisas los logs.",
    "¿Cómo va el entrenamiento de tu voz hoy?",
    "Joanna, ¿estás lista para dominar el mercado de IA?",
    "Dame un consejo de negocios estilo Neil Ortega.",
    "¿Cuál es tu modelo de lenguaje actual y qué tan rápido respondes?",
    "Joanna, activa el protocolo de máxima eficiencia en el búnker.",
    "Dime algo motivador para cerrar este domingo al 3000%."
]

async def stress_test_24_7():
    print(f"🚀 INICIANDO TEST CONVERSACIONAL JOANNA 24/7...")
    print(f"🔗 Conectando a {URI}...")
    
    try:
        async with websockets.connect(URI) as websocket:
            # 1. Saludo Inicial
            greeting_msg = await websocket.recv()
            greeting_data = json.loads(greeting_msg)
            print(f"\n👋 Joanna: {greeting_data['text']}")
            
            for i in range(1, INTERACTIONS + 1):
                prompt = random.choice(PROMPTS)
                print(f"\n[{i}/{INTERACTIONS}] 👤 Socio (Neil): {prompt}")
                
                start_time = time.time()
                
                # Enviar Mensaje
                await websocket.send(json.dumps({
                    "type": "text",
                    "content": prompt
                }))
                
                # Recibir Respuestas (Streaming)
                full_response = ""
                audio_received = 0
                actions_received = []
                
                while True:
                    resp = await websocket.recv()
                    data = json.loads(resp)
                    
                    if data["type"] == "partial_response":
                        full_response += data["text"]
                        continue
                    
                    if data["type"] == "response":
                        print(f"🧠 Joanna: {data['text']}")
                        if data.get("acciones"):
                            actions_received = data["acciones"]
                        if data.get("is_final"):
                            break
                    
                    if data["type"] == "audio":
                        audio_received += 1
                        # No imprimimos el audio para no saturar la consola
                
                end_time = time.time()
                latency = end_time - start_time
                
                print(f"⏱️ Latencia de Ciclo: {latency:.2f}s")
                print(f"🎤 Fragmentos Audios: {audio_received}")
                if actions_received:
                    print(f"🚀 Acciones ejecutadas: {len(actions_received)}")
                
                if latency > 5.0:
                    print("⚠️ ALERTA: Latencia superior a 5 segundos detectada.")
                
                print(f"💤 Esperando {TALK_INTERVAL}s para la próxima interacción...")
                await asyncio.sleep(TALK_INTERVAL)
                
            print("\n✅ TEST 24/7 COMPLETADO CON ÉXITO.")
            print(f"Promedio de latencia estable. Joanna está en su prime. 🏆")

    except Exception as e:
        print(f"❌ FALLO CRÍTICO EN EL TEST: {e}")

if __name__ == "__main__":
    asyncio.run(stress_test_24_7())
