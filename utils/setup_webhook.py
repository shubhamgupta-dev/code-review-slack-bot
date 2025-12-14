"""
Script to set up GitHub webhook for automatic PR sync
"""
from github import Github, Auth
from app.config import settings
import sys

def setup_webhook(webhook_url):
    """Set up webhook in GitHub repository"""

    print("=" * 80)
    print("SETTING UP GITHUB WEBHOOK")
    print("=" * 80)
    print()

    try:
        # Authenticate
        auth = Auth.Token(settings.github_token)
        client = Github(auth=auth)

        # Get repository
        repo = client.get_repo("shubhamgupta-dev/10X_Dev_Workshop")

        print(f"📦 Repository: {repo.full_name}")
        print(f"🔗 Webhook URL: {webhook_url}")
        print()

        # Check existing webhooks
        print("🔍 Checking existing webhooks...")
        existing_hooks = list(repo.get_hooks())

        for hook in existing_hooks:
            if hook.config.get('url') == webhook_url:
                print(f"   ⚠️  Webhook already exists with this URL")
                print(f"   ID: {hook.id}")
                print()
                response = input("   Delete and recreate? (y/n): ")
                if response.lower() == 'y':
                    hook.delete()
                    print(f"   🗑️  Deleted webhook #{hook.id}")
                else:
                    print("   ⏭️  Keeping existing webhook")
                    return

        # Create webhook configuration
        config = {
            "url": webhook_url + "/webhooks/github",
            "content_type": "json",
            "secret": settings.github_webhook_secret,
            "insecure_ssl": "0"
        }

        print("🎯 Creating webhook...")
        hook = repo.create_hook(
            name="web",
            config=config,
            events=["pull_request", "pull_request_review"],
            active=True
        )

        print(f"   ✅ Webhook created!")
        print(f"   ID: {hook.id}")
        print(f"   URL: {hook.config['url']}")
        print()

        print("=" * 80)
        print("✅ WEBHOOK SETUP COMPLETE!")
        print("=" * 80)
        print()
        print("🎉 Your repository is now connected to ReviewFlow!")
        print()
        print("📋 Next steps:")
        print("1. Create a new PR on GitHub")
        print("2. The webhook will automatically notify ReviewFlow")
        print("3. Check the dashboard: http://localhost:8000/dashboard/?token=demo-token-123")
        print()
        print("🔔 Events being tracked:")
        print("   - pull_request (opened, reopened, synchronize)")
        print("   - pull_request_review (submitted)")
        print()
        print("=" * 80)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 setup_webhook.py <webhook_url>")
        print()
        print("Example:")
        print("  python3 setup_webhook.py https://abc123.ngrok.io")
        print()
        print("💡 Tips:")
        print("1. Run ngrok first: ngrok http 8000")
        print("2. Get your ngrok URL from the output")
        print("3. Use that URL with this script")
        sys.exit(1)

    webhook_url = sys.argv[1].rstrip('/')
    success = setup_webhook(webhook_url)
    sys.exit(0 if success else 1)
