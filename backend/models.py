from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

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

class MessageType(str, Enum):
    """Enum for different message classification types"""
    TEXT = "text"
    PROJECTS_LIST = "projects_list"
    SKILLS_LIST = "skills_list"
    EDUCATION_LIST = "education_list"
    EXPERIENCE_LIST = "experience_list"
    ACHIEVEMENTS_LIST = "achievements_list"
    CONTACT_INFO = "contact_info"

class ChatRequest(BaseModel):
    """Model for chat request"""
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ProjectData(BaseModel):
    """Model for project information"""
    name: str
    description: str
    technologies: List[str]
    link: Optional[str] = None
    github_link: Optional[str] = None
    image: Optional[str] = None

class SkillData(BaseModel):
    """Model for skill information"""
    category: str
    skills: List[str]
    # proficiency: Optional[str] = None

class EducationData(BaseModel):
    """Model for education information"""
    institution: str
    degree: str
    field: str
    year: str
    description: Optional[str] = None

class ExperienceData(BaseModel):
    """Model for work experience information"""
    company: str
    position: str
    duration: str
    description: str
    technologies: List[str]

class AchievementData(BaseModel):
    """Model for achievement information"""
    title: str
    description: str
    date: Optional[str] = None
    link: Optional[str] = None

class ContactData(BaseModel):
    """Model for contact information"""
    email: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class ChatResponse(BaseModel):
    """Model for chat response"""
    type: MessageType
    data: Union[str, List[ProjectData], List[SkillData], List[EducationData], 
                List[ExperienceData], List[AchievementData], ContactData]
    session_id: str

class ClassificationResult(BaseModel):
    """Model for message classification result"""
    category: str
    intent: str
    confidence: float
    requires_special_ui: bool


# ==================== Authentication Models ====================

class AnonymousAuthRequest(BaseModel):
    """Model for requesting anonymous authentication"""
    pass

class AnonymousAuthResponse(BaseModel):
    """Model for anonymous authentication response"""
    success: bool
    user_id: str
    session_id: str
    token: str
    is_anonymous: bool
    expires_at: Optional[datetime] = None

class SessionInfo(BaseModel):
    """Model for session information"""
    session_id: str
    user_id: str
    is_anonymous: bool
    created_at: datetime
    expires_at: Optional[datetime] = None

class SessionValidationResponse(BaseModel):
    """Model for session validation response"""
    valid: bool
    user_id: Optional[str] = None
    message: Optional[str] = None


# ==================== Chat History Models ====================

class ChatMessage(BaseModel):
    """Model for a single chat message entry"""
    id: Optional[str] = None
    user_id: str
    session_id: str
    message: str
    response: str
    message_type: str
    created_at: Optional[datetime] = None

class ChatHistoryEntry(BaseModel):
    """Model for chat history entry with metadata"""
    id: str
    user_id: str
    session_id: str
    message: str
    response: str
    message_type: str
    created_at: datetime

class ChatHistoryRequest(BaseModel):
    """Model for requesting chat history"""
    user_id: str
    session_id: Optional[str] = None
    limit: int = 50

class ChatHistoryResponse(BaseModel):
    """Model for chat history response"""
    success: bool
    messages: List[ChatHistoryEntry]
    total_count: int

class ClearChatHistoryRequest(BaseModel):
    """Model for requesting to clear chat history"""
    user_id: str
    session_id: Optional[str] = None

class ClearChatHistoryResponse(BaseModel):
    """Model for clear chat history response"""
    success: bool
    message: str
    deleted_count: int


