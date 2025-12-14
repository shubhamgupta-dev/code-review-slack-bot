# Setup Guide - Getting GitHub & Slack Credentials

## 1. GitHub Webhook Secret ✅

**What is it?** A secret key you create to verify webhooks are from GitHub.

**How to get it:**
```bash
# Already generated for you!
GITHUB_WEBHOOK_SECRET=woojgrCHvYXJFWRBgYdpIyCdOikLyVsRWhZOVCOCCTc
```

Just copy this to your `.env` file!

---

## 2. GitHub Personal Access Token

**What is it?** Allows the bot to fetch PR details, diffs, and commits from GitHub API.

**Step-by-step:**

1. **Go to GitHub:**
   - Open: https://github.com/settings/tokens

2. **Generate New Token:**
   - Click **"Generate new token (classic)"**
   - Note: "Code Review Slack Bot"

3. **Select Scopes:**
   - ✅ `repo` (Full control of private repositories)

4. **Generate and Copy:**
   - Click "Generate token"
   - Copy the token (starts with `ghp_`)
   - ⚠️ You can only see this once!

5. **Update `.env`:**
   ```bash
   GITHUB_TOKEN=ghp_your_copied_token_here
   ```

---

## 3. Slack Bot Token

**What is it?** Allows the bot to post messages to Slack channels.

**Step-by-step:**

### 3.1 Create Slack App

1. **Go to Slack API:**
   - Open: https://api.slack.com/apps
   - Click **"Create New App"** → **"From scratch"**

2. **Configure App:**
   - App Name: "Code Review Bot"
   - Pick your workspace
   - Click **"Create App"**

### 3.2 Add Bot Permissions

1. **Go to OAuth & Permissions** (in left sidebar)

2. **Add Bot Token Scopes:**
   - Scroll to "Scopes" → "Bot Token Scopes"
   - Click "Add an OAuth Scope"
   - Add these scopes:
     - ✅ `chat:write` - Post messages
     - ✅ `chat:write.public` - Post to public channels without joining
     - ✅ `channels:read` - View basic channel info
     - ✅ `im:write` - Start direct messages

### 3.3 Install to Workspace

1. **Scroll to top** of OAuth & Permissions page

2. **Click "Install to Workspace"**
   - Review permissions
   - Click "Allow"

3. **Copy Bot User OAuth Token:**
   - You'll see: "Bot User OAuth Token"
   - Starts with `xoxb-`
   - Click "Copy"

4. **Update `.env`:**
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-copied-token-here
   ```

### 3.4 Get Signing Secret

1. **Go to Basic Information** (in left sidebar)

2. **Scroll to "App Credentials"**

3. **Copy "Signing Secret":**
   ```bash
   SLACK_SIGNING_SECRET=your_signing_secret_here
   ```

---

## 4. Fix SSL Certificates (macOS Only)

If you're on macOS and see SSL certificate errors:

```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

Or navigate in Finder:
- Applications → Python 3.13 → Double-click "Install Certificates.command"

---

## 5. Your Complete `.env` File Should Look Like:

```bash
# GitHub Configuration
GITHUB_WEBHOOK_SECRET=woojgrCHvYXJFWRBgYdpIyCdOikLyVsRWhZOVCOCCTc
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # Get from GitHub

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx  # Get from Slack
SLACK_SIGNING_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # Get from Slack
SLACK_APP_TOKEN=xapp-your-app-token-here  # Optional

# Nerd-Completion Configuration (Already configured!)
NERD_COMPLETION_API_KEY=NCT-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NERD_COMPLETION_BASE_URL=https://nerd-completion.staging-service.datanerd.one

# Application Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 6. Test It!

After updating your `.env` with real credentials:

```bash
# Restart the server (Ctrl+C to stop current one)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, test the webhook
python3 test_webhook_endpoint.py
```

You should see:
- ✅ Webhook processed successfully
- ✅ AI analysis completed
- ✅ Slack notification sent!

---

## 7. (Optional) Invite Bot to Slack Channel

To test, invite the bot to a channel:

1. Go to your Slack workspace
2. Go to any channel (or create a test channel)
3. Type: `/invite @Code Review Bot`
4. The bot can now post to that channel!

To set which channel to use by default, you'll need to update the code or use the channel ID.

---

## Quick Reference

| Credential | Where to Get | Starts With | Required? |
|------------|-------------|-------------|-----------|
| `GITHUB_WEBHOOK_SECRET` | You generate it | Any string | Yes |
| `GITHUB_TOKEN` | github.com/settings/tokens | `ghp_` | Yes |
| `SLACK_BOT_TOKEN` | api.slack.com/apps | `xoxb-` | Yes |
| `SLACK_SIGNING_SECRET` | api.slack.com/apps | Various | Yes |
| `NERD_COMPLETION_API_KEY` | Already have it! | `NCT-` | Yes ✅ |

---

## Need Help?

**GitHub Token Issues:**
- Make sure you selected `repo` scope
- Token must have access to the repository you're testing

**Slack Issues:**
- Make sure bot is invited to the channel
- Check bot has required scopes
- Run the SSL certificate fix if on macOS

**Still Having Issues?**
- Check server logs: Look at the terminal where server is running
- Check `.env` file: Make sure no extra spaces or quotes
- Restart server after updating `.env`

---

## Production Setup (Later)

When ready to deploy:

1. **Get a public URL:**
   ```bash
   ngrok http 8000
   ```

2. **Add webhook to GitHub:**
   - Repository → Settings → Webhooks
   - URL: `https://your-ngrok-url.ngrok.io/webhooks/github`
   - Secret: Use your `GITHUB_WEBHOOK_SECRET`

3. **Create a PR** and watch the magic happen! ✨