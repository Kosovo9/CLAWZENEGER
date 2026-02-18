import redis
import json
import uuid
import asyncio
from typing import Dict, Any, List

class AgentOrchestrator:
    def __init__(self, redis_url="redis://:clawzeneger2026prod@redis:6379/0", redis_client=None):
        if redis_client:
            self.redis = redis_client
        else:
            self.redis = redis.from_url(redis_url, decode_responses=True)
    
    async def send_command(self, agent: str, command: str, params: Dict, user_id: str) -> Dict:
        task_id = str(uuid.uuid4())
        reply_queue = f"user:{user_id}:responses"
        
        message = {
            "task_id": task_id,
            "action": command,
            "params": params,
            "reply_to": reply_queue,
            "user_id": user_id
        }
        
        self.redis.rpush(f"queue:{agent}", json.dumps(message))
        
        # Esperar respuesta
        start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start < 30:
            result = self.redis.blpop(reply_queue, timeout=1)
            if result:
                data = json.loads(result[1])
                if data.get("task_id") == task_id:
                    return data
            await asyncio.sleep(0.1)
        
        return {"status": "timeout", "error": f"No response from agent {agent}"}
    
    async def broadcast_to_agents(self, command: str, params: Any, agents: List[str], user_id: str) -> List[Dict]:
        tasks = []
        for agent in agents:
            # Si params es una lista de acciones del LLM, filtrar para este agente
            if isinstance(params, list):
                agent_params = [p for p in params if p.get("agente") == agent]
                if not agent_params: continue
                tasks.append(self.send_command(agent, command, {"actions": agent_params}, user_id))
            else:
                tasks.append(self.send_command(agent, command, params, user_id))
        
        if not tasks: return []
        return await asyncio.gather(*tasks)

# Instancia unica para el bunker
orchestrator = AgentOrchestrator()
