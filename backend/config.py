import os
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # Supabase configuration
    SUPABASE_URL: Optional[str] = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.environ.get("SUPABASE_KEY")
    
    # OpenAI configuration
    OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
    
    # Server configuration
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))
    
    # App configuration
    APP_NAME: str = "Portfolio Backend API"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"
    
    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Local development
        "http://localhost:3001", 
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://127.0.0.1:3001",
        "https://arif.it.com",  # Replace with your actual domain
        "https://*.vercel.app",  # Vercel deployments
        "*"  # Allow all origins (use with caution in production)
    ]

# Create settings instance
settings = Settings()
