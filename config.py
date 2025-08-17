import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["DB_URL"]
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 2))
    )
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # # Extensions
    # CACHE_TYPE = "SimpleCache"
    # RATELIMIT_DEFAULT = "100/hour"