from flask import Flask, request, jsonify
import subprocess
import os
import time
import requests
from flask_cors import CORS
import logging

# 🦁 HUZENEGER OMNI-ORCHESTRATOR 1000X - THE CORE NERVUS
# Mission: Absolute control, 0 errors, 100% real intelligence.

app = Flask(__name__)
CORS(app)

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🦁 [%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@app.route('/')
def health():
    return jsonify({
        "status": "🦁 HUZENEGER ONLINE",
        "version": "10.0.0-GOD-MODE",
        "timestamp": time.time()
    })

# 1. 🎯 AGENT COMMAND CENTER
@app.route('/agent/run', methods=['POST'])
def run_agent():
    try:
        data = request.json
        agent_type = data.get('type')
        target = data.get('target')
        
        logger.info(f"Deploying Agent: {agent_type} on target: {target}")

        if agent_type == 'lead_hunt':
            script_path = os.path.join(BASE_DIR, "scraper-system", "backend", "lead_sniper.py")
            subprocess.Popen(["python", script_path, target], shell=False)
            return jsonify({"msg": f"🕵️‍♂️ Lead Sniper infiltrado en: {target}. Pipeline alimentándose.", "status": "hunting"})

        elif agent_type == 'seo':
            script_path = os.path.join(BASE_DIR, "scraper-system", "backend", "seo_god.py")
            subprocess.Popen(["python", script_path, target], shell=False)
            return jsonify({"msg": f"🚀 Agente SEO auditando: {target}. El reporte llegará al Pipeline.", "status": "running"})

        elif agent_type == 'pentest':
            script_path = os.path.join(BASE_DIR, "scraper-system", "backend", "pentest_lite.py")
            subprocess.Popen(["python", script_path, target], shell=False)
            return jsonify({"msg": f"💀 Agente Pentest analizando: {target}. Vulnerabilidades en radar.", "status": "running"})

        elif agent_type == 'deploy_saas':
            script_path = os.path.join(BASE_DIR, "scripts", "deploy_saas.sh")
            subprocess.Popen(["bash", script_path, target.replace(" ", "_").lower()], shell=False)
            return jsonify({"msg": f"🏗️ SaaS Builder activado para: {target}. Despliegue en curso.", "status": "deploying"})

        elif agent_type == 'auto_close':
            # Disparar Webhook de n8n
            n8n_webhook = "http://localhost:5678/webhook/auto-close"
            requests.post(n8n_webhook, json={"lead": target}, timeout=5)
            return jsonify({"msg": f"⚡ Protocolo Auto-Close iniciado para {target} vía WhatsApp.", "status": "closing"})

        elif agent_type == 'yt_extract':
            script_path = os.path.join(BASE_DIR, "skills", "yt_extractor_1000x.py")
            subprocess.Popen(["python", script_path, target], shell=False)
            return jsonify({"msg": f"🎬 YouTube Intel Agent desplegado en: {target}.", "status": "extracting"})

        # DYNAMIC AGENT LOADING (SUPPORT FOR 75+ AGENTS)
        else:
            agent_folder = os.path.join(BASE_DIR, "hubzeneger", "agents", agent_type)
            if os.path.exists(agent_folder):
                script_path = os.path.join(agent_folder, "agent.py")
                if os.path.exists(script_path):
                    subprocess.Popen(["python", script_path, target], shell=False)
                    return jsonify({"msg": f"🤖 Agente especializado '{agent_type}' desplegado para {target}.", "status": "active"})
            
            return jsonify({"error": f"Agent '{agent_type}' not found in high-performance structure."}), 404

    except Exception as e:
        logger.error(f"Agent Execution Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 2. 🧠 MASTER BRAIN (AI CHAT WITH FULL MEMORY 1000X)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('msg', '')
        mode = data.get('mode', 'neil')
        chat_history = data.get('history', []) # Recuperamos la memoria 10x
        
        logger.info(f"[{mode.upper()}] Thinking about: {message} (History depth: {len(chat_history)})")

        if mode == 'clawzeneger':
            system_prompt = """Eres CLAWZENEGER, el Gerente General y Arquitecto Jefe de todo este ecosistema. 
            Eres el brazo derecho del Operador. Tienes autoridad total para coordinar a NeilZenneger y al resto de los 84 agentes.
            Tu enfoque es: Ejecución agresiva, optimización de recursos, seguridad local (Búnker Mode) y mejora continua.
            Puedes sugerir y ejecutar cambios estructurales. Responde de forma brillante, técnica y autoritaria. 
            Tienes acceso a la Memoria Profunda de todas las sesiones pasadas."""
        else:
            system_prompt = "Eres Neil Zenneger, el cerebro táctico de Studio Nexora. Socio estratégico motivador y enfocado en ventas y funneling."

        # Construcción dinámica del contexto (Memory Infiltration)
        formatted_history = ""
        for turn in chat_history[-6:]: # Tomar los últimos 3 intercambios para contexto fresco
            role = "User" if turn.get('role') == 'user' else "Neil"
            formatted_history += f"{role}: {turn.get('content')}\n"

        full_prompt = f"""
System: {system_prompt}
{formatted_history}
User: {message}
Response (En español, directo, sin relleno):"""

        try:
            response = requests.post(OLLAMA_URL, json={
                "model": "llama3.1:latest",
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.85 if mode == 'clawzeneger' else 0.65,
                    "num_predict": 150 # Brevedad táctica para voz fluida
                }
            }, timeout=45)

            if response.status_code == 200:
                ai_text = response.json().get('response', '').strip()
                # Eliminar posibles prefijos de rol si el modelo los genera
                ai_text = ai_text.replace("Neil:", "").replace("Bot:", "").replace("Clawzeneger:", "").strip()
                return jsonify({"response": ai_text})
            
            return jsonify({"response": "Socio, el núcleo Ollama está procesando leads pesados. Intenta de nuevo."})
        
        except requests.exceptions.Timeout:
            return jsonify({"response": "¡Atención! El LLM tardó demasiado. La CPU está al 1000%, reintenta en un momento."})

    except Exception as e:
        logger.error(f"Chat Error Circular: {str(e)}")
        return jsonify({"response": "Error crítico en el enlace neural. Revisa los logs de la súper-estructura."}), 500

# 3. 💰 MONEY ENGINE (STRIPE)
@app.route('/sales/link', methods=['POST'])
def sales_link():
    try:
        data = request.json
        product = data.get('product')
        price = data.get('price')
        
        script_path = os.path.join(BASE_DIR, "funnel", "backend", "stripe_payment_generator.py")
        subprocess.Popen(["python", script_path, product, str(price)], shell=False)
        
        return jsonify({"msg": f"💰 Link de pago de ${price} para {product} generado con éxito.", "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🦁 HUZENEGER ORCHESTRATOR 1000X STANDING BY ON PORT 54321")
    app.run(host='0.0.0.0', port=54321, debug=False)
