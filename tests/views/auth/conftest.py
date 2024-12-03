import pytest


@pytest.fixture
def new_user_data():
    return {
        "username": "test_user",
        "password": "test_password",
    }
