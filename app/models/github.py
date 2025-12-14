from pydantic import BaseModel, Field
from typing import Literal


class User(BaseModel):
    login: str
    avatar_url: str | None = None


class Repository(BaseModel):
    name: str
    full_name: str
    html_url: str


class PullRequest(BaseModel):
    number: int
    title: str
    html_url: str
    state: str
    body: str | None = None
    user: User
    head: dict
    base: dict
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0


class PullRequestEvent(BaseModel):
    action: Literal["opened", "synchronize", "reopened", "closed", "review_requested"]
    pull_request: PullRequest
    repository: Repository
    sender: User
    requested_reviewer: User | None = None


class Review(BaseModel):
    user: User
    state: Literal["approved", "changes_requested", "commented"]
    html_url: str
    body: str | None = None


class ReviewEvent(BaseModel):
    action: Literal["submitted", "edited", "dismissed"]
    review: Review
    pull_request: PullRequest
    repository: Repository
