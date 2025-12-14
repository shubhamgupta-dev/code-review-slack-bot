"""
Email service for password reset and notifications
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Handle email sending for password resets"""

    @staticmethod
    async def send_password_reset_email(to_email: str, reset_token: str, reset_url: str):
        """Send password reset email"""

        # Check if SMTP is configured
        if not settings.smtp_username or not settings.smtp_password:
            logger.warning("SMTP not configured. Cannot send password reset email.")
            raise Exception("Email service not configured. Please contact administrator.")

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "ReviewFlow - Password Reset Request"
            message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email or settings.smtp_username}>"
            message["To"] = to_email

            # Plain text version
            text_content = f"""
Hi,

You requested to reset your password for ReviewFlow Dashboard.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

---
ReviewFlow Dashboard
            """

            # HTML version
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .container {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .content {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .logo {{
            font-size: 48px;
            margin-bottom: 20px;
        }}
        .title {{
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #f0f0f0;
            font-size: 14px;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin: 20px 0;
            transition: transform 0.2s;
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 14px;
            color: #856404;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 12px;
            color: #999;
            text-align: center;
        }}
        .link {{
            color: #667eea;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🔐</div>
        <div class="title">Password Reset Request</div>
        <div class="subtitle">ReviewFlow Dashboard</div>

        <div class="content">
            <p>Hi there,</p>

            <p>You requested to reset your password for your ReviewFlow Dashboard account.</p>

            <p>Click the button below to reset your password:</p>

            <a href="{reset_url}" class="button">Reset Password</a>

            <div class="warning">
                ⏰ <strong>This link expires in 1 hour</strong><br>
                For security reasons, password reset links are only valid for 60 minutes.
            </div>

            <p style="margin-top: 30px; font-size: 13px; color: #666;">
                Or copy and paste this link in your browser:<br>
                <span class="link">{reset_url}</span>
            </p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">

            <p style="font-size: 13px; color: #666;">
                If you didn't request this password reset, please ignore this email.
                Your password will remain unchanged.
            </p>
        </div>
    </div>

    <div class="footer">
        <p>This is an automated email from ReviewFlow Dashboard</p>
        <p>Please do not reply to this email</p>
    </div>
</body>
</html>
            """

            # Attach both versions
            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            message.attach(part1)
            message.attach(part2)

            # Send email
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(message)

            logger.info(f"✅ Password reset email sent to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check username/password.")
            raise Exception("Email service authentication failed. Please contact administrator.")
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            raise Exception("Failed to send email. Please contact administrator.")
        except Exception as e:
            logger.error(f"Error sending email: {e}", exc_info=True)
            raise Exception("Failed to send password reset email. Please contact administrator.")


# Create singleton instance
email_service = EmailService()
