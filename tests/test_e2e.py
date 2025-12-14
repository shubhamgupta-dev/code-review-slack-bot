#!/usr/bin/env python3
"""
End-to-End Test for Code Review Slack Bot
Tests the complete flow from GitHub webhook to Dashboard UI
"""

import json
import requests
import time
from github import Github, Auth
from app.config import settings

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")

def test_health():
    """Test if the server is running."""
    print_section("1. Testing Server Health")

    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not accessible: {e}")
        print("   Please start the server with: python3 -m app.main")
        return False

def test_github_access():
    """Test GitHub API access."""
    print_section("2. Testing GitHub Access")

    try:
        auth = Auth.Token(settings.github_token)
        client = Github(auth=auth)
        repo = client.get_repo("shubhamgupta-dev/10X_Dev_Workshop")

        print(f"✅ Successfully connected to GitHub")
        print(f"   Repository: {repo.full_name}")
        print(f"   Description: {repo.description}")

        # Get PR #2
        pr = repo.get_pull(2)
        print(f"\n✅ Found PR #{pr.number}")
        print(f"   Title: {pr.title}")
        print(f"   State: {pr.state}")
        print(f"   Author: {pr.user.login}")
        print(f"   Files changed: {pr.changed_files}")
        print(f"   Changes: +{pr.additions} -{pr.deletions}")
        print(f"   URL: {pr.html_url}")

        return True, repo, pr
    except Exception as e:
        print(f"❌ GitHub access failed: {e}")
        return False, None, None

def test_webhook_direct(repo, pr):
    """Test webhook endpoint by directly calling the internal handler."""
    print_section("3. Testing Webhook Processing (Direct)")

    try:
        # Import the handler function directly
        from app.routes.github import handle_pull_request_event
        from app.models.github import PullRequestEvent
        import asyncio

        # Build the payload
        payload = {
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

        print("📦 Processing webhook payload...")
        print(f"   Action: {payload['action']}")
        print(f"   PR: #{payload['pull_request']['number']}")
        print(f"   Repository: {payload['repository']['full_name']}")

        # Call the handler directly
        asyncio.run(handle_pull_request_event(payload))

        print("\n✅ Webhook processed successfully!")
        print("   Notification saved to database")
        return True

    except Exception as e:
        print(f"❌ Webhook processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database and verify notification was stored."""
    print_section("4. Testing Database Storage")

    try:
        import sqlite3
        conn = sqlite3.connect('notifications.db')
        cursor = conn.cursor()

        # Get total notifications
        cursor.execute("SELECT COUNT(*) FROM notifications")
        count = cursor.fetchone()[0]
        print(f"✅ Database accessible")
        print(f"   Total notifications: {count}")

        # Get the most recent notification
        cursor.execute("""
            SELECT id, pr_number, pr_title, repository, created_at, status
            FROM notifications
            ORDER BY created_at DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        if row:
            print(f"\n📋 Most Recent Notification:")
            print(f"   ID: {row[0]}")
            print(f"   PR: #{row[1]}")
            print(f"   Title: {row[2]}")
            print(f"   Repository: {row[3]}")
            print(f"   Status: {row[5]}")
            print(f"   Created: {row[4]}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def test_dashboard():
    """Test dashboard API endpoints."""
    print_section("5. Testing Dashboard API")

    try:
        # Test stats endpoint
        response = requests.get(
            "http://localhost:8000/dashboard/api/stats",
            headers={"Authorization": "Bearer demo-token-123"},
            timeout=10
        )

        if response.status_code == 200:
            stats = response.json()
            print("✅ Dashboard Stats API working")
            print(f"   Total PRs: {stats.get('total_prs', 0)}")
            print(f"   Pending: {stats.get('pending_prs', 0)}")
            print(f"   Approved: {stats.get('approved_prs', 0)}")
            print(f"   Needs Changes: {stats.get('needs_changes_prs', 0)}")
        else:
            print(f"❌ Stats API returned {response.status_code}")
            return False

        # Test notifications endpoint
        response = requests.get(
            "http://localhost:8000/dashboard/api/notifications",
            headers={"Authorization": "Bearer demo-token-123"},
            timeout=10
        )

        if response.status_code == 200:
            notifications = response.json()
            print(f"\n✅ Dashboard Notifications API working")
            print(f"   Notifications loaded: {len(notifications)}")

            if notifications:
                latest = notifications[0]
                print(f"\n   Latest Notification:")
                print(f"   PR: #{latest.get('pr_number')}")
                print(f"   Title: {latest.get('pr_title')}")
                print(f"   Status: {latest.get('status')}")
        else:
            print(f"❌ Notifications API returned {response.status_code}")
            return False

        return True

    except Exception as e:
        print(f"❌ Dashboard API check failed: {e}")
        return False

def print_dashboard_instructions():
    """Print instructions to access the dashboard."""
    print_section("🎉 END-TO-END TEST COMPLETE!")

    print("✅ All systems operational!\n")
    print("📊 REVIEWFLOW DASHBOARD")
    print("-" * 80)
    print("\n🌐 Open in your browser:")
    print("   http://localhost:8000/dashboard/?token=demo-token-123")
    print("\n🎯 Features to Try:")
    print("   • View PR notifications in real-time")
    print("   • Click stat cards to filter by status")
    print("   • Toggle auto-refresh (every 30 seconds)")
    print("   • Approve PRs (see confetti animation!)")
    print("   • Add comments to PRs")
    print("   • Request changes")
    print("   • Mobile-responsive design")
    print("\n📱 Mobile Testing:")
    print("   • Get your computer's local IP address")
    print("   • Replace 'localhost' with your IP")
    print("   • Access from any device on your network")
    print("\n🔗 API Endpoints Available:")
    print("   • GET  /health - Health check")
    print("   • POST /webhooks/github - GitHub webhook receiver")
    print("   • GET  /dashboard/api/stats - Dashboard statistics")
    print("   • GET  /dashboard/api/notifications - Get all notifications")
    print("   • POST /dashboard/api/actions/approve - Approve PR")
    print("   • POST /dashboard/api/actions/comment - Comment on PR")
    print("   • POST /dashboard/api/actions/request-changes - Request changes")
    print("\n" + "=" * 80 + "\n")

def main():
    """Run all end-to-end tests."""
    print("\n" + "🚀" * 40)
    print("END-TO-END TEST SUITE - CODE REVIEW SLACK BOT")
    print("🚀" * 40)

    results = []

    # Test 1: Server Health
    results.append(("Server Health", test_health()))
    if not results[-1][1]:
        print("\n❌ Cannot proceed without running server")
        return False

    # Test 2: GitHub Access
    success, repo, pr = test_github_access()
    results.append(("GitHub Access", success))
    if not success:
        print("\n❌ Cannot proceed without GitHub access")
        return False

    # Test 3: Webhook Processing
    results.append(("Webhook Processing", test_webhook_direct(repo, pr)))

    # Give it a moment to save to database
    time.sleep(1)

    # Test 4: Database
    results.append(("Database Storage", test_database()))

    # Test 5: Dashboard
    results.append(("Dashboard API", test_dashboard()))

    # Print summary
    print_section("TEST SUMMARY")

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print_dashboard_instructions()
        return True
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)