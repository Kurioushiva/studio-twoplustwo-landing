import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.content_models import AdminUser, AdminSession, LoginRequest, LoginResponse
from passlib.context import CryptContext
import os
import logging

logger = logging.getLogger(__name__)

class AdminAuthService:
    """Admin authentication service"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_hours = 24
    
    async def create_admin_user(self, username: str, password: str) -> AdminUser:
        """Create new admin user"""
        
        # Check if user already exists
        existing_user = await self.db.admin_users.find_one({"username": username})
        if existing_user:
            raise ValueError("Admin user already exists")
        
        # Hash password
        password_hash = self.pwd_context.hash(password)
        
        # Create user
        admin_user = AdminUser(
            username=username,
            password_hash=password_hash
        )
        
        # Insert to database
        await self.db.admin_users.insert_one(admin_user.dict())
        
        logger.info(f"Created admin user: {username}")
        return admin_user
    
    async def authenticate_user(self, username: str, password: str) -> Optional[AdminUser]:
        """Authenticate admin user"""
        
        try:
            # Find user
            user_data = await self.db.admin_users.find_one({"username": username, "is_active": True})
            if not user_data:
                return None
            
            user = AdminUser(**user_data)
            
            # Verify password
            if not self.pwd_context.verify(password, user.password_hash):
                return None
            
            # Update last login
            await self.db.admin_users.update_one(
                {"id": user.id},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    async def create_access_token(self, user: AdminUser) -> LoginResponse:
        """Create JWT access token"""
        
        expires_at = datetime.utcnow() + timedelta(hours=self.access_token_expire_hours)
        
        payload = {
            "sub": user.id,
            "username": user.username,
            "exp": expires_at,
            "iat": datetime.utcnow(),
            "type": "access_token"
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store session in database
        session = AdminSession(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        
        await self.db.admin_sessions.insert_one(session.dict())
        
        return LoginResponse(
            access_token=token,
            expires_at=expires_at,
            user_info={
                "id": user.id,
                "username": user.username,
                "last_login": user.last_login
            }
        )
    
    async def verify_token(self, token: str) -> Optional[AdminUser]:
        """Verify JWT token and return user"""
        
        try:
            # Decode token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            
            if not user_id:
                return None
            
            # Check session in database
            session_data = await self.db.admin_sessions.find_one({
                "token": token,
                "user_id": user_id,
                "expires_at": {"$gt": datetime.utcnow()}
            })
            
            if not session_data:
                return None
            
            # Get user
            user_data = await self.db.admin_users.find_one({
                "id": user_id,
                "is_active": True
            })
            
            if not user_data:
                return None
            
            # Update last accessed
            await self.db.admin_sessions.update_one(
                {"token": token},
                {"$set": {"last_accessed": datetime.utcnow()}}
            )
            
            return AdminUser(**user_data)
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.JWTError as e:
            logger.warning(f"JWT error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return None
    
    async def logout(self, token: str) -> bool:
        """Logout user by invalidating token"""
        
        try:
            result = await self.db.admin_sessions.delete_one({"token": token})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return False
    
    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        
        try:
            result = await self.db.admin_sessions.delete_many({
                "expires_at": {"$lt": datetime.utcnow()}
            })
            return result.deleted_count
        except Exception as e:
            logger.error(f"Session cleanup error: {str(e)}")
            return 0
    
    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        
        try:
            # Get current user
            user_data = await self.db.admin_users.find_one({"id": user_id})
            if not user_data:
                return False
            
            user = AdminUser(**user_data)
            
            # Verify old password
            if not self.pwd_context.verify(old_password, user.password_hash):
                return False
            
            # Hash new password
            new_password_hash = self.pwd_context.hash(new_password)
            
            # Update password
            await self.db.admin_users.update_one(
                {"id": user_id},
                {"$set": {"password_hash": new_password_hash}}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return False