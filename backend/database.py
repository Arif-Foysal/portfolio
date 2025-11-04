from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from config import settings
from datetime import datetime

class DatabaseManager:
    """Handles database connections and operations"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Supabase client with error handling"""
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                print("✅ Supabase client initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Supabase client: {e}")
                self.client = None
        else:
            print("⚠️  Supabase credentials not found in environment variables")
            print("   Set SUPABASE_URL and SUPABASE_KEY to enable database functionality")
    
    def is_connected(self) -> bool:
        """Check if database client is available"""
        return self.client is not None
    
    async def save_newsletter_subscription(self, email: str, name: Optional[str] = None) -> dict:
        """Save newsletter subscription to database"""
        if not self.client:
            raise Exception("Database client not available")
        
        try:
            result = (
                self.client.table("newsletter_subscribers")
                .insert({"email": email, "name": name})
                .execute()
            )
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"Database error: {e}")
            raise e
    
    async def save_chat_message(self, user_id: str, message: str, response: str, 
                               session_id: str, message_type: str) -> Dict[str, Any]:
        """Save chat message and response to database"""
        if not self.client:
            print("DEBUG: Database client not available")
            raise Exception("Database client not available")
        
        try:
            print(f"DEBUG: Inserting chat message - user_id: {user_id}, message: {message[:50]}...")
            
            # Ensure session_id is a valid UUID, generate one if empty or invalid
            import uuid
            if not session_id or session_id == "":
                session_id = str(uuid.uuid4())
            
            # Validate if session_id is a valid UUID format, if not generate a new one
            try:
                uuid.UUID(session_id)
            except ValueError:
                print(f"DEBUG: Invalid UUID format for session_id: {session_id}, generating new UUID")
                session_id = str(uuid.uuid4())
            
            result = (
                self.client.table("chat_history")
                .insert({
                    "user_id": user_id,
                    "message": message,
                    "response": response,
                    "session_id": session_id,
                    "message_type": message_type,
                    "created_at": datetime.utcnow().isoformat()
                })
                .execute()
            )
            
            print(f"DEBUG: Successfully inserted chat message. Result: {result.data}")
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"Database error saving chat message: {e}")
            raise e
    
    async def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history for a user"""
        if not self.client:
            raise Exception("Database client not available")
        
        try:
            result = (
                self.client.table("chat_history")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return result.data if result.data else []
        except Exception as e:
            print(f"Database error retrieving chat history: {e}")
            raise e
    
    async def delete_chat_history(self, user_id: str) -> Dict[str, Any]:
        """Delete all chat history for a user"""
        if not self.client:
            raise Exception("Database client not available")
        
        try:
            result = (
                self.client.table("chat_history")
                .delete()
                .eq("user_id", user_id)
                .execute()
            )
            return {"success": True, "message": "Chat history deleted"}
        except Exception as e:
            print(f"Database error deleting chat history: {e}")
            raise e
    
    async def clear_old_sessions(self, days: int = 30) -> Dict[str, Any]:
        """Clear chat history older than specified days"""
        if not self.client:
            raise Exception("Database client not available")
        
        try:
            from datetime import datetime, timedelta
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            result = (
                self.client.table("chat_history")
                .delete()
                .lt("created_at", cutoff_date)
                .execute()
            )
            return {"success": True, "message": f"Cleared chat history older than {days} days"}
        except Exception as e:
            print(f"Database error clearing old sessions: {e}")
            raise e

# Create database manager instance
db_manager = DatabaseManager()
