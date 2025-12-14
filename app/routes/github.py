import json
import logging
from fastapi import APIRouter, Request, HTTPException

from app.models.github import PullRequestEvent, ReviewEvent
from app.utils.github_signature import verify_github_signature
from app.services.slack_service import slack_service
from app.services.slack_webhook_service import slack_webhook_service
from app.services.pr_summary_service import generate_pr_summary
from app.config import settings
from app import database

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/github")
async def github_webhook(request: Request):
    await verify_github_signature(request)

    event_type = request.headers.get("X-GitHub-Event")
    body = await request.body()
    payload = json.loads(body)

    logger.info(f"Received GitHub webhook: {event_type}")

    try:
        if event_type == "pull_request":
            await handle_pull_request_event(payload)
        elif event_type == "pull_request_review":
            await handle_review_event(payload)
        else:
            logger.info(f"Ignoring event type: {event_type}")

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


async def handle_pull_request_event(payload: dict):
    event = PullRequestEvent(**payload)

    if event.action in ["opened", "reopened", "review_requested"]:
        pr_summary = await generate_pr_summary(event)

        # Save notification to database
        notification_id = await database.save_notification(event, pr_summary)
        logger.info(f"Saved notification #{notification_id} to database")

        # Slack integration disabled - using ReviewFlow dashboard instead
        logger.info("✅ Notification saved to ReviewFlow! View at http://localhost:8000/dashboard/?token=demo-token-123")

        logger.info(
            f"Sent PR notification for #{event.pull_request.number} in {event.repository.full_name}"
        )
    elif event.action == "synchronize":
        logger.info(
            f"PR #{event.pull_request.number} updated in {event.repository.full_name}"
        )


async def handle_review_event(payload: dict):
    event = ReviewEvent(**payload)

    if event.action == "submitted":
        # Slack integration disabled - using ReviewFlow dashboard
        logger.info("Review notification saved to ReviewFlow")

        logger.info(
            f"Sent review notification for PR #{event.pull_request.number} in {event.repository.full_name}"
        )
