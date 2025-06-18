# News & Weather Aggregation API

A FastAPI-based backend service that provides authenticated access to news data and public access to weather information from third-party APIs.

## Features

- **🔐 Authentication**: JWT-based user registration, login, and logout
- **📰 News API**: Authenticated access to news articles from NewsAPI
- **🌤️ Weather API**: Public access to weather data from OpenWeatherMap
- **⚡ Caching**: Redis/in-memory caching for improved performance
- **🛡️ Rate Limiting**: Protection against API abuse
- **📊 Monitoring**: Request timing and health checks
- **🧪 Testing**: Comprehensive unit tests with pytest
- **🐳 Docker**: Containerized deployment

## Quick Start

### Prerequisites

- Python 3.8+
- API keys for NewsAPI and OpenWeatherMap (optional for testing)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## API Endpoints

### Authentication (Required for News)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/signup` | Register a new user |
| POST | `/api/login` | Login and get JWT token |
| POST | `/api/logout` | Logout and blacklist token |
| GET | `/api/me` | Get current user info |

### News (Authenticated)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/news` | Get top headlines |
| GET | `/api/news?search=query` | Search news articles |

### Weather (Public)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/weather?location=city` | Get current weather |
| GET | `/api/weather?location=city&forecast=true` | Get weather forecast |

## Configuration

### Environment Variables

```bash
# FastAPI Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./news_weather.db

# Third-party APIs
NEWSAPI_KEY=your-newsapi-key-here
OPENWEATHER_API_KEY=your-openweather-api-key-here

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Application Configuration
APP_NAME=News & Weather API
APP_VERSION=1.0.0
DEBUG=True
```

### API Keys Setup

1. **NewsAPI**: Get your free API key from [NewsAPI](https://newsapi.org/)
2. **OpenWeatherMap**: Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

## Usage Examples

### Authentication Flow

1. **Register a new user:**
```bash
curl -X POST "http://localhost:8000/api/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "password": "secure123"
     }'
```

2. **Login to get token:**
```bash
curl -X POST "http://localhost:8000/api/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "password": "secure123"
     }'
```

3. **Use token for authenticated requests:**
```bash
curl -X GET "http://localhost:8000/api/news" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Weather Data (No Authentication)

```bash
# Current weather
curl "http://localhost:8000/api/weather?location=London"

# Weather forecast
curl "http://localhost:8000/api/weather?location=London&forecast=true"
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t news-weather-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -e NEWSAPI_KEY=your-key \
  -e OPENWEATHER_API_KEY=your-key \
  news-weather-api
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database models and setup
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── middleware.py        # Custom middleware
│   ├── routers/
│   │   ├── auth.py          # Authentication routes
│   │   ├── news.py          # News routes
│   │   └── weather.py       # Weather routes
│   └── services/
│       ├── cache_service.py # Caching service
│       ├── news_service.py  # News API integration
│       └── weather_service.py # Weather API integration
├── tests/
│   └── test_auth.py         # Authentication tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md               # This file
```

### Code Quality

The project follows these practices:

- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception handling
- **Validation**: Pydantic models for request/response validation
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Security**: JWT authentication, password hashing, rate limiting
- **Performance**: Caching, connection pooling, async operations

## Performance Features

- **Caching**: Responses cached for 10-30 minutes to reduce API calls
- **Rate Limiting**: 100 requests per minute per IP by default
- **Async Operations**: Non-blocking I/O for better concurrency
- **Connection Pooling**: Efficient database connections
- **Request Timing**: Performance monitoring headers

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Token Blacklisting**: Logout invalidates tokens
- **Rate Limiting**: Protection against abuse
- **CORS Configuration**: Configurable cross-origin requests
- **Input Validation**: Pydantic schema validation

## Monitoring & Health

- **Health Check**: `/health` endpoint for service monitoring
- **Request Timing**: `X-Process-Time` header in responses
- **Structured Logging**: Comprehensive application logging
- **Error Tracking**: Global exception handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please:

1. Check the [documentation](http://localhost:8000/docs)
2. Search existing issues
3. Create a new issue with detailed information

---

Built with ❤️ using FastAPI, SQLAlchemy, and modern Python practices. 