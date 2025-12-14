"""
Test script to send a mock GitHub webhook to the running server.
This simulates what happens when a PR is opened on GitHub.
"""
import json
import hmac
import hashlib
import requests
from app.config import settings

# Mock PR webhook payload
webhook_payload = {
    "action": "opened",
    "pull_request": {
        "number": 456,
        "title": "Implement real-time notification system",
        "body": "Adds WebSocket support for real-time push notifications to clients. Includes connection management, message queuing, and reconnection logic.",
        "state": "open",
        "html_url": "https://github.com/test-org/test-repo/pull/456",
        "user": {
            "login": "developer-alice",
            "avatar_url": "https://avatars.githubusercontent.com/u/999888",
            "html_url": "https://github.com/developer-alice"
        },
        "head": {
            "ref": "feature/websocket-notifications",
            "sha": "xyz789abc123"
        },
        "base": {
            "ref": "main",
            "sha": "abc123xyz789"
        },
        "additions": 456,
        "deletions": 89,
        "changed_files": 8,
        "commits": 7,
        "requested_reviewers": [
            {
                "login": "senior-dev-bob",
                "avatar_url": "https://avatars.githubusercontent.com/u/111333",
                "html_url": "https://github.com/senior-dev-bob"
            }
        ]
    },
    "repository": {
        "name": "awesome-app",
        "full_name": "test-org/awesome-app",
        "html_url": "https://github.com/test-org/awesome-app",
        "owner": {
            "login": "test-org",
            "avatar_url": "https://avatars.githubusercontent.com/u/555666",
            "html_url": "https://github.com/test-org"
        }
    },
    "sender": {
        "login": "developer-alice",
        "avatar_url": "https://avatars.githubusercontent.com/u/999888",
        "html_url": "https://github.com/developer-alice"
    }
}


def create_github_signature(payload_body: bytes, secret: str) -> str:
    """Create GitHub webhook signature."""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


def test_webhook():
    """Send test webhook to local server."""
    url = "http://localhost:8000/webhooks/github"

    # Convert payload to JSON bytes
    payload_body = json.dumps(webhook_payload).encode('utf-8')

    # Create signature
    signature = create_github_signature(payload_body, settings.github_webhook_secret)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature,
        "X-GitHub-Delivery": "test-delivery-123"
    }

    print("=" * 80)
    print("TESTING WEBHOOK ENDPOINT")
    print("=" * 80)
    print()
    print(f"📡 Sending webhook to: {url}")
    print(f"📋 Event type: pull_request")
    print(f"🔐 Signature: {signature[:50]}...")
    print()
    print("📦 Payload:")
    print(f"   Repository: {webhook_payload['repository']['full_name']}")
    print(f"   PR #{webhook_payload['pull_request']['number']}: {webhook_payload['pull_request']['title']}")
    print(f"   Author: {webhook_payload['pull_request']['user']['login']}")
    print(f"   Changes: +{webhook_payload['pull_request']['additions']} -{webhook_payload['pull_request']['deletions']} across {webhook_payload['pull_request']['changed_files']} files")
    print()

    try:
        # Send the request
        print("🚀 Sending request...")
        response = requests.post(url, data=payload_body, headers=headers, timeout=30)

        print()
        print("=" * 80)
        print("RESPONSE")
        print("=" * 80)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print()

        if response.status_code == 200:
            print("✅ Webhook processed successfully!")
            print()
            print("📝 What happened:")
            print("   1. ✅ Server received the webhook")
            print("   2. ✅ Signature validation passed")
            print("   3. ✅ PR event was parsed")
            print("   4. ✅ AI analysis was triggered (via Nerd-Completion)")
            print("   5. ⚠️  Slack notification attempted (will fail without real Slack token)")
            print()
            print("💡 To see full Slack integration:")
            print("   - Add real SLACK_BOT_TOKEN to .env")
            print("   - Add real GITHUB_TOKEN to .env (for fetching PR diffs)")
            print("   - The bot will post to Slack with AI-powered summary")
            print()
        else:
            print(f"❌ Webhook failed with status {response.status_code}")
            print()

    except Exception as e:
        print()
        print("❌ Error sending webhook:")
        print(f"   {e}")
        print()


if __name__ == "__main__":
    test_webhook()