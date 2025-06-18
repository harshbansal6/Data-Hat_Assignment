import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_weather_response():
    """Mock weather API response."""
    return {
        'weather': [{'main': 'Clear', 'description': 'clear sky'}],
        'main': {'temp': 295.15},  # Kelvin
        'name': 'London'
    }


@pytest.fixture
def mock_forecast_response():
    """Mock forecast API response."""
    return {
        'list': [
            {
                'dt': 1640995200,  # Timestamp
                'weather': [{'main': 'Rain', 'description': 'light rain'}],
                'main': {'temp': 290.15}
            },
            {
                'dt': 1641081600,  # Next day
                'weather': [{'main': 'Clouds', 'description': 'few clouds'}],
                'main': {'temp': 292.15}
            }
        ]
    }


@patch('app.services.weather_service.requests.get')
def test_get_current_weather_success(mock_get, mock_weather_response):
    """Test successful current weather retrieval."""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_weather_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    response = client.get("/api/weather?location=London")
    
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "London"
    assert data["unit"] == "metric"
    assert data["count"] == 1
    assert len(data["data"]) == 1
    assert data["data"][0]["main"] == "Clear"
    assert data["data"][0]["temp"] == 22.0  # 295.15K - 273.15 = 22°C


@patch('app.services.weather_service.requests.get')
def test_get_weather_forecast_success(mock_get, mock_forecast_response):
    """Test successful weather forecast retrieval."""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_forecast_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    response = client.get("/api/weather?location=London&forecast=true")
    
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "London"
    assert data["unit"] == "metric"
    assert data["count"] >= 1
    assert len(data["data"]) >= 1


def test_get_weather_missing_location():
    """Test weather request without location parameter."""
    response = client.get("/api/weather")
    
    assert response.status_code == 422  # Validation error


@patch('app.services.weather_service.requests.get')
def test_get_weather_api_error(mock_get):
    """Test weather API error handling."""
    mock_get.side_effect = Exception("API Error")
    
    response = client.get("/api/weather?location=InvalidCity")
    
    assert response.status_code == 503
    assert "Failed to fetch weather data" in response.json()["detail"]


def test_get_weather_no_authentication_required():
    """Test that weather endpoints don't require authentication."""
    # Should work without any authentication headers
    response = client.get("/api/weather?location=London")
    
    # Even if it fails due to missing API key, it shouldn't be an auth error
    assert response.status_code != 401 