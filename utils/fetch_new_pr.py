"""
Fetch the latest PR from GitHub and add it to the database
"""
from github import Github, Auth
from app.config import settings
from app.models.github import PullRequestEvent
from app.services.pr_summary_service import generate_pr_summary
from app import database
import asyncio
from datetime import datetime

async def fetch_and_add_pr():
    """Fetch latest PR from GitHub and add to database"""

    print("=" * 80)
    print("FETCHING LATEST PR FROM GITHUB")
    print("=" * 80)
    print()

    # Initialize database
    await database.init_db()

    # Authenticate with GitHub
    auth = Auth.Token(settings.github_token)
    client = Github(auth=auth)

    # Get repository
    repo = client.get_repo("shubhamgupta-dev/10X_Dev_Workshop")

    print(f"📦 Repository: {repo.full_name}")
    print()

    # Get the latest PRs (both open and closed)
    print("🔍 Fetching latest PRs (open and recently closed)...")
    prs = list(repo.get_pulls(state='all', sort='created', direction='desc'))[:10]  # Last 10 PRs

    if not prs:
        print("❌ No PRs found")
        return

    # Get PRs already in database
    existing_notifs = await database.get_all_notifications(limit=100)
    existing_pr_numbers = {n['pr_number'] for n in existing_notifs if n['repository'] == repo.full_name}

    print(f"📊 Found {len(prs)} open PR(s)")
    print(f"💾 Already in database: {existing_pr_numbers}")
    print()

    for gh_pr in prs:
        if gh_pr.number in existing_pr_numbers:
            print(f"   ⏭️  PR #{gh_pr.number}: Already in database")
            continue

        print(f"   🆕 PR #{gh_pr.number}: {gh_pr.title}")
        print(f"       Author: {gh_pr.user.login}")
        print(f"       {gh_pr.head.ref} → {gh_pr.base.ref}")
        print(f"       Files: {gh_pr.changed_files}, +{gh_pr.additions}/-{gh_pr.deletions}")
        print()

        # Create a PullRequestEvent object
        event_dict = {
            "action": "opened",
            "number": gh_pr.number,
            "pull_request": {
                "id": gh_pr.id,
                "number": gh_pr.number,
                "title": gh_pr.title,
                "body": gh_pr.body or "",
                "state": gh_pr.state,
                "html_url": gh_pr.html_url,
                "user": {
                    "login": gh_pr.user.login,
                    "avatar_url": gh_pr.user.avatar_url
                },
                "head": {
                    "ref": gh_pr.head.ref,
                    "sha": gh_pr.head.sha
                },
                "base": {
                    "ref": gh_pr.base.ref,
                    "sha": gh_pr.base.sha
                },
                "created_at": gh_pr.created_at.isoformat(),
                "updated_at": gh_pr.updated_at.isoformat(),
                "additions": gh_pr.additions,
                "deletions": gh_pr.deletions,
                "changed_files": gh_pr.changed_files
            },
            "repository": {
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "owner": {
                    "login": repo.owner.login
                },
                "html_url": repo.html_url
            },
            "sender": {
                "login": gh_pr.user.login
            }
        }

        print(f"   🤖 Generating AI summary...")
        event = PullRequestEvent(**event_dict)
        pr_summary = await generate_pr_summary(event)

        print(f"   💾 Saving to database...")
        notification_id = await database.save_notification(event, pr_summary)

        # Update status if PR is closed or merged
        if gh_pr.merged:
            await database.update_notification_status(notification_id, "merged")
            print(f"   🎉 Marked as merged")
        elif gh_pr.state == "closed":
            await database.update_notification_status(notification_id, "closed")
            print(f"   🔒 Marked as closed")

        print(f"   ✅ Notification #{notification_id} saved!")
        print()

    print("=" * 80)
    print("✅ SYNC COMPLETE!")
    print("🔗 View dashboard: http://localhost:8000/dashboard/?token=demo-token-123")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(fetch_and_add_pr())
