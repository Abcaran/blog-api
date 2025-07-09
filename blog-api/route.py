"""
Simple routes for the blog API.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

router = APIRouter()


@router.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Simple Blog API!",
        "docs": "/docs",
        "endpoints": {
            "posts": "/posts",
            "health": "/health"
        }
    }
