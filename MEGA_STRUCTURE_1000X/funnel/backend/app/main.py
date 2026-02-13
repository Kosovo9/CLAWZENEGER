
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import funnel
from .database import engine, Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Placeholder routers for leads and ai (to be implemented fully)
from fastapi import APIRouter
leads_router = APIRouter()
ai_router = APIRouter()

@leads_router.get("/")
def get_leads_placeholder():
    return {"message": "Leads logic coming soon"}

@ai_router.get("/score")
def get_score_placeholder():
    return {"message": "AI scoring logic coming soon"}

app.include_router(funnel.router, prefix=f"{settings.API_V1_STR}/funnels", tags=["funnels"])
app.include_router(leads_router, prefix=f"{settings.API_V1_STR}/leads", tags=["leads"])
app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "Funnel Premium"}
