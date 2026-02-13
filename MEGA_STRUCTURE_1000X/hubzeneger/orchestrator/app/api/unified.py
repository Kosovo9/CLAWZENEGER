
from fastapi import APIRouter, Depends
from ..utils.auth import verify_api_key
import httpx
from ..config import settings
import asyncio

router = APIRouter()

@router.get("/leads")
async def get_all_leads(api_key: str = Depends(verify_api_key)):
    """Obtiene leads de todos los sistemas (funnel + scraper) y los unifica"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Ejecutar peticiones en paralelo
        try:
            funnel_req = client.get(f"{settings.FUNNEL_API_URL}/leads")
            scraper_req = client.get(f"{settings.SCRAPER_API_URL}/leads")
            
            responses = await asyncio.gather(funnel_req, scraper_req, return_exceptions=True)
            
            funnel_data = responses[0].json() if not isinstance(responses[0], Exception) and responses[0].status_code == 200 else []
            scraper_data = responses[1].json() if not isinstance(responses[1], Exception) and responses[1].status_code == 200 else []
            
            return {
                "total": len(funnel_data) + len(scraper_data),
                "sources": {
                    "funnel": funnel_data,
                    "scraper": scraper_data
                }
            }
        except Exception as e:
            return {"error": str(e)}

@router.get("/stats")
async def get_global_stats(api_key: str = Depends(verify_api_key)):
    """Métricas globales para el dashboard"""
    return {
        "revenue_mtd": 12500, # Fake por ahora, conectar a Stripe
        "active_funnels": 3,   # Conectar a funnel service
        "leads_today": 12,
        "agents_active": 3
    }
