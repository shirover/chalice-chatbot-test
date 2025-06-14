from typing import List, Optional
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Environment configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # AWS EC2 specific configuration
    AWS_REGION: Optional[str] = os.getenv("AWS_REGION", None)
    EC2_PUBLIC_IP: Optional[str] = os.getenv("EC2_PUBLIC_IP", None)
    
    # Production frontend URL
    PRODUCTION_FRONTEND_URL: Optional[str] = os.getenv("PRODUCTION_FRONTEND_URL", None)
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add EC2 public IP to allowed origins if provided
        if self.EC2_PUBLIC_IP:
            self.ALLOWED_ORIGINS.append(f"http://{self.EC2_PUBLIC_IP}")
            self.ALLOWED_ORIGINS.append(f"https://{self.EC2_PUBLIC_IP}")
        
        # Add production frontend URL if provided
        if self.PRODUCTION_FRONTEND_URL:
            self.ALLOWED_ORIGINS.append(self.PRODUCTION_FRONTEND_URL)

settings = Settings()