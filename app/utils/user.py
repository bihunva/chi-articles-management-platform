from flask_smorest import abort

from app.crud.user import get_user
from app.models import User


def get_user_or_404(user_id) -> User | None:
    user = get_user(user_id)

    if user is None:
        abort(404, message="User not found")

    return user
