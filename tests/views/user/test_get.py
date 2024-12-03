from flask import url_for


def test_get_all_success(client, db, mock_redis, admin_user):
    access_token = admin_user["access_token"]
    response = client.get(
        url_for("Users.get_all_users_view"), headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) == 1, "Expected only one user created"


def test_get_all_unauthorized(client):
    response = client.get(url_for("Users.get_all_users_view"))
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"


def test_get_all_forbidden(client, db, mock_redis, viewer_user):
    not_admin_access_token = viewer_user["access_token"]

    response = client.get(
        url_for("Users.get_all_users_view"),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
    )
    assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"


def test_get_success(client, db, mock_redis, admin_user, viewer_user):
    access_token = admin_user["access_token"]
    user_id_to_get = viewer_user["id"]

    response = client.get(
        url_for("Users.get_user_view", user_id=user_id_to_get),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert (
        data["username"] == viewer_user["user_data"]["username"]
    ), f"Expected username {viewer_user["user_data"]["username"]}, got {data['username']}"


def test_get_unauthorized(client):
    response = client.get(url_for("Users.get_user_view", user_id=1))
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"


def test_get_forbidden(client, db, mock_redis, viewer_user):
    not_admin_access_token = viewer_user["access_token"]

    response = client.get(
        url_for("Users.get_user_view", user_id=1),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
    )
    assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"
