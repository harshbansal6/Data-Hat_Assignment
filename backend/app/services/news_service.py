import requests
import json
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.config import settings
from app.schemas import NewsArticle, NewsResponse
from app.services.cache_service import CacheService

class NewsService:
    def __init__(self):
        self.api_key = settings.newsapi_key
        self.base_url = "https://newsapi.org/v2"
        self.cache = CacheService()
    
    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make a request to NewsAPI."""
        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="NewsAPI key not configured"
            )
        
        params['apiKey'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch news: {str(e)}"
            )
    
    def _parse_articles(self, articles: List[dict]) -> List[NewsArticle]:
        """Parse articles from NewsAPI response."""
        parsed_articles = []
        for article in articles:
            try:
                parsed_article = NewsArticle(
                    title=article.get('title', ''),
                    description=article.get('description'),
                    url=article.get('url', ''),
                    published_at=article.get('publishedAt', ''),
                    source=article.get('source', {}).get('name', 'Unknown')
                )
                parsed_articles.append(parsed_article)
            except Exception:
                # Skip invalid articles
                continue
        return parsed_articles
    
    async def get_top_headlines(self, search: Optional[str] = None) -> NewsResponse:
        """Get top headlines, optionally filtered by search term."""
        # Create cache key
        cache_key = f"news:headlines:{search or 'top'}"
        
        # Try to get from cache first
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return NewsResponse(**json.loads(cached_result))
        
        # Prepare parameters
        params = {
            'country': 'us',
            'pageSize': 20
        }
        
        if search:
            params['q'] = search
            del params['country']  # Can't use country with search
        
        # Make API request
        response_data = self._make_request("top-headlines", params)
        
        # Parse articles
        articles = self._parse_articles(response_data.get('articles', []))
        
        # Create response
        news_response = NewsResponse(
            count=len(articles),
            articles=articles
        )
        
        # Cache the result for 15 minutes
        await self.cache.set(cache_key, news_response.json(), expire=900)
        
        return news_response
    
    async def search_news(self, query: str) -> NewsResponse:
        """Search for news articles."""
        cache_key = f"news:search:{query}"
        
        # Try to get from cache first
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return NewsResponse(**json.loads(cached_result))
        
        # Prepare parameters
        params = {
            'q': query,
            'sortBy': 'publishedAt',
            'pageSize': 20
        }
        
        # Make API request
        response_data = self._make_request("everything", params)
        
        # Parse articles
        articles = self._parse_articles(response_data.get('articles', []))
        
        # Create response
        news_response = NewsResponse(
            count=len(articles),
            articles=articles
        )
        
        # Cache the result for 10 minutes
        await self.cache.set(cache_key, news_response.json(), expire=600)
        
        return news_response 