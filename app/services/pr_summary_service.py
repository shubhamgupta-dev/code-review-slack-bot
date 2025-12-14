import logging
from app.models.github import PullRequestEvent
from app.services.github_service import github_service
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)


async def generate_pr_summary(event: PullRequestEvent) -> dict:
    """
    Generates an intelligent PR summary using AI-powered NLP analysis.
    Analyzes code diffs, commit history, and contextual information to provide
    comprehensive insights for code reviewers.
    """
    pr = event.pull_request
    repo = event.repository

    try:
        diff_summary = github_service.get_pr_diff_summary(
            repo.full_name, pr.number
        )
    except Exception as e:
        logger.error(f"Error getting PR diff summary: {e}")
        diff_summary = {
            "total_files": pr.changed_files,
            "total_additions": pr.additions,
            "total_deletions": pr.deletions,
            "file_types": {},
            "files": [],
        }

    # Fetch commit messages for contextual analysis
    try:
        commit_messages = github_service.get_pr_commits(repo.full_name, pr.number)
    except Exception as e:
        logger.error(f"Error getting commit messages: {e}")
        commit_messages = []

    complexity = _calculate_complexity(
        diff_summary["total_additions"] + diff_summary["total_deletions"]
    )

    # Use AI to analyze PR changes
    try:
        ai_analysis = await ai_service.analyze_pr_changes(
            pr_title=pr.title,
            pr_description=pr.body or "",
            file_changes=diff_summary.get("files", []),
            commit_messages=commit_messages,
            diff_stats=diff_summary,
        )
    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        ai_analysis = None

    # Generate summary text
    if ai_analysis and ai_analysis.get("functional_summary"):
        summary_text = ai_analysis["functional_summary"]
    else:
        summary_text = _generate_summary_text(pr, diff_summary)

    key_files = [f["filename"] for f in diff_summary.get("files", [])[:5]]

    return {
        "summary_text": summary_text,
        "files_changed": diff_summary["total_files"],
        "additions": diff_summary["total_additions"],
        "deletions": diff_summary["total_deletions"],
        "complexity": complexity,
        "key_files": key_files,
        "file_types": diff_summary["file_types"],
        "ai_analysis": ai_analysis,  # Include full AI analysis
    }


def _calculate_complexity(total_changes: int) -> str:
    if total_changes < 50:
        return "Small (< 5 min review)"
    elif total_changes < 200:
        return "Medium (~15 min review)"
    elif total_changes < 500:
        return "Large (~30 min review)"
    else:
        return "Very Large (> 1 hour review)"


def _generate_summary_text(pr, diff_summary: dict) -> str:
    if pr.body and len(pr.body) > 0:
        description = pr.body[:200]
        if len(pr.body) > 200:
            description += "..."
        return description

    file_types = diff_summary.get("file_types", {})
    if file_types:
        top_types = sorted(
            file_types.items(), key=lambda x: x[1]["count"], reverse=True
        )[:3]
        types_str = ", ".join([f"{count} {ext}" for ext, data in top_types for count in [data["count"]]])
        return f"Changes in {types_str} files"

    return "No description provided"
