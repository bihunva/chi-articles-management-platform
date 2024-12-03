import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.extensions import db


class Role(enum.StrEnum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.viewer, nullable=False)

    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")
