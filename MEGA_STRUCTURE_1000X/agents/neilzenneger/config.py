from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    AGENT_NAME: str = "neilzenneger"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # URLs de servicios
    ORCHESTRATOR_URL: str = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")
    FUNNEL_URL: str = os.getenv("FUNNEL_URL", "http://funnel-backend:8002")
    AFFILIATE_URL: str = os.getenv("AFFILIATE_URL", "http://affiliate-backend:9200")
    SCRAPER_URL: str = os.getenv("SCRAPER_URL", "http://scraper-api:8001")
    
    # API Keys
    HUBZENEGER_API_KEY: str = os.getenv("HUBZENEGER_API_KEY", "")
    
    # ChromaDB
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "chromadb")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))
    
    # Horarios (en formato cron)
    AUDIT_CRON: str = os.getenv("AUDIT_CRON", "0 */3 * * *")  
    DAILY_PLAN_CRON: str = os.getenv("DAILY_PLAN_CRON", "0 9 * * *")  
    NIGHTLY_REPORT_CRON: str = os.getenv("NIGHTLY_REPORT_CRON", "0 21 * * *")  
    
    # Webhook para notificaciones (opcional)
    NOTIFICATION_WEBHOOK: str = os.getenv("NOTIFICATION_WEBHOOK", "")

settings = Settings()
