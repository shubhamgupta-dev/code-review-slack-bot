# Custom Notification Dashboard - Design Doc

## Overview
Building a lightweight, mobile-friendly web UI as an alternative to Slack integration.

## Features

### Phase 1 - Core Notification Feed ✅
- **Real-time PR notifications**
- **AI-powered summaries**
- **Mobile-responsive design**
- **Simple authentication**

### Phase 2 - Interactive Actions ✅
- **Approve PR** button → GitHub API
- **Request Changes** button → GitHub API
- **Add Comments** → GitHub API
- **View on GitHub** link

### Phase 3 - Advanced (Future)
- WebSocket for real-time updates
- Push notifications
- User preferences
- Multiple users/teams

---

## Architecture

```
GitHub Webhook → FastAPI Server → SQLite DB
                      ↓
                 Web Dashboard (React/HTML)
                      ↓
                 User Actions → GitHub API
```

---

## Tech Stack

### Backend (Already have FastAPI)
- **FastAPI** - REST API endpoints
- **SQLite** - Store notifications (lightweight, no setup)
- **GitHub API** - Send PR actions back

### Frontend (Lightweight)
- **HTML + Tailwind CSS** - Mobile-responsive
- **Alpine.js** or **HTMX** - Minimal JS framework
- **Progressive Web App (PWA)** - Install on mobile like an app

---

## Database Schema

```sql
-- Notifications table
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pr_number INTEGER NOT NULL,
    pr_title TEXT NOT NULL,
    pr_url TEXT NOT NULL,
    repository TEXT NOT NULL,
    author TEXT NOT NULL,
    author_avatar TEXT,
    branch_from TEXT,
    branch_to TEXT,
    summary TEXT,
    ai_analysis JSON,
    files_changed INTEGER,
    additions INTEGER,
    deletions INTEGER,
    complexity TEXT,
    status TEXT DEFAULT 'pending',  -- pending, approved, changes_requested, commented
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User actions table
CREATE TABLE user_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_id INTEGER,
    action TEXT NOT NULL,  -- approve, request_changes, comment
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notification_id) REFERENCES notifications(id)
);
```

---

## UI Mockup

```
┌─────────────────────────────────────┐
│  🤖 Code Review Dashboard           │
│  [Menu] [Pending: 3] [User: John]   │
├─────────────────────────────────────┤
│                                     │
│  📋 PR #123: Add authentication     │
│  test-org/app • john-doe • 2h ago   │
│  ─────────────────────────────────  │
│  📝 Implements JWT-based auth...    │
│  📊 5 files • +282 -17 • Medium     │
│                                     │
│  [✅ Approve] [💬 Comment]          │
│  [❌ Changes] [🔗 GitHub]           │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  📋 PR #122: Fix login bug          │
│  test-org/app • alice • 5h ago      │
│  ─────────────────────────────────  │
│  📝 Fixes issue with...             │
│  📊 2 files • +45 -12 • Small       │
│                                     │
│  [✅ Approve] [💬 Comment]          │
│  [❌ Changes] [🔗 GitHub]           │
│                                     │
└─────────────────────────────────────┘
```

---

## Mobile Experience

- **Responsive design** - Works on any screen size
- **Touch-friendly** - Large tap targets
- **PWA** - Install as app icon on home screen
- **Fast loading** - Minimal JS, mostly server-rendered
- **Offline capable** - Service worker caching

---

## API Endpoints

### Get Notifications
```
GET /api/notifications
GET /api/notifications/{id}
```

### Take Actions
```
POST /api/notifications/{id}/approve
POST /api/notifications/{id}/comment
POST /api/notifications/{id}/request-changes
```

### WebSocket (Optional - Phase 3)
```
WS /api/notifications/live
```

---

## Authentication Options

### Option 1: Simple Token (Recommended for prototype)
```bash
# In .env
DASHBOARD_ACCESS_TOKEN=your-secret-token-123
```

Access: `https://your-dashboard.com/?token=your-secret-token-123`

### Option 2: GitHub OAuth (Production)
- Login with GitHub account
- Verify user has repo access
- More secure for multi-user

### Option 3: Basic Auth (Quick)
```
Username: admin
Password: your-secure-password
```

---

## Implementation Plan

### Step 1: Database Setup ✅
- Create SQLite database
- Define models
- Add migration scripts

### Step 2: Store Notifications ✅
- Modify webhook handler to save to DB
- Store AI analysis results

### Step 3: Create Dashboard UI ✅
- Build HTML template with Tailwind
- Create notification feed
- Add responsive layout

### Step 4: Action Buttons ✅
- Connect to GitHub API
- Update notification status
- Show success/error messages

### Step 5: Deploy & Test ✅
- Test on mobile browser
- Add PWA manifest
- Set up simple auth

---

## Benefits Over Slack

✅ **Full control** - Customize everything
✅ **No API limits** - No Slack rate limits
✅ **Better mobile UX** - Optimized for your use case
✅ **Cheaper** - No Slack workspace costs
✅ **Easier setup** - No OAuth dance
✅ **More features** - Add whatever you want
✅ **Works offline** - Cache notifications locally

---

## Example: Mobile PWA

Once installed on mobile:
1. GitHub PR opened → Webhook → Your server → DB
2. Badge shows "3 pending reviews"
3. Tap app icon → Opens dashboard
4. Swipe through PRs like Tinder
5. Tap "Approve" → Sent to GitHub API
6. Badge updates to "2 pending"

---

## Progressive Enhancement

**Week 1:** Basic dashboard with static refresh
**Week 2:** Add real-time updates with WebSocket
**Week 3:** Add PWA for mobile install
**Week 4:** Add push notifications
**Week 5:** Multi-user support

---

## Let's Build It!

I'll start implementing this now. It will be:
- ✅ Lightweight (no heavy dependencies)
- ✅ Mobile-first design
- ✅ Easy to deploy (SQLite, no external DB)
- ✅ Secure (simple token auth to start)
- ✅ Fast to develop (can be done today!)

Ready to proceed?
