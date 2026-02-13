from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Clawzeneger Affiliate System"
    
    # Database (Postgres del stack God Mode)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://litellm:litellm@postgres:5432/affiliate")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # JWT / Auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "claw-affiliate-secret-key-2026")
    JWT_ALGORITHM: str = "HS256"
    
    # Supabase (Si se usa auth de Supabase)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # URL base para enlaces de afiliado
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:3000")
    
    # Configuración de Comisión (30% por defecto)
    DEFAULT_COMMISSION_RATE: float = 30.0

settings = Settings()
