import pytest
from flask import url_for


@pytest.fixture
def new_user_data():
    return {
        "username": "new_user",
        "password": "new_user_password",
        "role": "viewer",
    }


def test_create_success(client, db, mock_redis, admin_user, new_user_data):
    access_token = admin_user["access_token"]

    response = client.post(
        url_for("Users.create_user_view"),
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_user_data,
    )
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert (
        data["username"] == new_user_data["username"]
    ), f"Expected username {new_user_data['username']}, got {data['username']}"
    assert (
        data["role"] == new_user_data["role"]
    ), f"Expected role {new_user_data['role']}, got {data['role']}"


def test_create_unauthorized(client, new_user_data):
    response = client.post(url_for("Users.create_user_view"), json=new_user_data)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"


def test_create_forbidden(client, db, mock_redis, viewer_user, new_user_data):
    not_admin_access_token = viewer_user["access_token"]

    response = client.post(
        url_for("Users.create_user_view"),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
        json=new_user_data,
    )
    assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"


def test_create_existing_username(client, db, mock_redis, admin_user, new_user_data):
    access_token = admin_user["access_token"]

    client.post(
        url_for("Users.create_user_view"),
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_user_data,
    )

    response = client.post(
        url_for("Users.create_user_view"),
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_user_data,
    )
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert data["message"] == "Username already exists"
