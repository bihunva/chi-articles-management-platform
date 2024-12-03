from flask import url_for


def test_get_all_success(client, db, admin_user, article_by_admin):
    access_token = admin_user["access_token"]

    response = client.get(
        url_for("Articles.get_all_articles_view"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert len(data) == 1, f"Expected 1 article, got {len(data)}"
    assert data[0]["title"] == article_by_admin["title"]
    assert data[0]["content"] == article_by_admin["content"]


def test_get_all_unauthorized(client):
    response = client.get(url_for("Articles.get_all_articles_view"))
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"


def test_get_success(client, db, admin_user, article_by_admin):
    access_token = admin_user["access_token"]

    article_id_to_get = article_by_admin["id"]

    response = client.get(
        url_for("Articles.get_article_view", article_id=article_id_to_get),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert data["title"] == article_by_admin["title"]
    assert data["content"] == article_by_admin["content"]


def test_get_unauthorized(client):
    response = client.get(url_for("Articles.get_article_view", article_id=1))
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"
