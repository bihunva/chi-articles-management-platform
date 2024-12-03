import datetime

from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.extensions import db


class Article(db.Model):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(onupdate=func.now(), nullable=True)

    author = relationship("User", back_populates="articles")
