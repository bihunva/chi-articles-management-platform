from flask_smorest import Blueprint

article_bp = Blueprint("Articles", __name__, url_prefix="/articles")
