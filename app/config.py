import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class RedisConfig:
    REDIS_URL = (
        f"redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/{os.getenv("REDIS_DATABASE")}"
    )


class APIConfig:
    API_TITLE = "CHI TEST TASK"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "security": [{"accessTokenAuth": []}, {"refreshTokenAuth": []}],
        "components": {
            "securitySchemes": {
                "accessTokenAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Access token for accessing protected resources",
                },
                "refreshTokenAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Refresh token for obtaining new access tokens",
                },
            }
        },
    }


class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("POSTGRES_DB"),
    )


class JWTConfig:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class Config(
    DatabaseConfig,
    JWTConfig,
    APIConfig,
    RedisConfig,
): ...
