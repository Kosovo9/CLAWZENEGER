import httpx
import asyncio
import json

async def debug_xtts():
    url = "http://localhost:5002"
    
    print(f"Checking speakers at {url}...")
    try:
        # Usually /api/speakers or checking via tts endpoint
        # XTTS API is a bit ad-hoc in the docker container. 
        # But let's try a simple synthesis with the problematic text.
        
        text = "¡Hola! ¿Cómo puedo ayudarte hoy?"
        print(f"Testing TTS with text: '{text}'")
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{url}/api/tts",
                json={"text": text, "speaker": "neilzenneger", "language": "es"},
                timeout=60.0 # Increased timeout for CPU
            )
            
            print(f"Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"Error: {resp.text}")
            else:
                print(f"Success! Received {len(resp.content)} bytes.")
                with open("debug_output.wav", "wb") as f:
                    f.write(resp.content)
                    
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(debug_xtts())
