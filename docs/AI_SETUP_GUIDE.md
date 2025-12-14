# AI Integration Setup Guide

## Quick Start

This guide walks you through setting up the AI-powered PR analysis feature.

## Prerequisites

- Existing Code Review Slack Bot installation
- GitHub and Slack already configured
- Python 3.11+ environment

## Step 1: Get Anthropic API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-`)

## Step 2: Update Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install new dependency
pip install anthropic==0.39.0

# Or reinstall all dependencies
pip install -r requirements.txt
```

## Step 3: Configure Environment Variable

Edit your `.env` file and add:

```bash
# AI Configuration (Required for NLP-based PR analysis)
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

**Important:** Replace `sk-ant-your-actual-api-key-here` with your real API key from Step 1.

## Step 4: Verify Configuration

Check that your `.env` file now has:

```bash
# GitHub Configuration
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_TOKEN=ghp_your_token

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your_secret

# AI Configuration (NEW)
ANTHROPIC_API_KEY=sk-ant-your-key

# Application Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## Step 5: Test AI Integration

Run the test script to verify everything works:

```bash
python test_ai_integration.py
```

**Expected Output:**
```
Testing AI-powered PR analysis...
------------------------------------------------------------

✅ AI Analysis Successful!

📝 Functional Summary:
Implements JWT-based authentication with refresh tokens...

🎯 Scope of Change:
Backend API, authentication system, database models

💡 Key Changes:
  • JWT token generation and validation logic
  • Authentication middleware for route protection
  ...

⚠️ Risk Assessment:
Low risk - well-tested authentication implementation

🔍 Review Focus Areas:
  • Token expiration and refresh logic
  • Password hashing security
  ...

------------------------------------------------------------
✅ Test completed successfully!
```

## Step 6: Restart the Application

```bash
# Stop the running application (Ctrl+C)

# Start it again
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 7: Test with Real PR

1. Create a test pull request in your GitHub repository
2. Check your Slack channel for the notification
3. Verify it includes AI-generated insights:
   - Functional summary
   - Scope of change
   - Key changes
   - Risk assessment
   - Review focus areas

## What You'll See in Slack

Before (without AI):
```
📋 Pull Request: Add authentication

Summary: No description provided

📁 5 files | ➕ 282 additions | ➖ 17 deletions
```

After (with AI):
```
📋 Pull Request: Add authentication

Summary: Implements JWT-based authentication with refresh tokens
and secure session management

📁 5 files | ➕ 282 additions | ➖ 17 deletions | ⏱ Medium (~15 min)

🎯 Scope: Backend API, authentication system, database models
💡 Key Changes:
  • JWT token generation and validation logic
  • Authentication middleware for route protection
  • User model with bcrypt password hashing

✅ Risk: Low risk - well-tested implementation
🔍 Review Focus:
  • Token expiration handling
  • Password security
  • Test coverage
```

## Troubleshooting

### Error: "anthropic_api_key field required"

**Solution:** Make sure you added `ANTHROPIC_API_KEY` to your `.env` file and restarted the app.

### Error: "Invalid API key"

**Solution:**
1. Check your API key is correct and starts with `sk-ant-`
2. Ensure there are no extra spaces or quotes in `.env`
3. Verify your Anthropic account is active

### AI Analysis Not Showing

**Solution:**
1. Check application logs for errors
2. Verify the AI service is imported: `from app.services.ai_service import ai_service`
3. The bot includes fallback - check if basic summary appears instead

### Slow Response Times

**Normal:** AI analysis adds 2-4 seconds to PR notifications
**If slower:** Check your internet connection to Anthropic API

## Cost Monitoring

Monitor your Anthropic API usage:
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Go to **Usage** section
3. Review API calls and costs

**Typical costs:**
- ~$0.01 per PR analysis
- ~$10/month for 1,000 PRs
- ~$100/month for 10,000 PRs

## Advanced Configuration

### Customize AI Analysis

Edit `app/services/ai_service.py` to modify:

**Change AI model:**
```python
self.model = "claude-3-5-sonnet-20241022"  # Latest model
# or
self.model = "claude-3-haiku-20240307"     # Faster, cheaper
```

**Adjust temperature:**
```python
temperature=0.3  # More focused (default)
temperature=0.7  # More creative
```

**Modify token limits:**
```python
max_tokens=1500  # Current default
max_tokens=2000  # Longer summaries
max_tokens=1000  # Shorter, cheaper
```

### Disable AI for Specific PRs

The system automatically falls back to basic summaries if:
- AI analysis fails
- API key is invalid
- Network issues occur

No manual intervention needed - reviews continue uninterrupted.

## Security Best Practices

1. **Never commit `.env` file** to Git
2. **Rotate API keys** periodically (every 90 days)
3. **Monitor API usage** for unexpected spikes
4. **Use environment-specific keys** (dev vs prod)
5. **Set up billing alerts** in Anthropic Console

## Support

If you encounter issues:

1. Check application logs: `tail -f logs/app.log`
2. Test AI service independently: `python test_ai_integration.py`
3. Review [Anthropic Documentation](https://docs.anthropic.com/)
4. Check GitHub Issues for known problems

## Next Steps

Now that AI analysis is working:

1. ✅ Test with various PR types (bugfix, feature, refactor)
2. ✅ Train your team on new AI insights
3. ✅ Monitor review velocity improvements
4. ✅ Collect feedback on AI accuracy
5. ✅ Consider custom review templates based on AI analysis

---

**Congratulations!** Your Code Review Slack Bot is now powered by AI. 🎉
