import logging
from github import Github, Auth
from github.PullRequest import PullRequest
from github.Repository import Repository

from app.config import settings

logger = logging.getLogger(__name__)


class GitHubService:
    def __init__(self):
        auth = Auth.Token(settings.github_token)
        self.client = Github(auth=auth)

    def get_repository(self, repo_full_name: str) -> Repository:
        return self.client.get_repo(repo_full_name)

    def get_pull_request(self, repo_full_name: str, pr_number: int) -> PullRequest:
        repo = self.get_repository(repo_full_name)
        return repo.get_pull(pr_number)

    def get_pr_files(self, repo_full_name: str, pr_number: int) -> list[dict]:
        pr = self.get_pull_request(repo_full_name, pr_number)
        files = []
        for file in pr.get_files():
            files.append(
                {
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                }
            )
        return files

    def get_pr_diff_summary(self, repo_full_name: str, pr_number: int) -> dict:
        pr = self.get_pull_request(repo_full_name, pr_number)
        files = self.get_pr_files(repo_full_name, pr_number)

        file_types = {}
        for file in files:
            ext = file["filename"].split(".")[-1] if "." in file["filename"] else "other"
            if ext not in file_types:
                file_types[ext] = {"count": 0, "additions": 0, "deletions": 0}
            file_types[ext]["count"] += 1
            file_types[ext]["additions"] += file["additions"]
            file_types[ext]["deletions"] += file["deletions"]

        return {
            "total_files": len(files),
            "total_additions": pr.additions,
            "total_deletions": pr.deletions,
            "file_types": file_types,
            "files": files[:10],
        }

    def get_pr_commits(self, repo_full_name: str, pr_number: int) -> list[str]:
        """Fetches commit messages from the PR for contextual analysis."""
        try:
            pr = self.get_pull_request(repo_full_name, pr_number)
            commits = pr.get_commits()
            commit_messages = []

            for commit in commits:
                if commit.commit.message:
                    # Get first line of commit message (summary)
                    message = commit.commit.message.split("\n")[0].strip()
                    if message:
                        commit_messages.append(message)

            logger.info(f"Retrieved {len(commit_messages)} commit messages for PR #{pr_number}")
            return commit_messages
        except Exception as e:
            logger.error(f"Error fetching commits for PR #{pr_number}: {e}")
            return []

    async def add_review_comment(
        self, repo_full_name: str, pr_number: int, comment: str, event: str = "COMMENT"
    ):
        pr = self.get_pull_request(repo_full_name, pr_number)
        pr.create_review(body=comment, event=event)
        logger.info(f"Added {event} review to PR #{pr_number} in {repo_full_name}")

    async def approve_pr(self, repo_full_name: str, pr_number: int, comment: str = ""):
        await self.add_review_comment(repo_full_name, pr_number, comment, "APPROVE")

    async def request_changes(
        self, repo_full_name: str, pr_number: int, comment: str = ""
    ):
        await self.add_review_comment(
            repo_full_name, pr_number, comment, "REQUEST_CHANGES"
        )

    async def close_pr(self, repo_full_name: str, pr_number: int):
        """Close a pull request on GitHub."""
        pr = self.get_pull_request(repo_full_name, pr_number)
        pr.edit(state="closed")
        logger.info(f"Closed PR #{pr_number} in {repo_full_name}")

    def get_pr_diff(self, repo_full_name: str, pr_number: int) -> list[dict]:
        """Get detailed file diffs for a pull request."""
        pr = self.get_pull_request(repo_full_name, pr_number)
        files = []

        for file in pr.get_files():
            file_data = {
                "filename": file.filename,
                "status": file.status,  # added, modified, removed, renamed
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "patch": file.patch if hasattr(file, 'patch') and file.patch else None,
                "previous_filename": file.previous_filename if hasattr(file, 'previous_filename') else None
            }
            files.append(file_data)

        logger.info(f"Retrieved diff for {len(files)} files in PR #{pr_number}")
        return files


github_service = GitHubService()
