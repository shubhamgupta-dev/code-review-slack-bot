# 📧 Email Setup Guide - Password Reset

Complete guide to configure email service for password reset functionality.

---

## 🎯 Overview

ReviewFlow now includes a complete password reset system with:
- ✅ "Forgot Password?" link on login page
- ✅ Email-based password reset
- ✅ Secure token system (1-hour expiration)
- ✅ Beautiful HTML email templates
- ✅ One-time use reset links

---

## ⚙️ Configuration

### **Step 1: Choose Email Provider**

You can use any SMTP email service. Popular options:

#### **Option 1: Gmail (Recommended for Testing)**
- Free and easy to setup
- Requires "App Password" (more secure than regular password)
- SMTP: `smtp.gmail.com` Port: `587`

#### **Option 2: Outlook/Hotmail**
- Free
- SMTP: `smtp-mail.outlook.com` Port: `587`

#### **Option 3: SendGrid**
- Professional email service
- Free tier: 100 emails/day
- Best for production

#### **Option 4: AWS SES**
- Amazon's email service
- Very reliable
- Best for high-volume production

---

## 🔧 Setup Instructions

### **For Gmail:**

#### 1. Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow setup steps

#### 2. Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Name it "ReviewFlow Dashboard"
4. Click "Generate"
5. **Copy the 16-character password** (you won't see it again!)

#### 3. Update `.env` File
```bash
# Email Configuration (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=your.email@gmail.com
SMTP_FROM_NAME=ReviewFlow Dashboard

# Admin email for password reset
DASHBOARD_EMAIL=your.email@gmail.com
```

---

### **For Outlook/Hotmail:**

#### 1. Enable 2-Step Verification
1. Go to https://account.live.com/proofs/manage
2. Enable two-step verification

#### 2. Generate App Password
1. Go to https://account.live.com/proofs/apppassword
2. Create app password
3. Copy the password

#### 3. Update `.env` File
```bash
# Email Configuration (Outlook)
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your.email@outlook.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your.email@outlook.com
SMTP_FROM_NAME=ReviewFlow Dashboard

# Admin email for password reset
DASHBOARD_EMAIL=your.email@outlook.com
```

---

### **For SendGrid:**

#### 1. Sign Up
1. Go to https://sendgrid.com
2. Create free account
3. Verify your email

#### 2. Create API Key
1. Go to Settings → API Keys
2. Click "Create API Key"
3. Give it a name and "Full Access"
4. Copy the API key

#### 3. Configure Domain (Optional but Recommended)
1. Go to Settings → Sender Authentication
2. Authenticate your domain
3. Follow DNS setup instructions

#### 4. Update `.env` File
```bash
# Email Configuration (SendGrid)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=ReviewFlow Dashboard

# Admin email for password reset
DASHBOARD_EMAIL=admin@yourdomain.com
```

---

## 📝 Complete `.env` Configuration

Here's a complete example `.env` file:

```bash
# GitHub Configuration
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_TOKEN=ghp_your-github-token

# AI Service
NERD_COMPLETION_API_KEY=your-api-key
NERD_COMPLETION_BASE_URL=https://api-url.com

# Dashboard Authentication
DASHBOARD_ACCESS_TOKEN=demo-token-123
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your-secure-password
DASHBOARD_EMAIL=admin@yourdomain.com
SESSION_SECRET_KEY=your-random-secret-key-here

# Email Configuration for Password Reset
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-app-password-here
SMTP_FROM_EMAIL=your.email@gmail.com
SMTP_FROM_NAME=ReviewFlow Dashboard

# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 🧪 Testing the Email Setup

### **Test 1: From CLI (Quick Test)**

Create a test script `utils/test_email.py`:

```python
import asyncio
from app.services.email_service import email_service
from app.config import settings

async def test_email():
    try:
        await email_service.send_password_reset_email(
            to_email=settings.dashboard_email,
            reset_token="test-token-123",
            reset_url="http://localhost:8000/dashboard/reset-password?token=test-token-123"
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_email())
```

Run it:
```bash
python3 utils/test_email.py
```

### **Test 2: From Web Interface**

1. Start the server:
   ```bash
   ./start.sh
   ```

2. Go to: `http://localhost:8000/dashboard/login`

3. Click "Forgot Password?"

4. Enter your email address (must match `DASHBOARD_EMAIL` in `.env`)

5. Click "Send Reset Link"

6. Check your email (including spam folder)

7. Click the reset link in the email

8. Enter new password

9. Login with new password

---

## 🔍 Troubleshooting

### **Error: "SMTP authentication failed"**

**Cause:** Wrong username or password

**Solution:**
- Double-check `SMTP_USERNAME` and `SMTP_PASSWORD`
- For Gmail, make sure you're using App Password, not regular password
- Verify 2-step verification is enabled

---

### **Error: "Email service not configured"**

**Cause:** SMTP settings are empty

**Solution:**
- Make sure all SMTP fields are filled in `.env`
- Restart the server after updating `.env`
- Check there are no extra spaces in values

---

### **Email not received**

**Possible causes:**
1. Check spam/junk folder
2. Verify `DASHBOARD_EMAIL` matches the email you entered
3. Check email service logs for errors
4. Verify email provider allows SMTP access

**Solution:**
- Check server logs: `tail -f server.log`
- Try test email script
- Verify SMTP credentials are correct

---

### **Error: "Connection refused"**

**Cause:** Firewall or wrong SMTP host/port

**Solution:**
- Verify `SMTP_HOST` and `SMTP_PORT` are correct
- Check firewall isn't blocking outgoing SMTP
- Try telnet test: `telnet smtp.gmail.com 587`

---

### **Gmail "Less secure app access" error**

**This is outdated!**

Gmail no longer supports "less secure apps". You MUST use App Passwords.

**Solution:**
- Enable 2-step verification
- Generate App Password
- Use App Password in `.env`

---

## 🔒 Security Best Practices

### **1. Use App Passwords**
Never use your real email password. Always use app-specific passwords.

### **2. Keep `.env` Secret**
Never commit `.env` to git. It's already in `.gitignore`.

### **3. Use Strong Passwords**
For production, use strong random passwords:
```bash
# Generate random password
openssl rand -base64 32
```

### **4. Production Considerations**
- Use dedicated email service (SendGrid, SES)
- Set up SPF, DKIM, DMARC records
- Use your own domain email
- Monitor email deliverability
- Set up email rate limiting

---

## 📧 Email Flow Diagram

```
User Forgets Password
         ↓
Clicks "Forgot Password?"
         ↓
Enters Email Address
         ↓
Server Generates Token
         ↓
Server Sends Email (SMTP)
         ↓
User Receives Email
         ↓
User Clicks Reset Link
         ↓
Token Validated (1-hour expiry)
         ↓
User Enters New Password
         ↓
Password Updated
         ↓
User Redirected to Login
         ↓
Login with New Password ✅
```

---

## 🎨 Email Template Preview

The password reset email includes:
- ✅ Professional HTML design
- ✅ Gradient purple header
- ✅ Large "Reset Password" button
- ✅ Security warning (1-hour expiry)
- ✅ Plain text fallback
- ✅ Mobile responsive

**Preview:**
```
┌──────────────────────────────┐
│  🔐 Password Reset Request   │
│    ReviewFlow Dashboard       │
├──────────────────────────────┤
│                              │
│  Hi there,                   │
│                              │
│  You requested to reset your │
│  password...                 │
│                              │
│  [Reset Password Button]     │
│                              │
│  ⏰ Link expires in 1 hour   │
│                              │
└──────────────────────────────┘
```

---

## 💡 Quick Start Commands

```bash
# 1. Copy example env
cp .env.example .env

# 2. Edit .env and add email settings
nano .env

# 3. Test email (optional)
python3 utils/test_email.py

# 4. Start server
./start.sh

# 5. Test forgot password flow
# Go to: http://localhost:8000/dashboard/login
# Click: "Forgot Password?"
```

---

## 🎯 Production Checklist

Before going to production:

- [ ] Set up dedicated email service (SendGrid/SES)
- [ ] Use your own domain email
- [ ] Configure SPF/DKIM/DMARC
- [ ] Change default admin password
- [ ] Update `DASHBOARD_EMAIL` to real admin email
- [ ] Set strong `SESSION_SECRET_KEY`
- [ ] Test email deliverability
- [ ] Monitor email bounce rates
- [ ] Set up email rate limiting
- [ ] Use database for tokens (not in-memory)

---

## 📚 Additional Resources

- **Gmail App Passwords:** https://support.google.com/accounts/answer/185833
- **Outlook App Passwords:** https://support.microsoft.com/account-billing
- **SendGrid Docs:** https://docs.sendgrid.com
- **AWS SES Docs:** https://docs.aws.amazon.com/ses/

---

**Last Updated:** 2025-12-12
**Feature Version:** 2.0.0
