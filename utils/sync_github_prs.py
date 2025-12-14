"""
Script to sync GitHub PR status with the database
"""
from github import Github, Auth
from app.config import settings
from app import database
import asyncio

async def sync_prs():
    """Check GitHub PRs and update database"""

    print("=" * 80)
    print("SYNCING GITHUB PRs WITH DATABASE")
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

    # Get all PRs from GitHub
    print("🔍 Checking GitHub PRs...")
    github_prs = {}

    for pr in repo.get_pulls(state='all'):
        github_prs[pr.number] = {
            'number': pr.number,
            'title': pr.title,
            'state': pr.state,
            'merged': pr.merged,
            'url': pr.html_url
        }
        status = "merged" if pr.merged else pr.state
        print(f"   PR #{pr.number}: {pr.title[:50]}... - {status}")

    print()

    # Get notifications from database
    print("💾 Checking Database Notifications...")
    notifications = await database.get_all_notifications(limit=100)

    updates_made = False

    for notif in notifications:
        pr_num = notif['pr_number']
        notif_repo = notif['repository']

        # Only sync for the same repository
        if notif_repo != repo.full_name:
            continue

        if pr_num in github_prs:
            gh_pr = github_prs[pr_num]
            current_status = notif['status']

            # Determine what the status should be based on GitHub
            if gh_pr['merged']:
                new_status = 'merged'
            elif gh_pr['state'] == 'closed':
                new_status = 'closed'
            elif gh_pr['state'] == 'open':
                # Keep the current review status if it's still open
                if current_status in ['approved', 'changes_requested', 'commented']:
                    new_status = current_status
                else:
                    new_status = 'pending'
            else:
                new_status = current_status

            # Update if status changed
            if new_status != current_status:
                print(f"   ✏️  PR #{pr_num}: {current_status} → {new_status}")
                await database.update_notification_status(notif['id'], new_status)
                updates_made = True
            else:
                print(f"   ✅ PR #{pr_num}: {current_status} (no change)")
        else:
            print(f"   ⚠️  PR #{pr_num}: Not found in GitHub")

    print()

    if updates_made:
        print("✅ Database synced with GitHub!")

        # Trigger WebSocket broadcast for live update
        try:
            import requests
            requests.get("http://localhost:8000/dashboard/api/notifications/updates", timeout=2)
            print("📡 Live sync broadcast sent")
        except:
            pass  # Silently fail if server is not running or auth required
    else:
        print("✅ Database already in sync with GitHub!")

    print()
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(sync_prs())
