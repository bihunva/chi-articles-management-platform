from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_smorest import (
    Blueprint,
    abort,
)

from app.crud.article import (
    get_all_articles,
    create_article,
    delete_article,
    search_articles_by_title,
    update_article,
)
from app.schemas.article import (
    ArticleResponseSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema,
    ArticleSearchSchema,
)
from app.utils.article import (
    get_article_or_404,
    is_author,
)

article_bp = Blueprint("Articles", __name__, url_prefix="/articles")


@article_bp.route("/", methods=["GET"])
@jwt_required()
@article_bp.response(status_code=200, schema=ArticleResponseSchema(many=True))
def get_all_articles_view():
    return get_all_articles()


@article_bp.route("/<int:article_id>", methods=["GET"])
@jwt_required()
@article_bp.response(status_code=200, schema=ArticleResponseSchema)
def get_article_view(article_id):
    article = get_article_or_404(article_id)
    return article


@article_bp.route("/", methods=["POST"])
@jwt_required()
@article_bp.arguments(ArticleCreateSchema)
@article_bp.response(status_code=201, schema=ArticleResponseSchema)
def create_article_view(data):
    current_user_id = get_jwt_identity()
    new_article = create_article(
        title=data["title"],
        content=data["content"],
        author_id=current_user_id,
    )
    return new_article


@article_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
@article_bp.arguments(ArticleUpdateSchema)
@article_bp.response(status_code=200, schema=ArticleResponseSchema)
def update_article_view(data, article_id):
    article = get_article_or_404(article_id)
    current_user_id = get_jwt_identity()
    role = get_jwt().get("role")

    if role == "viewer" and not is_author(article=article, author_id=current_user_id):
        abort(403, message="You can only modify your own articles")

    updated_article = update_article(data, article)
    return updated_article


@article_bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
@article_bp.response(status_code=200)
def delete_article_view(article_id):
    article = get_article_or_404(article_id)
    current_user_id = get_jwt_identity()
    role = get_jwt().get("role")

    if role in ("editor", "viewer") and not is_author(article, current_user_id):
        abort(403, message="You can only delete your own articles")

    delete_article(article)
    return {"message": "Article deleted successfully"}


@article_bp.route("/search", methods=["GET"])
@jwt_required()
@article_bp.arguments(ArticleSearchSchema, location="query")
@article_bp.response(status_code=200, schema=ArticleResponseSchema(many=True))
def search_articles_view(args):
    return search_articles_by_title(args["title"])
