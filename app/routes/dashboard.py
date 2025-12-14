"""
Dashboard API endpoints with username/password authentication
"""
import logging
import json
import hashlib
import secrets
from fastapi import APIRouter, HTTPException, Request, Depends, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app import database
from app.services.github_service import github_service
from app.services.email_service import email_service
from app.services.public_url_service import get_public_url, get_login_url
from app.services.websocket_manager import ws_manager
from app.config import settings
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# In-memory session store (use Redis in production)
active_sessions = {}

# In-memory reset tokens (use Redis/database in production)
# Format: {token: {"email": email, "expires": datetime, "used": bool}}
reset_tokens = {}


def create_session_token() -> str:
    """Create a secure session token."""
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    """Hash password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


async def get_current_user(request: Request):
    """Verify user is logged in via session cookie."""
    session_token = request.cookies.get("session_token")

    if not session_token or session_token not in active_sessions:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return active_sessions[session_token]


class LoginRequest(BaseModel):
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str


class ActionRequest(BaseModel):
    comment: str | None = None


@router.get("/current-url-info", response_class=HTMLResponse)
async def show_current_url_info(request: Request):
    """Show current public URL info page (for localhost access)."""
    return templates.TemplateResponse("current_url.html", {
        "request": request
    })


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render login page with public URL for QR code."""
    public_url = get_login_url()

    return templates.TemplateResponse("login.html", {
        "request": request,
        "public_url": public_url
    })


@router.post("/login")
async def login(request: Request, login_data: LoginRequest, response: Response):
    """Handle login request."""
    # Verify credentials
    if (login_data.username == settings.dashboard_username and
        login_data.password == settings.dashboard_password):

        # Create session
        session_token = create_session_token()
        active_sessions[session_token] = {
            "username": login_data.username,
            "logged_in_at": json.dumps({"time": "now"})  # Could use datetime
        }

        # Set secure cookie
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=86400,  # 24 hours
            samesite="lax"
        )

        logger.info(f"✅ User '{login_data.username}' logged in successfully")

        return {
            "status": "success",
            "message": "Login successful",
            "redirect": "/dashboard/"
        }
    else:
        logger.warning(f"❌ Failed login attempt for user '{login_data.username}'")
        raise HTTPException(status_code=401, detail="Invalid username or password")


@router.post("/logout")
async def logout(request: Request, response: Response):
    """Handle logout request."""
    session_token = request.cookies.get("session_token")

    if session_token and session_token in active_sessions:
        username = active_sessions[session_token].get("username", "unknown")
        del active_sessions[session_token]
        logger.info(f"👋 User '{username}' logged out")

    response.delete_cookie("session_token")

    return {
        "status": "success",
        "message": "Logged out successfully",
        "redirect": "/dashboard/login"
    }


@router.post("/forgot-password")
async def forgot_password(forgot_request: ForgotPasswordRequest):
    """Handle forgot password request - send reset email"""

    # Verify email matches admin email
    if forgot_request.email != settings.dashboard_email:
        # Don't reveal if email exists or not (security)
        logger.warning(f"Password reset requested for non-existent email: {forgot_request.email}")
        return {
            "status": "success",
            "message": "If the email exists, a password reset link has been sent."
        }

    try:
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=1)

        # Store token
        reset_tokens[reset_token] = {
            "email": forgot_request.email,
            "expires": expires_at,
            "used": False
        }

        # Build reset URL
        reset_url = f"http://localhost:8000/dashboard/reset-password?token={reset_token}"

        # Send email
        await email_service.send_password_reset_email(
            to_email=forgot_request.email,
            reset_token=reset_token,
            reset_url=reset_url
        )

        logger.info(f"📧 Password reset email sent to {forgot_request.email}")

        return {
            "status": "success",
            "message": "Password reset link has been sent to your email."
        }

    except Exception as e:
        logger.error(f"Error in forgot password: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    """Render password reset page"""

    # Verify token exists and is valid
    if token not in reset_tokens:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "error": "Invalid or expired reset link",
            "token": None
        })

    token_data = reset_tokens[token]

    # Check if expired
    if datetime.now() > token_data["expires"]:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "error": "Reset link has expired",
            "token": None
        })

    # Check if already used
    if token_data["used"]:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "error": "Reset link has already been used",
            "token": None
        })

    return templates.TemplateResponse("reset_password.html", {
        "request": request,
        "token": token,
        "error": None
    })


@router.post("/reset-password")
async def reset_password(reset_request: ResetPasswordRequest):
    """Handle password reset submission"""

    # Verify token
    if reset_request.token not in reset_tokens:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    token_data = reset_tokens[reset_request.token]

    # Check if expired
    if datetime.now() > token_data["expires"]:
        raise HTTPException(status_code=400, detail="Reset token has expired")

    # Check if already used
    if token_data["used"]:
        raise HTTPException(status_code=400, detail="Reset token has already been used")

    # Verify passwords match
    if reset_request.new_password != reset_request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Validate password strength
    if len(reset_request.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # Update password in settings (in production, update database/vault)
    # Note: This won't persist across restarts. In production, update .env or use database
    settings.dashboard_password = reset_request.new_password

    # Mark token as used
    token_data["used"] = True

    logger.info(f"✅ Password reset successfully for {token_data['email']}")

    return {
        "status": "success",
        "message": "Password reset successfully. You can now login with your new password.",
        "redirect": "/dashboard/login"
    }


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Render forgot password page"""
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request, user: dict = Depends(get_current_user)):
    """Render the main dashboard page."""
    stats = await database.get_notification_stats()
    notifications = await database.get_all_notifications(limit=20)

    # Parse AI analysis JSON for each notification
    for notif in notifications:
        if notif.get('ai_analysis'):
            try:
                notif['ai_analysis'] = json.loads(notif['ai_analysis'])
            except:
                notif['ai_analysis'] = {}

    # Get public URL for WebSocket connection
    public_url = get_public_url()
    ws_url = None
    if public_url:
        # Convert https:// to wss:// for WebSocket
        ws_url = public_url.replace("https://", "wss://").replace("http://", "ws://")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "notifications": notifications,
        "ws_url": ws_url
    })


@router.get("/api/notifications")
async def get_notifications(
    status: str | None = None,
    limit: int = 50,
    user: dict = Depends(get_current_user)
):
    """Get all notifications."""
    notifications = await database.get_all_notifications(status_filter=status, limit=limit)

    # Parse AI analysis JSON
    for notif in notifications:
        if notif.get('ai_analysis'):
            try:
                notif['ai_analysis'] = json.loads(notif['ai_analysis'])
            except:
                notif['ai_analysis'] = {}

    return notifications


@router.get("/api/dashboard-data")
async def get_dashboard_data(
    user: dict = Depends(get_current_user)
):
    """Get dashboard data (stats + notifications) for dynamic refresh."""
    stats = await database.get_notification_stats()
    notifications = await database.get_all_notifications(limit=20)

    # Parse AI analysis JSON for each notification
    for notif in notifications:
        if notif.get('ai_analysis'):
            try:
                notif['ai_analysis'] = json.loads(notif['ai_analysis'])
            except:
                notif['ai_analysis'] = {}

    return {
        "stats": stats,
        "notifications": notifications
    }


@router.get("/api/notifications/{notification_id}")
async def get_notification(
    notification_id: int,
    user: dict = Depends(get_current_user)
):
    """Get a single notification by ID."""
    notification = await database.get_notification_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Parse AI analysis JSON
    if notification.get('ai_analysis'):
        try:
            notification['ai_analysis'] = json.loads(notification['ai_analysis'])
        except:
            notification['ai_analysis'] = {}

    return notification


@router.post("/api/notifications/{notification_id}/approve")
async def approve_pr(
    notification_id: int,
    action_request: ActionRequest,
    user: dict = Depends(get_current_user)
):
    """Approve a PR on GitHub."""
    notification = await database.get_notification_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    try:
        # Approve PR on GitHub
        await github_service.approve_pr(
            notification['repository'],
            notification['pr_number'],
            action_request.comment or "Approved via Code Review Dashboard"
        )

        # Update notification status
        await database.update_notification_status(notification_id, "approved")

        # Save user action
        await database.save_user_action(
            notification_id,
            "approve",
            action_request.comment
        )

        logger.info(f"✅ Approved PR #{notification['pr_number']} in {notification['repository']}")

        return {
            "status": "success",
            "message": f"PR #{notification['pr_number']} approved successfully",
            "pr_url": notification['pr_url']
        }

    except Exception as e:
        logger.error(f"Error approving PR: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/notifications/{notification_id}/request-changes")
async def request_changes(
    notification_id: int,
    action_request: ActionRequest,
    user: dict = Depends(get_current_user)
):
    """Request changes on a PR."""
    notification = await database.get_notification_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if not action_request.comment:
        raise HTTPException(status_code=400, detail="Comment is required when requesting changes")

    try:
        # Request changes on GitHub
        await github_service.request_changes(
            notification['repository'],
            notification['pr_number'],
            action_request.comment
        )

        # Update notification status
        await database.update_notification_status(notification_id, "changes_requested")

        # Save user action
        await database.save_user_action(
            notification_id,
            "request_changes",
            action_request.comment
        )

        logger.info(f"❌ Requested changes on PR #{notification['pr_number']} in {notification['repository']}")

        return {
            "status": "success",
            "message": f"Changes requested on PR #{notification['pr_number']}",
            "pr_url": notification['pr_url']
        }

    except Exception as e:
        logger.error(f"Error requesting changes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/notifications/{notification_id}/comment")
async def add_comment(
    notification_id: int,
    action_request: ActionRequest,
    user: dict = Depends(get_current_user)
):
    """Add a comment to a PR."""
    notification = await database.get_notification_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if not action_request.comment:
        raise HTTPException(status_code=400, detail="Comment is required")

    try:
        # Add comment on GitHub
        await github_service.add_review_comment(
            notification['repository'],
            notification['pr_number'],
            action_request.comment,
            "COMMENT"
        )

        # Update notification status
        await database.update_notification_status(notification_id, "commented")

        # Save user action
        await database.save_user_action(
            notification_id,
            "comment",
            action_request.comment
        )

        logger.info(f"💬 Added comment to PR #{notification['pr_number']} in {notification['repository']}")

        return {
            "status": "success",
            "message": f"Comment added to PR #{notification['pr_number']}",
            "pr_url": notification['pr_url']
        }

    except Exception as e:
        logger.error(f"Error adding comment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/notifications/{notification_id}/close")
async def close_pr(
    notification_id: int,
    user: dict = Depends(get_current_user)
):
    """Close a PR on GitHub."""
    notification = await database.get_notification_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    try:
        # Close PR on GitHub
        await github_service.close_pr(
            notification['repository'],
            notification['pr_number']
        )

        # Update notification status
        await database.update_notification_status(notification_id, "closed")

        # Save user action
        await database.save_user_action(
            notification_id,
            "close",
            "Closed via ReviewFlow Dashboard"
        )

        logger.info(f"🔒 Closed PR #{notification['pr_number']} in {notification['repository']}")

        return {
            "status": "success",
            "message": f"PR #{notification['pr_number']} closed successfully",
            "pr_url": notification['pr_url']
        }

    except Exception as e:
        logger.error(f"Error closing PR: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/stats")
async def get_stats(user: dict = Depends(get_current_user)):
    """Get dashboard statistics."""
    return await database.get_notification_stats()


@router.get("/api/notifications/{notification_id}/diff")
async def get_pr_diff(
    notification_id: int,
    user: dict = Depends(get_current_user)
):
    """Get the diff/changes for a PR."""
    notification = await database.get_notification_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    try:
        diff = github_service.get_pr_diff(
            notification['repository'],
            notification['pr_number']
        )

        return {
            "status": "success",
            "pr_number": notification['pr_number'],
            "repository": notification['repository'],
            "files": diff
        }

    except Exception as e:
        logger.error(f"Error fetching diff: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/current-url")
async def get_current_public_url():
    """Get the current public tunnel URL (no auth required for convenience)."""
    import subprocess
    import re

    try:
        # Try to get URL from localhostrun.log
        result = subprocess.run(
            ["grep", "-a", "tunneled with tls termination", "localhostrun.log"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            # Extract the last URL
            matches = re.findall(r'https://[a-z0-9]+\.lhr\.life', result.stdout)
            if matches:
                current_url = matches[-1]
                return {
                    "status": "success",
                    "public_url": current_url,
                    "login_url": f"{current_url}/dashboard/login",
                    "tunnel_type": "localhost.run"
                }

        # If no URL found
        return {
            "status": "no_tunnel",
            "message": "No active public tunnel found",
            "public_url": None
        }

    except Exception as e:
        logger.error(f"Error getting public URL: {e}")
        return {
            "status": "error",
            "message": str(e),
            "public_url": None
        }


@router.get("/api/qr-info")
async def get_qr_info(request: Request, user: dict = Depends(get_current_user)):
    """Get QR code information (local IP URL for mobile access)."""
    import socket

    try:
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        # Fallback to localhost
        local_ip = "localhost"

    # Get the dashboard token from request
    token = request.query_params.get("token", "demo-token-123")

    # Construct the full URL
    dashboard_url = f"http://{local_ip}:8000/dashboard/?token={token}"

    return {
        "status": "success",
        "url": dashboard_url,
        "ip": local_ip,
        "port": 8000
    }


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for live updates"""
    await ws_manager.connect(websocket)

    try:
        # Send initial connection message
        await ws_manager.send_personal_message({
            "type": "connection",
            "status": "connected",
            "message": "Live sync enabled"
        }, websocket)

        # Keep connection alive and handle incoming messages
        while True:
            # Wait for messages from client (ping/pong for keepalive)
            data = await websocket.receive_text()

            # Handle ping
            if data == "ping":
                await ws_manager.send_personal_message({
                    "type": "pong"
                }, websocket)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)


@router.get("/api/notifications/updates")
async def check_for_updates(user: dict = Depends(get_current_user)):
    """Check for new updates - used by WebSocket for live sync"""
    try:
        # Get latest notifications
        notifications = await database.get_all_notifications(limit=20)
        stats = await database.get_notification_stats()

        # Broadcast to all WebSocket clients
        await ws_manager.broadcast({
            "type": "data_update",
            "notifications": notifications,
            "stats": stats
        })

        return {
            "status": "success",
            "count": len(notifications),
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error checking updates: {e}")
        raise HTTPException(status_code=500, detail=str(e))
