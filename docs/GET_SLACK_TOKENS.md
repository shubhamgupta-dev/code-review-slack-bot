# Get Tokens for Your Slack App: SlackBot_Github_AI

You've created the app! Now let's get the credentials you need.

## Step 1: Go to Your App's Settings

1. Go to: **https://api.slack.com/apps**
2. Click on your app: **"SlackBot_Github_AI"**

---

## Step 2: Add Bot Token Scopes (IMPORTANT - Do This First!)

Before you can get the token, you need to add permissions:

### 2.1 Click "OAuth & Permissions" in the left sidebar

### 2.2 Scroll down to "Scopes" → "Bot Token Scopes"

### 2.3 Click "Add an OAuth Scope" and add these 4 scopes:

```
chat:write
chat:write.public
channels:read
im:write
```

After adding each scope, you should see them listed like:

```
✓ chat:write - Send messages as @SlackBot_Github_AI
✓ chat:write.public - Send messages to channels @SlackBot_Github_AI isn't a member of
✓ channels:read - View basic information about public channels in a workspace
✓ im:write - Start direct messages with people
```

---

## Step 3: Install App to Workspace

### 3.1 Scroll back to the TOP of the "OAuth & Permissions" page

### 3.2 Click the big green button: "Install to Workspace"

### 3.3 Review permissions and click "Allow"

---

## Step 4: Copy Your Bot Token

After installation, you'll immediately see:

```
OAuth Tokens for Your Workspace

Bot User OAuth Token
xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
                                                   [Copy]
```

### ✅ Copy this token!

Paste it into your `.env` file:

```bash
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 5: Get Your Signing Secret

### 5.1 In the left sidebar, click "Basic Information"

### 5.2 Scroll down to "App Credentials"

### 5.3 Find "Signing Secret" and click "Show"

### 5.4 Copy the signing secret

It looks something like:
```
abc123def456ghi789jkl012mno345pq
```

Paste it into your `.env` file:

```bash
SLACK_SIGNING_SECRET=abc123def456ghi789jkl012mno345pq
```

---

## Your .env File Should Now Have:

```bash
# GitHub Configuration
GITHUB_WEBHOOK_SECRET=your-webhook-secret-here
GITHUB_TOKEN=ghp_YOUR_GITHUB_TOKEN_HERE

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx  # ← ADD THIS
SLACK_SIGNING_SECRET=abc123def456ghi789jkl012mno345pq                    # ← ADD THIS
SLACK_APP_TOKEN=xapp-your-app-token-here

# Nerd-Completion Configuration
NERD_COMPLETION_API_KEY=NCT-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NERD_COMPLETION_BASE_URL=https://nerd-completion.staging-service.datanerd.one

# Application Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## Quick Navigation:

- **Your App**: https://api.slack.com/apps
- **OAuth & Permissions**: https://api.slack.com/apps → SlackBot_Github_AI → OAuth & Permissions
- **Basic Information**: https://api.slack.com/apps → SlackBot_Github_AI → Basic Information

---

## After You Update .env:

1. Save the `.env` file
2. Restart your server (it will auto-reload)
3. Run: `python3 test_webhook_endpoint.py`
4. You should see a message in your Slack channel! 🎉

---

## Next Steps:

Once you have the tokens working:

1. **Invite the bot to a channel:**
   - In Slack, go to any channel
   - Type: `/invite @SlackBot_Github_AI`

2. **Test it:**
   - Run the webhook test
   - Check the channel for a message from your bot

3. **Set up GitHub webhook** (for production):
   - Use ngrok to expose your local server
   - Add webhook URL to your GitHub repository