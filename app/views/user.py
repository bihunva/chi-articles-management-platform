from flask_smorest import Blueprint

user_bp = Blueprint("Users", __name__, url_prefix="/users")
