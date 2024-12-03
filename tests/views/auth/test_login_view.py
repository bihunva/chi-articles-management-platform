from flask import url_for


def test_login(client, new_user_data):
    client.post(url_for("Auth.register_view"), json=new_user_data)
    response = client.post(url_for("Auth.login_view"), json=new_user_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials(client):
    invalid_user = {"username": "wrong", "password": "wrong"}
    response = client.post(url_for("Auth.login_view"), json=invalid_user)
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Invalid credentials"
