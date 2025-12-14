# 📂 ReviewFlow - Project Structure

## 🎯 Clean & Organized Structure

```
code-review-slack-bot/
│
├── 📱 app/                          # Core Application
│   ├── main.py                      # FastAPI application entry
│   ├── config.py                    # Settings & credentials
│   ├── database.py                  # SQLite operations
│   │
│   ├── routes/                      # API Endpoints
│   │   ├── dashboard.py             # Dashboard + Authentication
│   │   ├── github.py                # GitHub webhooks
│   │   ├── slack.py                 # Slack integration
│   │   └── health.py                # Health checks
│   │
│   ├── services/                    # Business Logic
│   │   ├── ai_service.py            # Claude AI integration
│   │   ├── github_service.py        # GitHub API client
│   │   └── pr_summary_service.py    # PR analysis
│   │
│   └── templates/                   # HTML Templates
│       ├── dashboard.html           # Main dashboard UI
│       └── login.html               # Login page
│
├── 📄 docs/                         # Documentation
│   ├── AUTOMATION_COMPLETE.md       # Auto-sync guide
│   ├── DASHBOARD_SUMMARY.md         # Dashboard features
│   ├── IMPLEMENTATION_SUMMARY.md    # Feature list
│   ├── MOBILE_ACCESS_SOLUTION.md    # Mobile setup
│   ├── MOBILE_TROUBLESHOOTING.md    # Mobile issues
│   ├── MUST_DO_FOR_MOBILE.txt       # Quick mobile guide
│   ├── PUBLIC_ACCESS_GUIDE.md       # ngrok/public access
│   ├── QUICK_MOBILE_ACCESS.md       # Quick reference
│   └── WEBHOOK_SETUP_GUIDE.md       # Webhook configuration
│
├── 🔧 scripts/                      # Shell Scripts
│   ├── START_SERVICES.sh            # Start server + auto-sync
│   ├── STOP_SERVICES.sh             # Stop all services
│   ├── CHECK_STATUS.sh              # Service status
│   ├── SHOW_QR.sh                   # Display QR code
│   ├── SETUP_PUBLIC_ACCESS.sh       # Setup ngrok
│   ├── FIX_MOBILE_ACCESS.sh         # Mobile troubleshooting
│   ├── diagnose_mobile_access.sh    # Diagnostic tool
│   └── fix_ssl.sh                   # SSL fixes
│
├── 🛠️  utils/                        # Utility Scripts
│   ├── auto_sync_service.py         # Background sync service
│   ├── show_qr_code.py              # QR code generator
│   ├── fetch_new_pr.py              # Manual PR fetch
│   ├── sync_github_prs.py           # Status sync
│   ├── create_test_pr.py            # Test PR creator
│   ├── setup_webhook.py             # Webhook setup
│   └── trigger_webhook.py           # Webhook tester
│
├── 💾 data/                         # Data Files
│   ├── notifications.db             # SQLite database
│   └── reviewflow_qr_code.png       # Generated QR code
│
├── 📝 Root Files                    # Configuration
│   ├── .env                         # Environment variables (SECRET!)
│   ├── .env.example                 # Example config
│   ├── .gitignore                   # Git ignore rules
│   ├── README.md                    # Main documentation
│   ├── PROJECT_STRUCTURE.md         # This file
│   ├── requirements.txt             # Python dependencies
│   ├── pyproject.toml               # Project metadata
│   │
│   └── 🚀 Quick Scripts            # Convenience wrappers
│       ├── start.sh                 # → scripts/START_SERVICES.sh
│       ├── stop.sh                  # → scripts/STOP_SERVICES.sh
│       └── status.sh                # → scripts/CHECK_STATUS.sh
│
└── 📋 Generated Files (Runtime)
    ├── server.log                   # Server logs
    ├── auto_sync.log                # Auto-sync logs
    └── __pycache__/                 # Python cache
```

---

## 🎯 Quick Reference

### **Start Services:**
```bash
./start.sh
# or
./scripts/START_SERVICES.sh
```

### **Stop Services:**
```bash
./stop.sh
# or
./scripts/STOP_SERVICES.sh
```

### **Check Status:**
```bash
./status.sh
# or
./scripts/CHECK_STATUS.sh
```

### **Show QR Code:**
```bash
./scripts/SHOW_QR.sh
```

### **Public Access:**
```bash
./scripts/SETUP_PUBLIC_ACCESS.sh
```

---

## 📂 Folder Purposes

### **`app/`** - Core Application
The main FastAPI application with all backend logic.

**What's inside:**
- `main.py` - App initialization, CORS, middleware
- `config.py` - Settings loaded from .env
- `database.py` - SQLite async operations
- `routes/` - API endpoints organized by feature
- `services/` - Business logic (GitHub, AI, etc.)
- `templates/` - Jinja2 HTML templates

**When to modify:**
- Add new features: Add routes/services here
- Change logic: Modify services
- Update UI: Edit templates

---

### **`docs/`** - Documentation
All markdown documentation files.

**What's inside:**
- Setup guides
- Troubleshooting docs
- Feature documentation
- Quick references

**When to modify:**
- Add new features: Update relevant docs
- User issues: Update troubleshooting guides

---

### **`scripts/`** - Shell Scripts
Bash scripts for common operations.

**What's inside:**
- Service management scripts
- Diagnostic tools
- Setup helpers
- QR code display

**When to modify:**
- Add new automation: Create new script here
- Change startup: Modify START_SERVICES.sh

---

### **`utils/`** - Python Utilities
Standalone Python scripts and utilities.

**What's inside:**
- Background services (auto_sync_service.py)
- CLI tools (fetch_new_pr.py)
- Generators (show_qr_code.py)
- Setup scripts (setup_webhook.py)

**When to modify:**
- Add new CLI tool: Create here
- Modify sync interval: Edit auto_sync_service.py

---

### **`data/`** - Data Files
Database and generated files.

**What's inside:**
- `notifications.db` - SQLite database
- `reviewflow_qr_code.png` - Generated QR code
- Log files (if configured)

**When to modify:**
- Database schema: Update database.py
- Backup: Copy notifications.db

---

## 🔧 Important Files

### **Configuration:**
- `.env` - **SECRET!** Contains passwords, tokens, API keys
- `.env.example` - Template for .env
- `config.py` - Loads and validates .env

### **Entry Points:**
- `app/main.py` - FastAPI application
- `utils/auto_sync_service.py` - Background sync

### **Quick Access:**
- `start.sh` - Start everything
- `stop.sh` - Stop everything
- `status.sh` - Check status

---

## 🚀 Common Tasks

### **Add New Feature:**
1. Add route in `app/routes/`
2. Add service logic in `app/services/`
3. Update templates if needed
4. Update documentation in `docs/`

### **Change Database:**
1. Modify schema in `app/database.py`
2. Delete `data/notifications.db`
3. Restart server (recreates with new schema)

### **Add New Script:**
1. Create in `scripts/` (shell) or `utils/` (Python)
2. Make executable: `chmod +x script_name.sh`
3. Document in README.md

### **Deploy to Production:**
1. Review all `.env` variables
2. Change default passwords
3. Use production database (PostgreSQL)
4. Set up proper logging
5. Configure reverse proxy (nginx)
6. Enable HTTPS

---

## 📊 File Count Summary

```
Core App:       12 files  (app/)
Documentation:   9 files  (docs/)
Scripts:         8 files  (scripts/)
Utilities:       7 files  (utils/)
Data:            2 files  (data/)
Config:          7 files  (root)
---
Total:          45 files
```

---

## 🎨 Development Workflow

### **Local Development:**
```bash
1. Start services: ./start.sh
2. Edit code in app/
3. Server auto-reloads (--reload flag)
4. Test at http://localhost:8000/dashboard/login
5. Check logs: tail -f server.log
```

### **Testing:**
```bash
1. Create test PR: python3 utils/create_test_pr.py
2. Fetch manually: python3 utils/fetch_new_pr.py
3. Check status: ./status.sh
```

### **Mobile Testing:**
```bash
1. Show QR: ./scripts/SHOW_QR.sh
2. Scan with phone
3. Login and test
4. Check diagnostics if issues
```

---

## 🔒 Security Notes

### **Sensitive Files (Never Commit!):**
- `.env` - Contains secrets
- `data/notifications.db` - Contains data
- `*.log` - May contain sensitive info

### **Public Files (OK to Commit):**
- All code in `app/`
- All scripts in `scripts/`, `utils/`
- All docs in `docs/`
- `requirements.txt`, `.gitignore`, etc.

---

## 🎉 Benefits of This Structure

✅ **Organized** - Easy to find files
✅ **Scalable** - Add features easily
✅ **Clean Root** - No clutter
✅ **Clear Purpose** - Each folder has specific role
✅ **Easy Navigation** - Logical hierarchy
✅ **Production Ready** - Professional structure

---

**Last Updated:** 2025-12-12
**Structure Version:** 2.0
