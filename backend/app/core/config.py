from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Environment configuration
    ENVIRONMENT: str = Field(default="development")
    
    # Server configuration
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # CORS configuration - use property to make it dynamic
    _allowed_origins_base: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # AWS EC2 specific configuration
    AWS_REGION: Optional[str] = Field(default=None)
    EC2_PUBLIC_IP: Optional[str] = Field(default=None)
    
    # Production frontend URL
    PRODUCTION_FRONTEND_URL: Optional[str] = Field(default=None)
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    
    # Request size limit (1MB by default)
    MAX_REQUEST_SIZE: int = Field(default=1024 * 1024)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
    
    @property
    def allowed_origins(self) -> List[str]:
        """Dynamically build allowed origins list based on configuration"""
        origins = self._allowed_origins_base.copy()
        
        # Add EC2 public IP to allowed origins if provided
        if self.EC2_PUBLIC_IP:
            origins.append(f"http://{self.EC2_PUBLIC_IP}")
            origins.append(f"https://{self.EC2_PUBLIC_IP}")
        
        # Add production frontend URL if provided
        if self.PRODUCTION_FRONTEND_URL:
            origins.append(self.PRODUCTION_FRONTEND_URL)
            
        return origins

settings = Settings()