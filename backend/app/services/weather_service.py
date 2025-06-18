import requests
import json
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.config import settings
from app.schemas import WeatherData, WeatherResponse
from app.services.cache_service import CacheService

class WeatherService:
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = CacheService()
    
    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make a request to OpenWeatherMap API."""
        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenWeatherMap API key not configured"
            )
        
        params['appid'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch weather data: {str(e)}"
            )
    
    def _kelvin_to_celsius(self, kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return round(kelvin - 273.15, 2)
    
    def _parse_current_weather(self, data: dict, location: str) -> WeatherResponse:
        """Parse current weather data."""
        weather_data = WeatherData(
            date=datetime.now().strftime("%a %B %d %Y"),
            main=data['weather'][0]['main'],
            temp=self._kelvin_to_celsius(data['main']['temp']),
            description=data['weather'][0]['description']
        )
        
        return WeatherResponse(
            count=1,
            unit="metric",
            location=location,
            data=[weather_data]
        )
    
    def _parse_forecast_weather(self, data: dict, location: str) -> WeatherResponse:
        """Parse 5-day forecast weather data."""
        weather_list = []
        
        # Group by date and take one entry per day
        daily_data = {}
        for item in data['list'][:10]:  # Limit to 10 entries (about 3-4 days)
            date_str = datetime.fromtimestamp(item['dt']).strftime("%a %B %d %Y")
            if date_str not in daily_data:
                daily_data[date_str] = item
        
        for date_str, item in daily_data.items():
            weather_data = WeatherData(
                date=date_str,
                main=item['weather'][0]['main'],
                temp=self._kelvin_to_celsius(item['main']['temp']),
                description=item['weather'][0]['description']
            )
            weather_list.append(weather_data)
        
        return WeatherResponse(
            count=len(weather_list),
            unit="metric",
            location=location,
            data=weather_list
        )
    
    async def get_current_weather(self, location: str) -> WeatherResponse:
        """Get current weather for a location."""
        cache_key = f"weather:current:{location.lower()}"
        
        # Try to get from cache first
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return WeatherResponse(**json.loads(cached_result))
        
        # Prepare parameters
        params = {
            'q': location,
            'units': 'metric'
        }
        
        # Make API request
        response_data = self._make_request("weather", params)
        
        # Parse response
        weather_response = self._parse_current_weather(response_data, location)
        
        # Cache the result for 10 minutes
        await self.cache.set(cache_key, weather_response.json(), expire=600)
        
        return weather_response
    
    async def get_weather_forecast(self, location: str) -> WeatherResponse:
        """Get 5-day weather forecast for a location."""
        cache_key = f"weather:forecast:{location.lower()}"
        
        # Try to get from cache first
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return WeatherResponse(**json.loads(cached_result))
        
        # Prepare parameters
        params = {
            'q': location,
            'units': 'metric'
        }
        
        # Make API request
        response_data = self._make_request("forecast", params)
        
        # Parse response
        weather_response = self._parse_forecast_weather(response_data, location)
        
        # Cache the result for 30 minutes
        await self.cache.set(cache_key, weather_response.json(), expire=1800)
        
        return weather_response 