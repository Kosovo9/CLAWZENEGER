
from fastapi import APIRouter, Depends, Request
import httpx
from ..config import settings
from ..utils.auth import verify_api_key

router = APIRouter()
# Cliente HTTP asíncrono reutilizable
client = httpx.AsyncClient(base_url=settings.FUNNEL_API_URL, timeout=30.0)

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_funnel(path: str, request: Request, api_key: str = Depends(verify_api_key)):
    url = f"/{path}"
    if request.query_params:
        url += "?" + str(request.query_params)
    
    # Leer body
    body = await request.body()
    
    # Filtrar headers conflictivos
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length"]}
    
    try:
        resp = await client.request(
            method=request.method,
            url=url,
            content=body,
            headers=headers
        )
        return resp.json()
    except httpx.RequestError as exc:
        return {"error": f"Error connecting to Funnel Service: {exc}"}
