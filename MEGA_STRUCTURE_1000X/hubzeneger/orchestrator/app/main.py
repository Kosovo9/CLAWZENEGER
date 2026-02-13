
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import funnel_proxy, scraper_proxy, agents_proxy, unified
from .config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# CORS permisivo para dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(funnel_proxy.router, prefix="/api/v1/funnel", tags=["Funnel"])
app.include_router(scraper_proxy.router, prefix="/api/v1/scraper", tags=["Scraper"])
app.include_router(agents_proxy.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(unified.router, prefix="/api/v1", tags=["Unified"])

@app.get("/")
async def root():
    return {"message": "HubZeneger Orchestrator Running", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok"}
