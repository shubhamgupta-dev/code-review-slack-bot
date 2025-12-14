"""
Test script to simulate the complete PR notification flow.
This bypasses webhooks and directly tests the PR analysis and notification logic.
"""
import asyncio
import sys
from unittest.mock import patch, MagicMock
from app.services.pr_summary_service import generate_pr_summary
from app.models.github import PullRequestEvent, PullRequest, Repository, User


async def test_pr_notification_flow():
    """Simulate a PR being opened and test the full notification flow."""

    print("=" * 80)
    print("TESTING PR NOTIFICATION FLOW")
    print("=" * 80)
    print()

    # Create a realistic PR event payload
    mock_pr_event = {
        "action": "opened",
        "pull_request": {
            "number": 123,
            "title": "Add user authentication module",
            "body": "Implements JWT-based authentication with refresh tokens and session management",
            "state": "open",
            "html_url": "https://github.com/test-org/test-repo/pull/123",
            "user": {
                "login": "john-doe",
                "avatar_url": "https://avatars.githubusercontent.com/u/123456",
                "html_url": "https://github.com/john-doe"
            },
            "head": {
                "ref": "feature/auth-module",
                "sha": "abc123def456"
            },
            "base": {
                "ref": "main",
                "sha": "def456abc789"
            },
            "additions": 282,
            "deletions": 17,
            "changed_files": 5,
            "commits": 5,
            "requested_reviewers": [
                {
                    "login": "jane-reviewer",
                    "avatar_url": "https://avatars.githubusercontent.com/u/789012",
                    "html_url": "https://github.com/jane-reviewer"
                }
            ]
        },
        "repository": {
            "name": "code-review-slack-bot",
            "full_name": "test-org/code-review-slack-bot",
            "html_url": "https://github.com/test-org/code-review-slack-bot",
            "owner": {
                "login": "test-org",
                "avatar_url": "https://avatars.githubusercontent.com/u/111222",
                "html_url": "https://github.com/test-org"
            }
        },
        "sender": {
            "login": "john-doe",
            "avatar_url": "https://avatars.githubusercontent.com/u/123456",
            "html_url": "https://github.com/john-doe"
        }
    }

    print("📋 Simulating PR Event:")
    print(f"   Repository: {mock_pr_event['repository']['full_name']}")
    print(f"   PR #{mock_pr_event['pull_request']['number']}: {mock_pr_event['pull_request']['title']}")
    print(f"   Author: {mock_pr_event['pull_request']['user']['login']}")
    print(f"   Branch: {mock_pr_event['pull_request']['head']['ref']} → {mock_pr_event['pull_request']['base']['ref']}")
    print(f"   Changes: +{mock_pr_event['pull_request']['additions']} -{mock_pr_event['pull_request']['deletions']} across {mock_pr_event['pull_request']['changed_files']} files")
    print()

    try:
        # Parse the event
        print("🔄 Step 1: Parsing PR event...")
        event = PullRequestEvent(**mock_pr_event)
        print("   ✅ Event parsed successfully")
        print()

        # Mock GitHub service responses (to avoid needing real API token)
        mock_diff_summary = {
            "total_files": 5,
            "total_additions": 282,
            "total_deletions": 17,
            "file_types": {
                "py": {"count": 4, "additions": 250, "deletions": 15},
                "txt": {"count": 1, "additions": 32, "deletions": 2}
            },
            "files": [
                {"filename": "src/auth/jwt.py", "additions": 120, "deletions": 5, "status": "added"},
                {"filename": "src/auth/middleware.py", "additions": 45, "deletions": 10, "status": "modified"},
                {"filename": "src/models/user.py", "additions": 30, "deletions": 2, "status": "modified"},
                {"filename": "tests/test_auth.py", "additions": 85, "deletions": 0, "status": "added"},
                {"filename": "requirements.txt", "additions": 2, "deletions": 0, "status": "modified"},
            ]
        }

        mock_commits = [
            "feat: add JWT token generation and validation",
            "feat: implement authentication middleware",
            "feat: add user model with password hashing",
            "test: add comprehensive auth tests",
            "docs: update authentication documentation"
        ]

        # Generate PR summary with AI analysis (mocking GitHub API calls)
        print("🤖 Step 2: Generating AI-powered PR summary...")
        print("   (This uses the Nerd-Completion gateway with Claude)")

        with patch('app.services.github_service.github_service.get_pr_diff_summary', return_value=mock_diff_summary), \
             patch('app.services.github_service.github_service.get_pr_commits', return_value=mock_commits):
            pr_summary = await generate_pr_summary(event)

        print("   ✅ AI analysis completed")
        print()

        # Display the summary
        print("=" * 80)
        print("📊 PR SUMMARY & AI ANALYSIS")
        print("=" * 80)
        print()

        ai_analysis = pr_summary.get('ai_analysis')

        if ai_analysis:
            print(f"📝 Functional Summary:")
            print(f"   {ai_analysis.get('functional_summary', 'N/A')}")
            print()

            print(f"🎯 Scope of Change:")
            print(f"   {ai_analysis.get('scope_of_change', 'N/A')}")
            print()

            print(f"💡 Key Changes:")
            for change in ai_analysis.get('key_changes', []):
                print(f"   • {change}")
            print()

            print(f"⚠️  Risk Assessment:")
            print(f"   {ai_analysis.get('risk_assessment', 'N/A')}")
            print()

            print(f"🔍 Review Focus Areas:")
            for area in ai_analysis.get('review_focus_areas', []):
                print(f"   • {area}")
            print()
        else:
            print("⚠️  AI analysis was not available")
            print()

        print(f"📈 Statistics:")
        print(f"   Total Files Changed: {pr_summary['files_changed']}")
        print(f"   Total Additions: {pr_summary['additions']}")
        print(f"   Total Deletions: {pr_summary['deletions']}")
        print(f"   Complexity: {pr_summary['complexity']}")
        print()

        print(f"📂 File Types:")
        for file_type, data in pr_summary.get('file_types', {}).items():
            print(f"   {data['count']} {file_type} files (+{data['additions']} -{data['deletions']})")
        print()

        print(f"🔑 Key Files:")
        for file in pr_summary.get('key_files', [])[:5]:
            print(f"   • {file}")
        print()

        # Simulate Slack notification
        print("=" * 80)
        print("📤 SLACK NOTIFICATION (Simulated)")
        print("=" * 80)
        print()
        print("🔔 The following would be sent to Slack:")
        print()
        print(f"   Title: 🔔 New PR #{event.pull_request.number}: {event.pull_request.title}")
        print(f"   Repository: {event.repository.full_name}")
        print(f"   Author: {event.pull_request.user.login}")
        print(f"   Branch: {event.pull_request.head['ref']} → {event.pull_request.base['ref']}")
        print(f"   URL: {event.pull_request.html_url}")
        print()
        summary_text = pr_summary.get('summary_text', 'No summary available')
        print(f"   AI Summary: {summary_text[:100]}...")
        print()
        print("   Interactive Actions:")
        print("   [✅ Approve] [💬 Comment] [❌ Request Changes] [🔗 View on GitHub]")
        print()

        print("=" * 80)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("📝 What happens in production:")
        print("   1. GitHub sends webhook when PR is opened")
        print("   2. Server receives webhook and validates signature")
        print("   3. AI analyzes the PR changes using Claude")
        print("   4. Rich notification is sent to Slack with:")
        print("      - PR metadata and statistics")
        print("      - AI-generated summary and insights")
        print("      - Interactive action buttons")
        print("   5. Reviewers can approve/comment directly from Slack")
        print("   6. Actions are sent back to GitHub via API")
        print()

        return True

    except Exception as e:
        print()
        print("=" * 80)
        print("❌ TEST FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_pr_notification_flow())
    sys.exit(0 if success else 1)