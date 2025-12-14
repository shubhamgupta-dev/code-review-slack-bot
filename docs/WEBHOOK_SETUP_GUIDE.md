# GitHub Webhook Setup for Automatic PR Sync

This guide will help you set up automatic PR synchronization so that whenever you raise a PR on GitHub, it automatically appears in your ReviewFlow dashboard.

## Prerequisites

✅ ngrok installed (already done)
✅ Server running on port 8000
✅ GitHub personal access token configured

## Step-by-Step Setup

### Option 1: Using ngrok (Temporary - For Development)

#### Step 1: Start ngrok

First, you need to authenticate ngrok (one-time setup):

```bash
# Sign up for free at: https://ngrok.com/
# Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken

# Authenticate ngrok (replace with your token)
ngrok config add-authtoken <your-ngrok-token>
```

Then start the tunnel:

```bash
# Open a new terminal window and run:
ngrok http 8000
```

You'll see output like:
```
ngrok

Session Status                online
Account                       your-email (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS forwarding URL** (e.g., `https://abc123.ngrok.io`)

#### Step 2: Set up the GitHub webhook

```bash
# In your project terminal, run:
python3 setup_webhook.py https://abc123.ngrok.io
```

This will:
- Connect to your GitHub repository
- Create a webhook pointing to your ngrok URL
- Configure it to send pull_request events
- Use the secret from your `.env` file

#### Step 3: Test it!

1. Create a new PR on GitHub (either through web UI or CLI)
2. Watch your server logs - you should see the webhook event
3. Refresh your dashboard: http://localhost:8000/dashboard/?token=demo-token-123
4. The new PR should appear automatically!

**⚠️ Note:** ngrok free URLs expire when you restart ngrok. You'll need to update the webhook URL each time.

---

### Option 2: Using a Permanent Public URL (Production)

For production or long-term use, you need a permanent public URL. Here are some options:

#### A. Deploy to a Cloud Platform

**Heroku:**
```bash
heroku create your-reviewflow-app
git push heroku main
# Your URL: https://your-reviewflow-app.herokuapp.com
```

**Railway:**
```bash
railway init
railway up
# Railway provides automatic HTTPS URL
```

**Render:**
- Connect your GitHub repo
- Auto-deploys on push
- Free tier available

#### B. Use Your Own Server

If you have a VPS or server with a public IP:

```bash
# Update your DNS to point to your server
# Set up nginx as reverse proxy
# Configure SSL with Let's Encrypt

# Example nginx config:
server {
    listen 443 ssl;
    server_name reviewflow.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

Then set up webhook:
```bash
python3 setup_webhook.py https://reviewflow.yourdomain.com
```

#### C. GitHub Actions (Alternative Approach)

Instead of webhooks, poll GitHub periodically:

Create a cron job to fetch new PRs every 5 minutes:

```bash
# Add to crontab
*/5 * * * * cd /path/to/project && python3 fetch_new_pr.py
```

Or create a simple polling service:

```python
# polling_service.py
import asyncio
import subprocess
import time

async def poll_github():
    while True:
        print("🔄 Checking for new PRs...")
        subprocess.run(["python3", "fetch_new_pr.py"])
        await asyncio.sleep(300)  # 5 minutes

asyncio.run(poll_github())
```

Run it:
```bash
python3 polling_service.py &
```

---

## Quick Start (Recommended for Testing)

### Single Command Setup:

```bash
# Terminal 1: Start your server (already running)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start ngrok
ngrok http 8000

# Terminal 3: Set up webhook (replace URL with your ngrok URL from Terminal 2)
python3 setup_webhook.py https://YOUR-NGROK-URL.ngrok.io
```

---

## Verification

After setup, verify webhook is working:

### 1. Check GitHub Webhook Settings

Go to: https://github.com/shubhamgupta-dev/10X_Dev_Workshop/settings/hooks

You should see your webhook listed with a green checkmark.

### 2. Test with a New PR

```bash
# Create a test PR
python3 create_test_pr.py

# Or manually create one on GitHub
# Go to your repo → Pull requests → New pull request
```

### 3. Check Server Logs

You should see:
```
INFO - Received GitHub webhook: pull_request
INFO - Retrieved X commit messages for PR #Y
INFO - AI analysis completed for PR: <title>
INFO - Saved notification #Z to database
```

### 4. Check Dashboard

Refresh: http://localhost:8000/dashboard/?token=demo-token-123

Your new PR should appear automatically!

---

## Troubleshooting

### Webhook not receiving events?

1. **Check ngrok is running:**
   ```bash
   curl http://localhost:4040/api/tunnels
   ```

2. **Test webhook manually:**
   ```bash
   python3 trigger_webhook.py
   ```

3. **Check GitHub webhook deliveries:**
   - Go to repo → Settings → Webhooks
   - Click on your webhook
   - Check "Recent Deliveries" tab
   - Look for errors (red X)

### ngrok session expired?

Free ngrok sessions expire after 2 hours. Restart ngrok and update webhook:

```bash
# Restart ngrok
ngrok http 8000

# Update webhook with new URL
python3 setup_webhook.py https://NEW-NGROK-URL.ngrok.io
```

### Webhook secret mismatch?

Ensure `GITHUB_WEBHOOK_SECRET` in `.env` matches what's configured in GitHub.

---

## Production Deployment Checklist

- [ ] Deploy to cloud platform with permanent URL
- [ ] Set up SSL/HTTPS (required by GitHub)
- [ ] Configure environment variables on server
- [ ] Set up webhook with production URL
- [ ] Test webhook delivery
- [ ] Set up monitoring/logging
- [ ] Configure auto-restart on crashes
- [ ] Set up database backups

---

## Alternative: Manual Sync

If you don't want to deal with webhooks, you can manually sync:

```bash
# Fetch new PRs anytime
python3 fetch_new_pr.py

# Or set up a periodic sync
watch -n 300 python3 fetch_new_pr.py  # Every 5 minutes
```

---

## Current Status

✅ Server running: http://localhost:8000
✅ Dashboard accessible: http://localhost:8000/dashboard/?token=demo-token-123
✅ ngrok installed
⏳ Webhook setup pending (follow steps above)

## Next Steps

1. **For Quick Testing:**
   ```bash
   # Terminal 2:
   ngrok config add-authtoken <get-from-ngrok.com>
   ngrok http 8000

   # Terminal 3:
   python3 setup_webhook.py https://YOUR-NGROK-URL.ngrok.io
   ```

2. **For Production:**
   - Deploy to Heroku/Railway/Render
   - Update webhook with permanent URL

3. **For Simple Setup:**
   - Use polling: `python3 fetch_new_pr.py` when needed
   - Or set up cron job to poll every 5 minutes

Choose the option that works best for your use case!
