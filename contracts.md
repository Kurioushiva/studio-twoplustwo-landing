# Architecture Studio Landing Page - API Contracts

## Overview
This document outlines the integration contracts between frontend and backend for the architecture studio landing page. The current implementation uses mock data that will be replaced with live API integrations.

## Current Mock Implementation

### Mock Data Location: `/src/data/mock.js`
- **mockInstagramPosts**: Array of 9 placeholder Instagram posts
- **studioInfo**: Studio contact information and details
- **services**: List of studio services
- **expectations**: What visitors can expect on the new site

## Planned API Integrations

### 1. Instagram Feed Integration
**Endpoint**: External Instagram Basic Display API
**Purpose**: Replace mock Instagram grid with live posts
**Current Mock**: 9 placeholder posts in `SocialMediaSection.jsx`
**Integration Requirements**:
- Instagram App ID and App Secret
- User Access Token
- Fetch recent 6-9 posts
- Display in responsive grid format
- Handle API rate limits and errors

### 2. Contact Form (Future)
**Endpoint**: `POST /api/contact`
**Purpose**: Handle contact inquiries
**Fields**: name, email, message, project_type
**Response**: Success/error status

### 3. Studio Information Management
**Endpoint**: `GET /api/studio-info`
**Purpose**: Dynamic studio information updates
**Current Mock**: Static data in `mock.js`
**Fields**: name, tagline, contact details, address, working hours

### 4. Content Management (Future)
**Endpoints**:
- `GET /api/content/hero` - Hero section content
- `GET /api/content/about` - About section content
- `GET /api/content/expectations` - What's coming content

## Frontend-Backend Integration Plan

### Phase 1: Instagram Feed
1. Create Instagram service in backend
2. Implement token refresh mechanism
3. Add error handling for API failures
4. Update `SocialMediaSection.jsx` to use live data
5. Remove mock posts from `mock.js`

### Phase 2: Contact System
1. Add contact form to landing page
2. Implement email notification system
3. Add form validation and error handling

### Phase 3: Content Management
1. Create admin interface for content updates
2. Replace static content with dynamic API calls
3. Add caching for better performance

## Environment Variables Needed
```
# Instagram Integration
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_REDIRECT_URI=your_redirect_uri

# Email System (Future)
SMTP_HOST=your_smtp_host
SMTP_USER=your_email
SMTP_PASS=your_password
```

## Error Handling Strategy
- Instagram API failures: Fall back to cached posts or show "Follow us on Instagram" message
- Contact form errors: Show user-friendly error messages
- Network issues: Implement retry mechanisms with exponential backoff

## Performance Considerations
- Cache Instagram posts for 1 hour to reduce API calls
- Lazy load Instagram images
- Optimize image sizes and formats
- Implement proper loading states

## Security Requirements
- Validate all form inputs
- Rate limit contact form submissions
- Secure Instagram tokens storage
- HTTPS enforcement for all API calls

This contract ensures seamless integration while maintaining the minimalist, elegant design of the architecture studio landing page.