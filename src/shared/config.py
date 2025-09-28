"""
Project configuration for FastAPI with layered architecture and CQRS
"""
import os
from typing import Optional


class Settings:
    """Application settings"""
    
    # Application configuration
    APP_NAME: str = "Spaced Repetition Language Learning API"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "API for language learning using spaced repetition with layered architecture and CQRS"
    
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/spaced_repetition_db"
    )
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Application configuration
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"


# Global settings instance
settings = Settings()
