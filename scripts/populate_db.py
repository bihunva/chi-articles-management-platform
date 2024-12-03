from flask import Flask

from app import create_app
from app.extensions import db
from app.models import User, Article
from app.utils.auth import generate_password_hash

users_with_articles = [
    {
        "username": "admin",
        "password": "admin",
        "role": "admin",
        "article_title": "Admin's First Article",
        "article_content": "Content of admin's first article"
    },
    {
        "username": "editor",
        "password": "editor",
        "role": "editor",
        "article_title": "Editor's First Article",
        "article_content": "Content of editor's first article"
    },
    {
        "username": "viewer",
        "password": "viewer",
        "role": "viewer",
        "article_title": "Viewer's First Article",
        "article_content": "Content of viewer's first article"
    }
]


def create_user_and_article(
        username: str,
        password: str,
        role: str,
        article_title: str,
        article_content: str
) -> None:
    hashed_password: bytes = generate_password_hash(password)
    new_user: User = User(username=username, hashed_password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    user_id: int = new_user.id

    new_article: Article = Article(title=article_title, content=article_content, author_id=user_id)
    db.session.add(new_article)
    db.session.commit()


def populate_users_with_articles(users_with_articles: list[dict[str, str]]) -> None:
    existing_users = User.query.first()
    if existing_users:
        print("INFO: Initial data already entered into database previously")
        return

    for user_data in users_with_articles:
        create_user_and_article(
            user_data["username"],
            user_data["password"],
            user_data["role"],
            user_data["article_title"],
            user_data["article_content"]
        )
    print("INFO: Initial data successfully inserted into database")


if __name__ == "__main__":
    app: Flask = create_app()
    with app.app_context():
        populate_users_with_articles(users_with_articles)
