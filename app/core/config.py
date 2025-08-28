from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://tms_user:tms_password@db:5432/tms_db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TMS v3.0 - Multi-tenant Transport Management System"
    
    # File Storage
    REPORTS_DIR: str = "/app/reports"
    
    # v3.0 - Novas configurações
    # Multi-tenant
    DEFAULT_TENANT_ID: str = "default"
    
    # Integrações
    GOOGLE_MAPS_API_KEY: str = ""
    OPENSTREETMAP_ENABLED: bool = True
    
    # Notificações
    SENDGRID_API_KEY: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    class Config:
        env_file = ".env"


settings = Settings()