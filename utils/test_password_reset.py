#!/usr/bin/env python3
"""
Test script for password reset functionality
Tests the complete password reset flow without actually sending emails
"""

import asyncio
import secrets
from datetime import datetime, timedelta

# Simulate the reset token system from dashboard.py
reset_tokens = {}


def generate_reset_token(email: str) -> str:
    """Generate a password reset token"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=1)

    reset_tokens[token] = {
        "email": email,
        "expires": expires_at,
        "used": False
    }

    return token


def validate_reset_token(token: str) -> tuple[bool, str]:
    """Validate a reset token

    Returns:
        (is_valid, error_message)
    """
    if token not in reset_tokens:
        return False, "Invalid or expired reset token"

    token_data = reset_tokens[token]

    # Check expiration
    if datetime.now() > token_data["expires"]:
        return False, "Reset token has expired"

    # Check if already used
    if token_data["used"]:
        return False, "Reset token has already been used"

    return True, ""


def use_reset_token(token: str) -> bool:
    """Mark a token as used"""
    if token in reset_tokens:
        reset_tokens[token]["used"] = True
        return True
    return False


def test_password_reset_flow():
    """Test the complete password reset flow"""
    print("🧪 Testing Password Reset System\n")

    # Test 1: Generate token
    print("✅ Test 1: Generate reset token")
    email = "admin@example.com"
    token = generate_reset_token(email)
    print(f"   Generated token: {token[:20]}...")
    print(f"   Token length: {len(token)} characters")
    print(f"   Email: {email}\n")

    # Test 2: Validate valid token
    print("✅ Test 2: Validate valid token")
    is_valid, error = validate_reset_token(token)
    assert is_valid, f"Token should be valid: {error}"
    print(f"   Token is valid: {is_valid}\n")

    # Test 3: Validate invalid token
    print("✅ Test 3: Validate invalid token")
    is_valid, error = validate_reset_token("invalid-token-123")
    assert not is_valid, "Invalid token should not be valid"
    print(f"   Expected error: {error}\n")

    # Test 4: Use token
    print("✅ Test 4: Use reset token")
    success = use_reset_token(token)
    assert success, "Token should be marked as used"
    print(f"   Token marked as used: {success}\n")

    # Test 5: Try to use token again
    print("✅ Test 5: Validate already-used token")
    is_valid, error = validate_reset_token(token)
    assert not is_valid, "Used token should not be valid"
    print(f"   Expected error: {error}\n")

    # Test 6: Test expiration
    print("✅ Test 6: Test token expiration")
    expired_token = secrets.token_urlsafe(32)
    reset_tokens[expired_token] = {
        "email": email,
        "expires": datetime.now() - timedelta(hours=1),  # Expired 1 hour ago
        "used": False
    }
    is_valid, error = validate_reset_token(expired_token)
    assert not is_valid, "Expired token should not be valid"
    print(f"   Expected error: {error}\n")

    # Test 7: Token security (uniqueness)
    print("✅ Test 7: Token uniqueness")
    tokens = set()
    for _ in range(100):
        token = secrets.token_urlsafe(32)
        tokens.add(token)
    assert len(tokens) == 100, "All tokens should be unique"
    print(f"   Generated 100 unique tokens\n")

    print("=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\n📋 Summary:")
    print(f"   - Token generation: Working")
    print(f"   - Token validation: Working")
    print(f"   - Token expiration: Working")
    print(f"   - Token single-use: Working")
    print(f"   - Token security: Working (cryptographically secure)")
    print("\n💡 Next steps:")
    print("   1. Configure SMTP credentials in .env")
    print("   2. Test email sending with utils/test_email.py")
    print("   3. Test complete flow in browser:")
    print("      - Go to http://localhost:8000/dashboard/login")
    print("      - Click 'Forgot Password?'")
    print("      - Enter email and request reset")
    print("      - Check email for reset link")
    print("      - Click link and reset password")


if __name__ == "__main__":
    test_password_reset_flow()
