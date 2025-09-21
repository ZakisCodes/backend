from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models import user, message  # Import models to create tables
from app.api import auth, messages
from app.websocket.chat import websocket_endpoint
import os

# Create database tables
user.Base.metadata.create_all(bind=engine)
message.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media Backend API",
    description="A FastAPI backend for social media platform with chat functionality",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
os.makedirs("uploads", exist_ok=True)

# Mount static files for serving uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(messages.router)

# WebSocket endpoint
app.websocket("/ws/chat")(websocket_endpoint)


@app.get("/")
def read_root():
    return {
        "message": "Social Media Backend API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "messages": "/messages", 
            "websocket": "/ws/chat",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)