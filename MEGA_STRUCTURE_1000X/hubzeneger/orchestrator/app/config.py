
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "HubZeneger Orchestrator"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-in-prod")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    # URLs de servicios internos (nombres de contenedor en docker-compose)
    # Valores por defecto apuntan a los nombres definidos en docker-compose.hubzeneger.yml
    FUNNEL_API_URL: str = os.getenv("FUNNEL_API_URL", "http://funnel-backend:8002")
    SCRAPER_API_URL: str = os.getenv("SCRAPER_API_URL", "http://scraper-api:8001")
    MARKET_AGENT_URL: str = os.getenv("MARKET_AGENT_URL", "http://claw-agent-market:8003") 
    CODER_AGENT_URL: str = os.getenv("CODER_AGENT_URL", "http://claw-agent-coder:8004")
    MECHANIC_AGENT_URL: str = os.getenv("MECHANIC_AGENT_URL", "http://claw-agent-mechanic:8005")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://claw:claw123@postgres:5432/hubzeneger")

settings = Settings()
