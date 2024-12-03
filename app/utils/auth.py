from functools import wraps

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt
from flask_smorest import abort
from sqlalchemy.orm import Mapped

from app.extensions import redis_client, bcrypt


def admin_required(fn: callable) -> callable:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> callable:
        claims = get_jwt()
        if "role" not in claims or claims["role"] != "admin":
            abort(403, message="Admin access required")

        return fn(*args, **kwargs)

    return wrapper


def is_token_blacklisted(jti: str) -> bool:
    return redis_client.get(jti) is not None


def add_token_to_blacklist(jti: str) -> None:
    redis_client.set(jti, "", ex=3600)


def generate_tokens(identity: str, additional_claims=None) -> tuple:
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
    return access_token, refresh_token


def generate_password_hash(password: str) -> bytes:
    return bcrypt.generate_password_hash(password=password)


def check_password(pw_hash: bytes | Mapped[bytes], password: bytes) -> bool:
    return bcrypt.check_password_hash(pw_hash=pw_hash, password=password)
