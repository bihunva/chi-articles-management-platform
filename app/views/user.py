from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from app.crud.user import (
    get_all_users,
    create_user,
    update_user,
    delete_user,
)
from app.schemas.user import (
    UserResponseSchema,
    CreateUserSchema,
    UpdateUserSchema,
)
from app.utils.auth import admin_required
from app.utils.user import get_user_or_404

user_bp = Blueprint("Users", __name__, url_prefix="/users")


@user_bp.route("/", methods=["GET"])
@jwt_required()
@admin_required
@user_bp.response(status_code=200, schema=UserResponseSchema(many=True))
def get_all_users_view():
    return get_all_users()


@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@admin_required
@user_bp.response(status_code=200, schema=UserResponseSchema)
def get_user_view(user_id):
    user = get_user_or_404(user_id=user_id)
    return user


@user_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
@user_bp.arguments(CreateUserSchema)
@user_bp.response(status_code=201, schema=UserResponseSchema)
def create_user_view(data):
    new_user = create_user(
        username=data["username"],
        password=data["password"],
        role=data["role"],
    )

    if new_user is None:
        abort(400, message="Username already exists")

    return new_user


@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
@user_bp.arguments(UpdateUserSchema)
@user_bp.response(status_code=200, schema=UserResponseSchema)
def update_user_view(data, user_id):
    user = get_user_or_404(user_id=user_id)
    updated_user = update_user(data=data, user=user)
    return updated_user


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
@user_bp.response(status_code=200)
def delete_user_view(user_id):
    user = get_user_or_404(user_id=user_id)
    delete_user(user=user)
    return {"message": "User deleted successfully"}
