"""
Simple Slack Webhook Service for Prototype
Uses Incoming Webhooks instead of Bot Token - perfect for testing!
"""
import logging
import httpx
from app.config import settings
from app.models.github import PullRequestEvent, ReviewEvent

logger = logging.getLogger(__name__)


class SlackWebhookService:
    """Simple Slack integration using Incoming Webhooks."""

    def __init__(self):
        self.webhook_url = getattr(settings, 'slack_webhook_url', None)
        if not self.webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not configured. Slack notifications will be disabled.")

    async def send_pr_notification(self, event: PullRequestEvent, pr_summary: dict):
        """Send PR notification to Slack via webhook."""
        if not self.webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not set, skipping Slack notification")
            return

        try:
            # Build message blocks
            blocks = self._build_pr_blocks(event, pr_summary)

            payload = {
                "text": f"New PR #{event.pull_request.number}: {event.pull_request.title}",
                "blocks": blocks
            }

            # Send to Slack
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload, timeout=10.0)

                if response.status_code == 200 and response.text == "ok":
                    logger.info(f"✅ Sent PR notification to Slack for #{event.pull_request.number}")
                else:
                    logger.error(f"Failed to send Slack notification: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"Error sending PR notification to Slack: {e}", exc_info=True)

    def _build_pr_blocks(self, event: PullRequestEvent, pr_summary: dict):
        """Build Slack Block Kit message for PR notification."""
        pr = event.pull_request
        repo = event.repository

        # Header
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🔔 New PR #{pr.number}: {pr.title}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Repository:*\n{repo.full_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Author:*\n<{pr.user.html_url}|{pr.user.login}>"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Branch:*\n`{pr.head['ref']}` → `{pr.base['ref']}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Link:*\n<{pr.html_url}|View PR on GitHub>"
                    }
                ]
            }
        ]

        # AI Analysis Summary
        ai_analysis = pr_summary.get('ai_analysis', {})
        if ai_analysis:
            summary_text = ai_analysis.get('functional_summary', 'No summary available')
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📝 AI Summary:*\n{summary_text}"
                }
            })

            # Scope and Risk
            scope = ai_analysis.get('scope_of_change', '')
            risk = ai_analysis.get('risk_assessment', '')

            if scope or risk:
                blocks.append({
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*🎯 Scope:*\n{scope}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⚠️ Risk:*\n{risk}"
                        }
                    ]
                })

            # Key Changes
            key_changes = ai_analysis.get('key_changes', [])
            if key_changes:
                changes_text = "\n".join([f"• {change}" for change in key_changes[:3]])
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*💡 Key Changes:*\n{changes_text}"
                    }
                })

        # Stats
        complexity = pr_summary.get('complexity', 'Unknown')
        blocks.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*📊 Stats:*\n📁 {pr_summary.get('files_changed', 0)} files | ➕ {pr_summary.get('additions', 0)} | ➖ {pr_summary.get('deletions', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*⏱ Complexity:*\n{complexity}"
                }
            ]
        })

        # Divider and footer
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "🤖 _Note: This is a prototype using Slack Incoming Webhook. Interactive buttons (Approve/Comment) require full bot token._"
                }
            ]
        })

        return blocks

    async def send_review_notification(self, event: ReviewEvent):
        """Send review notification to Slack."""
        if not self.webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not set, skipping review notification")
            return

        try:
            pr = event.pull_request
            review = event.review

            # Determine emoji based on review state
            emoji_map = {
                "approved": "✅",
                "changes_requested": "❌",
                "commented": "💬"
            }
            emoji = emoji_map.get(review.state.lower(), "📝")

            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{emoji} *PR Review Update*\n<{review.user.html_url}|{review.user.login}> {review.state.replace('_', ' ')} PR #{pr.number}\n\n<{pr.html_url}|{pr.title}>"
                    }
                }
            ]

            if review.body:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Comment:*\n{review.body[:500]}"
                    }
                })

            payload = {
                "text": f"PR Review: {review.state}",
                "blocks": blocks
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload, timeout=10.0)

                if response.status_code == 200:
                    logger.info(f"✅ Sent review notification to Slack")
                else:
                    logger.error(f"Failed to send review notification: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending review notification: {e}", exc_info=True)


# Create singleton instance
slack_webhook_service = SlackWebhookService()