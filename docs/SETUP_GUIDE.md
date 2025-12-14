# Detailed Setup Guide

This guide walks you through setting up the Code Review Slack Bot step-by-step.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [GitHub Configuration](#github-configuration)
4. [Slack Configuration](#slack-configuration)
5. [Testing the Setup](#testing-the-setup)
6. [Production Deployment](#production-deployment)

## Prerequisites

- Python 3.11+ installed
- GitHub repository with admin access
- Slack workspace with app creation permissions
- ngrok or similar tool for local testing (optional)

## Local Development Setup

### Step 1: Install Python Dependencies

```bash
cd ~/Desktop/code-review-slack-bot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

You'll fill in these values in the following steps.

## GitHub Configuration

### Step 1: Create Personal Access Token

1. Visit [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a descriptive name: "Code Review Slack Bot"
4. Set expiration (recommend 90 days for security)
5. Select these scopes:
   ```
   ✓ repo (all)
     ✓ repo:status
     ✓ repo_deployment
     ✓ public_repo
     ✓ repo:invite
     ✓ security_events
   ```
6. Click **"Generate token"**
7. Copy the token (starts with `ghp_`)
8. Add to `.env`:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   ```

### Step 2: Generate Webhook Secret

```bash
# Generate a random secret
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and add to `.env`:
```
GITHUB_WEBHOOK_SECRET=your_generated_secret_here
```

### Step 3: Configure Repository Webhook

**Note**: For local testing, first expose your local server (see Step 4 below)

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `https://your-domain.com/webhooks/github`
     - For local testing: `https://your-ngrok-url.ngrok.io/webhooks/github`
   - **Content type**: `application/json`
   - **Secret**: Paste the webhook secret from your `.env` file
   - **SSL verification**: Enable (for production)

4. Under "Which events would you like to trigger this webhook?":
   - Select **"Let me select individual events"**
   - Check these boxes:
     - ✓ Pull requests
     - ✓ Pull request reviews
     - ✓ Pull request review comments
   - Uncheck everything else

5. Ensure **"Active"** is checked
6. Click **"Add webhook"**

### Step 4: Expose Local Server (for development)

If testing locally, use ngrok:

```bash
# Install ngrok (if not already installed)
# Visit https://ngrok.com/download

# Start ngrok
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and use it in your webhook configuration.

## Slack Configuration

### Step 1: Create Slack App

1. Visit [Slack API Apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Select **"From scratch"**
4. Enter:
   - **App Name**: "Code Review Bot" (or your preferred name)
   - **Workspace**: Select your workspace
5. Click **"Create App"**

### Step 2: Configure Bot Token Scopes

1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Click **"Add an OAuth Scope"** and add:
   ```
   chat:write
   chat:write.public
   channels:read
   im:write
   ```

These permissions allow the bot to:
- Post messages to channels
- Post to channels without being invited
- View channel information
- Send direct messages

### Step 3: Install App to Workspace

1. Scroll to top of **"OAuth & Permissions"** page
2. Click **"Install to Workspace"**
3. Review permissions and click **"Allow"**
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)
5. Add to `.env`:
   ```
   SLACK_BOT_TOKEN=xoxb-your-token-here
   ```

### Step 4: Get Signing Secret

1. In left sidebar, click **"Basic Information"**
2. Scroll to **"App Credentials"**
3. Copy the **"Signing Secret"**
4. Add to `.env`:
   ```
   SLACK_SIGNING_SECRET=your-signing-secret-here
   ```

### Step 5: Enable Interactivity

1. In left sidebar, click **"Interactivity & Shortcuts"**
2. Toggle **"Interactivity"** to **ON**
3. Set **"Request URL"**: `https://your-domain.com/slack/interactions`
   - For local testing: `https://your-ngrok-url.ngrok.io/slack/interactions`
4. Click **"Save Changes"**

### Step 6: Subscribe to Events (Optional)

For future enhancements, you can subscribe to events:

1. In left sidebar, click **"Event Subscriptions"**
2. Toggle to **ON**
3. Set **"Request URL"**: `https://your-domain.com/slack/events`
4. Add Bot User Events:
   - `message.channels` (for threaded conversations)
   - `app_mention` (for @mentions)
5. Click **"Save Changes"**

### Step 7: Customize App Appearance

1. Click **"Basic Information"** in left sidebar
2. Scroll to **"Display Information"**
3. Add:
   - **App name**: Code Review Bot
   - **Short description**: Brings GitHub PR reviews to Slack
   - **Icon**: Upload a custom icon (optional)
   - **Background color**: Choose your preferred color
4. Click **"Save Changes"**

### Step 8: Invite Bot to Channel

1. In Slack, go to the channel where you want PR notifications (e.g., `#code-reviews`)
2. Type: `/invite @Code Review Bot`
3. The bot should join the channel

**Note**: If using a private channel, you must manually invite the bot or add `groups:read` and `groups:write` scopes.

## Testing the Setup

### Step 1: Start the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
python -m app.main
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test Health Endpoint

In a new terminal:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Code Review Slack Bot is running"
}
```

### Step 3: Test GitHub Webhook

1. Create a test pull request in your repository
2. Check your Slack channel for the PR notification
3. Verify the message includes:
   - PR title and description
   - File changes summary
   - Action buttons (Approve, Comment, Request Changes, View on GitHub)

### Step 4: Test Slack Interactions

1. Click the **"Approve"** button in Slack
2. Verify:
   - A reply appears in the thread confirming approval
   - The PR is marked as approved on GitHub

3. Click the **"Comment"** button
4. Verify:
   - A modal opens for entering a comment
   - After submitting, the comment appears on GitHub

### Step 5: Check Logs

Monitor the application logs for any errors:
```bash
# Logs will appear in the terminal where you ran the app
# Look for:
INFO:     Received GitHub webhook: pull_request
INFO:     Sent PR notification to #code-reviews
INFO:     Received Slack interaction: block_actions
```

## Troubleshooting

### Issue: Webhook not triggering

**Solution**:
1. Check GitHub webhook delivery logs:
   - Go to Repository → Settings → Webhooks
   - Click on your webhook
   - Check "Recent Deliveries" tab
2. Verify the response status is `200`
3. If getting errors, check:
   - URL is correct and accessible
   - Webhook secret matches `.env`
   - Server is running

### Issue: Slack interactions not working

**Solution**:
1. Verify signing secret is correct in `.env`
2. Check interactivity URL is accessible
3. Review Slack app permissions
4. Check logs for signature verification errors

### Issue: Bot not posting to channel

**Solution**:
1. Verify bot is in the channel: `/invite @your-bot-name`
2. Check `chat:write.public` scope is enabled
3. Update channel name in code if needed:
   - Edit `app/services/slack_service.py:12`
   - Change `self.default_channel = "#code-reviews"` to your channel

### Issue: GitHub API errors

**Solution**:
1. Verify GitHub token has correct permissions
2. Check token hasn't expired
3. Verify repository name is correct
4. Check GitHub API rate limits

## Production Deployment

### Option 1: Cloud Platform (Heroku, Railway, Render)

1. Create new app on your platform
2. Connect to GitHub repository
3. Set environment variables in platform settings
4. Deploy
5. Update webhook URLs to production URLs

### Option 2: VPS (DigitalOcean, AWS EC2, etc.)

1. Set up server with Python 3.11+
2. Clone repository
3. Install dependencies
4. Set up systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/code-review-bot.service
```

```ini
[Unit]
Description=Code Review Slack Bot
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/code-review-slack-bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

5. Start service:
```bash
sudo systemctl start code-review-bot
sudo systemctl enable code-review-bot
```

6. Set up nginx reverse proxy with SSL

### Option 3: Docker

See README.md for Docker deployment instructions.

## Security Best Practices

1. **Use Environment Variables**: Never commit secrets to Git
2. **Rotate Tokens**: Regularly rotate GitHub and Slack tokens
3. **Enable HTTPS**: Always use HTTPS in production
4. **Webhook Secrets**: Use strong, random secrets
5. **Minimal Permissions**: Only grant necessary scopes
6. **Monitor Logs**: Set up logging and monitoring
7. **Rate Limiting**: Implement rate limiting for webhooks

## Next Steps

- Customize Slack message formatting
- Add more review actions
- Set up monitoring and alerting
- Configure logging for production
- Add analytics tracking

## Getting Help

- Check application logs for errors
- Review GitHub webhook delivery logs
- Test endpoints manually with curl
- Consult Slack API documentation
- Open an issue on GitHub
