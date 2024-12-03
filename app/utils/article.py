from flask_smorest import abort

from app.crud.article import get_article
from app.models import Article


def get_article_or_404(article_id: int) -> Article:
    article = get_article(article_id=article_id)
    if article is None:
        abort(404, message="Article not found")
    return article


def is_author(article: Article, author_id: int | str) -> bool:
    return article.author_id == int(author_id)
