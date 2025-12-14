# 🚀 Deployment Guide - ReviewFlow

## Quick Deploy to GitHub

### Step 1: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `reviewflow` (or your preferred name)
3. **Description:** `AI-powered PR review dashboard with real-time sync`
4. **Visibility:** Public or Private (your choice)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. **Click:** "Create repository"

### Step 2: Push to GitHub

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/reviewflow.git

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## 🌐 Deployment Options

### Option 1: Local Development (Current Setup)

**Best for:** Testing, development, small teams

```bash
# Start services
./start.sh

# Access locally
http://localhost:8000/dashboard/login

# Access publicly (with tunnel)
https://[random].lhr.life/dashboard/login
```

**Pros:**
- ✅ Zero cost
- ✅ Quick setup
- ✅ Full control

**Cons:**
- ❌ Must keep laptop running
- ❌ Tunnel URL changes on restart
- ❌ Not suitable for production

---

### Option 2: Heroku (Easiest Cloud Deploy)

**Best for:** Small teams, MVP, quick production

#### Prerequisites:
```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Deploy Steps:

1. **Create Procfile:**
```bash
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
git add Procfile
git commit -m "Add Procfile for Heroku"
```

2. **Create Heroku app:**
```bash
heroku create reviewflow-your-team
```

3. **Add PostgreSQL (recommended for production):**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Set environment variables:**
```bash
heroku config:set GITHUB_TOKEN=ghp_your_token
heroku config:set NERD_COMPLETION_API_KEY=your_api_key
heroku config:set NERD_COMPLETION_BASE_URL=https://api.anthropic.com
heroku config:set DASHBOARD_USERNAME=admin
heroku config:set DASHBOARD_PASSWORD=your_secure_password
heroku config:set ENVIRONMENT=production
```

5. **Deploy:**
```bash
git push heroku main
```

6. **Open app:**
```bash
heroku open
```

**Cost:** $7/month (Eco Dynos) + $5/month (PostgreSQL Mini) = **$12/month**

---

### Option 3: Railway (Modern Alternative)

**Best for:** Modern stack, automatic deployments

#### Deploy Steps:

1. **Go to:** https://railway.app
2. **Click:** "Start a New Project"
3. **Select:** "Deploy from GitHub repo"
4. **Choose:** Your `reviewflow` repository
5. **Railway auto-detects:** Python/FastAPI
6. **Add environment variables** in Railway dashboard
7. **Deploy!**

**Cost:** $5/month (Starter plan)

---

### Option 4: Render (Free Tier Available)

**Best for:** Tight budget, learning

#### Deploy Steps:

1. **Go to:** https://render.com
2. **Click:** "New +" → "Web Service"
3. **Connect GitHub repository**
4. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Add environment variables**
6. **Create Web Service**

**Cost:** Free (with limitations: sleeps after 15 mins inactivity) or $7/month (always on)

---

### Option 5: AWS/GCP/Azure (Enterprise)

**Best for:** Large teams, compliance requirements, enterprise security

#### AWS Deployment (ECS + Fargate):

1. **Containerize:**
```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and push to ECR:**
```bash
docker build -t reviewflow .
aws ecr create-repository --repository-name reviewflow
docker tag reviewflow:latest [ECR_URL]/reviewflow:latest
docker push [ECR_URL]/reviewflow:latest
```

3. **Deploy to ECS Fargate:**
- Create ECS cluster
- Create task definition
- Create service with load balancer
- Configure environment variables

**Cost:** ~$30-50/month (t3.small + load balancer)

---

## 🔧 Production Configuration

### Environment Variables Required:

```bash
# GitHub Integration
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx           # GitHub personal access token
GITHUB_WEBHOOK_SECRET=your_secret        # For webhook validation

# AI Service
NERD_COMPLETION_API_KEY=sk-ant-xxx      # Anthropic API key
NERD_COMPLETION_BASE_URL=https://api.anthropic.com

# Authentication
DASHBOARD_USERNAME=your_username         # Change from default!
DASHBOARD_PASSWORD=strong_password_here  # Use strong password!
DASHBOARD_EMAIL=admin@yourcompany.com    # For password resets

# Email (Optional - for password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production                   # Enables production optimizations
LOG_LEVEL=INFO

# Session Security
SESSION_SECRET_KEY=generate_random_key   # Use: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🗄️ Database Migration (SQLite → PostgreSQL)

### Why Migrate?
- SQLite: Great for development, limited concurrency
- PostgreSQL: Production-ready, handles 100+ concurrent users

### Migration Steps:

1. **Install PostgreSQL adapter:**
```bash
pip install psycopg2-binary
```

2. **Update `app/database.py`:**
```python
# Replace SQLite connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/notifications.db")

# PostgreSQL connection (auto-provided by Heroku/Railway)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
```

3. **Export existing data:**
```bash
sqlite3 data/notifications.db .dump > backup.sql
```

4. **Import to PostgreSQL:**
```bash
# Convert SQLite dump to PostgreSQL format (manual edits needed)
# Then: psql $DATABASE_URL < backup_postgres.sql
```

---

## 🔒 Security Checklist for Production

### Before Going Live:

- [ ] Change default username/password in `.env`
- [ ] Generate secure `SESSION_SECRET_KEY`
- [ ] Enable HTTPS (handled by cloud providers)
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure CORS if needed
- [ ] Set up rate limiting (add `slowapi` package)
- [ ] Enable database backups
- [ ] Configure monitoring/logging (Sentry, Datadog)
- [ ] Review GitHub token permissions (minimal scope needed)
- [ ] Set up SSL for custom domain
- [ ] Configure firewall rules (cloud provider)

---

## 📊 Monitoring & Logging

### Add Application Monitoring:

**Option A: Sentry (Errors)**
```bash
pip install sentry-sdk[fastapi]
```

```python
# app/main.py
import sentry_sdk
sentry_sdk.init(dsn="your_sentry_dsn")
```

**Option B: Datadog (Metrics + Logs)**
```bash
pip install ddtrace
```

**Option C: New Relic (APM)**
```bash
pip install newrelic
```

---

## 🚦 Health Checks

Already configured at `/health` endpoint:

```bash
# Check if app is healthy
curl https://your-app.com/health

# Response:
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 🔄 CI/CD Setup (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/

      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.14
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "reviewflow-your-team"
          heroku_email: "your@email.com"
```

---

## 🌍 Custom Domain Setup

### Add Custom Domain:

**Heroku:**
```bash
heroku domains:add reviews.yourcompany.com
heroku certs:auto:enable
```

**Update DNS (at your domain provider):**
```
Type: CNAME
Name: reviews
Value: [your-heroku-app].herokuapp.com
```

**Railway/Render:** Similar process in their dashboards

---

## 📈 Scaling Considerations

### Horizontal Scaling:

**Heroku:**
```bash
# Scale to 2 dynos
heroku ps:scale web=2
```

**Add Redis for session storage:**
```bash
heroku addons:create heroku-redis:mini
```

Update `app/routes/dashboard.py` to use Redis:
```python
import redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))
```

---

## 🎉 Post-Deployment Checklist

- [ ] Test login at `https://your-app.com/dashboard/login`
- [ ] Verify WebSocket connection (check browser console)
- [ ] Create test PR and verify it appears in dashboard
- [ ] Test approve/comment/close actions
- [ ] Check mobile responsiveness
- [ ] Test from different networks (WiFi, mobile data)
- [ ] Monitor error logs for first 24 hours
- [ ] Share URL with team via Slack/email
- [ ] Add to team's bookmarks/internal wiki
- [ ] Set up monitoring alerts

---

## 📞 Support & Resources

**Documentation:**
- Full setup: `docs/SETUP_GUIDE.md`
- Mobile access: `docs/MOBILE_ACCESS_SOLUTION.md`
- Live sync: `docs/LIVE_SYNC_IMPLEMENTATION.md`

**Troubleshooting:**
- Check logs: `heroku logs --tail` (or cloud provider equivalent)
- Health endpoint: `https://your-app.com/health`
- GitHub issues: Submit issues on your repo

**Community:**
- Built with Claude Code: https://claude.com/claude-code
- FastAPI docs: https://fastapi.tiangolo.com
- Anthropic API: https://docs.anthropic.com

---

## 🚀 Quick Deploy Commands Summary

```bash
# 1. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/reviewflow.git
git push -u origin main

# 2. Deploy to Heroku (easiest)
heroku create reviewflow-your-team
heroku addons:create heroku-postgresql:mini
heroku config:set GITHUB_TOKEN=xxx NERD_COMPLETION_API_KEY=xxx
git push heroku main
heroku open

# 3. Or Railway (one command)
railway login
railway init
railway up

# 4. Or Render (via web UI)
# Just connect GitHub repo at render.com
```

---

**Recommended:** Start with **Heroku** for easiest setup, migrate to **AWS/GCP** when you have 50+ users.

**Cost Estimate:**
- **Free tier:** Render (limited) or localhost
- **Small team:** $12/month (Heroku)
- **Medium team:** $50/month (AWS)
- **Enterprise:** $500+/month (dedicated infrastructure)

---

🎉 **Your ReviewFlow is ready to deploy!**
