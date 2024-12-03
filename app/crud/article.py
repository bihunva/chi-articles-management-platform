from app.extensions import db
from app.models import Article


def get_article(article_id: int) -> Article | None:
    if not (article := Article.query.filter_by(id=article_id).first()):
        return None
    return article


def get_all_articles() -> list[Article]:
    return Article.query.all()


def create_article(title, content, author_id) -> Article:
    new_article = Article(title=title, content=content, author_id=author_id)
    db.session.add(new_article)
    db.session.commit()
    return new_article


def update_article(data, article) -> Article:
    if "title" in data:
        article.title = data["title"]
    if "content" in data:
        article.content = data["content"]

    db.session.commit()
    return article


def delete_article(article) -> None:
    db.session.delete(article)
    db.session.commit()


def search_articles_by_title(title: str) -> list[Article]:
    return Article.query.filter(Article.title.ilike(f"%{title}%")).all()
