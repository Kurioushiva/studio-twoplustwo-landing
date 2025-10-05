from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.content_models import (
    LandingPageContent, 
    ContentUpdateRequest,
    HeroSection,
    AboutSection,
    SocialSection,
    ExpectationsSection,
    ContactPreviewSection,
    FooterSection,
    ContactInfo,
    StudioAddress,
    SocialMediaLinks
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ContentService:
    """Content management service"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.landing_page_content
    
    async def initialize_default_content(self) -> LandingPageContent:
        """Initialize default content if none exists"""
        
        try:
            # Check if content already exists
            existing = await self.get_published_content()
            if existing:
                return existing
            
            # Create default content
            default_content = LandingPageContent(
                is_published=True,
                created_by="system",
                updated_by="system"
            )
            
            # Insert to database
            await self.collection.insert_one(default_content.dict())
            
            logger.info("Initialized default landing page content")
            return default_content
            
        except Exception as e:
            logger.error(f"Failed to initialize default content: {str(e)}")
            raise
    
    async def get_published_content(self) -> Optional[LandingPageContent]:
        """Get currently published content"""
        
        try:
            content_data = await self.collection.find_one(
                {"is_published": True},
                sort=[("updated_at", -1)]
            )
            
            if content_data:
                return LandingPageContent(**content_data)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get published content: {str(e)}")
            return None
    
    async def get_content_by_id(self, content_id: str) -> Optional[LandingPageContent]:
        """Get content by ID"""
        
        try:
            content_data = await self.collection.find_one({"id": content_id})
            if content_data:
                return LandingPageContent(**content_data)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get content by ID: {str(e)}")
            return None
    
    async def get_all_content_versions(self) -> List[LandingPageContent]:
        """Get all content versions"""
        
        try:
            cursor = self.collection.find().sort("updated_at", -1)
            content_versions = []
            
            async for doc in cursor:
                content_versions.append(LandingPageContent(**doc))
            
            return content_versions
            
        except Exception as e:
            logger.error(f"Failed to get content versions: {str(e)}")
            return []
    
    async def create_content_draft(self, 
                                 base_content_id: Optional[str] = None, 
                                 updated_by: str = "admin") -> LandingPageContent:
        """Create new content draft"""
        
        try:
            # Get base content
            if base_content_id:
                base_content = await self.get_content_by_id(base_content_id)
            else:
                base_content = await self.get_published_content()
            
            if not base_content:
                base_content = LandingPageContent()
            
            # Create new draft
            draft_content = LandingPageContent(
                version=f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                is_published=False,
                hero=base_content.hero,
                about=base_content.about,
                social=base_content.social,
                expectations=base_content.expectations,
                contact_preview=base_content.contact_preview,
                footer=base_content.footer,
                contact_info=base_content.contact_info,
                studio_address=base_content.studio_address,
                social_links=base_content.social_links,
                created_by=updated_by,
                updated_by=updated_by
            )
            
            # Insert to database
            await self.collection.insert_one(draft_content.dict())
            
            logger.info(f"Created content draft: {draft_content.id}")
            return draft_content
            
        except Exception as e:
            logger.error(f"Failed to create content draft: {str(e)}")
            raise
    
    async def update_content(self, 
                           content_id: str, 
                           updates: ContentUpdateRequest, 
                           updated_by: str = "admin") -> Optional[LandingPageContent]:
        """Update content"""
        
        try:
            # Get existing content
            existing_content = await self.get_content_by_id(content_id)
            if not existing_content:
                raise ValueError(f"Content not found: {content_id}")
            
            # Prepare update data
            update_data = {
                "updated_at": datetime.utcnow(),
                "updated_by": updated_by
            }
            
            # Update sections if provided
            if updates.hero:
                update_data["hero"] = updates.hero.dict()
            if updates.about:
                update_data["about"] = updates.about.dict()
            if updates.social:
                update_data["social"] = updates.social.dict()
            if updates.expectations:
                update_data["expectations"] = updates.expectations.dict()
            if updates.contact_preview:
                update_data["contact_preview"] = updates.contact_preview.dict()
            if updates.footer:
                update_data["footer"] = updates.footer.dict()
            if updates.contact_info:
                update_data["contact_info"] = updates.contact_info.dict()
            if updates.studio_address:
                update_data["studio_address"] = updates.studio_address.dict()
            if updates.social_links:
                update_data["social_links"] = updates.social_links.dict()
            
            # Update in database
            result = await self.collection.update_one(
                {"id": content_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                # Return updated content
                return await self.get_content_by_id(content_id)
            else:
                logger.warning(f"No content was updated for ID: {content_id}")
                return existing_content
            
        except Exception as e:
            logger.error(f"Failed to update content: {str(e)}")
            raise
    
    async def publish_content(self, content_id: str, published_by: str = "admin") -> bool:
        """Publish content (unpublish others)"""
        
        try:
            # Unpublish all current published content
            await self.collection.update_many(
                {"is_published": True},
                {"$set": {"is_published": False}}
            )
            
            # Publish the specified content
            result = await self.collection.update_one(
                {"id": content_id},
                {
                    "$set": {
                        "is_published": True,
                        "updated_at": datetime.utcnow(),
                        "updated_by": published_by
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"Published content: {content_id}")
                return True
            else:
                logger.warning(f"Failed to publish content: {content_id}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to publish content: {str(e)}")
            return False
    
    async def delete_content(self, content_id: str) -> bool:
        """Delete content (cannot delete published content)"""
        
        try:
            # Check if content is published
            content = await self.get_content_by_id(content_id)
            if not content:
                return False
            
            if content.is_published:
                raise ValueError("Cannot delete published content")
            
            # Delete content
            result = await self.collection.delete_one({"id": content_id})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted content: {content_id}")
                return True
            else:
                return False
            
        except Exception as e:
            logger.error(f"Failed to delete content: {str(e)}")
            raise
    
    async def get_content_summary(self) -> Dict[str, Any]:
        """Get content management summary"""
        
        try:
            total_versions = await self.collection.count_documents({})
            published_content = await self.get_published_content()
            draft_count = await self.collection.count_documents({"is_published": False})
            
            return {
                "total_versions": total_versions,
                "draft_count": draft_count,
                "published_version": {
                    "id": published_content.id if published_content else None,
                    "version": published_content.version if published_content else None,
                    "updated_at": published_content.updated_at if published_content else None,
                    "updated_by": published_content.updated_by if published_content else None
                } if published_content else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get content summary: {str(e)}")
            return {
                "total_versions": 0,
                "draft_count": 0,
                "published_version": None
            }