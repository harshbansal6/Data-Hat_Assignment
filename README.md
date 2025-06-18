# Data-Hat Assignment - News & Weather Aggregation

A comprehensive full-stack application that provides authenticated access to news data and public access to weather information, built with FastAPI backend and modern web technologies.

## 🚀 Project Overview

This project delivers fast, reliable, and relevant news and weather updates by aggregating, filtering, and serving clean information from multiple third-party sources. The application consists of:

- **Backend API**: FastAPI-based REST API with JWT authentication
- **Frontend**: Modern web interface (if applicable)

## 🏗️ Architecture

```
Data-Hat_Assignment/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic & external APIs
│   │   ├── auth.py         # JWT authentication
│   │   └── database.py     # SQLAlchemy models
│   ├── tests/              # Unit tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container configuration
└── README.md              # This file
```

## ✨ Features

### 🔐 Authentication System
- User registration with email validation
- JWT-based authentication
- Secure password hashing (bcrypt)
- Token blacklisting for logout
- Protected endpoint access

### 📰 News Integration
- NewsAPI integration for real-time news
- Search functionality for specific topics
- Top headlines aggregation
- Authentication-required access
- Response caching for performance

### 🌤️ Weather Services
- OpenWeatherMap API integration
- Current weather data
- 5-day weather forecasts
- Multi-city support
- Public access (no authentication required)

### ⚡ Performance & Security
- Redis caching for API responses
- Rate limiting (100 requests/minute)
- Request timing monitoring
- CORS configuration
- Comprehensive error handling
- Input validation with Pydantic

### 🧪 Quality Assurance
- Unit tests with pytest
- Test coverage reporting
- Docker containerization
- API documentation (Swagger/OpenAPI)
- Type hints throughout

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API Keys:
  - [NewsAPI](https://newsapi.org/) - Free tier available
  - [OpenWeatherMap](https://openweathermap.org/api) - Free tier available

### Setup Instructions

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Data-Hat_Assignment
```

2. **Backend Setup:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn app.main:app --reload
```

3. **Access the API:**
- API Base URL: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## 📋 API Documentation

### Authentication Endpoints
```
POST /api/signup     - Register new user
POST /api/login      - User authentication
POST /api/logout     - Invalidate token
GET  /api/me         - Get current user info
```

### News Endpoints (🔒 Authenticated)
```
GET /api/news                    - Get top headlines
GET /api/news?search={query}     - Search news articles
```

### Weather Endpoints (🌐 Public)
```
GET /api/weather?location={city}              - Current weather
GET /api/weather?location={city}&forecast=true - Weather forecast
```

## 🔧 Configuration

Key environment variables:

```env
# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
NEWSAPI_KEY=your-newsapi-key
OPENWEATHER_API_KEY=your-openweather-key

# Database
DATABASE_URL=sqlite:///./news_weather.db

# Caching (Optional)
REDIS_URL=redis://localhost:6379

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
cd backend
docker-compose up -d
```

This starts:
- FastAPI application on port 8000
- Redis cache on port 6379
- Persistent data volumes

### Using Docker Only
```bash
cd backend
docker build -t news-weather-api .
docker run -d -p 8000:8000 -e NEWSAPI_KEY=your-key -e OPENWEATHER_API_KEY=your-key news-weather-api
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## 📊 API Usage Examples

### Complete Authentication Flow
```bash
# 1. Register user
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "secure123"}'

# 2. Login to get token
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secure123"}'

# 3. Use token for news access
curl -X GET "http://localhost:8000/api/news" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 4. Search news
curl -X GET "http://localhost:8000/api/news?search=technology" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Public Weather Access
```bash
# Current weather
curl "http://localhost:8000/api/weather?location=London"

# Weather forecast
curl "http://localhost:8000/api/weather?location=London&forecast=true"
```

## 🔍 Sample API Responses

### News Response
```json
{
  "count": 5,
  "articles": [
    {
      "title": "Breaking News Title",
      "description": "Article description...",
      "url": "https://example.com/article",
      "published_at": "2024-01-01T10:00:00Z",
      "source": "BBC News"
    }
  ]
}
```

### Weather Response
```json
{
  "count": 5,
  "unit": "metric",
  "location": "Bangalore",
  "data": [
    {
      "date": "Sun March 06 2024",
      "main": "Rain",
      "temp": 20.4,
      "description": "light rain"
    }
  ]
}
```

## 🛠️ Development

### Project Structure
- **Modular Design**: Separate routers, services, and utilities
- **Type Safety**: Full type annotations with Pydantic
- **Error Handling**: Comprehensive exception management
- **Security**: JWT auth, rate limiting, input validation
- **Performance**: Async operations, caching, connection pooling

### Code Quality Standards
- PEP 8 compliance
- Type hints throughout
- Comprehensive docstrings
- Unit test coverage
- Security best practices

## 📈 Performance Features

- **Caching Strategy**: 10-30 minute cache for API responses
- **Rate Limiting**: Configurable per-IP request limits
- **Async Operations**: Non-blocking I/O for better concurrency
- **Request Monitoring**: Timing headers for performance tracking
- **Health Checks**: Service monitoring endpoints

## 🔒 Security Implementation

- **JWT Authentication**: Secure token-based auth
- **Password Security**: Bcrypt hashing with salt
- **Token Management**: Blacklisting for secure logout
- **Input Validation**: Pydantic schema validation
- **Rate Protection**: Abuse prevention mechanisms
- **CORS Management**: Configurable cross-origin policies

## 🚦 CI/CD Ready

The project includes:
- Dockerfiles for containerization
- Test automation with pytest
- Environment configuration
- Health check endpoints
- Structured logging
- Error monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

For support and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Review the backend [README](backend/README.md)
- Open an issue for bugs or feature requests

---
