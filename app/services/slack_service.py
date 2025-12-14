import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.config import settings
from app.models.github import PullRequestEvent, ReviewEvent

logger = logging.getLogger(__name__)


class SlackService:
    def __init__(self):
        self.enabled = bool(settings.slack_bot_token)
        if self.enabled:
            self.client = WebClient(token=settings.slack_bot_token)
            self.default_channel = "#code-reviews"
        else:
            logger.info("Slack service disabled (no bot token configured)")

    def _format_pr_blocks(self, event: PullRequestEvent, summary: dict):
        pr = event.pull_request
        repo = event.repository

        action_emoji = {
            "opened": ":new:",
            "reopened": ":recycle:",
            "review_requested": ":eyes:",
        }.get(event.action, ":bell:")

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{action_emoji} Pull Request: {pr.title}",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Repository:*\n{repo.full_name}"},
                    {"type": "mrkdwn", "text": f"*Author:*\n{pr.user.login}"},
                    {"type": "mrkdwn", "text": f"*PR Number:*\n#{pr.number}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Branch:*\n{pr.head['ref']} → {pr.base['ref']}",
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n{summary['summary_text']}",
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f":file_folder: *{summary['files_changed']}* files",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f":heavy_plus_sign: *{summary['additions']}* additions",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f":heavy_minus_sign: *{summary['deletions']}* deletions",
                    },
                    {"type": "mrkdwn", "text": f":clock1: *{summary['complexity']}*"},
                ],
            },
        ]

        # Add AI-powered insights section
        ai_analysis = summary.get("ai_analysis")
        if ai_analysis:
            blocks.append({"type": "divider"})

            # Scope of change
            if ai_analysis.get("scope_of_change"):
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":dart: *Scope:* {ai_analysis['scope_of_change']}",
                        },
                    }
                )

            # Key changes
            if ai_analysis.get("key_changes"):
                changes_text = "\n".join(
                    [f"• {change}" for change in ai_analysis["key_changes"][:4]]
                )
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":bulb: *Key Changes:*\n{changes_text}",
                        },
                    }
                )

            # Risk assessment
            if ai_analysis.get("risk_assessment"):
                risk_emoji = ":white_check_mark:" if "low" in ai_analysis["risk_assessment"].lower() else ":warning:"
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{risk_emoji} *Risk:* {ai_analysis['risk_assessment']}",
                        },
                    }
                )

            # Review focus areas
            if ai_analysis.get("review_focus_areas"):
                focus_text = "\n".join(
                    [f"• {area}" for area in ai_analysis["review_focus_areas"][:3]]
                )
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":mag: *Review Focus:*\n{focus_text}",
                        },
                    }
                )

        if summary.get("key_files"):
            files_text = "\n".join([f"• `{f}`" for f in summary["key_files"][:5]])
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Key Files:*\n{files_text}"},
                }
            )

        blocks.extend(
            [
                {"type": "divider"},
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": ":white_check_mark: Approve"},
                            "style": "primary",
                            "action_id": "approve_pr",
                            "value": f"{repo.full_name}|{pr.number}",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":speech_balloon: Comment",
                            },
                            "action_id": "comment_pr",
                            "value": f"{repo.full_name}|{pr.number}",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":x: Request Changes",
                            },
                            "style": "danger",
                            "action_id": "request_changes",
                            "value": f"{repo.full_name}|{pr.number}",
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": ":link: View on GitHub"},
                            "url": pr.html_url,
                            "action_id": "view_github",
                        },
                    ],
                },
            ]
        )

        return blocks

    def _format_review_blocks(self, event: ReviewEvent):
        review = event.review
        pr = event.pull_request
        repo = event.repository

        state_emoji = {
            "approved": ":white_check_mark:",
            "changes_requested": ":x:",
            "commented": ":speech_balloon:",
        }.get(review.state, ":bell:")

        state_text = {
            "approved": "approved",
            "changes_requested": "requested changes on",
            "commented": "commented on",
        }.get(review.state, "reviewed")

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{state_emoji} *{review.user.login}* {state_text} PR #{pr.number}: *{pr.title}*",
                },
            }
        ]

        if review.body:
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f">{review.body}"},
                }
            )

        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View Review"},
                        "url": review.html_url,
                        "action_id": "view_review",
                    }
                ],
            }
        )

        return blocks

    async def send_pr_notification(self, event: PullRequestEvent, summary: dict):
        if not self.enabled:
            logger.info("Slack notifications disabled")
            return

        try:
            blocks = self._format_pr_blocks(event, summary)
            response = self.client.chat_postMessage(
                channel=self.default_channel, blocks=blocks, text=f"New PR: {event.pull_request.title}"
            )
            logger.info(f"Sent PR notification to {self.default_channel}")
            return response
        except SlackApiError as e:
            logger.error(f"Error sending PR notification: {e.response['error']}")
            raise

    async def send_review_notification(self, event: ReviewEvent):
        try:
            blocks = self._format_review_blocks(event)
            response = self.client.chat_postMessage(
                channel=self.default_channel,
                blocks=blocks,
                text=f"{event.review.user.login} reviewed PR #{event.pull_request.number}",
            )
            logger.info(f"Sent review notification to {self.default_channel}")
            return response
        except SlackApiError as e:
            logger.error(f"Error sending review notification: {e.response['error']}")
            raise

    async def update_message(self, channel: str, timestamp: str, text: str):
        try:
            response = self.client.chat_update(channel=channel, ts=timestamp, text=text)
            return response
        except SlackApiError as e:
            logger.error(f"Error updating message: {e.response['error']}")
            raise

    async def open_modal(self, trigger_id: str, repo_full_name: str, pr_number: int):
        modal = {
            "type": "modal",
            "callback_id": f"review_modal|{repo_full_name}|{pr_number}",
            "title": {"type": "plain_text", "text": "Add Review Comment"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "comment_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "comment_input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter your review comment...",
                        },
                    },
                    "label": {"type": "plain_text", "text": "Comment"},
                }
            ],
        }

        try:
            response = self.client.views_open(trigger_id=trigger_id, view=modal)
            return response
        except SlackApiError as e:
            logger.error(f"Error opening modal: {e.response['error']}")
            raise


slack_service = SlackService()
