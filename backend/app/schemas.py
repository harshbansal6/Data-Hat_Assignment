from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Any
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# News Schemas
class NewsArticle(BaseModel):
    title: str
    description: Optional[str]
    url: str
    published_at: str
    source: str


class NewsResponse(BaseModel):
    count: int
    articles: List[NewsArticle]


# Weather Schemas
class WeatherData(BaseModel):
    date: str
    main: str
    temp: float
    description: Optional[str]


class WeatherResponse(BaseModel):
    count: int
    unit: str
    location: str
    data: List[WeatherData]


# Generic Response Schema
class GenericResponse(BaseModel):
    message: str
    status: str = "success" 