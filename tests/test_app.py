from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Basketball Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Basketball Club"
    email = "duplicate@mergington.edu"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Basketball Club"
    email = "removeme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]
