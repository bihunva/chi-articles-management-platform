from flask import url_for


def test_create_success(client, db, admin_user, new_article_data):
    access_token = admin_user["access_token"]
    current_user_id = admin_user["id"]

    create_response = client.post(
        url_for("Articles.create_article_view"),
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_article_data,
    )
    assert (
        create_response.status_code == 201
    ), f"Expected 201, got {create_response.status_code}: {create_response.data}"
    data = create_response.get_json()
    assert data["title"] == new_article_data["title"]
    assert data["content"] == new_article_data["content"]
    assert "id" in data
    assert "author_id" in data
    assert (
        data["author_id"] == current_user_id
    ), f"Expected author_id to be {current_user_id}, got {data['author_id']}"


def test_create_article_unauthorized(client, new_article_data):
    create_response = client.post(url_for("Articles.create_article_view"), json=new_article_data)
    assert (
        create_response.status_code == 401
    ), f"Expected 401, got {create_response.status_code}: {create_response.data}"
