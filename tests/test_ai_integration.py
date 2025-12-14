"""
Test script to verify AI integration is working correctly.
This script tests the AI service independently before full integration.
"""
import asyncio
import sys
from app.services.ai_service import ai_service


async def test_ai_analysis():
    """Test AI analysis with sample PR data."""

    print("Testing AI-powered PR analysis...")
    print("-" * 60)

    # Sample PR data
    pr_title = "Add user authentication module"
    pr_description = "Implements JWT-based authentication with refresh tokens and session management"

    file_changes = [
        {"filename": "src/auth/jwt.py", "additions": 120, "deletions": 5, "status": "added"},
        {"filename": "src/auth/middleware.py", "additions": 45, "deletions": 10, "status": "modified"},
        {"filename": "src/models/user.py", "additions": 30, "deletions": 2, "status": "modified"},
        {"filename": "tests/test_auth.py", "additions": 85, "deletions": 0, "status": "added"},
        {"filename": "requirements.txt", "additions": 2, "deletions": 0, "status": "modified"},
    ]

    commit_messages = [
        "feat: add JWT token generation and validation",
        "feat: implement authentication middleware",
        "feat: add user model with password hashing",
        "test: add comprehensive auth tests",
        "docs: update authentication documentation",
    ]

    diff_stats = {
        "total_files": 5,
        "total_additions": 282,
        "total_deletions": 17,
    }

    try:
        analysis = await ai_service.analyze_pr_changes(
            pr_title=pr_title,
            pr_description=pr_description,
            file_changes=file_changes,
            commit_messages=commit_messages,
            diff_stats=diff_stats,
        )

        print("\n✅ AI Analysis Successful!\n")
        print(f"📝 Functional Summary:\n{analysis['functional_summary']}\n")
        print(f"🎯 Scope of Change:\n{analysis['scope_of_change']}\n")
        print(f"💡 Key Changes:")
        for change in analysis['key_changes']:
            print(f"  • {change}")
        print(f"\n⚠️  Risk Assessment:\n{analysis['risk_assessment']}\n")
        print(f"🔍 Review Focus Areas:")
        for area in analysis['review_focus_areas']:
            print(f"  • {area}")

        print("\n" + "-" * 60)
        print("✅ Test completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during AI analysis: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_ai_analysis())
    sys.exit(0 if success else 1)