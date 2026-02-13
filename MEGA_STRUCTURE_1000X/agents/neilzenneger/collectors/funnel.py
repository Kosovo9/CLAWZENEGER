import httpx
import logging
from ..config import settings

logger = logging.getLogger(__name__)

async def get_daily_stats():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.FUNNEL_URL}/api/v1/stats/daily")
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error fetching funnel stats: {e}")
        return {"leads": 0, "conversions": 0, "revenue": 0}

async def get_recent_transactions(limit=10):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.FUNNEL_URL}/api/v1/transactions?limit={limit}")
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        return []
