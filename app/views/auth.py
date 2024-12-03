from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_smorest import (
    Blueprint,
    abort,
)

from app.crud.user import (
    get_user_by_username,
    create_user,
)
from app.schemas.auth import (
    RegisterSchema,
    RegisterResponseSchema,
    LoginSchema,
    LoginResponseSchema,
    RefreshResponseSchema,
)
from app.utils.auth import (
    generate_tokens,
    check_password,
    is_token_blacklisted,
    add_token_to_blacklist,
)

auth_bp = Blueprint("Auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
@auth_bp.arguments(schema=RegisterSchema)
@auth_bp.response(status_code=201, schema=RegisterResponseSchema)
def register_view(credentials):
    username = credentials["username"]
    user_exists = get_user_by_username(username)

    if user_exists is not None:
        abort(400, message="Username already exists")

    new_user = create_user(username=username, password=credentials["password"])
    return new_user


@auth_bp.route("/login", methods=["POST"])
@auth_bp.arguments(schema=LoginSchema)
@auth_bp.response(status_code=200, schema=LoginResponseSchema)
def login_view(credentials):
    user = get_user_by_username(credentials["username"])

    if not user or not check_password(user.hashed_password, credentials["password"]):
        abort(404, message="Invalid credentials")

    additional_claims = {"role": user.role.value}
    access_token, refresh_token = generate_tokens(
        identity=str(user.id), additional_claims=additional_claims
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@auth_bp.response(status_code=200, schema=RefreshResponseSchema)
def refresh_view():
    current_user_id = get_jwt_identity()
    jti = get_jwt().get("jti")
    role = get_jwt().get("role")

    if is_token_blacklisted(jti):
        abort(401, message="Token is revoked")

    add_token_to_blacklist(jti)
    additional_claims = {"role": role}
    access_token, refresh_token = generate_tokens(
        identity=str(current_user_id), additional_claims=additional_claims
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
@auth_bp.response(status_code=200)
def logout_view():
    jti = get_jwt().get("jti")

    if is_token_blacklisted(jti):
        abort(401, message="Token is revoked")

    add_token_to_blacklist(jti)
    return jsonify(message="Successfully logged out")
