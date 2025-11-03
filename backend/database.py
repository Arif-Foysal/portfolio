from typing import Optional
from supabase import create_client, Client
from config import settings

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

# Create database manager instance
db_manager = DatabaseManager()
