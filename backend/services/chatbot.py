"""
Chatbot service with message classification, routing, and response generation using OpenAI API.
Implements short-term memory and semantic caching using vector database.
"""

import os
import json
import uuid
import asyncio
import math
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from openai import AsyncOpenAI

from models import (
    MessageType, ClassificationResult, ChatResponse, 
    ProjectData, SkillData, EducationData, ExperienceData, 
    AchievementData, ContactData
)
from services.portfolio_data import portfolio_service

# Try to import vector store, but make it optional
try:
    from services.vector_store import VectorStore
    VECTOR_STORE_AVAILABLE = True
except Exception as e:
    print(f"Warning: Vector store not available: {e}")
    VECTOR_STORE_AVAILABLE = False

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
        
        # Initialize vector store for semantic caching
        self.vector_store = None
        if VECTOR_STORE_AVAILABLE:
            try:
                self.vector_store = VectorStore()
                print("✓ Vector store initialized for semantic caching")
            except Exception as e:
                print(f"⚠ Vector store initialization failed: {e}")
        
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
            # Add 2 second delay to make it feel more natural
            await asyncio.sleep(2)
            cached_response = self.response_cache[normalized_message]
            # Update session_id and return copy
            return ChatResponse(
                type=cached_response.type,
                data=cached_response.data,
                session_id=session_id
            )
        return None
    
    async def _get_semantic_cached_response(self, message: str, session_id: str) -> Optional[ChatResponse]:
        """Search for semantically similar cached responses using vector database"""
        if not self.vector_store:
            return None
        
        try:
            similar_responses = await self.vector_store.search_similar_responses(message, limit=1, threshold=0.85)
            
            if similar_responses and len(similar_responses) > 0:
                # Found a very similar past response
                await asyncio.sleep(2)
                
                similar_response = similar_responses[0]
                response_str = similar_response.get("response", "{}")
                
                # Handle both JSON and plain text responses
                try:
                    response_data = json.loads(response_str)
                except (json.JSONDecodeError, ValueError):
                    # If parsing fails, treat as plain text
                    response_data = {
                        "type": MessageType.TEXT,
                        "data": response_str
                    }
                
                return ChatResponse(
                    type=response_data.get("type", MessageType.TEXT),
                    data=response_data.get("data"),
                    session_id=session_id
                )
        except Exception as e:
            print(f"Error in semantic caching: {e}")
        
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
    
    async def _is_portfolio_relevant_semantic(self, message: str, classification: ClassificationResult) -> bool:
        """
        Check if message is portfolio-relevant using semantic similarity.
        More intelligent than keyword matching!
        """
        
        if not self.vector_store:
            # Fallback to keyword matching if vector store unavailable
            return self._is_portfolio_relevant_keywords(message, classification)
        
        try:
            # Always cache structured responses
            always_cache_categories = {
                'projects', 'skills', 'education', 'experience', 
                'achievements', 'contact', 'personal'
            }
            
            if classification.category in always_cache_categories:
                return True
            
            # Skip obvious off-topic intents
            if classification.category == "other" and classification.intent in ["greeting", "general_question"]:
                return False
            
            # For other cases, use semantic similarity
            # Get embedding of the user message
            message_embedding = await self.vector_store.get_embedding(message)
            
            # Compare with portfolio context embeddings
            portfolio_context = """
            Full Stack Developer projects technologies React Vue Python FastAPI 
            machine learning AI artificial intelligence web development backend frontend 
            database docker deployment cloud AWS skills experience achievements awards
            education certification professional background innovation technology solutions
            """
            
            portfolio_embedding = await self.vector_store.get_embedding(portfolio_context)
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(message_embedding, portfolio_embedding)
            
            print(f"Semantic relevance for '{message[:50]}...': {similarity:.2f}")
            
            # Cache if similarity > 0.65 (on a scale of -1 to 1, where 1 is identical)
            return similarity > 0.65
            
        except Exception as e:
            print(f"Error in semantic relevance check: {e}")
            # Fallback to keyword matching
            return self._is_portfolio_relevant_keywords(message, classification)
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        
        if not vec1 or not vec2:
            return 0.0
        
        # Dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Cosine similarity
        return dot_product / (magnitude1 * magnitude2)
    
    def _is_portfolio_relevant_keywords(self, message: str, classification: ClassificationResult) -> bool:
        """
        Fallback keyword matching for when vector store is unavailable.
        This is the old method kept as a backup.
        """
        
        portfolio_keywords = {
            'project', 'skill', 'experience', 'work', 'technology', 'code',
            'programming', 'development', 'developer', 'engineer', 'portfolio',
            'github', 'fullstack', 'frontend', 'backend', 'react',
            'vue', 'python', 'javascript', 'node', 'fastapi', 'database',
            'deployment', 'docker', 'aws', 'education', 'degree', 'certificate',
            'achievement', 'award', 'accomplishment', 'contact', 'email',
            'linkedin', 'website', 'langchain', 'ai', 'ml', 'machine learning',
            'llm', 'gpt', 'vector', 'rag', 'agent', 'automation', 'iot',
            'api', 'rest', 'graphql', 'sql', 'mongodb', 'firebase',
            'git', 'version control', 'scrum', 'agile', 'testing', 'ci/cd'
        }
        
        always_cache_categories = {
            'projects', 'skills', 'education', 'experience', 
            'achievements', 'contact', 'personal'
        }
        
        if classification.category in always_cache_categories:
            return True
        
        message_lower = message.lower()
        keyword_match = any(keyword in message_lower for keyword in portfolio_keywords)
        
        if keyword_match:
            return True
        
        if classification.category == "other" and classification.intent in ["greeting", "general_question"]:
            return False
        
        if classification.confidence > 0.7:
            return True
        
        return False
    
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
- "specific_item" - User asks about a specific project, skill, etc. (e.g., "Tell me about Blue Horizon", "What technologies use React?")
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
    
    def _get_portfolio_data(self, classification: ClassificationResult, message: str = "") -> Any:
        """Get relevant portfolio data based on classification"""
        
        if classification.category == "projects":
            # If it's a specific project question, search for it
            if classification.intent == "specific_item" and message:
                search_results = portfolio_service.search_projects(message)
                if search_results:
                    # If only one result, return it as single object
                    # If multiple results, return as list (for technology/multi-match queries)
                    return search_results if len(search_results) > 1 else search_results[0]
            # Otherwise return all projects
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
    
    def _determine_response_type(self, classification: ClassificationResult, portfolio_data: Any = None) -> MessageType:
        """Determine the response type based on classification"""
        
        if not classification.requires_special_ui:
            return MessageType.TEXT
        
        if classification.category == "projects":
            # If it's a specific project (single ProjectData object) or multiple projects, show as list
            if classification.intent == "specific_item":
                return MessageType.PROJECTS_LIST
            elif classification.intent == "list_all":
                return MessageType.PROJECTS_LIST
            return MessageType.TEXT
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
        
        return MessageType.TEXT
    
    async def generate_response(self, message: str, classification: ClassificationResult, 
                              portfolio_data: Any, chat_history: str) -> str:
        """Generate conversational response using OpenAI"""
        
        # Check if it's a specific project question
        is_specific_project = (
            classification.category == "projects" and 
            classification.intent == "specific_item" and 
            portfolio_data
        )
        
        # Check if multiple projects (list) or single project
        is_multiple_projects = (
            is_specific_project and 
            isinstance(portfolio_data, list) and 
            len(portfolio_data) > 1
        )
        
        is_single_project = (
            is_specific_project and 
            not isinstance(portfolio_data, list)
        )
        
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
- Specializes in React, Vue.js, Python, FastAPI, Langchain, AI Agent
- Built projects like fuel station automation solutions, RAG agents, Underwater ROV, Skin Cancer detection system and so on
- Won innovation awards, active open-source contributor
- Currently working as Software Engineer at Amar Fuel & freelancer on Fiverr

RESPONSE GUIDELINES:
- Keep responses conversational and engaging
- When discussing specific projects, mention technologies used
- If asked about skills, relate them to real projects you've worked on
- For work experience, highlight key achievements
- Always speak in first person as Arif Foysal
- Don't mention that you're an AI - respond as if you're the actual person
- For specific projects: Provide a detailed description, highlight key features, technologies used, and the link
- For multiple matching projects: List all matching projects with brief descriptions and highlights

CONVERSATION HISTORY:
{chat_history}

CLASSIFICATION INFO:
Category: {classification.category}
Intent: {classification.intent}

RELEVANT DATA:
{str(portfolio_data)[:2000] if portfolio_data else "No specific data"}

USER MESSAGE: {message}

{"SPECIAL INSTRUCTION: The user is asking about a specific project. Provide a detailed, engaging description including what it does, the technologies used, key features, and why it's interesting." if is_single_project else ""}
{"SPECIAL INSTRUCTION: The user is asking about projects using a specific technology or matching a criteria. List ALL matching projects with brief descriptions highlighting their key features and the specific technology/feature they asked about." if is_multiple_projects else ""}

Respond naturally as Arif Foysal:"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Even cheaper than gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": response_prompt}
                ],
                temperature=0.7,
                max_tokens=600  # Increased for multiple projects
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
        
        # 1. Try exact match cache first (fastest)
        cached_response = await self._get_cached_response(message, session_id)
        if cached_response:
            return cached_response
        
        # 2. Try semantic cache (using vector similarity)
        semantic_cached = await self._get_semantic_cached_response(message, session_id)
        if semantic_cached:
            return semantic_cached
        
        # 3. Get session memory
        memory = self._get_or_create_memory(session_id)
        
        # 4. Classify the message
        classification = await self.classify_message(message)
        
        # 5. Get relevant portfolio data
        portfolio_data = self._get_portfolio_data(classification, message)
        
        # 6. Determine response type
        response_type = self._determine_response_type(classification, portfolio_data)
        
        # 7. Get chat history
        chat_history = memory.get_context()
        
        # 8. Generate conversational response
        response_text = await self.generate_response(
            message, classification, portfolio_data, chat_history
        )
        
        # 9. Store in vector database for future semantic search
        # Only cache if content is relevant to portfolio/technology (using semantic similarity!)
        if self.vector_store:
            is_relevant = await self._is_portfolio_relevant_semantic(message, classification)
            
            if is_relevant:
                try:
                    response_type_str = response_type.value if hasattr(response_type, 'value') else str(response_type)
                    
                    if response_type != MessageType.TEXT and portfolio_data:
                        response_to_store = json.dumps({
                            "type": response_type_str,
                            "data": portfolio_data
                        })
                    else:
                        response_to_store = response_text
                    
                    await self.vector_store.store_response(
                        message, 
                        response_to_store,
                        {"category": classification.category, "intent": classification.intent},
                        response_type=response_type_str
                    )
                except Exception as e:
                    print(f"Warning: Could not store in vector database: {e}")
            else:
                print(f"Skipping cache (not semantically relevant): {message[:50]}...")
        
        # 10. Save to memory
        memory.add_message(message, response_text)
        
        # 11. If special UI is required, return structured data
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
