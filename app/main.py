import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import github, slack, health, dashboard
from app import database

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Code Review Slack Bot...")
    logger.info(f"Environment: {settings.environment}")
    # Initialize database
    await database.init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down Code Review Slack Bot...")


app = FastAPI(
    title="Code Review Slack Bot",
    description="Reduces context-switching by bringing GitHub PR reviews directly into Slack",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(github.router, prefix="/webhooks", tags=["github"])
app.include_router(slack.router, prefix="/slack", tags=["slack"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
