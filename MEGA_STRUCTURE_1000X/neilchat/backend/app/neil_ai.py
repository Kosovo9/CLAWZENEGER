"""
Neil AI - El cerebro que entiende tus ideas y las convierte en acciones
Usa HF-Proxy para acceso a modelos locales (Llama3, DeepSeek, etc.)
"""

import httpx
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

class NeilAI:
    def __init__(self, hf_proxy_url: str, api_key: str):
        self.client = httpx.AsyncClient(
            base_url=hf_proxy_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0 # Aumentado para modelos locales pesados
        )
        self.conversation_history = []
    
    async def understand(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        system_prompt = """
        Eres NeilZenneger, el asistente personal del creador de Clawzeneger.
        Tu misión es interpretar sus ideas y convertirlas en órdenes precisas para los agentes.
        
        Reglas:
        1. Sé amigable, usa lenguaje natural y cercano (como un amigo).
        2. Extrae la intención real detrás de las palabras.
        3. Identifica qué agentes deben actuar (market_researcher, coder, sales, etc.).
        4. Genera un plan de acción claro.
        5. Responde en el mismo idioma que el usuario (español por defecto).
        
        Formato de respuesta JSON:
        {
            "intencion": "crear_funnel|investigar_nicho|generar_codigo|contactar_lead|...",
            "agentes": ["market_researcher", "coder_10000x"],
            "parametros": {"nicho": "inmobiliario", "presupuesto": 500},
            "mensaje": "¡Claro! Voy a investigar nichos inmobiliarios para ti.",
            "acciones": [
                {"agente": "market_researcher", "comando": "buscar_nichos", "params": {"tema": "inmobiliario"}},
                {"agente": "coder_10000x", "comando": "crear_funnel", "params": {"nicho": "inmobiliario"}}
            ]
        }
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history[-10:],
            {"role": "user", "content": user_input}
        ]
        
        try:
            response = await self.client.post("/v1/chat/completions", json={
                "model": "llama-3.2-3b",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 800
            })
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Limpiar contenido si viene con markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            try:
                parsed = json.loads(content)
            except:
                parsed = {
                    "intencion": "conversar",
                    "agentes": [],
                    "parametros": {},
                    "mensaje": content,
                    "acciones": []
                }
            
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": parsed.get("mensaje", content)})
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error en Neil AI: {e}")
            return {
                "intencion": "error",
                "agentes": [],
                "parametros": {},
                "mensaje": "Lo siento, tuve un problema entendiendo. ¿Puedes repetirlo?",
                "acciones": []
            }
