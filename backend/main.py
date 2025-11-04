from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import settings
from routes import main as main_routes, newsletter, chat, auth, history

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(main_routes.router)
app.include_router(newsletter.router)
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(history.router)
    
def run_server():
    """Run the FastAPI application locally"""
    print(f"Starting {settings.APP_NAME}...")
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )

# For Vercel deployment
handler = app

if __name__ == "__main__":
    run_server()