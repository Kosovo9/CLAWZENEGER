
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Clawzeneger Scraper Intelligent"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://claw:claw123@postgres:5432/clawscraper")
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "chromadb")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))
    HF_PROXY_URL: str = os.getenv("HF_PROXY_URL", "http://hf-proxy:8000")
    HF_API_KEY: str = os.getenv("LITELLM_MASTER_KEY", "sk-clawzeneger-master-2026")
    YT_DLP_PATH: str = "yt-dlp"

settings = Settings()
