from flask import url_for


def test_logout_view(client, db, new_user_data, mock_redis):
    client.post(url_for("Auth.register_view"), json=new_user_data)
    login_response = client.post(url_for("Auth.login_view"), json=new_user_data)
    refresh_token = login_response.get_json()["refresh_token"]

    mock_redis.get.return_value = None

    response = client.post(
        url_for("Auth.logout_view"),
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Successfully logged out"


def test_logout_view_with_revoked_token(client, db, new_user_data, mock_redis):
    client.post(url_for("Auth.register_view"), json=new_user_data)
    login_response = client.post(url_for("Auth.login_view"), json=new_user_data)
    refresh_token = login_response.get_json()["refresh_token"]

    mock_redis.get.return_value = "true"

    response = client.post(
        url_for("Auth.logout_view"),
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Token is revoked"
