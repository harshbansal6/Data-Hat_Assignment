from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
from app.config import settings
from app.routers import auth, news, weather
from app.middleware import limiter, rate_limit_handler, setup_cors, TimingMiddleware
from app.services.cache_service import CacheService
from slowapi.errors import RateLimitExceeded


# Cache cleanup task
async def cleanup_cache():
    """Periodic task to clean up expired cache entries."""
    cache_service = CacheService()
    while True:
        await cache_service.clear_expired()
        await asyncio.sleep(300)  # Run every 5 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting up News & Weather API...")
    
    # Start cache cleanup task
    cleanup_task = asyncio.create_task(cleanup_cache())
    
    yield
    
    # Shutdown
    print("Shutting down News & Weather API...")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    News & Weather Aggregation API
    
    This API provides:
    - **Authentication**: User registration, login, and logout with JWT tokens
    - **News**: Authenticated access to news articles from NewsAPI
    - **Weather**: Public access to weather data from OpenWeatherMap
    
    ## Authentication
    
    Most endpoints require authentication. To access protected endpoints:
    1. Register a new account using `/api/signup`
    2. Login using `/api/login` to receive a JWT token
    3. Include the token in the Authorization header: `Bearer <your-token>`
    
    ## Rate Limiting
    
    This API implements rate limiting to ensure fair usage:
    - Default: 100 requests per minute per IP
    - Rate limits are enforced across all endpoints
    
    ## Caching
    
    Response caching is implemented to improve performance:
    - News data: Cached for 10-15 minutes
    - Weather data: Cached for 10-30 minutes
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Setup middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_middleware(TimingMiddleware)
setup_cors(app)

# Include routers
app.include_router(auth.router)
app.include_router(news.router)
app.include_router(weather.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to News & Weather API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": settings.app_version
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    if settings.debug:
        # In debug mode, show the actual error
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Internal server error: {str(exc)}",
                "status": "error",
                "type": type(exc).__name__
            }
        )
    else:
        # In production, show a generic error message
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "status": "error"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 