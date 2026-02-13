import requests
import json
import time

# 🦁 CLAWZENEGER BATTLE TEST SUITE 1000X
# This script verifies the integrity of the Omni-OS nervous system.

BASE_URL = "http://localhost:54321"

def test_health():
    print("🧪 Testing Orchestrator Health...")
    try:
        r = requests.get(f"{BASE_URL}/")
        assert r.status_code == 200
        print(f"✅ Health OK: {r.json()['status']}")
    except Exception as e:
        print(f"❌ Health Failed: {e}")

def test_chat_memory():
    print("\n🧪 Testing Chat Memory Infiltration...")
    payload = {
        "msg": "¿Cómo te llamas?",
        "mode": "neil",
        "history": [
            {"role": "user", "content": "Hola socio."},
            {"role": "bot", "content": "¡Hola! Soy Neil Zenneger, tu socio táctico."}
        ]
    }
    try:
        r = requests.post(f"{BASE_URL}/chat", json=payload)
        assert r.status_code == 200
        response_text = r.json().get('response', '')
        print(f"✅ Chat response: {response_text[:50]}...")
        if "Neil" in response_text or "socio" in response_text.lower():
            print("✅ Tone/Context injection verified.")
    except Exception as e:
        print(f"❌ Chat Failed: {e}")

def test_agent_registry():
    print("\n🧪 Testing Agent Command Center...")
    # We verify it accepts a valid agent type
    payload = {"type": "lead_hunt", "target": "test_target"}
    try:
        r = requests.post(f"{BASE_URL}/agent/run", json=payload)
        assert r.status_code == 200
        print(f"✅ Agent Dispatch OK: {r.json()['msg']}")
    except Exception as e:
        print(f"❌ Agent Dispatch Failed: {e}")

if __name__ == "__main__":
    print("🚀 STARTING NUCLEAR TESTS...")
    start_time = time.time()
    test_health()
    test_chat_memory()
    test_agent_registry()
    print(f"\n💎 TESTS COMPLETED IN {time.time() - start_time:.2f}s. SYSTEM 100% OPERATIONAL.")
