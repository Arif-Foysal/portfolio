from fastapi import APIRouter

# Create router for general API endpoints
router = APIRouter()

@router.get("/")
async def welcome():
    """Welcome endpoint"""
    return {"message": "Welcome to my portfolio backend!"}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}
