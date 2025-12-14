"""
Service to get the current public URL from localhost.run tunnel
"""

import re
from pathlib import Path


def get_public_url() -> str | None:
    """
    Get the current public URL from localhost.run log

    Returns:
        Public URL if tunnel is active, None otherwise
    """
    log_file = Path("localhostrun.log")

    if not log_file.exists():
        return None

    try:
        with open(log_file, 'r') as f:
            content = f.read()
            # Look for the URL pattern from localhost.run
            match = re.search(r'(https://[a-z0-9]+\.lhr\.life)', content)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error reading public URL: {e}")
        return None

    return None


def get_login_url() -> str | None:
    """
    Get the login page public URL

    Returns:
        Login URL if tunnel is active, None otherwise
    """
    base_url = get_public_url()
    if base_url:
        return f"{base_url}/dashboard/login"
    return None


def is_tunnel_active() -> bool:
    """
    Check if the public tunnel is currently active

    Returns:
        True if tunnel is active, False otherwise
    """
    return get_public_url() is not None
