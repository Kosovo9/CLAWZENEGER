from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HF_PROXY_URL: str = "http://hf-proxy:8000"
    LITELLM_MASTER_KEY: str = "sk-clawzeneger-secret-key"
    WHISPER_URL: str = "http://whisper:9000"
    XTTS_URL: str = "http://xtts:5002"
    REDIS_URL: str = "redis://redis:6379/0"
    CHROMADB_HOST: str = "chromadb"
    CHROMADB_PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
