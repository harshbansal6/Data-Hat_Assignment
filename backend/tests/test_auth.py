import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test."""
    # Setup
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown
    Base.metadata.drop_all(bind=engine)


def test_signup_success():
    """Test successful user registration."""
    response = client.post(
        "/api/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_signup_duplicate_email():
    """Test registration with duplicate email."""
    # First registration
    client.post(
        "/api/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Second registration with same email
    response = client.post(
        "/api/signup",
        json={
            "name": "Another User",
            "email": "test@example.com",
            "password": "anotherpassword"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_signup_invalid_password():
    """Test registration with invalid password."""
    response = client.post(
        "/api/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123"  # Too short
        }
    )
    assert response.status_code == 422


def test_login_success():
    """Test successful login."""
    # First, register a user
    client.post(
        "/api/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Then, login
    response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user():
    """Test getting current user information."""
    # Register and login
    client.post(
        "/api/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    login_response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"


def test_logout():
    """Test user logout."""
    # Register and login
    client.post(
        "/api/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    login_response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Logout
    response = client.post(
        "/api/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/api/me")
    assert response.status_code == 401 