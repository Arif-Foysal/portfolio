"""
Chatbot service with message classification, routing, and response generation using OpenAI API.
Implements short-term memory using simple dictionary storage.
"""

import os
import json
import uuid
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from openai import AsyncOpenAI

from models import (
    MessageType, ClassificationResult, ChatResponse, 
    ProjectData, SkillData, EducationData, ExperienceData, 
    AchievementData, ContactData
)
from services.portfolio_data import portfolio_service

class SimpleMemory:
    """Simple conversation memory implementation"""
    
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
    
    def add_message(self, user_message: str, ai_response: str):
        """Add a message pair to memory"""
        self.messages.append({
            "user": user_message,
            "assistant": ai_response
        })
        
        # Keep only last 10 message pairs to avoid token limit
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]
    
    def get_context(self) -> str:
        """Get conversation context as formatted string"""
        if not self.messages:
            return "No previous conversation."
        
        context = []
        for msg in self.messages:
            context.append(f"User: {msg['user']}")
            context.append(f"Assistant: {msg['assistant']}")
        
        return "\n".join(context)

class ChatbotService:
    """Main chatbot service handling classification, routing, and response generation"""
    
    def __init__(self):
        # Initialize OpenAI API
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=self.openai_api_key)
        
        # Session memory storage (in production, use Redis or database)
        self.session_memories: Dict[str, SimpleMemory] = {}
        self.session_timestamps: Dict[str, datetime] = {}
        
        # Simple response cache for common questions
        self.response_cache: Dict[str, ChatResponse] = {}
        self._init_common_responses()
    
    def _init_common_responses(self):
        """Initialize cache with common responses to avoid API calls"""
        # Cache common greetings and simple questions
        self.response_cache = {
            "hello": ChatResponse(
                type=MessageType.TEXT,
                data="Hello! I'm Arif Foysal, a Full Stack Developer and AI enthusiast. How can I help you today?",
                session_id=""
            ),
            "hi": ChatResponse(
                type=MessageType.TEXT,
                data="Hi there! I'm Arif, nice to meet you! What would you like to know about my work?",
                session_id=""
            ),
            "what is your name": ChatResponse(
                type=MessageType.TEXT,
                data="I'm Arif Foysal, a Full Stack Developer and AI Engineer from Bangladesh.",
                session_id=""
            ),
            "who are you": ChatResponse(
                type=MessageType.TEXT,
                data="I'm Arif Foysal, a passionate software developer specializing in full-stack web development and AI. I love building innovative solutions that solve real-world problems.",
                session_id=""
            ),
            # Cached responses for quick action buttons (zero API cost!)
            "show me your projects": ChatResponse(
                type=MessageType.PROJECTS_LIST,
                data=portfolio_service.get_projects(),
                session_id=""
            ),
            "what are your skills?": ChatResponse(
                type=MessageType.SKILLS_LIST,
                data=portfolio_service.get_skills(),
                session_id=""
            ),
            "tell me about your experience": ChatResponse(
                type=MessageType.EXPERIENCE_LIST,
                data=portfolio_service.get_experience(),
                session_id=""
            ),
            "how can i contact you?": ChatResponse(
                type=MessageType.CONTACT_INFO,
                data=portfolio_service.get_contact_info(),
                session_id=""
            ),
            "what is your background?": ChatResponse(
                type=MessageType.TEXT,
                data="I'm Arif Foysal, a Full Stack Developer and AI Enthusiast from Bangladesh with 3+ years of experience. I specialize in building innovative web applications and AI solutions. I've won multiple awards including finalist positions in national project showcases like UIU CSE Fest, Inventious 4.1, and Hult Prize Bangladesh 2025. Currently, I work at Amar Fuel developing IoT-based fuel station solutions, while also freelancing as a Full Stack Developer on Fiverr. My passion lies in creating technology solutions that solve real-world problems.",
                session_id=""
            ),
        }
    
    async def _get_cached_response(self, message: str, session_id: str) -> Optional[ChatResponse]:
        """Check if we have a cached response for this message"""
        normalized_message = message.lower().strip()
        if normalized_message in self.response_cache:
            # Add 1 second delay to make it feel more natural
            await asyncio.sleep(2)
            cached_response = self.response_cache[normalized_message]
            # Update session_id and return copy
            return ChatResponse(
                type=cached_response.type,
                data=cached_response.data,
                session_id=session_id
            )
        return None
    
    def _get_or_create_memory(self, session_id: str) -> SimpleMemory:
        """Get existing memory or create new one for session"""
        
        # Clean up old sessions (older than 1 hour)
        current_time = datetime.now()
        sessions_to_remove = []
        
        for sid, timestamp in self.session_timestamps.items():
            if current_time - timestamp > timedelta(hours=1):
                sessions_to_remove.append(sid)
        
        for sid in sessions_to_remove:
            if sid in self.session_memories:
                del self.session_memories[sid]
            if sid in self.session_timestamps:
                del self.session_timestamps[sid]
        
        # Get or create memory for current session
        if session_id not in self.session_memories:
            self.session_memories[session_id] = SimpleMemory()
        
        self.session_timestamps[session_id] = current_time
        return self.session_memories[session_id]
    
    async def classify_message(self, message: str) -> ClassificationResult:
        """Classify user message into category and intent"""
        
        classification_prompt = f"""You are a message classifier for Arif Foysal's portfolio chatbot. 
Your job is to analyze user messages and classify them into specific categories and intents.

CLASSIFICATION CATEGORIES:
1. "projects" - User wants to know about projects, portfolio work
2. "skills" - User asks about technical skills, programming languages, technologies
3. "education" - Questions about academic background, degrees, certifications
4. "experience" - Work experience, jobs, professional background
5. "achievements" - Awards, recognition, accomplishments
6. "contact" - Contact information, how to reach out
7. "personal" - Personal information, bio, general questions about the person
8. "other" - General conversation, greetings, unclear intent

INTENT TYPES:
- "list_all" - User wants to see all items (e.g., "show me all projects", "list your skills")
- "specific_item" - User asks about a specific project, skill, etc.
- "general_question" - General questions that need conversational responses
- "greeting" - Greetings, small talk
- "contact_request" - Direct request for contact information

SPECIAL UI TRIGGERS:
- If intent is "list_all" for projects, skills, education, experience, or achievements → requires_special_ui: true
- If asking for contact info → requires_special_ui: true  
- Otherwise → requires_special_ui: false

Respond ONLY with a JSON object in this exact format:
{{
    "category": "category_name",
    "intent": "intent_type", 
    "confidence": 0.95,
    "requires_special_ui": true/false
}}

User message: "{message}"
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Even cheaper than gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": classification_prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse JSON response
            result_text = response.choices[0].message.content.strip()
            classification_data = json.loads(result_text)
            
            return ClassificationResult(
                category=classification_data["category"],
                intent=classification_data["intent"],
                confidence=classification_data["confidence"],
                requires_special_ui=classification_data["requires_special_ui"]
            )
            
        except Exception as e:
            print(f"Classification error: {e}")
            # Fallback classification
            return ClassificationResult(
                category="other",
                intent="general_question",
                confidence=0.5,
                requires_special_ui=False
            )
    
    def _get_portfolio_data(self, classification: ClassificationResult) -> Any:
        """Get relevant portfolio data based on classification"""
        
        if classification.category == "projects":
            return portfolio_service.get_projects()
        elif classification.category == "skills":
            return portfolio_service.get_skills()
        elif classification.category == "education":
            return portfolio_service.get_education()
        elif classification.category == "experience":
            return portfolio_service.get_experience()
        elif classification.category == "achievements":
            return portfolio_service.get_achievements()
        elif classification.category == "contact":
            return portfolio_service.get_contact_info()
        elif classification.category == "personal":
            return portfolio_service.get_personal_info()
        else:
            return None
    
    def _determine_response_type(self, classification: ClassificationResult) -> MessageType:
        """Determine the response type based on classification"""
        
        if not classification.requires_special_ui:
            return MessageType.TEXT
        
        if classification.category == "projects" and classification.intent == "list_all":
            return MessageType.PROJECTS_LIST
        elif classification.category == "skills" and classification.intent == "list_all":
            return MessageType.SKILLS_LIST
        elif classification.category == "education" and classification.intent == "list_all":
            return MessageType.EDUCATION_LIST
        elif classification.category == "experience" and classification.intent == "list_all":
            return MessageType.EXPERIENCE_LIST
        elif classification.category == "achievements" and classification.intent == "list_all":
            return MessageType.ACHIEVEMENTS_LIST
        elif classification.category == "contact":
            return MessageType.CONTACT_INFO
        else:
            return MessageType.TEXT
    
    async def generate_response(self, message: str, classification: ClassificationResult, 
                              portfolio_data: Any, chat_history: str) -> str:
        """Generate conversational response using OpenAI"""
        
        response_prompt = f"""You are Arif Foysal's AI representative, speaking on his behalf in first person. 
You are helpful, professional, and enthusiastic about technology and software development.

PERSONALITY TRAITS:
- Speak as "I" (first person) as if you ARE Arif Foysal
- Passionate about technology, AI, and solving real-world problems
- Friendly but professional tone
- Concise but informative responses
- Show enthusiasm for your work and projects

CONTEXT ABOUT ARIF:
- Full Stack Developer & AI Enthusiast from Bangladesh
- 3+ years of experience in web development
- Specializes in React, Vue.js, Python, FastAPI, AI/ML
- Built projects like skin disease detection app, portfolio websites, analytics dashboards
- Won innovation awards, active open-source contributor
- Currently working as Full Stack Developer at Tech Solutions Inc.

RESPONSE GUIDELINES:
- Keep responses conversational and engaging
- When discussing specific projects, mention technologies used
- If asked about skills, relate them to real projects you've worked on
- For work experience, highlight key achievements
- Always speak in first person as Arif Foysal
- Don't mention that you're an AI - respond as if you're the actual person

CONVERSATION HISTORY:
{chat_history}

CLASSIFICATION INFO:
Category: {classification.category}
Intent: {classification.intent}

RELEVANT DATA:
{str(portfolio_data)[:1000] if portfolio_data else "No specific data"}

USER MESSAGE: {message}

Respond naturally as Arif Foysal:"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Even cheaper than gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": response_prompt}
                ],
                temperature=0.7,
                max_tokens=400  # Reduced from 500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Response generation error: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    async def process_message(self, message: str, session_id: Optional[str] = None) -> ChatResponse:
        """Main method to process user message and generate response"""
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Check cache first (with 1 second delay)
        cached_response = await self._get_cached_response(message, session_id)
        if cached_response:
            return cached_response
        
        # Get session memory
        memory = self._get_or_create_memory(session_id)
        
        # Classify the message
        classification = await self.classify_message(message)
        
        # Get relevant portfolio data
        portfolio_data = self._get_portfolio_data(classification)
        
        # Determine response type
        response_type = self._determine_response_type(classification)
        
        # Get chat history
        chat_history = memory.get_context()
        
        # Generate conversational response
        response_text = await self.generate_response(
            message, classification, portfolio_data, chat_history
        )
        
        # Save to memory
        memory.add_message(message, response_text)
        
        # If special UI is required, return structured data
        if classification.requires_special_ui and portfolio_data:
            return ChatResponse(
                type=response_type,
                data=portfolio_data,
                session_id=session_id
            )
        
        return ChatResponse(
            type=MessageType.TEXT,
            data=response_text,
            session_id=session_id
        )

# Create global instance
try:
    chatbot_service = ChatbotService()
except ValueError as e:
    print(f"Warning: {e}. Chatbot service will not be available.")
    chatbot_service = None
