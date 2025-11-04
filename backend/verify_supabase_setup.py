#!/usr/bin/env python3
"""
Supabase Setup Verification Script
Checks if everything is configured correctly for chat history storage
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Checking Environment Variables...")
    print("=" * 50)
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    checks = {
        "SUPABASE_URL": supabase_url,
        "SUPABASE_KEY": supabase_key,
        "OPENAI_API_KEY": openai_key,
    }
    
    all_good = True
    for var, value in checks.items():
        if value:
            # Hide sensitive values
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {masked}")
        else:
            print(f"❌ {var}: NOT SET")
            all_good = False
    
    return all_good


def check_supabase_connection():
    """Test connection to Supabase"""
    print("\n🔍 Checking Supabase Connection...")
    print("=" * 50)
    
    try:
        from supabase import create_client
        
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Missing Supabase credentials")
            return False
        
        client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")
        
        # Try to query the table
        try:
            result = client.table("chat_history").select("count()", count="exact").execute()
            print(f"✅ chat_history table exists")
            print(f"   Current record count: {result.count if hasattr(result, 'count') else 'unknown'}")
            return True
        except Exception as e:
            error_msg = str(e)
            if "does not exist" in error_msg:
                print(f"❌ chat_history table does NOT exist")
                print(f"   → You need to create it first!")
                print(f"   → See: SUPABASE_DATA_NOT_SAVING_FIX.md")
            else:
                print(f"❌ Error querying table: {error_msg}")
            return False
            
    except ImportError:
        print("❌ Supabase library not installed")
        print("   Run: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


def check_database_manager():
    """Check if database manager can be initialized"""
    print("\n🔍 Checking Database Manager...")
    print("=" * 50)
    
    try:
        from database import db_manager
        
        if db_manager.is_connected():
            print("✅ Database manager connected")
            return True
        else:
            print("❌ Database manager NOT connected")
            print("   → Check Supabase credentials")
            return False
    except Exception as e:
        print(f"❌ Error importing database manager: {e}")
        return False


def check_auth_service():
    """Check if auth service can be initialized"""
    print("\n🔍 Checking Auth Service...")
    print("=" * 50)
    
    try:
        from services.auth_service import auth_service
        print("✅ Auth service initialized")
        print(f"   Active sessions: {len(auth_service.session_cache)}")
        return True
    except Exception as e:
        print(f"❌ Error initializing auth service: {e}")
        return False


def check_models():
    """Check if models are properly defined"""
    print("\n🔍 Checking Models...")
    print("=" * 50)
    
    try:
        from models import (
            ChatRequest, ChatResponse, AnonymousAuthResponse,
            ChatHistoryEntry, ClearChatHistoryResponse
        )
        print("✅ All required models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False


def check_routes():
    """Check if routes are properly defined"""
    print("\n🔍 Checking Routes...")
    print("=" * 50)
    
    try:
        from routes import auth, history, chat
        print("✅ Auth routes loaded")
        print("✅ History routes loaded")
        print("✅ Chat routes loaded")
        return True
    except Exception as e:
        print(f"❌ Error importing routes: {e}")
        return False


def run_all_checks():
    """Run all verification checks"""
    print("\n" + "=" * 50)
    print("🚀 Supabase Setup Verification Script")
    print("=" * 50)
    
    results = {
        "Environment Variables": check_env_variables(),
        "Supabase Connection": check_supabase_connection(),
        "Database Manager": check_database_manager(),
        "Auth Service": check_auth_service(),
        "Models": check_models(),
        "Routes": check_routes(),
    }
    
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Everything looks good! You're ready to save chat history.")
        return True
    else:
        print("\n⚠️  Some checks failed. See details above.")
        print("📖 For fixes, see: SUPABASE_DATA_NOT_SAVING_FIX.md")
        return False


if __name__ == "__main__":
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    sys.path.insert(0, backend_dir)
    
    success = run_all_checks()
    sys.exit(0 if success else 1)
