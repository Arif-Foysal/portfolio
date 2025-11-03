from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models import ChatRequest, ChatResponse, ErrorResponse
from services.chatbot import chatbot_service

# Create router for chat endpoints
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Process a chat message and return a response with classification-based UI components
    """
    try:
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


