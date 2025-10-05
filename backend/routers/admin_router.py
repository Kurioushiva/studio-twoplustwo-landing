from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from services.auth_service import AdminAuthService
from services.content_service import ContentService
from models.content_models import (
    LoginRequest, LoginResponse, AdminUser, 
    LandingPageContent, ContentUpdateRequest
)
from dependencies import get_admin_auth_service, get_content_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["Admin"])
security = HTTPBearer()

async def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AdminAuthService = Depends(get_admin_auth_service)
) -> AdminUser:
    """Get current authenticated admin user"""
    
    user = await auth_service.verify_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Authentication endpoints
@router.post("/auth/login", response_model=LoginResponse)
async def admin_login(
    login_request: LoginRequest,
    auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    """Admin login endpoint"""
    
    try:
        # Authenticate user
        user = await auth_service.authenticate_user(
            login_request.username, 
            login_request.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Create access token
        login_response = await auth_service.create_access_token(user)
        
        return login_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/auth/logout")
async def admin_logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    """Admin logout endpoint"""
    
    try:
        success = await auth_service.logout(credentials.credentials)
        return {"success": success, "message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@router.get("/auth/me")
async def get_current_user_info(
    current_user: AdminUser = Depends(get_current_admin_user)
):
    """Get current user information"""
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "last_login": current_user.last_login,
        "created_at": current_user.created_at
    }

# Content management endpoints
@router.get("/content/published", response_model=LandingPageContent)
async def get_published_content(
    content_service: ContentService = Depends(get_content_service)
):
    """Get currently published content"""
    
    try:
        content = await content_service.get_published_content()
        if not content:
            # Initialize default content if none exists
            content = await content_service.initialize_default_content()
        
        return content
        
    except Exception as e:
        logger.error(f"Failed to get published content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content"
        )

@router.get("/content/all", response_model=List[LandingPageContent])
async def get_all_content_versions(
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Get all content versions"""
    
    try:
        versions = await content_service.get_all_content_versions()
        return versions
        
    except Exception as e:
        logger.error(f"Failed to get content versions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content versions"
        )

@router.get("/content/{content_id}", response_model=LandingPageContent)
async def get_content_by_id(
    content_id: str,
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Get content by ID"""
    
    try:
        content = await content_service.get_content_by_id(content_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content"
        )

@router.post("/content/draft", response_model=LandingPageContent)
async def create_content_draft(
    base_content_id: Optional[str] = None,
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Create new content draft"""
    
    try:
        draft = await content_service.create_content_draft(
            base_content_id=base_content_id,
            updated_by=current_user.username
        )
        
        return draft
        
    except Exception as e:
        logger.error(f"Failed to create content draft: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create draft"
        )

@router.put("/content/{content_id}", response_model=LandingPageContent)
async def update_content(
    content_id: str,
    updates: ContentUpdateRequest,
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Update content"""
    
    try:
        updated_content = await content_service.update_content(
            content_id=content_id,
            updates=updates,
            updated_by=current_user.username
        )
        
        if not updated_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        return updated_content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update content"
        )

@router.post("/content/{content_id}/publish")
async def publish_content(
    content_id: str,
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Publish content"""
    
    try:
        success = await content_service.publish_content(
            content_id=content_id,
            published_by=current_user.username
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found or already published"
            )
        
        return {"success": True, "message": "Content published successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to publish content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish content"
        )

@router.delete("/content/{content_id}")
async def delete_content(
    content_id: str,
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Delete content draft"""
    
    try:
        success = await content_service.delete_content(content_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found or cannot be deleted"
            )
        
        return {"success": True, "message": "Content deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete content"
        )

@router.get("/content/summary")
async def get_content_summary(
    current_user: AdminUser = Depends(get_current_admin_user),
    content_service: ContentService = Depends(get_content_service)
):
    """Get content management summary"""
    
    try:
        summary = await content_service.get_content_summary()
        return summary
        
    except Exception as e:
        logger.error(f"Failed to get content summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get content summary"
        )

# Setup endpoint for initial admin user creation
@router.post("/setup", include_in_schema=False)
async def setup_admin(
    username: str = "admin",
    password: str = "admin123",
    auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    """Setup initial admin user (development only)"""
    
    try:
        # Check if any admin user exists
        existing_count = await auth_service.db.admin_users.count_documents({})
        if existing_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin user already exists"
            )
        
        # Create admin user
        admin_user = await auth_service.create_admin_user(username, password)
        
        return {
            "success": True, 
            "message": "Admin user created successfully",
            "username": admin_user.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Setup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Setup failed"
        )