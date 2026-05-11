"""Tests for POST /signup endpoint"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities"""

    def test_successful_signup(self, client, reset_activities):
        """Arrange: Student is not signed up for an activity
           Act: Send signup request with valid data
           Assert: Student is added and success message returned"""
        # Arrange
        activity = "Math Club"
        email = "new_student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_participant_added_after_signup(self, client, reset_activities):
        """Arrange: Student signs up for activity
           Act: Retrieve activities after signup
           Assert: Student appears in participants list"""
        # Arrange
        activity = "Math Club"
        email = "test_student@mergington.edu"

        # Act
        client.post(f"/activities/{activity}/signup?email={email}")
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity]["participants"]

    def test_signup_to_nonexistent_activity_returns_404(self, client):
        """Arrange: Nonexistent activity name
           Act: Send signup request for invalid activity
           Assert: 404 error is returned"""
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_duplicate_signup_returns_400(self, client, reset_activities):
        """Arrange: Student already signed up for activity
           Act: Send signup request for same activity
           Assert: 400 error with duplicate message returned"""
        # Arrange
        activity = "Soccer Team"
        email = "liam@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_multiple_activities_signup(self, client, reset_activities):
        """Arrange: Student wants to sign up for multiple activities
           Act: Sign up for multiple different activities
           Assert: Student appears in all activity participant lists"""
        # Arrange
        email = "multi_student@mergington.edu"
        activities_to_join = ["Math Club", "Chess Club", "Art Studio"]

        # Act
        for activity in activities_to_join:
            client.post(f"/activities/{activity}/signup?email={email}")

        response = client.get("/activities")
        all_activities = response.json()

        # Assert
        for activity in activities_to_join:
            assert email in all_activities[activity]["participants"]
