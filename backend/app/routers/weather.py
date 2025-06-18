from fastapi import APIRouter, Query
from app.schemas import WeatherResponse
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api", tags=["Weather"])


@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    location: str = Query(..., description="City name for weather data"),
    forecast: bool = Query(False, description="Get forecast data instead of current weather")
):
    """
    Get weather data for a specific location. No authentication required.
    
    - **location**: City name (e.g., "London", "New York", "Bangalore")
    - **forecast**: Set to true to get forecast data, false for current weather
    - Returns current weather by default
    - Returns 5-day forecast if forecast=true
    """
    weather_service = WeatherService()
    
    if forecast:
        return await weather_service.get_weather_forecast(location)
    else:
        return await weather_service.get_current_weather(location) 