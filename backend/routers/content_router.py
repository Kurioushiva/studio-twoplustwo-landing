from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from services.content_service import ContentService
from models.content_models import LandingPageContent
from dependencies import get_content_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/content", tags=["Content"])

@router.get("/landing-page", response_model=LandingPageContent)
async def get_landing_page_content(
    content_service: ContentService = Depends(get_content_service)
):
    """Get current landing page content for frontend display"""
    
    try:
        content = await content_service.get_published_content()
        
        if not content:
            # Initialize default content if none exists
            content = await content_service.initialize_default_content()
        
        return content
        
    except Exception as e:
        logger.error(f"Failed to get landing page content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve landing page content"
        )

@router.get("/preview/{content_id}", response_model=LandingPageContent)
async def preview_content(
    content_id: str,
    content_service: ContentService = Depends(get_content_service)
):
    """Preview content by ID (for admin preview)"""
    
    try:
        content = await content_service.get_content_by_id(content_id)
        
        if not content:
            raise HTTPException(
                status_code=404,
                detail="Content not found"
            )
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to preview content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve content for preview"
        )