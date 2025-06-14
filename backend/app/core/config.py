from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot API"
    PROJECT_VERSION: str = "1.0.0"
    
    # 環境設定
    ENVIRONMENT: str = Field(default="development")
    
    # サーバー設定
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # CORS設定 - 動的にするためプロパティを使用
    _allowed_origins_base: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # AWS EC2固有の設定
    AWS_REGION: Optional[str] = Field(default=None)
    EC2_PUBLIC_IP: Optional[str] = Field(default=None)
    
    # プロダクションフロントエンドURL
    PRODUCTION_FRONTEND_URL: Optional[str] = Field(default=None)
    
    # レート制限
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    
    # リクエストサイズ制限（デフォルト1MB）
    MAX_REQUEST_SIZE: int = Field(default=1024 * 1024)
    
    # ログ設定
    LOG_LEVEL: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
    
    @property
    def allowed_origins(self) -> List[str]:
        """設定に基づいて許可されたオリジンリストを動的に構築"""
        origins = self._allowed_origins_base.copy()
        
        # EC2パブリックIPが提供されている場合、許可されたオリジンに追加
        if self.EC2_PUBLIC_IP:
            origins.append(f"http://{self.EC2_PUBLIC_IP}")
            origins.append(f"https://{self.EC2_PUBLIC_IP}")
        
        # プロダクションフロントエンドURLが提供されている場合は追加
        if self.PRODUCTION_FRONTEND_URL:
            origins.append(self.PRODUCTION_FRONTEND_URL)
            
        return origins

settings = Settings()