import asyncio
import websockets
import json
import base64

async def test_joanna_live():
    uri = "ws://localhost:9300/ws/test_socio"
    print(f"🔗 Conectando a Joanna Live en {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            # Recibir saludo inicial
            greeting = await websocket.recv()
            print(f"\n👋 Saludo de Joanna: {json.loads(greeting)['text']}")
            
            # Enviar mensaje de prueba
            test_msg = "Joanna, ¿cuál es el estado actual de nuestro enjambre y qué misión de dinero tienes hoy?"
            print(f"\n👤 Socio: {test_msg}")
            
            await websocket.send(json.dumps({
                "type": "text",
                "content": test_msg
            }))
            
            # Recibir respuesta de pensamiento
            print("\n⏳ Joanna está pensando...")
            response = await websocket.recv()
            data = json.loads(response)
            
            print(f"\n🧠 Joanna (Texto): {data['text']}")
            
            if data.get('audio'):
                print(f"✅ Joanna (Voz): ¡RECIBIDA! (Base64 length: {len(data['audio'])})")
            else:
                print("❌ Joanna (Voz): No se generó audio.")
            
            if data.get('acciones'):
                print(f"🚀 Acciones: {data['acciones']}")
                
    except Exception as e:
        print(f"❌ Error en el test real: {e}")

if __name__ == "__main__":
    asyncio.run(test_joanna_live())
