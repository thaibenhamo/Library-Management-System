import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Flask application configuration class.

    Loads configuration from environment variables with sensible defaults.
    Uses python-dotenv to load .env file for development environments.

    Environment Variables Required:
        DB_URL: Database connection string (e.g., "sqlite:///app.db" or PostgreSQL URL)
        JWT_SECRET_KEY: Secret key for JWT token signing (should be cryptographically secure)

    Environment Variables Optional:
        JWT_ACCESS_TOKEN_EXPIRES_HOURS: Token expiration in hours (default: 2)
    """
    SQLALCHEMY_DATABASE_URI = os.environ["DB_URL"]

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 2))
    )
