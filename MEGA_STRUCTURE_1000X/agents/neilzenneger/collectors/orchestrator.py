import httpx
import logging
from ..config import settings

logger = logging.getLogger(__name__)

async def get_agents_status():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.ORCHESTRATOR_URL}/api/v1/agents/status",
                headers={"X-API-Key": settings.HUBZENEGER_API_KEY}
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error fetching agents status: {e}")
        return []

async def get_leads_summary():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.ORCHESTRATOR_URL}/api/v1/leads",
                headers={"X-API-Key": settings.HUBZENEGER_API_KEY}
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error fetching leads summary: {e}")
        return []
