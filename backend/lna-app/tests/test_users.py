from fastapi.testclient import TestClient
from lna_app.main import app

client = TestClient(app)


valid_token = "valid_jwt_token"
invalid_token = "abc"


def test_get_current_user_details() -> None:
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_user_preferences() -> None:
    # Valid token test
    response = client.post(
        "/api/users/update-preferences",
        json={"language": "en", "source_ids": ["source1", "source2"]},
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "User preferences updated successfully",
        "user_id": "some_user_id",
    }

    # Invalid token test
    response = client.post(
        "/api/users/update-preferences",
        json={"language": "en", "source_ids": ["source1", "source2"]},
        headers={"Authorization": f"Bearer {invalid_token}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}

    # No token test
    response = client.post(
        "/api/users/update-preferences",
        json={"language": "en", "source_ids": ["source1", "source2"]},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}
