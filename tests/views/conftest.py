import pytest
from flask import url_for

from app.models.user import User, Role


@pytest.fixture
def admin_user_data():
    return {"username": "admin_user", "password": "admin_password"}


@pytest.fixture
def editor_user_data():
    return {"username": "editor_user", "password": "editor_password"}


@pytest.fixture
def viewer_user_data():
    return {"username": "viewer_user", "password": "viewer_password"}


@pytest.fixture
def admin_user(client, db, admin_user_data):
    register_response = register_user(client, admin_user_data)
    update_user_role(db, admin_user_data["username"], "admin")
    access_token = get_access_token(client, admin_user_data)
    return {
        "id": register_response.get_json()["id"],
        "user_data": admin_user_data,
        "access_token": access_token,
    }


@pytest.fixture
def editor_user(client, db, editor_user_data):
    register_response = register_user(client, editor_user_data)
    update_user_role(db, editor_user_data["username"], "editor")
    access_token = get_access_token(client, editor_user_data)
    return {
        "id": register_response.get_json()["id"],
        "user_data": editor_user_data,
        "access_token": access_token,
    }


@pytest.fixture
def viewer_user(client, db, viewer_user_data):
    register_response = register_user(client, viewer_user_data)
    access_token = get_access_token(client, viewer_user_data)
    return {
        "id": register_response.get_json()["id"],
        "user_data": viewer_user_data,
        "access_token": access_token,
    }


def update_user_role(db, username, role):
    user = User.query.filter_by(username=username).first()
    user.role = Role[role]
    db.session.commit()


def register_user(client, user_data):
    return client.post(url_for("Auth.register_view"), json=user_data)


def login_user(client, user_data):
    return client.post(url_for("Auth.login_view"), json=user_data)


def get_access_token(client, user_data):
    login_response = login_user(client, user_data)
    assert login_response.status_code == 200, f"Login failed: {login_response.data}"
    return login_response.get_json()["access_token"]
