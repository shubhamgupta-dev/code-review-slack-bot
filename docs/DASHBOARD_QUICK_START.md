# 🤖 Custom Dashboard - Quick Start Guide

## ✅ Your Dashboard is Ready!

You now have a **mobile-friendly web dashboard** instead of Slack!

---

## 🚀 Access Your Dashboard

### Desktop/Laptop:
```
http://localhost:8000/dashboard/?token=demo-token-123
```

### Mobile (on same network):
```
http://YOUR_COMPUTER_IP:8000/dashboard/?token=demo-token-123
```

To find your computer's IP:
```bash
# On macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# On Windows
ipconfig
```

---

## 📱 How It Works

### 1. GitHub PR Opened
```
GitHub → Webhook → Your Server → Database → Dashboard
```

### 2. You Review PR
```
Open Dashboard → See PR with AI Summary → Click Action Button
```

### 3. Action Sent to GitHub
```
Dashboard → API → GitHub (Approve/Comment/Request Changes)
```

---

## 🎨 Dashboard Features

### ✅ What You Can Do:

- **View All PRs** - Real-time feed of pending reviews
- **AI Summaries** - Claude-powered analysis of each PR
- **Approve PRs** - One-click approval sent to GitHub
- **Request Changes** - Add comments with changes needed
- **Add Comments** - General review comments
- **Mobile-Friendly** - Works perfectly on phones
- **Secure Access** - Token-based authentication

### 📊 Dashboard Shows:

- PR title, number, and description
- Author and repository
- Branch names (from → to)
- Files changed, additions, deletions
- Complexity estimate (Small/Medium/Large)
- AI analysis:
  - Functional summary
  - Key changes
  - Scope of change
  - Risk assessment
  - Review focus areas

---

## 🧪 Test It Now!

### Step 1: Send a test PR webhook
```bash
python3 test_webhook_endpoint.py
```

### Step 2: Open the dashboard
```
http://localhost:8000/dashboard/?token=demo-token-123
```

### Step 3: You should see:
- 1 pending notification
- PR #456: "Implement real-time notification system"
- AI summary with key changes
- Action buttons (Approve, Comment, Request Changes)

### Step 4: Test an action
- Click **"✅ Approve"**
- Confirm the action
- Check GitHub - the PR will be approved!

---

## 📱 Install as Mobile App (PWA)

### On iPhone/iPad:
1. Open dashboard in Safari
2. Tap the Share button
3. Tap "Add to Home Screen"
4. Name it "Code Reviews"
5. Tap "Add"

### On Android:
1. Open dashboard in Chrome
2. Tap the menu (3 dots)
3. Tap "Add to Home screen"
4. Name it "Code Reviews"
5. Tap "Add"

Now you have an app icon on your phone!

---

## 🔐 Security

### Change the Access Token

**Important:** Change the default token in production!

Edit `.env`:
```bash
DASHBOARD_ACCESS_TOKEN=your-secret-token-here
```

Then access:
```
http://localhost:8000/dashboard/?token=your-secret-token-here
```

### Bookmark with Token

Save this URL in your browser/phone for quick access:
```
http://YOUR_IP:8000/dashboard/?token=your-token
```

---

## 🌐 Make it Accessible from Anywhere

### Option 1: ngrok (Development)

```bash
# Install ngrok (if not installed)
brew install ngrok  # macOS
# or download from https://ngrok.com

# Expose your server
ngrok http 8000
```

You'll get a public URL like:
```
https://abc123.ngrok.io
```

Access from anywhere:
```
https://abc123.ngrok.io/dashboard/?token=demo-token-123
```

### Option 2: Deploy to Cloud (Production)

- **Fly.io** - Free tier, easy deployment
- **Railway** - Simple Python deployments
- **DigitalOcean** - $5/month droplet
- **AWS/GCP** - Full control

---

## 🔔 Set Up GitHub Webhook (Production)

Once you have a public URL:

1. **Go to your GitHub repo** → Settings → Webhooks
2. **Add webhook**:
   - Payload URL: `https://your-url.com/webhooks/github`
   - Content type: `application/json`
   - Secret: Your `GITHUB_WEBHOOK_SECRET` from `.env`
3. **Select events**:
   - Pull requests
   - Pull request reviews
4. **Save**

Now every PR will automatically appear in your dashboard!

---

## 📊 Dashboard Statistics

The dashboard shows:
- **Pending** - PRs awaiting your review
- **Approved** - PRs you've approved
- **Changes** - PRs where you requested changes
- **Total** - All PRs received

---

## 💡 Tips

### Quick Actions
- **Approve** - One-click approval
- **Comment** - Opens modal for your comment
- **Request Changes** - Opens modal (comment required)
- **View on GitHub** - Opens PR in new tab

### Mobile Gestures
- **Pull down** to refresh
- **Tap** action buttons (large touch targets)
- **Scroll** through PR list
- **Modal** for comments with keyboard

### Workflow
1. Get notification on phone/computer
2. Open dashboard
3. Read AI summary
4. Make decision
5. Tap button
6. Done! ✅

---

## 🆚 Dashboard vs Slack

| Feature | Custom Dashboard | Slack |
|---------|-----------------|-------|
| **Setup Time** | ✅ 0 minutes (done!) | ❌ 15+ minutes |
| **Cost** | ✅ Free | ❌ May require paid plan |
| **Mobile UX** | ✅ Optimized | ⚠️ Generic |
| **Customization** | ✅ Full control | ❌ Limited |
| **Offline** | ✅ Caches locally | ❌ Requires connection |
| **API Limits** | ✅ None | ⚠️ Rate limits |
| **Works Anywhere** | ✅ Just a URL | ⚠️ Need Slack app |

---

## 🐛 Troubleshooting

### Dashboard shows "No notifications"
- Run `python3 test_webhook_endpoint.py` to create a test notification
- Check server logs for errors
- Verify database file exists: `ls notifications.db`

### "Invalid or missing access token"
- Make sure URL includes `?token=demo-token-123`
- Check token matches in `.env` file

### Actions not working
- Check `GITHUB_TOKEN` in `.env` is valid
- Verify token has `repo` scope
- Check server logs for GitHub API errors

### Can't access from mobile
- Make sure mobile is on same WiFi network
- Use computer's IP address, not `localhost`
- Check firewall isn't blocking port 8000

---

## 📚 API Documentation

All endpoints require `?token=your-token` or `X-Dashboard-Token` header.

### Get all notifications
```bash
GET /dashboard/api/notifications
GET /dashboard/api/notifications?status=pending
```

### Get single notification
```bash
GET /dashboard/api/notifications/{id}
```

### Approve PR
```bash
POST /dashboard/api/notifications/{id}/approve
Body: {"comment": "Looks good!"}
```

### Request changes
```bash
POST /dashboard/api/notifications/{id}/request-changes
Body: {"comment": "Please fix X"}
```

### Add comment
```bash
POST /dashboard/api/notifications/{id}/comment
Body: {"comment": "Nice work!"}
```

### Get stats
```bash
GET /dashboard/api/stats
```

---

## 🎉 You're All Set!

Your custom dashboard is:
- ✅ Running on http://localhost:8000/dashboard/?token=demo-token-123
- ✅ Saving notifications to SQLite database
- ✅ Connected to GitHub API
- ✅ Mobile-friendly and responsive
- ✅ Secure with token authentication
- ✅ Ready for production!

**Next Steps:**
1. Test it with `python3 test_webhook_endpoint.py`
2. Open dashboard and try approving/commenting
3. Bookmark the URL for quick access
4. (Optional) Set up ngrok for remote access
5. (Optional) Install as PWA on your phone

---

## 💬 Support

If you have questions or issues:
1. Check server logs: Look at the terminal where server is running
2. Check database: `sqlite3 notifications.db "SELECT * FROM notifications;"`
3. Test GitHub API: `python3 test_github_write.py`
4. Check the design doc: `CUSTOM_UI_DESIGN.md`

Enjoy your custom code review dashboard! 🚀
