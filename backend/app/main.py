from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import chat
from app.core.config import settings

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Add rate limit exceeded handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middleware for request body size limit (1MB)
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    if request.headers.get("content-length"):
        content_length = int(request.headers["content-length"])
        if content_length > 1024 * 1024:  # 1MB limit
            return JSONResponse(
                status_code=413,
                content={"detail": "Request body too large. Maximum size is 1MB"}
            )
    response = await call_next(request)
    return response

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Add CSP header for production
    if settings.ENVIRONMENT == "production":
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' " + " ".join(settings.ALLOWED_ORIGINS) + "; "
            "frame-ancestors 'none';"
        )
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add trusted host middleware for production
if settings.ENVIRONMENT == "production" and settings.PRODUCTION_FRONTEND_URL:
    import urllib.parse
    parsed_url = urllib.parse.urlparse(settings.PRODUCTION_FRONTEND_URL)
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
async def health_check():
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }