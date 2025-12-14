"""
Script to manually trigger the GitHub webhook for testing
"""
import httpx
import json
import hmac
import hashlib
from app.config import settings

def trigger_webhook():
    """Manually trigger the webhook with PR #3 data"""

    # Create a minimal PR event payload
    payload = {
        "action": "opened",
        "number": 3,
        "pull_request": {
            "id": 1234567890,
            "number": 3,
            "title": "✨ Test ReviewFlow Dashboard Integration",
            "body": "Test PR to demonstrate ReviewFlow dashboard",
            "state": "open",
            "html_url": "https://github.com/shubhamgupta-dev/10X_Dev_Workshop/pull/3",
            "user": {
                "login": "shubhamgupta-dev",
                "avatar_url": "https://github.com/shubhamgupta-dev.png"
            },
            "head": {
                "ref": "reviewflow-test-pr",
                "sha": "abc123"
            },
            "base": {
                "ref": "main",
                "sha": "def456"
            },
            "created_at": "2025-12-12T10:00:00Z",
            "updated_at": "2025-12-12T10:00:00Z",
            "additions": 50,
            "deletions": 10,
            "changed_files": 1
        },
        "repository": {
            "id": 123456,
            "name": "10X_Dev_Workshop",
            "full_name": "shubhamgupta-dev/10X_Dev_Workshop",
            "owner": {
                "login": "shubhamgupta-dev"
            },
            "html_url": "https://github.com/shubhamgupta-dev/10X_Dev_Workshop"
        },
        "sender": {
            "login": "shubhamgupta-dev"
        }
    }

    # Convert payload to JSON
    payload_json = json.dumps(payload)
    payload_bytes = payload_json.encode('utf-8')

    # Create signature
    secret = settings.github_webhook_secret.encode('utf-8')
    signature = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

    # Send request to webhook endpoint
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": f"sha256={signature}",
        "X-GitHub-Delivery": "test-delivery-123"
    }

    try:
        response = httpx.post(
            "http://localhost:8000/webhooks/github",
            content=payload_bytes,
            headers=headers,
            timeout=30.0
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("\n✅ Webhook triggered successfully!")
            print("🔗 Check the dashboard: http://localhost:8000/dashboard/?token=demo-token-123")
        else:
            print(f"\n❌ Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Error triggering webhook: {e}")

if __name__ == "__main__":
    trigger_webhook()
