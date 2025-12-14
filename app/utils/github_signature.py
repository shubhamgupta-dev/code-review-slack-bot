import hmac
import hashlib
from fastapi import HTTPException, Request

from app.config import settings


async def verify_github_signature(request: Request) -> bytes:
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        raise HTTPException(status_code=403, detail="Missing X-Hub-Signature-256 header")

    body = await request.body()
    expected_signature = (
        "sha256="
        + hmac.new(
            settings.github_webhook_secret.encode(), body, hashlib.sha256
        ).hexdigest()
    )

    if not hmac.compare_digest(signature_header, expected_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    return body
