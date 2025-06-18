from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth import get_current_user
from app.database import User
from app.schemas import NewsResponse
from app.services.news_service import NewsService

router = APIRouter(prefix="/api", tags=["News"])


@router.get("/news", response_model=NewsResponse)
async def get_news(
    search: Optional[str] = Query(None, description="Search term for news articles"),
    current_user: User = Depends(get_current_user)
):
    """
    Get news articles. Requires authentication.
    
    - **search**: Optional search term to filter news articles
    - Returns top headlines if no search term is provided
    - Returns search results if search term is provided
    """
    news_service = NewsService()
    
    if search:
        return await news_service.search_news(search)
    else:
        return await news_service.get_top_headlines() 