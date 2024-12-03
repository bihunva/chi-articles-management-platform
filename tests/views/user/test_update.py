import pytest
from flask import url_for


@pytest.fixture
def update_user_data():
    return {"username": "updated_user", "role": "editor"}


def test_update_success(client, db, mock_redis, admin_user, viewer_user, update_user_data):
    access_token = admin_user["access_token"]
    user_id_to_update = viewer_user["id"]

    response = client.put(
        url_for("Users.update_user_view", user_id=user_id_to_update),
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_user_data,
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert (
        data["username"] == update_user_data["username"]
    ), f"Expected username {update_user_data['username']}, got {data['username']}"
    assert (
        data["role"] == update_user_data["role"]
    ), f"Expected role {update_user_data['role']}, got {data['role']}"


def test_update_unauthorized(client, db, admin_user, update_user_data):
    response = client.put(url_for("Users.update_user_view", user_id=1), json=update_user_data)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"


def test_update_forbidden(client, db, admin_user, viewer_user, update_user_data, mock_redis):
    user_id_to_update = admin_user["id"]
    not_admin_access_token = viewer_user["access_token"]

    update_response = client.put(
        url_for("Users.update_user_view", user_id=user_id_to_update),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
        json=update_user_data,
    )
    assert (
        update_response.status_code == 403
    ), f"Expected 403, got {update_response.status_code}: {update_response.data}"
