import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # FastAPI Configuration
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Configuration
    database_url: str = "sqlite:///./news_weather.db"
    
    # Third-party APIs
    newsapi_key: Optional[str] = None
    openweather_api_key: Optional[str] = None
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # Application Configuration
    app_name: str = "News & Weather API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings() 