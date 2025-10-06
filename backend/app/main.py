import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Load environment variables from .env file
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment from: {env_path}")
else:
    # Fallback to current directory
    load_dotenv()
    print("⚠️ Using fallback environment loading")

from .routers import chat, documents, certificates, health, gemini_documents, advanced_qa, document_requests, auth
from .services.db import db_service

app = FastAPI(title="Org AI Chatbot", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    await db_service.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await db_service.disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (commented out since static directory was removed)
# project_root = Path(__file__).parent.parent.parent
# static_path = project_root / "static"
# app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(certificates.router, prefix="/certificates", tags=["certificates"])
app.include_router(gemini_documents.router, prefix="/gemini", tags=["gemini"])
app.include_router(advanced_qa.router, prefix="/advanced-qa", tags=["advanced-qa"])
app.include_router(document_requests.router, prefix="/document-requests", tags=["document-requests"])


@app.get("/")
async def root():
    """Root endpoint for testing"""
    return {
        "message": "Reliance Jio Infotech Solutions API is running!",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "ai_health": "/gemini/health",
            "chatbot": "React frontend available at http://localhost:3000"
        }
    }
