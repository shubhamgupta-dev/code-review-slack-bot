#!/usr/bin/env python3
"""
Test Dashboard Actions - Comment, Approve, Request Changes
"""

import requests
import json

TOKEN = "demo-token-123"
BASE_URL = "http://localhost:8000/dashboard"
NOTIFICATION_ID = 9  # The latest notification

def test_comment():
    """Test adding a comment to a PR."""
    print("\n" + "=" * 80)
    print("Testing: Add Comment")
    print("=" * 80)

    url = f"{BASE_URL}/api/notifications/{NOTIFICATION_ID}/comment?token={TOKEN}"
    payload = {
        "comment": "🎉 End-to-end test successful! Comment action is working perfectly."
    }

    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("✅ Comment added successfully!")
        return True
    else:
        print("❌ Failed to add comment")
        return False

def test_approve():
    """Test approving a PR."""
    print("\n" + "=" * 80)
    print("Testing: Approve PR")
    print("=" * 80)

    url = f"{BASE_URL}/api/notifications/{NOTIFICATION_ID}/approve?token={TOKEN}"
    payload = {
        "comment": "✅ Approved via end-to-end test! ReviewFlow dashboard is working great!"
    }

    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("✅ PR approved successfully!")
        return True
    else:
        print("❌ Failed to approve PR")
        return False

def test_stats_after_actions():
    """Check stats after actions."""
    print("\n" + "=" * 80)
    print("Testing: Stats After Actions")
    print("=" * 80)

    url = f"{BASE_URL}/api/stats?token={TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        stats = response.json()
        print("Dashboard Statistics:")
        print(f"  Total PRs: {stats.get('total', 0)}")
        print(f"  Pending: {stats.get('pending', 0)}")
        print(f"  Approved: {stats.get('approved', 0)}")
        print(f"  Commented: {stats.get('commented', 0)}")
        print(f"  Changes Requested: {stats.get('changes_requested', 0)}")
        print("✅ Stats retrieved successfully!")
        return True
    else:
        print("❌ Failed to get stats")
        return False

def main():
    print("\n" + "🎯" * 40)
    print("DASHBOARD ACTIONS END-TO-END TEST")
    print("🎯" * 40)

    results = []

    # Test comment
    results.append(("Add Comment", test_comment()))

    # Test approve
    results.append(("Approve PR", test_approve()))

    # Check stats
    results.append(("Get Stats", test_stats_after_actions()))

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n" + "=" * 80)
        print("🎉 ALL DASHBOARD ACTIONS WORK!")
        print("=" * 80)
        print("\n🌐 Open the dashboard to see the results:")
        print("   http://localhost:8000/dashboard/?token=demo-token-123")
        print("\n✅ You should see:")
        print("   • PR #2 marked as 'approved'")
        print("   • Comments visible on GitHub")
        print("   • Updated statistics")
        print("=" * 80 + "\n")
        return True
    else:
        print("\n❌ Some tests failed")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)