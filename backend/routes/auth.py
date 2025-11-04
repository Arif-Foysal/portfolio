"""
Authentication routes for anonymous sign-in and session management
"""
from fastapi import APIRouter, HTTPException, status
from models import (
    AnonymousAuthResponse, SessionValidationResponse, SessionInfo
)
from services.auth_service import auth_service
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/anonymous", response_model=AnonymousAuthResponse)
async def sign_in_anonymously():
    """
    Sign in a user anonymously and create a session for chat history tracking
    
    Returns:
        AnonymousAuthResponse with user_id, session_id, and token
    """
    try:
        result = await auth_service.sign_in_anonymously()
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail="Failed to create anonymous session"
            )
        
        return AnonymousAuthResponse(
            success=True,
            user_id=result["user_id"],
            session_id=result["session_id"],
            token=result["token"],
            is_anonymous=True
        )
        
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during authentication"
        )


@router.get("/validate/{session_id}", response_model=SessionValidationResponse)
async def validate_session(session_id: str):
    """
    Validate if a session is still active and not expired
    
    Args:
        session_id: The session ID to validate
        
    Returns:
        SessionValidationResponse with validation status
    """
    try:
        is_valid = auth_service.is_session_valid(session_id)
        
        if is_valid:
            session = auth_service.get_session(session_id)
            if session:
                return SessionValidationResponse(
                    valid=True,
                    user_id=session.get("user_id"),
                    message="Session is valid"
                )
            else:
                return SessionValidationResponse(
                    valid=False,
                    message="Session data not found"
                )
        else:
            return SessionValidationResponse(
                valid=False,
                message="Session expired or not found"
            )
            
    except Exception as e:
        print(f"Session validation error: {str(e)}")
        return SessionValidationResponse(
            valid=False,
            message="Error validating session"
        )


@router.post("/refresh/{session_id}")
async def refresh_session(session_id: str):
    """
    Refresh a session to extend its expiry time
    If session doesn't exist, create a new anonymous session
    
    Args:
        session_id: The session ID to refresh
        
    Returns:
        Success status or new session info
    """
    try:
        # Try to refresh existing session
        success = auth_service.refresh_session(session_id)
        
        if success:
            return {"success": True, "message": "Session refreshed"}
        else:
            # If session doesn't exist, create a new anonymous session
            print(f"Session {session_id} not found, creating new anonymous session")
            
            result = await auth_service.sign_in_anonymously()
            
            return {
                "success": True, 
                "message": "Session not found, created new anonymous session",
                "new_session": True,
                "user_id": result["user_id"],
                "session_id": result["session_id"],
                "token": result["token"]
            }
            
    except Exception as e:
        print(f"Session refresh error: {str(e)}")
        
        # Last resort: create new anonymous session
        try:
            result = await auth_service.sign_in_anonymously()
            return {
                "success": True, 
                "message": "Error occurred, created new anonymous session",
                "new_session": True,
                "user_id": result["user_id"],
                "session_id": result["session_id"],
                "token": result["token"]
            }
        except:
            raise HTTPException(
                status_code=500,
                detail="Error refreshing session and unable to create new session"
            )


@router.post("/logout/{session_id}")
async def logout_session(session_id: str):
    """
    Logout/revoke a session
    
    Args:
        session_id: The session ID to revoke
        
    Returns:
        Success status
    """
    try:
        await auth_service.revoke_session(session_id)
        
        return {"success": True, "message": "Session revoked"}
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error logging out"
        )


@router.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Get detailed information about a session
    
    Args:
        session_id: The session ID to retrieve info for
        
    Returns:
        Session information if found
    """
    try:
        summary = await auth_service.get_session_summary(session_id)
        
        if not summary.get("valid"):
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving session info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving session information"
        )


@router.post("/cleanup")
async def cleanup_sessions():
    """
    Clean up all expired sessions (admin endpoint - should be protected in production)
    
    Returns:
        Number of sessions cleaned up
    """
    try:
        count = auth_service.cleanup_expired_sessions()
        
        return {
            "success": True,
            "message": f"Cleaned up {count} expired sessions",
            "count": count
        }
        
    except Exception as e:
        print(f"Cleanup error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error cleaning up sessions"
        )


@router.get("/health")
async def auth_health_check():
    """
    Health check endpoint for the auth service
    """
    return {
        "status": "healthy",
        "message": "Auth service is running",
        "supabase_available": hasattr(auth_service, 'client') and auth_service.client is not None
    }


@router.post("/reconnect/{client_uuid}")
async def reconnect_user(client_uuid: str):
    """
    Reconnect a user using their client UUID
    This allows users to maintain their identity across sessions
    
    Args:
        client_uuid: The client-side UUID to reconnect
        
    Returns:
        New session info if user found, error otherwise
    """
    try:
        result = await auth_service.reconnect_user_by_client_uuid(client_uuid)
        
        if result:
            return AnonymousAuthResponse(
                success=True,
                user_id=result["user_id"],
                session_id=result["session_id"],
                token=result["token"],
                is_anonymous=True
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found. Please sign in again."
            )
            
    except Exception as e:
        print(f"User reconnection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error reconnecting user"
        )


@router.get("/history/{client_uuid}")
async def get_user_history(client_uuid: str, limit: int = 50):
    """
    Get chat history for a user by their client UUID
    
    Args:
        client_uuid: The client UUID to get history for
        limit: Maximum number of messages to return
        
    Returns:
        List of chat messages
    """
    try:
        history = await auth_service.get_user_chat_history(client_uuid, limit)
        
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
        
    except Exception as e:
        print(f"Chat history retrieval error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving chat history"
        )
