
from fastapi import APIRouter, Depends, Request
import httpx
from ..config import settings
from ..utils.auth import verify_api_key

router = APIRouter()
client = httpx.AsyncClient(base_url=settings.SCRAPER_API_URL, timeout=30.0)

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_scraper(path: str, request: Request, api_key: str = Depends(verify_api_key)):
    url = f"/{path}"
    if request.query_params:
        url += "?" + str(request.query_params)
    
    body = await request.body()
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
        return {"error": f"Error connecting to Scraper Service: {exc}"}
