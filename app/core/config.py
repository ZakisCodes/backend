from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./social_media.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Supabase settings (commented for demo)
    # supabase_url: Optional[str] = None
    # supabase_key: Optional[str] = None
    # supabase_jwt_secret: Optional[str] = None
    
    # File upload settings
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"


settings = Settings()