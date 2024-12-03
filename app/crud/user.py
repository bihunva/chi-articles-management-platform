from app.extensions import db
from app.models.user import Role, User
from app.utils.auth import generate_password_hash


def get_user(user_id: int) -> User | None:
    if not (user := User.query.filter_by(id=user_id).first()):
        return None
    return user


def get_user_by_username(username: str) -> User | None:
    if not (user := User.query.filter_by(username=username).first()):
        return None
    return user


def get_all_users() -> list[User]:
    return User.query.all()


def create_user(username: str, password: bytes, role: str | Role = Role.viewer) -> User | None:
    user = get_user_by_username(username)

    if user is not None:
        return None

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def update_user(data: dict, user: User) -> User | None:
    if "username" in data:
        user.username = data["username"]
    if "role" in data:
        user.role = data["role"]

    db.session.commit()
    return user


def delete_user(user) -> None:
    db.session.delete(user)
    db.session.commit()
