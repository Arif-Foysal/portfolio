"""
Chat history routes for storing and retrieving chat messages
"""
from fastapi import APIRouter, HTTPException
from models import (
    ChatHistoryRequest, ChatHistoryResponse, ChatHistoryEntry,
    ClearChatHistoryRequest, ClearChatHistoryResponse
)
from database import db_manager
from datetime import datetime
from typing import List, Dict, Any

# Create router for chat history endpoints
router = APIRouter(prefix="/history", tags=["chat-history"])


@router.post("/save")
async def save_chat_message(
    user_id: str,
    message: str,
    response: str,
    session_id: str,
    message_type: str = "text"
):
    """
    Save a chat message and response to the database
    
    Args:
        user_id: The user ID (anonymous user UUID)
        message: The user's message
        response: The chatbot's response
        session_id: The session ID
        message_type: Type of message (text, projects_list, etc.)
        
    Returns:
        Success status
    """
    try:
        if not db_manager.is_connected():
            return {
                "success": False,
                "message": "Database not available",
                "data": None
            }
        
        result = await db_manager.save_chat_message(
            user_id=user_id,
            message=message,
            response=response,
            session_id=session_id,
            message_type=message_type
        )
        
        return {
            "success": True,
            "message": "Chat message saved",
            "data": result.get("data")
        }
        
    except Exception as e:
        print(f"Error saving chat message: {str(e)}")
        return {
            "success": False,
            "message": f"Error saving chat message: {str(e)}",
            "data": None
        }


@router.post("/get", response_model=ChatHistoryResponse)
async def get_chat_history(request: ChatHistoryRequest):
    """
    Retrieve chat history for a user
    
    Args:
        request: ChatHistoryRequest with user_id and optional limit
        
    Returns:
        List of chat messages from history
    """
    try:
        if not db_manager.is_connected():
            raise HTTPException(
                status_code=503,
                detail="Database not available"
            )
        
        messages = await db_manager.get_chat_history(
            user_id=request.user_id,
            limit=request.limit
        )
        
        # Convert to ChatHistoryEntry objects
        history_entries: List[ChatHistoryEntry] = []
        for msg in messages:
            entry = ChatHistoryEntry(
                id=msg.get("id", ""),
                user_id=msg.get("user_id", ""),
                session_id=msg.get("session_id", ""),
                message=msg.get("message", ""),
                response=msg.get("response", ""),
                message_type=msg.get("message_type", "text"),
                created_at=datetime.fromisoformat(msg["created_at"]) if "created_at" in msg else datetime.utcnow()
            )
            history_entries.append(entry)
        
        return ChatHistoryResponse(
            success=True,
            messages=history_entries,
            total_count=len(history_entries)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving chat history"
        )


@router.post("/clear", response_model=ClearChatHistoryResponse)
async def clear_chat_history(request: ClearChatHistoryRequest):
    """
    Clear all chat history for a user
    
    Args:
        request: ClearChatHistoryRequest with user_id
        
    Returns:
        Success status with number of messages deleted
    """
    try:
        if not db_manager.is_connected():
            raise HTTPException(
                status_code=503,
                detail="Database not available"
            )
        
        result = await db_manager.delete_chat_history(user_id=request.user_id)
        
        return ClearChatHistoryResponse(
            success=True,
            message="Chat history cleared",
            deleted_count=0  # Note: Supabase delete doesn't return count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error clearing chat history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error clearing chat history"
        )


@router.get("/session/{session_id}")
async def get_session_chat_history(session_id: str, limit: int = 50):
    """
    Get chat history for a specific session
    
    Args:
        session_id: The session ID
        limit: Maximum number of messages to retrieve
        
    Returns:
        List of messages in the session
    """
    try:
        if not db_manager.is_connected():
            raise HTTPException(
                status_code=503,
                detail="Database not available"
            )
        
        # Note: This requires a session_id index in the database
        # For now, return a message indicating this needs to be queried differently
        return {
            "success": True,
            "message": "Use /history/get endpoint with user_id",
            "messages": []
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving session history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving session history"
        )


@router.get("/health")
async def history_health_check():
    """
    Health check endpoint for the chat history service
    """
    db_connected = db_manager.is_connected()
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "message": "Chat history service is running",
        "database_connected": db_connected
    }
