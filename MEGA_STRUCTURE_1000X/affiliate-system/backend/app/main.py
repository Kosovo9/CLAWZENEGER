from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import affiliates, webhooks
from .config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Routers
app.include_router(affiliates.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Clawzeneger Affiliate API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
