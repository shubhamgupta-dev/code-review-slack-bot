"""
Test script to fetch the real PR and send it through the webhook flow
"""
import json
import hmac
import hashlib
import requests
from github import Github, Auth
from app.config import settings

def test_real_pr():
    """Fetch real PR data and send through webhook."""

    print("=" * 80)
    print("TESTING REVIEWFLOW WITH REAL PR")
    print("=" * 80)
    print()

    try:
        # Authenticate with GitHub
        auth = Auth.Token(settings.github_token)
        client = Github(auth=auth)

        # Get the repository
        repo = client.get_repo("shubhamgupta-dev/10X_Dev_Workshop")
        print(f"✅ Repository: {repo.full_name}")

        # Get the PR
        pr = repo.get_pull(2)
        print(f"✅ PR #{pr.number}: {pr.title}")
        print(f"   Author: {pr.user.login}")
        print(f"   State: {pr.state}")
        print(f"   URL: {pr.html_url}")
        print()

        # Build webhook payload with real data
        webhook_payload = {
            "action": "opened",
            "pull_request": {
                "number": pr.number,
                "title": pr.title,
                "body": pr.body or "",
                "state": pr.state,
                "html_url": pr.html_url,
                "user": {
                    "login": pr.user.login,
                    "avatar_url": pr.user.avatar_url,
                    "html_url": pr.user.html_url
                },
                "head": {
                    "ref": pr.head.ref,
                    "sha": pr.head.sha
                },
                "base": {
                    "ref": pr.base.ref,
                    "sha": pr.base.sha
                },
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
                "commits": pr.commits,
                "requested_reviewers": []
            },
            "repository": {
                "name": repo.name,
                "full_name": repo.full_name,
                "html_url": repo.html_url,
                "owner": {
                    "login": repo.owner.login,
                    "avatar_url": repo.owner.avatar_url,
                    "html_url": repo.owner.html_url
                }
            },
            "sender": {
                "login": pr.user.login,
                "avatar_url": pr.user.avatar_url,
                "html_url": pr.user.html_url
            }
        }

        print("📦 Webhook Payload:")
        print(f"   PR: #{pr.number}")
        print(f"   Files: {pr.changed_files}")
        print(f"   Changes: +{pr.additions} -{pr.deletions}")
        print()

        # Send to webhook endpoint
        url = "http://localhost:8000/webhooks/github"
        payload_body = json.dumps(webhook_payload).encode('utf-8')

        # Create signature
        signature = hmac.new(
            settings.github_webhook_secret.encode('utf-8'),
            payload_body,
            hashlib.sha256
        ).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": f"sha256={signature}",
            "X-GitHub-Delivery": "test-delivery-real-pr"
        }

        print("🚀 Sending to webhook endpoint...")
        response = requests.post(url, data=payload_body, headers=headers, timeout=60)

        print()
        print("=" * 80)
        print("WEBHOOK RESPONSE")
        print("=" * 80)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()

        if response.status_code == 200:
            print("✅ SUCCESS! Webhook processed")
            print()
            print("=" * 80)
            print("🎉 OPEN REVIEWFLOW DASHBOARD NOW!")
            print("=" * 80)
            print()
            print("🌐 URL: http://localhost:8000/dashboard/?token=demo-token-123")
            print()
            print("You should see:")
            print("  ✅ Real PR #2 in the feed")
            print("  ✅ AI-powered summary")
            print("  ✅ Actual file changes and stats")
            print("  ✅ Interactive action buttons")
            print()
            print("Try these features:")
            print("  🎯 Click stat cards to filter notifications")
            print("  🔄 Toggle auto-refresh")
            print("  ✅ Approve the PR (confetti animation!)")
            print("  💬 Add a comment")
            print("  📱 Open on mobile (use your computer's IP)")
            print()
            print("=" * 80)
            print()
            return True
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            print()
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = test_real_pr()
    sys.exit(0 if success else 1)
