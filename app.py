from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

app = FastAPI(
    title="Hypixel API",
    description="A FastAPI application for interacting with Hypixel data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Hypixel API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Example protected endpoint
@app.get("/api/profile/{username}")
async def get_profile(username: str, api_key: str):
    """
    Get a player's Hypixel profile
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required"
        )
    
    # TODO: Implement Hypixel API integration
    return {
        "username": username,
        "message": "Profile endpoint - Implementation pending"
    }