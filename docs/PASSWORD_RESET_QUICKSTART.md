# Password Reset - Quick Start Guide

Complete password reset system is now implemented and ready to use!

---

## Current Status

- Login page with "Forgot Password?" link
- Forgot password page for requesting reset
- Email-based reset system with secure tokens
- Reset password page for setting new password
- Token validation (1-hour expiry, one-time use)
- Session-based authentication

**Server Configuration:**
- Username: `shubham-dev`
- Password: `yourlaptop`
- Email: `admin@example.com` (configured in .env)
- Session secret: Configured

---

## How to Use (Without Email Configured)

The password reset system is fully functional, but **email sending requires SMTP configuration**. Here's what works now:

### What Works Now:

1. **Login Page** - `http://localhost:8000/dashboard/login`
   - Enter username and password
   - "Forgot Password?" link is visible

2. **Forgot Password Page** - `http://localhost:8000/dashboard/forgot-password`
   - Enter email address
   - System generates secure token
   - Without SMTP: Token is generated but email won't send

3. **Reset Password Page** - `http://localhost:8000/dashboard/reset-password?token=<TOKEN>`
   - Enter new password
   - Validates token (expiry, single-use)
   - Updates password successfully

### Testing Without Email:

You can test the system by manually accessing the reset URL:

```bash
# The system generates tokens like this format:
http://localhost:8000/dashboard/reset-password?token=abc123xyz...

# Token properties:
# - 43 characters long
# - Cryptographically secure
# - 1-hour expiration
# - Single-use only
```

**Note:** Without SMTP configured, the forgot password flow will appear to work (shows success message), but the email won't actually be sent.

---

## How to Enable Email (Production Setup)

To enable actual email sending, configure SMTP in your `.env` file:

### Option 1: Gmail (Recommended for Testing)

```bash
# Dashboard Authentication
DASHBOARD_EMAIL=your.email@gmail.com

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=your.email@gmail.com
SMTP_FROM_NAME=ReviewFlow Dashboard
```

**Steps:**
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update `.env` with the 16-character app password
4. Restart server: `./start.sh`

### Option 2: Outlook/Hotmail

```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your.email@outlook.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your.email@outlook.com
```

### Option 3: SendGrid (Production)

```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

Complete setup instructions: See `docs/EMAIL_SETUP_GUIDE.md`

---

## Testing the System

### Test 1: Token System (No Email Required)

```bash
python3 utils/test_password_reset.py
```

This tests:
- Token generation
- Token validation
- Expiration handling
- Single-use enforcement
- Security (uniqueness)

### Test 2: Email Sending (Requires SMTP)

Create `utils/test_email.py`:

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

Run:
```bash
python3 utils/test_email.py
```

### Test 3: Complete Web Flow

1. Start server:
   ```bash
   ./start.sh
   ```

2. Open browser: `http://localhost:8000/dashboard/login`

3. Click "Forgot Password?"

4. Enter email: `admin@example.com`

5. Click "Send Reset Link"

6. Check your email inbox (and spam folder)

7. Click the reset link in email

8. Enter new password (min 8 characters)

9. Click "Reset Password"

10. Redirected to login page

11. Login with new password

---

## Features Implemented

### Security Features:

- **Secure Token Generation**: Uses `secrets.token_urlsafe(32)` (43 chars)
- **Token Expiration**: 1-hour time limit
- **Single-Use Tokens**: Token invalidated after use
- **Password Validation**: Minimum 8 characters
- **Session-Based Auth**: HttpOnly cookies, 24-hour expiry
- **CSRF Protection**: Session secret key

### UI/UX Features:

- **Modern Design**: Purple gradient theme, smooth animations
- **Responsive**: Works on mobile and desktop
- **Real-Time Validation**: Password matching feedback
- **Loading States**: Spinners during async operations
- **Error Handling**: Clear error messages
- **Success Feedback**: Visual confirmation of actions
- **Auto-Redirect**: After successful password reset

### Email Features:

- **HTML Email Template**: Beautiful gradient design
- **Plain Text Fallback**: For email clients without HTML
- **Professional Branding**: ReviewFlow logo and styling
- **Clear Instructions**: Step-by-step guidance
- **Security Warning**: Expiration time displayed

---

## File Structure

```
app/
├── config.py                      # SMTP and dashboard settings
├── services/
│   └── email_service.py          # Email sending logic
├── routes/
│   └── dashboard.py              # Password reset routes
└── templates/
    ├── login.html                # Login with "Forgot Password?" link
    ├── forgot_password.html      # Request reset page
    └── reset_password.html       # Set new password page

docs/
├── EMAIL_SETUP_GUIDE.md          # Detailed email setup
└── PASSWORD_RESET_QUICKSTART.md  # This file

utils/
└── test_password_reset.py        # Token system tests

.env                               # Configuration (add SMTP here)
```

---

## API Endpoints

### GET /dashboard/login
Returns login page with "Forgot Password?" link

### POST /dashboard/forgot-password
Request password reset email

**Request Body:**
```json
{
  "email": "admin@example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Password reset link has been sent to your email."
}
```

### GET /dashboard/forgot-password
Returns forgot password page

### GET /dashboard/reset-password?token=<TOKEN>
Returns reset password page with token validation

**Query Parameters:**
- `token`: Reset token from email

**Error Cases:**
- Invalid token
- Expired token (>1 hour)
- Already used token

### POST /dashboard/reset-password
Submit new password

**Request Body:**
```json
{
  "token": "abc123...",
  "new_password": "newpassword123",
  "confirm_password": "newpassword123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Password reset successfully.",
  "redirect": "/dashboard/login"
}
```

---

## Current Configuration

Your `.env` file is configured with:

```bash
# Dashboard Authentication
DASHBOARD_USERNAME=shubham-dev
DASHBOARD_PASSWORD=yourlaptop
DASHBOARD_EMAIL=admin@example.com
SESSION_SECRET_KEY=demo-session-secret-change-in-production

# Email Configuration (Empty - Add SMTP credentials)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=ReviewFlow Dashboard
```

**Status:** Email not configured (SMTP fields empty)

**To enable email:** Fill in SMTP credentials and restart server

---

## Troubleshooting

### Issue: "Email service not configured"

**Cause:** SMTP credentials are empty in `.env`

**Solution:**
1. Add SMTP credentials to `.env`
2. Restart server: `./stop.sh && ./start.sh`
3. Test email: `python3 utils/test_email.py`

### Issue: "SMTP authentication failed"

**Cause:** Wrong username or password

**Solution:**
- For Gmail: Use App Password, not regular password
- Verify 2-step verification is enabled
- Check for typos in credentials

### Issue: "Reset token expired"

**Cause:** Token is older than 1 hour

**Solution:**
- Request a new reset link
- Tokens expire for security

### Issue: "Reset token already used"

**Cause:** Token can only be used once

**Solution:**
- Request a new reset link
- Each token is single-use

### Issue: Email not received

**Possible Causes:**
1. Check spam/junk folder
2. Verify email address matches `DASHBOARD_EMAIL`
3. Check SMTP credentials are correct
4. View server logs: `tail -f server.log`

---

## Production Considerations

Before deploying to production:

- [ ] Use professional email service (SendGrid/AWS SES)
- [ ] Set up SPF, DKIM, DMARC records
- [ ] Use your own domain email
- [ ] Change default admin password
- [ ] Generate strong `SESSION_SECRET_KEY`:
  ```bash
  openssl rand -base64 32
  ```
- [ ] Use Redis/database for tokens (not in-memory)
- [ ] Enable HTTPS
- [ ] Monitor email deliverability
- [ ] Set up email rate limiting
- [ ] Store password hashes (not plain text)

---

## Next Steps

1. **If you want email now:**
   - Follow Gmail setup in `docs/EMAIL_SETUP_GUIDE.md`
   - Takes 5 minutes
   - Free for testing

2. **If you'll configure email later:**
   - Password reset system is ready
   - Just needs SMTP credentials
   - Everything else works

3. **Test without email:**
   - Run `python3 utils/test_password_reset.py`
   - Verifies token system works
   - No email required

---

## Quick Commands

```bash
# Test token system
python3 utils/test_password_reset.py

# Test email (requires SMTP config)
python3 utils/test_email.py

# Start server
./start.sh

# View logs
tail -f server.log

# Stop server
./stop.sh

# Check server status
./status.sh
```

---

**Last Updated:** 2025-12-12
**Feature Version:** 2.0.0
**Status:** Fully implemented, email optional
