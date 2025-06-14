from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import chat
from app.core.config import settings
import uuid
import logging
from urllib.parse import urlparse

# 構造化ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# レート制限の初期化
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# レート制限超過ハンドラーを追加
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# リクエストIDトラッキングとボディサイズ制限のミドルウェアを追加
@app.middleware("http")
async def add_request_id_and_limit_size(request: Request, call_next):
    # トレース用のリクエストIDを生成
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # リクエストボディサイズ制限をチェック (1MB)
    if request.headers.get("content-length"):
        content_length = int(request.headers["content-length"])
        if content_length > 1024 * 1024:  # 1MB制限
            logger.warning(f"Request {request_id} rejected: body too large ({content_length} bytes)")
            return JSONResponse(
                status_code=413,
                content={"detail": "Request body too large. Maximum size is 1MB"},
                headers={"X-Request-ID": request_id}
            )
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# セキュリティヘッダーミドルウェアを追加
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # プロダクション環境用により厳格な設定でCSPヘッダーを追加
    if settings.ENVIRONMENT == "production":
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "  # XSS保護を強化するためunsafe-evalなし
            "style-src 'self' 'unsafe-inline'; "  # スタイルのみunsafe-inlineを維持
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' " + " ".join(settings.allowed_origins) + "; "
            "frame-ancestors 'none';"
        )
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# プロダクション用の信頼済みホストミドルウェアを追加
if settings.ENVIRONMENT == "production" and settings.PRODUCTION_FRONTEND_URL:
    parsed_url = urlparse(settings.PRODUCTION_FRONTEND_URL)
    if parsed_url.hostname:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[parsed_url.hostname, f"*.{parsed_url.hostname}"]
        )

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Chatbot API"}

@app.get("/health")
@limiter.limit("10/minute")  # 悪用防止のためヘルスチェックにレート制限を追加
async def health_check(request: Request):
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }