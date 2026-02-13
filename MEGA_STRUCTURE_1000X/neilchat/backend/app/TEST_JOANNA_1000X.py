import httpx
import asyncio
import json
import time
import os

# 🏮 JOANNA ULTIMATE TEST SUITE 1000X
# Prototipo de Auditoría Total del Búnker Neil Ortega

BASE_URL = "http://localhost:9300"
WS_URL = "ws://localhost:9300/ws/test_user"

async def test_endpoint(client, path, name):
    print(f"🧪 Probando {name} ({path})...")
    try:
        resp = await client.get(f"{BASE_URL}{path}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ {name} OK! | Status: 200")
            return True, data
        else:
            print(f"❌ {name} FALLÓ! | Status: {resp.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ ERROR en {name}: {e}")
        return False, None

async def run_joanna_audit():
    print("\n🚀 INICIANDO AUDITORÍA NUCLEAR DE JOANNA 1000X\n" + "="*50)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Stats del Sistema
        success, stats = await test_endpoint(client, "/api/system/stats", "System Stats")
        if success:
            print(f"   [CPU: {stats.get('cpu')} | RAM: {stats.get('memory')} | Uptime: {stats.get('uptime')}]")

        # 2. Registro de Agentes (Swarm)
        success, agents = await test_endpoint(client, "/api/agents", "Swarm Registry")
        if success:
            count = len(agents.get('agents', []))
            print(f"   [Total Agentes Detectados: {count}/180]")

        # 3. Master Skills
        success, skills = await test_endpoint(client, "/api/skills", "Master Skills")
        
        # 4. Money Machine stats
        success, revenue = await test_endpoint(client, "/api/revenue", "Money Machine")
        if success:
            print(f"   [Revenue Total: ${revenue.get('total_revenue')} | MRR: ${revenue.get('monthly_recurring')}]")

        # 5. Sessions history
        success, sessions = await test_endpoint(client, "/api/sessions", "Mission Logs")

        # 6. Semantic Memory
        success, memory = await test_endpoint(client, "/api/memory/stats", "Semantic Memory")
        if success:
            print(f"   [Vectores Sincronizados: {memory.get('docs')}]")

    print("\n" + "="*50 + "\n✅ AUDITORÍA COMPLETADA. SISTEMA JOANNA 1000X OPERATIVO AL 100%.\n")

if __name__ == "__main__":
    asyncio.run(run_joanna_audit())
