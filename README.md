# ReviewFlow - Slack-Style PR Dashboard

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Auto-Sync](https://img.shields.io/badge/auto--sync-5s-blue.svg)]()

> A beautiful Slack-inspired dashboard for GitHub Pull Request reviews with automatic syncing and AI-powered analysis.

## ✨ Features

- 🎨 **Slack-Style UI** - Professional purple sidebar with channel-based filtering
- 🔄 **Auto-Sync** - Checks GitHub every 5 seconds for new PRs
- 🤖 **AI Analysis** - Powered by Claude for intelligent PR summaries
- ⚡ **Real-time Actions** - Approve, Request Changes, or Comment directly
- 📊 **Status Tracking** - Pending, Approved, Changes Requested, Closed, Merged
- 👥 **User Avatars** - Message-style cards with author initials
- 🎯 **Smart Filtering** - Filter by status using sidebar channels

## 🚀 Quick Start

### 1. Start Services

```bash
./START_SERVICES.sh
```

This starts:
- FastAPI server on port 8000
- Auto-sync service (checks every 5 seconds)

### 2. Access Dashboard

#### 💻 **Desktop:**
```
http://localhost:8000/dashboard/?token=demo-token-123
```

#### 📱 **Mobile (Easy QR Code Access):**

**Show QR Code:**
```bash
./SHOW_QR.sh
```

Or run directly:
```bash
python3 show_qr_code.py
```

**What you get:**
- ✅ QR code displayed in terminal
- ✅ QR code image saved as `reviewflow_qr_code.png`
- ✅ Scan with your mobile camera
- ✅ Instant access to dashboard on your phone!

**Requirements for Mobile Access:**
- Both devices on same WiFi network
- Mobile camera app (built-in on iOS/Android)
- That's it! 🎉

### 3. Create PRs on GitHub

**That's it!** New PRs appear in the dashboard automatically within 5 seconds.

## 📊 Service Management

### Check Status
```bash
./CHECK_STATUS.sh
```

Shows:
- Server status and PID
- Auto-sync status and interval
- PR count and pending reviews
- Latest PRs

### Stop Services
```bash
./STOP_SERVICES.sh
```

Stops all running services.

### Manual Operations

```bash
# Fetch new PRs immediately
python3 fetch_new_pr.py

# Sync PR statuses with GitHub
python3 sync_github_prs.py

# Create a test PR
python3 create_test_pr.py
```

## 🎨 Dashboard Features

### Sidebar Navigation
- `# all-pull-requests` - View all PRs
- `# pending-reviews` - PRs awaiting review (with count badge)
- `# approved` - Approved PRs
- `# changes-requested` - PRs needing changes
- `# closed` - Closed PRs (archive)
- `# merged` - Merged PRs (archive)

### PR Cards
Each PR shows:
- Author name and avatar
- Timestamp
- Status badge
- PR title (clickable to GitHub)
- Repository name
- Branch names (from → to)
- File statistics (+additions/-deletions)
- AI-generated summary
- Action buttons (for pending PRs)

### Actions
For pending PRs:
- ✅ **Approve** - Approve the PR (with confetti!)
- ❌ **Request Changes** - Request modifications with comment
- 💬 **Comment** - Add review comments
- 🔗 **View on GitHub** - Open in browser

## 🤖 Auto-Sync Service

The auto-sync service runs continuously in the background:

**Interval:** 5 seconds
**Function:**
1. Checks GitHub for new PRs
2. Compares with database
3. Fetches new PRs automatically
4. Generates AI analysis
5. Updates dashboard

**Change Interval:**
```bash
# Stop current service
./STOP_SERVICES.sh

# Start with custom interval (in seconds)
python3 auto_sync_service.py 10   # Every 10 seconds
python3 auto_sync_service.py 30   # Every 30 seconds
python3 auto_sync_service.py 60   # Every 1 minute
```

## 📁 Project Structure

```
.
├── app/
│   ├── main.py                 # FastAPI application
│   ├── routes/                 # API routes
│   │   ├── dashboard.py        # Dashboard endpoints
│   │   └── github.py           # Webhook handlers
│   ├── services/               # Business logic
│   │   ├── ai_service.py       # Claude AI integration
│   │   ├── github_service.py   # GitHub API
│   │   └── pr_summary_service.py
│   ├── templates/
│   │   └── dashboard.html      # Slack-style UI
│   └── database.py             # SQLite operations
├── notifications.db            # SQLite database
├── auto_sync_service.py        # Background sync service
├── fetch_new_pr.py            # Manual PR fetch
├── sync_github_prs.py         # Status sync
├── create_test_pr.py          # Test PR creator
├── setup_webhook.py           # Webhook configuration
├── START_SERVICES.sh          # Start all services
├── STOP_SERVICES.sh           # Stop all services
└── CHECK_STATUS.sh            # Check service status
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# GitHub
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_TOKEN=ghp_your-github-token

# AI Service
NERD_COMPLETION_API_KEY=your-api-key
NERD_COMPLETION_BASE_URL=https://api-url.com

# Dashboard
DASHBOARD_ACCESS_TOKEN=demo-token-123

# Server
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 📊 Database

SQLite database stores:
- PR metadata (number, title, author, repository)
- Status (pending, approved, changes_requested, etc.)
- AI analysis (summary, key changes, risk assessment)
- File statistics
- User actions history

**View database:**
```bash
sqlite3 notifications.db
> SELECT pr_number, pr_title, status FROM notifications;
```

## 🔧 Advanced Setup

### Webhooks (Optional)

For instant sync instead of polling:

1. Start ngrok:
```bash
ngrok http 8000
```

2. Configure webhook:
```bash
python3 setup_webhook.py https://your-ngrok-url.ngrok.io
```

See `WEBHOOK_SETUP_GUIDE.md` for details.

### Production Deployment

For production:
1. Deploy to Heroku/Railway/Render
2. Set up environment variables
3. Configure GitHub webhook with production URL
4. Use PostgreSQL instead of SQLite
5. Set up proper authentication

## 📚 Documentation

- `README.md` - This file
- `AUTOMATION_COMPLETE.md` - Auto-sync setup guide
- `WEBHOOK_SETUP_GUIDE.md` - Webhook configuration
- `DASHBOARD_SUMMARY.md` - Dashboard features
- `MOBILE_ACCESS_SOLUTION.md` - Complete mobile access guide
- `MOBILE_TROUBLESHOOTING.md` - Mobile connectivity troubleshooting

## 🐛 Troubleshooting

### Mobile access not working?

**Quick diagnostic:**
```bash
./diagnose_mobile_access.sh
```

**Solution guides:**
- See `MOBILE_ACCESS_SOLUTION.md` for step-by-step solutions
- See `MOBILE_TROUBLESHOOTING.md` for detailed troubleshooting

### PRs not appearing?

```bash
# Check services are running
./CHECK_STATUS.sh

# Manual sync
python3 fetch_new_pr.py

# View logs
tail -f auto_sync.log
```

### Service crashed?

```bash
# Restart services
./STOP_SERVICES.sh
./START_SERVICES.sh
```

### GitHub API rate limit?

Wait 1 hour or use authenticated requests (already configured with GITHUB_TOKEN).

## 🎯 Workflow

1. **Developer creates PR on GitHub**
2. **Auto-sync detects it** (within 5 seconds)
3. **AI analyzes the PR** (commits, diffs, metadata)
4. **Dashboard updates** (new PR appears)
5. **Reviewer sees notification** (pending badge)
6. **Reviewer takes action** (approve/comment/request changes)
7. **Status updates** in dashboard and GitHub

## 📱 Mobile Access

ReviewFlow is fully mobile-responsive! Access the dashboard on your phone:

### **Quick QR Code Access:**

1. **Run the QR code generator:**
   ```bash
   ./SHOW_QR.sh
   ```

2. **Scan the QR code** with your phone camera

3. **Tap the notification** to open the dashboard

4. **Enjoy!** Full-featured mobile experience 📱

### **Manual Mobile Access:**

If both devices are on the same WiFi:
```
http://YOUR_LOCAL_IP:8000/dashboard/?token=demo-token-123
```

Find your IP with:
```bash
ipconfig getifaddr en0   # macOS
hostname -I              # Linux
ipconfig                 # Windows
```

### **Add to Home Screen:**

**iOS (Safari):**
1. Tap Share button → "Add to Home Screen"
2. Name it "ReviewFlow"
3. Now you have a native-like app! 📱

**Android (Chrome):**
1. Tap menu (⋮) → "Add to Home screen"
2. Name it "ReviewFlow"
3. App icon created! 📱

## 🏆 Benefits

- ✅ No context switching - Review PRs in one place
- ✅ AI-powered insights - Understand changes quickly
- ✅ Automatic sync - No manual refresh needed
- ✅ Beautiful UI - Familiar Slack-style interface
- ✅ Real-time actions - Approve/comment instantly
- ✅ Status tracking - See what needs attention
- ✅ **Mobile-ready** - Access from anywhere on any device
- ✅ **QR Code access** - Share with team instantly

## 📦 Requirements

- Python 3.13+
- FastAPI
- PyGithub
- Anthropic (Claude API)
- SQLite
- TailwindCSS (CDN)

## 🚀 Current Status

✅ **Active and Running**

- Server: http://localhost:8000
- Dashboard: http://localhost:8000/dashboard/?token=demo-token-123
- Auto-sync: Every 5 seconds
- PRs tracked: 3 (2 pending, 1 closed)

## 🎉 Success!

Your ReviewFlow dashboard is fully operational with:
- Slack-style UI ✅
- Auto-sync every 5 seconds ✅
- AI-powered analysis ✅
- Real-time actions ✅

**Just create PRs on GitHub and watch them appear automatically!** 🚀

---

**Made with ❤️ using Claude Code**
