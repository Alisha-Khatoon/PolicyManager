from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:5173/auth/google/callback"
    FRONTEND_URL: str = "http://localhost:5173"
    DEBUG: bool = False
    COOKIE_DOMAIN: str = "localhost"
    PRODUCTION: bool = False
    VITE_API_URL: str = "http://localhost:8000/api"

    class Config:
        env_file = Path(__file__).parent.parent / ".env"  
        extra = "ignore"  # Prevent ValidationError for extra env vars

settings = Settings()
