from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    github_webhook_secret: str
    github_token: str

    slack_bot_token: str | None = None
    slack_signing_secret: str | None = None
    slack_app_token: str | None = None
    slack_webhook_url: str | None = None  # For simple webhook integration

    # Dashboard configuration
    dashboard_access_token: str = "demo-token-123"  # Change this in production!
    dashboard_username: str = "admin"  # Default username
    dashboard_password: str = "admin123"  # Default password - CHANGE THIS!
    dashboard_email: str = "admin@example.com"  # Admin email for password reset
    session_secret_key: str = "your-secret-key-change-in-production"  # For session encryption

    # Email configuration for password reset
    smtp_host: str = "smtp.gmail.com"  # SMTP server
    smtp_port: int = 587  # SMTP port (587 for TLS, 465 for SSL)
    smtp_username: str = ""  # Your email address
    smtp_password: str = ""  # Your email password or app password
    smtp_from_email: str = ""  # From email address
    smtp_from_name: str = "ReviewFlow Dashboard"  # From name

    # Nerd-Completion configuration (internal LLM gateway)
    nerd_completion_api_key: str
    nerd_completion_base_url: str

    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    environment: str = "development"


settings = Settings()
