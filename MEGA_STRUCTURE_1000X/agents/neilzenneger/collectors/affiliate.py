import httpx
import logging
from ..config import settings

logger = logging.getLogger(__name__)

async def get_affiliate_stats():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # En el sistema de afiliados creado, este es el endpoint de admin
            resp = await client.get(f"{settings.AFFILIATE_URL}/api/v1/affiliates/stats")
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error fetching affiliate stats: {e}")
        return {"total_earned": 0, "referrals_count": 0}

async def get_pending_payouts():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.AFFILIATE_URL}/api/v1/admin/payouts?status=pending")
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error fetching pending payouts: {e}")
        return []
