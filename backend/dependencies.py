from fastapi import Depends, Request
from services.content_service import ContentService
from services.auth_service import AdminAuthService
from motor.motor_asyncio import AsyncIOMotorDatabase
import os

def get_database(request: Request) -> AsyncIOMotorDatabase:
    """Get database dependency"""
    return request.app.state.db

def get_content_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> ContentService:
    """Get content service dependency"""
    return ContentService(db)

def get_admin_auth_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> AdminAuthService:
    """Get admin auth service dependency"""
    return AdminAuthService(db)