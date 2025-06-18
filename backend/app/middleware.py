import time
from typing import Dict
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config import settings

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)


# Rate limit exceeded handler
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit exceeded handler."""
    response = JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "message": f"Rate limit exceeded: {exc.detail}",
            "status": "error"
        }
    )
    response.headers["Retry-After"] = str(exc.retry_after)
    return response


# CORS middleware configuration
def setup_cors(app):
    """Setup CORS middleware."""
    from fastapi.middleware.cors import CORSMiddleware
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Request timing middleware
class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    process_time = time.time() - start_time
                    message["headers"].append(
                        (b"x-process-time", f"{process_time:.4f}".encode())
                    )
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send) 