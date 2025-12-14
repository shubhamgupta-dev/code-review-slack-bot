from pydantic import BaseModel
from typing import Any


class SlackInteraction(BaseModel):
    type: str
    user: dict[str, Any]
    token: str
    action_ts: str
    actions: list[dict[str, Any]] | None = None
    response_url: str | None = None
    message: dict[str, Any] | None = None
    container: dict[str, Any] | None = None
