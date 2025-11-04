"""
Authentication service for handling Supabase anonymous sign-in and user session management
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import uuid
import json

from config import settings

# Try to import supabase, but make it optional
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("Warning: Supabase client not available")


class AuthService:
    """Handle anonymous authentication and user session management"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
        self.session_cache: Dict[str, Dict[str, Any]] = {}
        self.session_expiry: Dict[str, datetime] = {}
    
    def _initialize_client(self) -> None:
        """Initialize Supabase client for auth operations"""
        if not SUPABASE_AVAILABLE:
            print("⚠️  Supabase not available for authentication")
            return
        
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                print("✅ Auth service initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize auth service: {e}")
                self.client = None
        else:
            print("⚠️  Supabase credentials not found. Anonymous auth will use local sessions.")
    
    async def sign_in_anonymously(self) -> Dict[str, Any]:
        """
        Sign in user anonymously and create a session
        Uses Supabase's native anonymous auth when available, otherwise creates custom anonymous user
        
        Returns:
            Dict with user_id, session_id, and auth token
        """
        try:
            if self.client:
                # Try Supabase's anonymous sign-in first
                try:
                    print("🔍 Attempting Supabase anonymous sign-in...")
                    result = self.client.auth.sign_in_anonymously()
                    
                    if result.user:
                        supabase_user_id = result.user.id
                        session_token = result.session.access_token if result.session else str(uuid.uuid4())
                        
                        print(f"✅ Supabase anonymous user created: {supabase_user_id}")
                        print("👤 This user should appear in Supabase Authentication → Users tab")
                        
                        # Generate client-side UUID for reconnection
                        client_uuid = str(uuid.uuid4())
                        session_id = str(uuid.uuid4())
                        
                        # Store both IDs in anonymous_users table for reconnection
                        try:
                            anonymous_user_data = {
                                "client_uuid": client_uuid,
                                "supabase_user_id": supabase_user_id,
                                "is_anonymous": True,
                                "created_at": datetime.utcnow().isoformat(),
                                "last_active": datetime.utcnow().isoformat()
                            }
                            
                            user_result = self.client.table("anonymous_users").insert(anonymous_user_data).execute()
                            print(f"✅ User mapping stored: client_uuid={client_uuid} → supabase_id={supabase_user_id}")
                            
                        except Exception as db_error:
                            print(f"⚠️ Could not store user mapping: {db_error}")
                            # Continue anyway - we'll use the supabase_user_id directly
                            client_uuid = supabase_user_id
                        
                        # Cache session locally for quick validation
                        session_data = {
                            "user_id": client_uuid,  # Use client UUID for consistency
                            "supabase_user_id": supabase_user_id,  # Keep reference to real Supabase ID
                            "session_id": session_id,
                            "token": session_token,
                            "created_at": datetime.utcnow().isoformat(),
                            "is_anonymous": True,
                            "source": "supabase"
                        }
                        
                        self.session_cache[session_id] = session_data
                        self.session_expiry[session_id] = datetime.utcnow() + timedelta(hours=24)
                        
                        return {
                            "success": True,
                            "user_id": client_uuid,  # Return client UUID for chat history tracking
                            "session_id": session_id,
                            "token": session_token,
                            "is_anonymous": True
                        }
                
                except Exception as supabase_error:
                    print(f"❌ Supabase anonymous auth failed: {supabase_error}")
                    print("💡 Enable anonymous sign-ins in Supabase Dashboard → Authentication → Settings")
                    # Fall through to custom anonymous user creation
                    
                # Create custom anonymous user in database
                user_id = str(uuid.uuid4())
                session_id = str(uuid.uuid4())
                session_token = str(uuid.uuid4())
                
                try:
                    # Try to store anonymous user in your database
                    # Check if you have an anonymous_users table, if not we'll just use local sessions
                    anonymous_user_data = {
                        "id": user_id,
                        "is_anonymous": True,
                        "created_at": datetime.utcnow().isoformat(),
                        "last_active": datetime.utcnow().isoformat()
                    }
                    
                    # Try to insert into anonymous_users table
                    try:
                        result = self.client.table("anonymous_users").insert(anonymous_user_data).execute()
                        print(f"✓ Custom anonymous user stored in database: {user_id}")
                        source = "database"
                    except Exception as db_error:
                        print(f"Note: Could not store in database (table may not exist): {db_error}")
                        source = "local"
                        
                except Exception as e:
                    print(f"Database storage failed: {e}")
                    source = "local"
                
                print(f"✓ Custom anonymous user created: {user_id}")
                    
            else:
                # Fallback: generate local session when Supabase unavailable
                user_id = str(uuid.uuid4())
                session_id = str(uuid.uuid4())
                session_token = str(uuid.uuid4())
                source = "local"
                print(f"✓ Local anonymous session created: {user_id}")
            
            # Cache session locally for quick validation
            session_data = {
                "user_id": user_id,
                "session_id": session_id,
                "token": session_token,
                "created_at": datetime.utcnow().isoformat(),
                "is_anonymous": True,
                "source": source
            }
            
            self.session_cache[session_id] = session_data
            self.session_expiry[session_id] = datetime.utcnow() + timedelta(hours=24)
            
            return {
                "success": True,
                "user_id": user_id,
                "session_id": session_id,
                "token": session_token,
                "is_anonymous": True
            }
            
        except Exception as e:
            print(f"Error in anonymous sign-in: {e}")
            
            # Ultimate fallback: generate local session
            user_id = str(uuid.uuid4())
            session_id = str(uuid.uuid4())
            session_token = str(uuid.uuid4())
            
            session_data = {
                "user_id": user_id,
                "session_id": session_id,
                "token": session_token,
                "created_at": datetime.utcnow().isoformat(),
                "is_anonymous": True,
                "source": "fallback"
            }
            
            self.session_cache[session_id] = session_data
            self.session_expiry[session_id] = datetime.utcnow() + timedelta(hours=24)
            
            print(f"✓ Fallback anonymous session created: {user_id}")
            
            return {
                "success": True,
                "user_id": user_id,
                "session_id": session_id,
                "token": session_token,
                "is_anonymous": True
            }
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cached session data
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Session data if valid, None otherwise
        """
        if session_id not in self.session_cache:
            return None
        
        # Check if session has expired
        if session_id in self.session_expiry:
            if datetime.utcnow() > self.session_expiry[session_id]:
                del self.session_cache[session_id]
                del self.session_expiry[session_id]
                return None
        
        return self.session_cache[session_id]
    
    def is_session_valid(self, session_id: str) -> bool:
        """Check if a session is valid and not expired"""
        return self.get_session(session_id) is not None
    
    async def get_user_by_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user info from session
        
        Args:
            session_id: The session ID
            
        Returns:
            User info if session is valid, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "user_id": session["user_id"],
            "is_anonymous": session.get("is_anonymous", True),
            "created_at": session.get("created_at")
        }
    
    def refresh_session(self, session_id: str) -> bool:
        """
        Refresh session expiry time
        
        Args:
            session_id: The session ID to refresh
            
        Returns:
            True if refreshed successfully, False otherwise
        """
        if session_id not in self.session_cache:
            return False
        
        self.session_expiry[session_id] = datetime.utcnow() + timedelta(hours=24)
        return True
    
    async def revoke_session(self, session_id: str) -> bool:
        """
        Revoke/logout a session
        
        Args:
            session_id: The session ID to revoke
            
        Returns:
            True if revoked successfully, False otherwise
        """
        if session_id in self.session_cache:
            del self.session_cache[session_id]
        
        if session_id in self.session_expiry:
            del self.session_expiry[session_id]
        
        return True
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up all expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        current_time = datetime.utcnow()
        expired_sessions = [
            sid for sid, expiry in self.session_expiry.items()
            if current_time > expiry
        ]
        
        count = len(expired_sessions)
        
        for session_id in expired_sessions:
            if session_id in self.session_cache:
                del self.session_cache[session_id]
            del self.session_expiry[session_id]
        
        if count > 0:
            print(f"🧹 Cleaned up {count} expired sessions")
        
        return count
    
    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of session information"""
        session = self.get_session(session_id)
        if not session:
            return {"valid": False, "message": "Session not found or expired"}
        
        expires_at = "unknown"
        if session_id in self.session_expiry:
            expires_dt = self.session_expiry[session_id]
            expires_at = expires_dt.isoformat() if isinstance(expires_dt, datetime) else str(expires_dt)
        
        return {
            "valid": True,
            "user_id": session["user_id"],
            "is_anonymous": session.get("is_anonymous", True),
            "created_at": session.get("created_at"),
            "expires_at": expires_at
        }
    
    async def reconnect_user_by_client_uuid(self, client_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Reconnect a user using their client UUID
        This allows users to maintain their identity across sessions
        
        Args:
            client_uuid: The client-side UUID to reconnect
            
        Returns:
            User session data if found, None otherwise
        """
        if not self.client:
            return None
            
        try:
            # Look up the user in anonymous_users table
            result = (
                self.client.table("anonymous_users")
                .select("*")
                .eq("client_uuid", client_uuid)
                .execute()
            )
            
            if result.data and len(result.data) > 0:
                user_data = result.data[0]
                
                # Update last_active timestamp
                self.client.table("anonymous_users").update({
                    "last_active": datetime.utcnow().isoformat()
                }).eq("client_uuid", client_uuid).execute()
                
                # Create new session for the reconnected user
                session_id = str(uuid.uuid4())
                session_token = str(uuid.uuid4())
                
                session_data = {
                    "user_id": client_uuid,
                    "supabase_user_id": user_data.get("supabase_user_id"),
                    "session_id": session_id,
                    "token": session_token,
                    "created_at": datetime.utcnow().isoformat(),
                    "is_anonymous": True,
                    "source": "reconnected"
                }
                
                self.session_cache[session_id] = session_data
                self.session_expiry[session_id] = datetime.utcnow() + timedelta(hours=24)
                
                print(f"✅ User reconnected: {client_uuid}")
                
                return {
                    "success": True,
                    "user_id": client_uuid,
                    "session_id": session_id,
                    "token": session_token,
                    "is_anonymous": True,
                    "reconnected": True
                }
                
        except Exception as e:
            print(f"Error reconnecting user: {e}")
            
        return None
    
    async def get_user_chat_history(self, client_uuid: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get chat history for a user by their client UUID
        
        Args:
            client_uuid: The client UUID to get history for
            limit: Maximum number of messages to return
            
        Returns:
            List of chat messages
        """
        if not self.client:
            return []
            
        try:
            result = (
                self.client.table("chat_history")
                .select("*")
                .eq("user_id", client_uuid)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []


# Create global instance
auth_service = AuthService()
