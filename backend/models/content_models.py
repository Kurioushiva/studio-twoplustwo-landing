from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class SocialMediaLinks(BaseModel):
    """Social media links configuration"""
    instagram: str = "#"
    facebook: str = "#"
    linkedin: str = "#"

class ContactInfo(BaseModel):
    """Contact information configuration"""
    email: str = "hello@studioname.com"
    phone: str = "+91 98765 43210"
    working_hours: str = "Mon - Sat: 9:00 AM - 6:00 PM"

class StudioAddress(BaseModel):
    """Studio address configuration"""
    line1: str = "123 Design District,"
    line2: str = "Vastrapur, Ahmedabad,"
    line3: str = "Gujarat 380015"
    maps_url: str = "#"

class HeroSection(BaseModel):
    """Hero section content"""
    main_title: str = "Something Extraordinary"
    subtitle: str = "is Coming"
    description: str = "We're crafting a new digital home for our architecture and interior design practice"
    launch_message: str = "Launching post-Diwali 2025"
    background_image: Optional[str] = None

class AboutSection(BaseModel):
    """About section content"""
    title: str = "Who We Are"
    description: str = "We are a contemporary architecture and interior design studio based in Ahmedabad, specializing in thoughtful spaces that blend modern aesthetics with sustainable practices. Our work spans architecture, interior design, master planning, and sustainable design solutions that respond to both human needs and environmental consciousness."

class SocialSection(BaseModel):
    """Social media section content"""
    title: str = "Meanwhile, Find Us Here"
    subtitle: str = "Stay connected with our latest projects and design inspiration"

class ExpectationsSection(BaseModel):
    """What to expect section content"""
    title: str = "What's Coming"
    items: List[str] = [
        "Portfolio of completed projects",
        "Our design philosophy and approach",
        "Services we offer",
        "Ways to connect with us"
    ]

class ContactPreviewSection(BaseModel):
    """Contact preview section content"""
    title: str = "Or reach us directly at:"

class FooterSection(BaseModel):
    """Footer section content"""
    studio_name: str = "[Studio Name]"
    tagline: str = "Crafting spaces that inspire and endure"
    copyright_text: str = "Designed with passion in Ahmedabad"

class LandingPageContent(BaseModel):
    """Complete landing page content model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = Field(default="1.0")
    is_published: bool = Field(default=False)
    
    # Content sections
    hero: HeroSection = Field(default_factory=HeroSection)
    about: AboutSection = Field(default_factory=AboutSection)
    social: SocialSection = Field(default_factory=SocialSection)
    expectations: ExpectationsSection = Field(default_factory=ExpectationsSection)
    contact_preview: ContactPreviewSection = Field(default_factory=ContactPreviewSection)
    footer: FooterSection = Field(default_factory=FooterSection)
    
    # Contact and studio info
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    studio_address: StudioAddress = Field(default_factory=StudioAddress)
    social_links: SocialMediaLinks = Field(default_factory=SocialMediaLinks)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = "admin"
    updated_by: str = "admin"

class ContentUpdateRequest(BaseModel):
    """Request model for content updates"""
    hero: Optional[HeroSection] = None
    about: Optional[AboutSection] = None
    social: Optional[SocialSection] = None
    expectations: Optional[ExpectationsSection] = None
    contact_preview: Optional[ContactPreviewSection] = None
    footer: Optional[FooterSection] = None
    contact_info: Optional[ContactInfo] = None
    studio_address: Optional[StudioAddress] = None
    social_links: Optional[SocialMediaLinks] = None
    
class AdminUser(BaseModel):
    """Admin user model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = True

class AdminSession(BaseModel):
    """Admin session model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)

class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    expires_at: datetime
    user_info: Dict[str, Any]