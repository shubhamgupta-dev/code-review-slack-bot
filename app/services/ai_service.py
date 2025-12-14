import logging
from anthropic import AsyncAnthropic
from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service for intelligent PR analysis using Natural Language Processing.
    Uses Claude AI to perform contextual summarization of code diffs and commit history.
    """

    def __init__(self):
        # Configure Anthropic client to use Nerd-Completion gateway
        self.client = AsyncAnthropic(
            api_key=settings.nerd_completion_api_key,
            base_url=settings.nerd_completion_base_url
        )
        # Use Nerd-Completion compatible model name
        self.model = "claude-3-5-sonnet"

    async def analyze_pr_changes(
        self,
        pr_title: str,
        pr_description: str,
        file_changes: list[dict],
        commit_messages: list[str],
        diff_stats: dict,
    ) -> dict:
        """
        Performs NLP-based analysis of PR changes to generate intelligent summaries.

        Args:
            pr_title: The pull request title
            pr_description: The pull request description
            file_changes: List of file changes with additions/deletions
            commit_messages: List of commit messages
            diff_stats: Statistics about the diff (additions, deletions, file count)

        Returns:
            Dictionary containing:
            - functional_summary: High-level summary of what changed
            - scope_of_change: Scope and impact analysis
            - key_changes: List of key functional changes
            - risk_assessment: Potential risks or breaking changes
            - review_focus_areas: Areas reviewers should focus on
        """
        try:
            prompt = self._build_analysis_prompt(
                pr_title,
                pr_description,
                file_changes,
                commit_messages,
                diff_stats,
            )

            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            analysis = self._parse_ai_response(response.content[0].text)
            logger.info(f"AI analysis completed for PR: {pr_title}")
            return analysis

        except Exception as e:
            logger.error(f"Error in AI analysis: {e}", exc_info=True)
            return self._fallback_analysis(
                pr_title, pr_description, file_changes, diff_stats
            )

    def _build_analysis_prompt(
        self,
        pr_title: str,
        pr_description: str,
        file_changes: list[dict],
        commit_messages: list[str],
        diff_stats: dict,
    ) -> str:
        """Builds a comprehensive prompt for AI analysis."""

        # Format file changes
        files_summary = "\n".join(
            [
                f"- {f['filename']}: +{f['additions']} -{f['deletions']} lines ({f['status']})"
                for f in file_changes[:15]  # Limit to avoid token overflow
            ]
        )

        # Format commit messages
        commits_summary = "\n".join(
            [f"- {msg}" for msg in commit_messages[:10]]  # Limit to recent commits
        )

        prompt = f"""You are a senior software engineer performing code review analysis. Analyze this Pull Request and provide a concise, intelligent summary.

**Pull Request Title:** {pr_title}

**Description:**
{pr_description or "No description provided"}

**Statistics:**
- Files Changed: {diff_stats.get('total_files', 0)}
- Lines Added: {diff_stats.get('total_additions', 0)}
- Lines Deleted: {diff_stats.get('total_deletions', 0)}

**Files Changed:**
{files_summary}

**Commit Messages:**
{commits_summary or "No commit messages available"}

Please provide your analysis in the following format:

FUNCTIONAL_SUMMARY:
[1-2 sentences explaining WHAT this PR does in plain English, focusing on the business/functional impact]

SCOPE_OF_CHANGE:
[Identify which parts of the system are affected: frontend, backend, database, API, infrastructure, etc.]

KEY_CHANGES:
[List 2-4 bullet points of the most important changes]

RISK_ASSESSMENT:
[Identify potential risks, breaking changes, or areas of concern. If none, say "Low risk"]

REVIEW_FOCUS:
[2-3 specific areas reviewers should pay attention to]

Keep your response concise and technical. Focus on semantic meaning, not just file counts."""

        return prompt

    def _parse_ai_response(self, response_text: str) -> dict:
        """Parses the AI response into structured data."""
        sections = {
            "functional_summary": "",
            "scope_of_change": "",
            "key_changes": [],
            "risk_assessment": "",
            "review_focus_areas": [],
        }

        try:
            lines = response_text.strip().split("\n")
            current_section = None

            for line in lines:
                line = line.strip()

                if line.startswith("FUNCTIONAL_SUMMARY:"):
                    current_section = "functional_summary"
                    continue
                elif line.startswith("SCOPE_OF_CHANGE:"):
                    current_section = "scope_of_change"
                    continue
                elif line.startswith("KEY_CHANGES:"):
                    current_section = "key_changes"
                    continue
                elif line.startswith("RISK_ASSESSMENT:"):
                    current_section = "risk_assessment"
                    continue
                elif line.startswith("REVIEW_FOCUS:"):
                    current_section = "review_focus_areas"
                    continue

                if line and current_section:
                    if current_section in ["key_changes", "review_focus_areas"]:
                        # Handle bullet points
                        clean_line = line.lstrip("•-*").strip()
                        if clean_line:
                            sections[current_section].append(clean_line)
                    else:
                        # Handle text sections
                        if sections[current_section]:
                            sections[current_section] += " " + line
                        else:
                            sections[current_section] = line

        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")

        return sections

    def _fallback_analysis(
        self,
        pr_title: str,
        pr_description: str,
        file_changes: list[dict],
        diff_stats: dict,
    ) -> dict:
        """Fallback analysis if AI fails."""
        file_types = {}
        for f in file_changes:
            ext = f["filename"].split(".")[-1] if "." in f["filename"] else "other"
            file_types[ext] = file_types.get(ext, 0) + 1

        top_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:3]
        types_str = ", ".join([f"{count} {ext}" for ext, count in top_types])

        return {
            "functional_summary": pr_description[:200] if pr_description else f"Changes in {types_str} files",
            "scope_of_change": f"Affects {diff_stats.get('total_files', 0)} files",
            "key_changes": [f"Modified {types_str} files"],
            "risk_assessment": "Unable to assess - AI analysis unavailable",
            "review_focus_areas": ["Review all changes carefully"],
        }


ai_service = AIService()