import pytest
from app.core.config import Settings
import os

def test_default_settings():
    settings = Settings()
    assert settings.PROJECT_NAME == "Chatbot API"
    assert settings.PROJECT_VERSION == "1.0.0"
    assert settings.ENVIRONMENT == "development"
    assert settings.HOST == "0.0.0.0"
    assert settings.PORT == 8000
    assert settings.RATE_LIMIT_PER_MINUTE == 60
    assert settings.LOG_LEVEL == "INFO"

def test_cors_origins():
    settings = Settings()
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS
    assert "http://localhost:5173" in settings.ALLOWED_ORIGINS

def test_ec2_configuration():
    # EC2設定でテスト
    os.environ["EC2_PUBLIC_IP"] = "54.123.45.67"
    settings = Settings()
    
    assert f"http://54.123.45.67" in settings.ALLOWED_ORIGINS
    assert f"https://54.123.45.67" in settings.ALLOWED_ORIGINS
    
    # クリーンアップ
    del os.environ["EC2_PUBLIC_IP"]

def test_production_frontend_url():
    os.environ["PRODUCTION_FRONTEND_URL"] = "https://mychatbot.com"
    settings = Settings()
    
    assert "https://mychatbot.com" in settings.ALLOWED_ORIGINS
    
    # クリーンアップ
    del os.environ["PRODUCTION_FRONTEND_URL"]