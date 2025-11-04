from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, EmailStr
from enum import Enum

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

