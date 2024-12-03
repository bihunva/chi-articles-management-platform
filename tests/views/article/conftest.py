import pytest
from flask import url_for


@pytest.fixture
def new_article_data():
    return {
        "title": "New Article",
        "content": "Content of the new article",
    }


def create_article(client, access_token, article_data):
    response = client.post(
        url_for("Articles.create_article_view"),
        headers={"Authorization": f"Bearer {access_token}"},
        json=article_data,
    )
    article_data["id"] = response.json["id"]
    return article_data


@pytest.fixture
def article_by_admin(client, db, admin_user, new_article_data):
    access_token = admin_user["access_token"]
    return create_article(client, access_token, new_article_data)


@pytest.fixture
def article_by_viewer(client, db, viewer_user, new_article_data):
    access_token = viewer_user["access_token"]
    return create_article(client, access_token, new_article_data)
