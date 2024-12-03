from flask import url_for


def test_delete_success(client, db, mock_redis, admin_user, viewer_user):
    admin_access_token = admin_user["access_token"]
    user_id_to_delete = viewer_user["id"]

    delete_response = client.delete(
        url_for("Users.delete_user_view", user_id=user_id_to_delete),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert (
        delete_response.status_code == 200
    ), f"Expected 200, got {delete_response.status_code}: {delete_response.data}"
    assert delete_response.get_json()["message"] == "User deleted successfully"


def test_delete_forbidden(client, db, mock_redis, admin_user, viewer_user):
    not_admin_access_token = viewer_user["access_token"]
    user_id_to_delete = admin_user["id"]

    delete_response = client.delete(
        url_for("Users.delete_user_view", user_id=user_id_to_delete),
        headers={"Authorization": f"Bearer {not_admin_access_token}"},
    )
    assert (
        delete_response.status_code == 403
    ), f"Expected 403, got {delete_response.status_code}: {delete_response.data}"
