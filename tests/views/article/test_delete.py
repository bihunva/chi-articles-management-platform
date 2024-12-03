from flask import url_for


def test_delete_author(client, db, viewer_user, article_by_viewer):
    access_token = viewer_user["access_token"]
    article_id_to_delete = article_by_viewer["id"]

    delete_response = client.delete(
        url_for("Articles.delete_article_view", article_id=article_id_to_delete),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert (
        delete_response.status_code == 200
    ), f"Expected 200, got {delete_response.status_code}: {delete_response.data}"
    assert delete_response.get_json()["message"] == "Article deleted successfully"


def test_delete_unauthorized(client, db):
    delete_response = client.delete(url_for("Articles.delete_article_view", article_id=1))
    assert (
        delete_response.status_code == 401
    ), f"Expected 401, got {delete_response.status_code}: {delete_response.data}"


def test_delete_not_author(client, db, viewer_user, article_by_admin):
    not_admin_access_token = viewer_user["access_token"]
    article_id_to_delete = article_by_admin["id"]

    delete_response = client.delete(
        url_for("Articles.delete_article_view", article_id=article_id_to_delete),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
    )
    assert (
        delete_response.status_code == 403
    ), f"Expected 403, got {delete_response.status_code}: {delete_response.data}"
    assert delete_response.get_json()["message"] == "You can only delete your own articles"


def test_delete_admin(client, db, admin_user, article_by_viewer):
    access_token = admin_user["access_token"]
    article_id_to_delete = article_by_viewer["id"]

    delete_response = client.delete(
        url_for("Articles.delete_article_view", article_id=article_id_to_delete),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert (
        delete_response.status_code == 200
    ), f"Expected 200, got {delete_response.status_code}: {delete_response.data}"
    assert delete_response.get_json()["message"] == "Article deleted successfully"


def test_delete_editor_not_author(client, db, editor_user, article_by_viewer):
    editor_access_token = editor_user["access_token"]
    article_id_to_delete = editor_user["id"]

    delete_response = client.delete(
        url_for("Articles.delete_article_view", article_id=article_id_to_delete),
        headers={"Authorization": f"Bearer {editor_access_token}"},
    )
    assert (
        delete_response.status_code == 403
    ), f"Expected 403, got {delete_response.status_code}: {delete_response.data}"
    assert delete_response.get_json()["message"] == "You can only delete your own articles"
