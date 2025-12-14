import json
import logging
from fastapi import APIRouter, Request, Form
from typing import Annotated

from app.services.github_service import github_service
from app.services.slack_service import slack_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/interactions")
async def slack_interactions(payload: Annotated[str, Form()]):
    data = json.loads(payload)
    interaction_type = data.get("type")

    logger.info(f"Received Slack interaction: {interaction_type}")

    try:
        if interaction_type == "block_actions":
            await handle_block_actions(data)
        elif interaction_type == "view_submission":
            await handle_view_submission(data)

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling interaction: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


async def handle_block_actions(data: dict):
    action = data["actions"][0]
    action_id = action["action_id"]
    user = data["user"]["username"]

    if action_id == "approve_pr":
        repo_full_name, pr_number = action["value"].split("|")
        pr_number = int(pr_number)

        await github_service.approve_pr(
            repo_full_name, pr_number, f"Approved by {user} via Slack"
        )

        await slack_service.client.chat_postMessage(
            channel=data["channel"]["id"],
            thread_ts=data["message"]["ts"],
            text=f":white_check_mark: {user} approved this PR",
        )

        logger.info(f"{user} approved PR #{pr_number} in {repo_full_name}")

    elif action_id == "request_changes":
        repo_full_name, pr_number = action["value"].split("|")
        pr_number = int(pr_number)

        await slack_service.open_modal(
            data["trigger_id"], repo_full_name, pr_number
        )

    elif action_id == "comment_pr":
        repo_full_name, pr_number = action["value"].split("|")
        pr_number = int(pr_number)

        await slack_service.open_modal(
            data["trigger_id"], repo_full_name, pr_number
        )


async def handle_view_submission(data: dict):
    callback_id = data["view"]["callback_id"]
    _, repo_full_name, pr_number = callback_id.split("|")
    pr_number = int(pr_number)

    values = data["view"]["state"]["values"]
    comment = values["comment_block"]["comment_input"]["value"]
    user = data["user"]["username"]

    await github_service.add_review_comment(
        repo_full_name, pr_number, f"{comment}\n\n_Submitted by {user} via Slack_"
    )

    logger.info(f"{user} commented on PR #{pr_number} in {repo_full_name}")
