from typing import Optional
from pydantic import BaseModel, EmailStr

class NewsletterSubscription(BaseModel):
    """Model for newsletter subscription request"""
    email: EmailStr
    name: Optional[str] = None

class NewsletterResponse(BaseModel):
    """Model for newsletter subscription response"""
    success: bool
    message: str
    email: Optional[str] = None

class ErrorResponse(BaseModel):
    """Model for error responses"""
    success: bool = False
    error: str
    detail: Optional[str] = None
