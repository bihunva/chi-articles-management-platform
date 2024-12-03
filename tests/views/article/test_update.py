import pytest
from flask import url_for


@pytest.fixture
def update_article_data():
    return {
        "title": "Updated Article",
        "content": "Updated content of the article",
    }


def test_update_author(client, db, viewer_user, article_by_viewer, update_article_data):
    access_token = viewer_user["access_token"]
    article_id_to_update = article_by_viewer["id"]

    response = client.put(
        url_for("Articles.update_article_view", article_id=article_id_to_update),
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_article_data,
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert data["title"] == update_article_data["title"]
    assert data["content"] == update_article_data["content"]
    assert data["author_id"] == viewer_user["id"]


def test_update_admin(
    client, db, admin_user, viewer_user, article_by_viewer, update_article_data
):
    admin_access_token = admin_user["access_token"]
    article_id_to_update = article_by_viewer["id"]

    response = client.put(
        url_for("Articles.update_article_view", article_id=article_id_to_update),
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=update_article_data,
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.get_json()
    assert data["title"] == update_article_data["title"]
    assert data["content"] == update_article_data["content"]
    assert data["author_id"] == viewer_user["id"]


def test_update_unauthorized(client, db, article_by_admin, update_article_data):
    article_id_to_update = article_by_admin["id"]

    response = client.put(
        url_for("Articles.update_article_view", article_id=article_id_to_update),
        json=update_article_data,
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"


def test_update_not_author(client, db, viewer_user, article_by_admin, update_article_data):
    not_admin_access_token = viewer_user["access_token"]
    article_id_to_delete = article_by_admin["id"]

    response = client.put(
        url_for("Articles.update_article_view", article_id=article_id_to_delete),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
        json=update_article_data,
    )
    assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"
    assert response.get_json()["message"] == "You can only modify your own articles"
