from flask import url_for


def test_register_view(client, new_user_data):
    response = client.post(url_for("Auth.register_view"), json=new_user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == new_user_data["username"]


def test_register_view_existing_user(client, new_user_data):
    client.post(url_for("Auth.register_view"), json=new_user_data)
    response = client.post(url_for("Auth.register_view"), json=new_user_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Username already exists"
