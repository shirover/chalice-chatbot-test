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

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Add rate limit exceeded handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middleware for request ID tracking and body size limit
@app.middleware("http")
async def add_request_id_and_limit_size(request: Request, call_next):
    # Generate request ID for tracing
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Check request body size limit (1MB)
    if request.headers.get("content-length"):
        content_length = int(request.headers["content-length"])
        if content_length > 1024 * 1024:  # 1MB limit
            logger.warning(f"Request {request_id} rejected: body too large ({content_length} bytes)")
            return JSONResponse(
                status_code=413,
                content={"detail": "Request body too large. Maximum size is 1MB"},
                headers={"X-Request-ID": request_id}
            )
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Add CSP header for production with stricter settings
    if settings.ENVIRONMENT == "production":
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "  # No unsafe-eval for better XSS protection
            "style-src 'self' 'unsafe-inline'; "  # Keep unsafe-inline for styles only
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' " + " ".join(settings.allowed_origins) + "; "
            "frame-ancestors 'none';"
        )
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add trusted host middleware for production
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
@limiter.limit("10/minute")  # Add rate limiting to health check to prevent abuse
async def health_check(request: Request):
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }