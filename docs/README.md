# Code Review Slack Bot

An intelligent, bidirectional integration between GitHub and Slack that leverages AI-powered Natural Language Processing to accelerate the Code Review Lifecycle and enhance developer velocity.

## Problem Statement

This initiative addresses the critical bottleneck in software development: context-switching during code reviews. Traditional workflows force reviewers to navigate between GitHub, Slack, and other tools, particularly challenging for mobile reviews. This friction significantly increases review latency, delays merge cycles, and reduces developer velocity, especially in distributed teams across time zones.

## Solution

This bot establishes an intelligent, bidirectional integration featuring:
- **AI-Powered NLP Analysis**: Utilizes Claude AI to perform contextual summarization of PR code diffs and commit history, distilling key functional changes and scope
- **Rich Slack Integration**: Structured messaging via Slack Blocks with real-time notifications and deep-linking
- **Interactive Messaging**: Slack Actions mapped to secure endpoints interfacing with GitHub REST API
- **Ubiquitous Access**: Enable PR approvals and feedback submission directly from mobile or desktop Slack clients
- **Reduced Context-Switching**: Comprehensive PR insights without leaving Slack

## Features

### 1. AI-Powered PR Analysis
When a new PR is opened or review is requested, the system performs intelligent NLP analysis:
- **Functional Summary**: AI-generated plain-English explanation of what the PR does
- **Scope Detection**: Automatic identification of affected system components (frontend, backend, API, etc.)
- **Key Changes**: Distilled list of the most important functional changes
- **Risk Assessment**: AI-powered identification of potential risks, breaking changes, or areas of concern
- **Review Focus Areas**: Intelligent recommendations on where reviewers should concentrate their attention
- **Commit History Analysis**: Contextual understanding based on commit messages and change patterns
- **Complexity Estimation**: Smart review time estimates based on change magnitude

### 2. Structured Slack Notifications
Real-time PR notifications with:
- PR metadata (title, author, branch, repository)
- File changes breakdown (additions/deletions/file types)
- AI-generated functional summary
- Key files changed
- Complexity and time estimates
- Direct GitHub deep-links

### 3. Interactive Review Actions
Review PRs without leaving Slack using Slack Actions:
- ✅ **Approve**: One-click PR approval mapped to GitHub API
- 💬 **Comment**: Add review comments via interactive modals
- ❌ **Request Changes**: Request changes with inline feedback
- 🔗 **View on GitHub**: Quick link for detailed review

### 4. Bidirectional Integration
- **GitHub → Slack**: Webhook-triggered notifications with AI analysis
- **Slack → GitHub**: Action buttons interface with GitHub REST API for PR operations
- **Review Notifications**: Get notified when someone reviews your PR

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **AI/NLP**: Anthropic Claude 3.5 Sonnet for intelligent code analysis
- **GitHub Integration**: PyGithub for GitHub REST API
- **Slack Integration**: Slack SDK for Python with Blocks API
- **Webhook Processing**: GitHub Webhooks for event-driven architecture
- **Async Support**: HTTPX for async HTTP requests

## Prerequisites

- Python 3.11 or higher
- GitHub account with admin access to your repository
- Slack workspace with permission to create apps

## Setup Instructions

### 1. Clone the Repository

```bash
cd ~/Desktop/code-review-slack-bot
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with Poetry:
```bash
poetry install
```

### 4. Configure GitHub

#### Create GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (Full control of private repositories)
   - `write:discussion` (Read and write team discussions)
4. Copy the token

#### Set Up GitHub Webhook
1. Go to your repository → Settings → Webhooks → Add webhook
2. Set Payload URL: `https://your-domain.com/webhooks/github`
3. Content type: `application/json`
4. Secret: Create a random secret (save for later)
5. Events: Select individual events:
   - Pull requests
   - Pull request reviews
   - Pull request review comments
6. Save webhook

### 5. Configure Slack

#### Create Slack App
1. Go to [Slack API](https://api.slack.com/apps) → Create New App → From scratch
2. Name your app (e.g., "Code Review Bot")
3. Select your workspace

#### Configure OAuth & Permissions
Add these Bot Token Scopes:
- `chat:write` - Post messages
- `chat:write.public` - Post to public channels
- `channels:read` - View basic channel info
- `im:write` - Start direct messages

#### Configure Interactivity
1. Turn on Interactivity
2. Request URL: `https://your-domain.com/slack/interactions`
3. Save changes

#### Install App to Workspace
1. Install App to Workspace
2. Copy the Bot User OAuth Token (starts with `xoxb-`)
3. Copy the Signing Secret from Basic Information

### 6. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
# GitHub Configuration
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
GITHUB_TOKEN=ghp_your_personal_access_token_here

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your_slack_signing_secret_here

# AI Configuration (Required for NLP-based PR analysis)
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Application Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**Note**: Get your Anthropic API key from [Anthropic Console](https://console.anthropic.com/)

### 7. Run the Application

#### Development Mode
```bash
python -m app.main
```

Or with Poetry:
```bash
poetry run python -m app.main
```

Or with Uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. Expose Local Server (for development)

Use ngrok or similar to expose your local server:
```bash
ngrok http 8000
```

Update your GitHub webhook URL and Slack interactivity URL with the ngrok URL.

## Project Structure

```
code-review-slack-bot/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── github.py              # GitHub event models
│   │   └── slack.py               # Slack interaction models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── github.py              # GitHub webhook endpoints
│   │   ├── slack.py               # Slack interaction endpoints
│   │   └── health.py              # Health check endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py          # AI/NLP analysis with Claude
│   │   ├── github_service.py      # GitHub API integration
│   │   ├── slack_service.py       # Slack API integration
│   │   └── pr_summary_service.py  # PR summary orchestration
│   └── utils/
│       ├── __init__.py
│       └── github_signature.py    # Webhook signature verification
├── tests/
│   ├── __init__.py
│   └── test_health.py
├── test_ai_integration.py         # AI service test script
├── .env.example                   # Example environment variables
├── .gitignore
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Poetry configuration
└── README.md
```

## Usage

### For Developers
1. Create or update a pull request on GitHub
2. The bot automatically posts a summary to your configured Slack channel (`#code-reviews` by default)
3. Review the summary and take action directly from Slack

### For Reviewers
1. Receive PR notification in Slack
2. Review the summary, file changes, and complexity estimate
3. Take action:
   - Click "Approve" to approve the PR
   - Click "Comment" to add review comments
   - Click "Request Changes" to request modifications
   - Click "View on GitHub" for detailed review

### Changing the Default Channel
Edit `app/services/slack_service.py:12`:
```python
self.default_channel = "#your-channel-name"
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /webhooks/github` - GitHub webhook receiver
- `POST /slack/interactions` - Slack interaction handler

## Testing

Health check:
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

## Deployment

### Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t code-review-bot .
docker run -p 8000:8000 --env-file .env code-review-bot
```

### Production Considerations

1. **HTTPS**: Use a reverse proxy (nginx) or cloud service with SSL
2. **Environment Variables**: Use secure secret management
3. **Logging**: Configure structured logging for monitoring
4. **Monitoring**: Set up health checks and alerting
5. **Scaling**: Use multiple workers for high traffic

## Customization

### Modify PR Summary Format
Edit `app/services/pr_summary_service.py` to customize:
- Complexity calculation
- Summary text generation
- File type categorization

### Customize Slack Message Format
Edit `app/services/slack_service.py` to modify:
- Block layout and styling
- Action buttons
- Emoji and formatting

### Add New Actions
1. Add action button in `slack_service.py`
2. Handle action in `routes/slack.py`
3. Implement logic in `services/github_service.py`

## Troubleshooting

### GitHub webhook not triggering
- Verify webhook URL is publicly accessible
- Check webhook secret matches `.env`
- Review GitHub webhook delivery logs

### Slack interactions failing
- Verify signing secret is correct
- Check interactivity URL is publicly accessible
- Review Slack app permissions

### Bot not posting to channel
- Ensure bot is invited to channel: `/invite @your-bot-name`
- Verify `chat:write.public` scope is enabled
- Check bot token is valid

## AI Analysis Features

The bot uses Claude 3.5 Sonnet to provide intelligent insights:

### What Gets Analyzed
- **Code Diffs**: File changes, additions, deletions
- **Commit History**: Commit messages and patterns
- **PR Context**: Title, description, and metadata

### AI Output
- **Functional Summary**: Plain-English explanation of changes
- **Scope of Change**: Affected system components
- **Key Changes**: Most important modifications
- **Risk Assessment**: Potential issues or breaking changes
- **Review Focus**: Where reviewers should concentrate

### Example Slack Message
```
📋 Pull Request: Add user authentication module

Repository: myorg/myapp
Author: johndoe
PR Number: #42
Branch: feature/auth → main

Summary: Implements JWT-based authentication with refresh tokens...

📁 5 files | ➕ 282 additions | ➖ 17 deletions | ⏱ Medium (~15 min review)

🎯 Scope: Backend API, authentication system, database models
💡 Key Changes:
  • JWT token generation and validation logic
  • Authentication middleware for route protection
  • User model with bcrypt password hashing
  • Comprehensive test coverage

✅ Risk: Low risk - well-tested authentication implementation
🔍 Review Focus:
  • Token expiration and refresh logic
  • Password hashing security
  • Test coverage completeness

[Approve] [Comment] [Request Changes] [View on GitHub]
```

## Future Enhancements

- [x] AI-powered PR analysis and suggestions
- [ ] Thread-based discussions for PR reviews
- [ ] Custom review templates
- [ ] Integration with JIRA/Linear for ticket linking
- [ ] Review reminders for pending PRs
- [ ] Analytics dashboard for review metrics
- [ ] Support for GitLab and Bitbucket
- [ ] Code quality scoring based on AI analysis
- [ ] Automated reviewer assignment based on expertise

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
