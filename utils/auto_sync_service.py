"""
Automatic PR Sync Service - Polls GitHub every few minutes for new PRs
This is an alternative to webhooks that doesn't require a public URL
"""
import asyncio
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# Ensure we're in the project root directory
project_root = Path(__file__).parent.parent
os.chdir(project_root)

class AutoSyncService:
    def __init__(self, interval_seconds=300):
        """
        Initialize the auto-sync service

        Args:
            interval_seconds: How often to check for new PRs (default: 300 = 5 minutes)
        """
        self.interval = interval_seconds
        self.running = True

    async def sync_once(self):
        """Run a single sync operation - both new PRs and status updates"""
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔄 Syncing with GitHub...")

            # Set PYTHONPATH to include project root
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path.cwd())

            # First, check for new PRs
            fetch_result = subprocess.run(
                ["python3", "utils/fetch_new_pr.py"],
                capture_output=True,
                text=True,
                timeout=60,
                env=env
            )

            new_prs_found = False
            if fetch_result.returncode == 0:
                if "🆕 PR #" in fetch_result.stdout:
                    new_prs_found = True
                    print("   ✅ New PR(s) found!")
                    for line in fetch_result.stdout.split('\n'):
                        if '🆕 PR #' in line:
                            print(f"   {line.strip()}")

            # Then, sync status updates for existing PRs
            sync_result = subprocess.run(
                ["python3", "utils/sync_github_prs.py"],
                capture_output=True,
                text=True,
                timeout=60,
                env=env
            )

            status_updates = False
            if sync_result.returncode == 0:
                if "✏️" in sync_result.stdout:
                    status_updates = True
                    print("   📝 Status updates:")
                    for line in sync_result.stdout.split('\n'):
                        if '✏️' in line:
                            print(f"   {line.strip()}")

            # Summary
            if not new_prs_found and not status_updates:
                print("   ℹ️  Already in sync")

        except subprocess.TimeoutExpired:
            print("   ⏱️  Sync timed out (took longer than 60s)")
        except Exception as e:
            print(f"   ❌ Error during sync: {e}")

    async def run(self):
        """Run the service continuously"""
        print("=" * 80)
        print("🚀 REVIEWFLOW AUTO-SYNC SERVICE")
        print("=" * 80)
        print()
        print(f"⏰ Polling interval: {self.interval} seconds ({self.interval//60} minutes)")
        print(f"📦 Repository: shubhamgupta-dev/10X_Dev_Workshop")
        print(f"🔗 Dashboard: http://localhost:8000/dashboard/?token=demo-token-123")
        print()
        print("💡 This service will automatically check for new PRs every few minutes")
        print("   and sync them to your dashboard without needing webhooks!")
        print()
        print("🛑 Press Ctrl+C to stop")
        print("=" * 80)
        print()

        # Initial sync on startup
        await self.sync_once()
        print()

        # Main loop
        try:
            while self.running:
                await asyncio.sleep(self.interval)
                await self.sync_once()
                print()

        except KeyboardInterrupt:
            print()
            print("=" * 80)
            print("🛑 STOPPING AUTO-SYNC SERVICE")
            print("=" * 80)
            print()
            print("✅ Service stopped gracefully")
            self.running = False


async def main():
    """Main entry point"""

    # Parse command line args
    interval = 300  # Default: 5 minutes

    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 30:
                print("⚠️  Warning: Interval too short. Using minimum of 30 seconds.")
                interval = 30
        except ValueError:
            print("❌ Invalid interval. Usage: python3 auto_sync_service.py [seconds]")
            sys.exit(1)

    service = AutoSyncService(interval_seconds=interval)
    await service.run()


if __name__ == "__main__":
    print()
    print("Starting ReviewFlow Auto-Sync Service...")
    print()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print("👋 Goodbye!")
