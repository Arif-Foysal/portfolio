from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models import ChatRequest, ChatResponse, ErrorResponse
from services.chatbot import chatbot_service
import time
from collections import defaultdict

# Simple rate limiting (in production, use Redis)
request_counts = defaultdict(list)
RATE_LIMIT_REQUESTS = 10  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

# Create router for chat endpoints
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Process a chat message and return a response with classification-based UI components
    """
    try:
        # Simple rate limiting by session
        session_key = request.session_id or "anonymous"
        current_time = time.time()
        
        # Clean old requests
        request_counts[session_key] = [
            req_time for req_time in request_counts[session_key]
            if current_time - req_time < RATE_LIMIT_WINDOW
        ]
        
        # Check rate limit
        if len(request_counts[session_key]) >= RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_REQUESTS} requests per minute."
            )
        
        # Add current request
        request_counts[session_key].append(current_time)
        
        # Check if chatbot service is available
        if chatbot_service is None:
            raise HTTPException(
                status_code=503,
                detail="Chatbot service is not available. Please check OpenAI API configuration."
            )
        
        # Process the message
        response = await chatbot_service.process_message(
            message=request.message,
            session_id=request.session_id
        )
        
        return response
        
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        # Log the error in production
        print(f"Chat processing error: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )

@router.get("/health")
async def chat_health_check():
    """
    Health check endpoint for the chat service
    """
    if chatbot_service is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "message": "Chatbot service is not available"
            }
        )
    
    return {
        "status": "healthy",
        "message": "Chat service is running"
    }


