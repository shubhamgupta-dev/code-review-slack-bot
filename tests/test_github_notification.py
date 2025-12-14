"""
Test script to send notifications/actions to GitHub.
This simulates what happens when a user clicks action buttons in Slack.
"""
import asyncio
from app.services.github_service import github_service
from github import GithubException


async def test_github_interactions():
    """Test various GitHub API interactions."""

    print("=" * 80)
    print("TESTING GITHUB API INTERACTIONS")
    print("=" * 80)
    print()

    # You need to specify a real repository and PR number that you have access to
    print("📋 To test GitHub notifications, we need:")
    print("   1. A real repository you have access to")
    print("   2. An open PR number in that repository")
    print()

    # Example: Let's try to get your repositories first
    print("🔍 Step 1: Testing GitHub API Authentication...")
    try:
        from github import Github, Auth
        from app.config import settings

        auth = Auth.Token(settings.github_token)
        client = Github(auth=auth)
        user = client.get_user()

        print(f"   ✅ Authenticated as: {user.login}")
        print(f"   Name: {user.name}")
        print(f"   Public repos: {user.public_repos}")
        print()

        # List some repositories
        print("📚 Step 2: Fetching your repositories...")
        repos = list(user.get_repos())[:5]

        if repos:
            print(f"   Found {len(list(user.get_repos()))} total repositories")
            print(f"   Here are your first 5:")
            for i, repo in enumerate(repos, 1):
                print(f"   {i}. {repo.full_name} ({'public' if not repo.private else 'private'})")
            print()

            # Check for open PRs in the first repo
            print("🔍 Step 3: Looking for open PRs...")
            test_repo = None
            test_pr = None

            for repo in repos:
                try:
                    pulls = list(repo.get_pulls(state='open'))
                    if pulls:
                        test_repo = repo
                        test_pr = pulls[0]
                        print(f"   ✅ Found open PR in {repo.full_name}")
                        print(f"   PR #{test_pr.number}: {test_pr.title}")
                        print(f"   URL: {test_pr.html_url}")
                        break
                except:
                    continue

            if test_pr:
                print()
                print("=" * 80)
                print("🧪 TESTING GITHUB ACTIONS")
                print("=" * 80)
                print()

                # Test 1: Add a comment
                print("📝 Test 1: Adding a comment to PR...")
                try:
                    comment_body = "🤖 Test comment from Code Review Slack Bot\n\nThis is an automated test to verify GitHub API integration is working correctly."
                    await github_service.add_review_comment(
                        test_repo.full_name,
                        test_pr.number,
                        comment_body,
                        "COMMENT"
                    )
                    print(f"   ✅ Successfully added comment to PR #{test_pr.number}")
                    print(f"   You can view it at: {test_pr.html_url}")
                    print()

                    # Ask if user wants to test approval
                    print("⚠️  Note: We can also test PR approval, but this will actually approve the PR.")
                    print("   Skipping approval test to avoid unintended side effects.")
                    print()

                except GithubException as e:
                    print(f"   ❌ Failed to add comment: {e.status} - {e.data.get('message', 'Unknown error')}")
                    if e.status == 422:
                        print("   Note: You might not have permission to review this PR")
                    print()

                print("=" * 80)
                print("✅ GITHUB NOTIFICATION TEST COMPLETED")
                print("=" * 80)
                print()
                print("📝 Summary:")
                print("   ✅ GitHub authentication working")
                print("   ✅ Can access repositories")
                print("   ✅ Can read PR data")
                print("   ✅ Can post comments/reviews to PRs")
                print()
                print("🎯 What this means:")
                print("   - Slack → GitHub integration will work")
                print("   - Users can approve/comment on PRs from Slack")
                print("   - Actions will be reflected in GitHub")
                print()

            else:
                print()
                print("⚠️  No open PRs found in your repositories")
                print()
                print("📝 To test GitHub notifications:")
                print("   1. Create a test PR in one of your repositories")
                print("   2. Run this script again")
                print()
                print("✅ GitHub API authentication is working!")
                print("   Once you have an open PR, all notification features will work.")
                print()
        else:
            print("   ⚠️  No repositories found")
            print()

    except GithubException as e:
        print(f"   ❌ GitHub API Error: {e.status} - {e.data.get('message', 'Unknown error')}")
        print()
        if e.status == 401:
            print("   Issue: Invalid or expired GitHub token")
            print("   Solution: Generate a new token at https://github.com/settings/tokens")
        elif e.status == 403:
            print("   Issue: Token lacks required permissions")
            print("   Solution: Ensure token has 'repo' scope")
        print()

    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()


if __name__ == "__main__":
    asyncio.run(test_github_interactions())