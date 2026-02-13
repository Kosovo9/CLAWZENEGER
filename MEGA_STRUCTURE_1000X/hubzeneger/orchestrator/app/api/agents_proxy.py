
from fastapi import APIRouter, Depends, Request, HTTPException
import httpx
import json
from ..config import settings
from ..utils.auth import verify_api_key
import redis

router = APIRouter()

# Initialize Redis for background task dispatching
r = redis.from_url(settings.REDIS_URL)

AGENTS_METADATA = [
    "orchestrator_agent", "brand_twins", "a2a_commerce", "intent_pipeline",
    "geo_optimizer", "aeo_optimizer", "unified_intent_graph", "content_generator",
    "dark_data_activator", "predictive_analytics", "causal_models", "drift_monitor",
    "realtime_personalizer", "self_healer_advanced", "outcome_pricing",
    "multichannel_optimizer", "b2a2c_platform", "market_researcher",
    "coder_10000x", "mechanic_247"
]

@router.get("/status")
async def get_all_agents_status(api_key: str = Depends(verify_api_key)):
    """Check heartbeat of agents in Redis"""
    results = {}
    
    for agent in AGENTS_METADATA:
        last_seen = r.get(f"heartbeat:{agent}")
        if last_seen:
            results[agent] = {"status": "online", "last_seen": last_seen.decode()}
        else:
            results[agent] = {"status": "unknown", "last_seen": "no data"}
            
    return results

@router.get("/system/metrics")
async def get_system_metrics(api_key: str = Depends(verify_api_key)):
    """Retrieve system-wide performance metrics from the database (simulated query here)"""
    # In a real scenario, we'd query the PerformanceMetric model in PostgreSQL
    # Here we simulate with the most recent values for demo
    metrics = {
        "orchestrator_latency": "0.12s",
        "lead_hunter_throughput": "15 leads/min",
        "redis_queue_depth": r.llen("task:orchestrator_agent"),
        "total_active_agents": len(AGENTS_METADATA)
    }
    return metrics

@router.post("/{agent_name}/run")
async def run_agent_task(agent_name: str, request: Request, api_key: str = Depends(verify_api_key)):
    """Dispatch task to agent via Redis queue or HTTP"""
    
    if agent_name not in AGENTS_METADATA and agent_name not in ["market", "coder", "mechanic"]:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    try:
        body = await request.json()
    except:
        body = {}

    # Logic: Most of our agents are background workers listening on redis queues: task:{agent_name}
    task_payload = {
        "action": "execute",
        "params": body,
        "metadata": {"source": "orchestrator_api"}
    }
    
    # Push to Redis
    queue_name = f"task:{agent_name}"
    r.lpush(queue_name, json.dumps(task_payload))
    
    return {
        "status": "dispatched",
        "agent": agent_name,
        "queue": queue_name,
        "payload": task_payload
    }
