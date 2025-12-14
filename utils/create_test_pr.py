"""
Script to create a real test PR in your GitHub repository
"""
from github import Github, Auth
from app.config import settings
import sys

def create_test_pr():
    """Create a test PR in a real repository."""

    print("=" * 80)
    print("CREATING TEST PR FOR REVIEWFLOW")
    print("=" * 80)
    print()

    try:
        # Authenticate
        auth = Auth.Token(settings.github_token)
        client = Github(auth=auth)
        user = client.get_user()

        print(f"✅ Authenticated as: {user.login}")
        print()

        # Get a repository
        repos = list(user.get_repos())
        if not repos:
            print("❌ No repositories found")
            return False

        # Use the first repo
        repo = repos[0]
        print(f"📦 Using repository: {repo.full_name}")
        print()

        # Get the default branch
        default_branch = repo.default_branch
        print(f"🌿 Default branch: {default_branch}")

        # Create a new branch
        branch_name = "reviewflow-test-pr"
        print(f"🌿 Creating branch: {branch_name}")

        try:
            # Get the reference to the default branch
            ref = repo.get_git_ref(f"heads/{default_branch}")
            sha = ref.object.sha

            # Try to delete existing test branch if it exists
            try:
                existing_ref = repo.get_git_ref(f"heads/{branch_name}")
                existing_ref.delete()
                print(f"   🗑️  Deleted existing branch")
            except:
                pass

            # Create new branch
            repo.create_git_ref(f"refs/heads/{branch_name}", sha)
            print(f"   ✅ Branch created")
            print()

        except Exception as e:
            print(f"   ⚠️  Branch may already exist: {e}")
            print()

        # Create a test file
        print("📝 Creating test file...")
        test_content = """# ReviewFlow Test

This is a test file created to demonstrate the ReviewFlow dashboard.

## Features Tested:
- ✅ GitHub Webhook Integration
- ✅ AI-Powered PR Analysis
- ✅ ReviewFlow Dashboard Display
- ✅ Interactive PR Actions (Approve/Comment/Request Changes)

## Test Date
2025-12-12

## About ReviewFlow
ReviewFlow is a smart PR review dashboard that provides:
- Real-time PR notifications
- AI-powered summaries using Claude
- Mobile-friendly interface
- One-click PR approvals
- Interactive filtering and auto-refresh

---

**Status**: Test PR for ReviewFlow
"""

        try:
            # Try to update if file exists
            file_path = "REVIEWFLOW_TEST.md"
            try:
                contents = repo.get_contents(file_path, ref=branch_name)
                repo.update_file(
                    file_path,
                    "Update ReviewFlow test file",
                    test_content,
                    contents.sha,
                    branch=branch_name
                )
                print(f"   ✅ Updated {file_path}")
            except:
                # Create new file
                repo.create_file(
                    file_path,
                    "Add ReviewFlow test file",
                    test_content,
                    branch=branch_name
                )
                print(f"   ✅ Created {file_path}")
            print()

        except Exception as e:
            print(f"   ❌ Error creating file: {e}")
            print()

        # Create pull request
        print("🎯 Creating pull request...")
        try:
            pr = repo.create_pull(
                title="✨ Test ReviewFlow Dashboard Integration",
                body="""## 🎯 Purpose
This is a test PR to demonstrate the ReviewFlow dashboard capabilities.

## 🚀 What's Being Tested

### ✅ GitHub Integration
- Webhook receives PR events
- AI analyzes code changes
- Notifications saved to database

### ✅ ReviewFlow Dashboard
- Real-time PR feed
- AI-powered summaries
- Interactive actions:
  - Approve PR
  - Request changes
  - Add comments
- Mobile-responsive design

### ✅ AI Analysis
- Claude analyzes:
  - Functional summary
  - Key changes
  - Scope of change
  - Risk assessment
  - Review focus areas

## 📱 How to Test

1. Open ReviewFlow: `http://localhost:8000/dashboard/?token=demo-token-123`
2. See this PR appear in the feed
3. Review the AI summary
4. Test action buttons:
   - Click "Approve" to approve
   - Click "Comment" to add a review comment
   - Click "Request Changes" to request modifications

## 🎨 Features to Notice
- 🔔 Notification badge on header
- 📊 Interactive statistics cards
- 🎨 Smooth animations and transitions
- 🎉 Confetti celebration on approval!
- 🔄 Auto-refresh toggle
- 🎯 Filter by status (click stat cards)

## 🤖 AI Analysis
The ReviewFlow dashboard will automatically:
1. Receive this PR via webhook
2. Analyze code changes with Claude AI
3. Generate a comprehensive summary
4. Display interactive review options

---

**Test this PR in ReviewFlow and experience smart PR reviews!** ⚡
""",
                head=branch_name,
                base=default_branch
            )

            print(f"   ✅ Pull request created!")
            print()
            print("=" * 80)
            print("🎉 SUCCESS!")
            print("=" * 80)
            print()
            print(f"📋 PR #{pr.number}: {pr.title}")
            print(f"🔗 URL: {pr.html_url}")
            print(f"📦 Repository: {repo.full_name}")
            print()
            print("🚀 Next Steps:")
            print()
            print("1. The webhook should have been triggered automatically!")
            print("   (If webhook is configured in GitHub repo settings)")
            print()
            print("2. Open ReviewFlow Dashboard:")
            print("   http://localhost:8000/dashboard/?token=demo-token-123")
            print()
            print("3. You should see this PR in the feed with AI analysis!")
            print()
            print("4. Test the interactive features:")
            print("   - Click stat cards to filter")
            print("   - Try approving the PR")
            print("   - Add a comment")
            print("   - Enable auto-refresh")
            print()
            print("5. After testing, you can:")
            print(f"   - Close the PR: gh pr close {pr.number}")
            print(f"   - Delete the branch: git push origin --delete {branch_name}")
            print()
            print("=" * 80)
            print()

            return True

        except Exception as e:
            print(f"   ❌ Error creating PR: {e}")
            print()
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_test_pr()
    sys.exit(0 if success else 1)
