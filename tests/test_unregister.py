"""Tests for POST /unregister endpoint"""
import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities"""

    def test_successful_unregister(self, client, reset_activities):
        """Arrange: Student is signed up for activity
           Act: Send unregister request
           Assert: Student is removed and success message returned"""
        # Arrange
        activity = "Soccer Team"
        email = "liam@mergington.edu"  # Already enrolled

        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_participant_removed_after_unregister(self, client, reset_activities):
        """Arrange: Student unregisters from activity
           Act: Retrieve activities after unregister
           Assert: Student is no longer in participants list"""
        # Arrange
        activity = "Soccer Team"
        email = "liam@mergington.edu"

        # Act
        client.post(f"/activities/{activity}/unregister?email={email}")
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email not in activities[activity]["participants"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Arrange: Nonexistent activity name
           Act: Send unregister request for invalid activity
           Assert: 404 error is returned"""
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_enrolled_student_returns_400(self, client, reset_activities):
        """Arrange: Student is not enrolled in activity
           Act: Send unregister request for activity they're not in
           Assert: 400 error with not registered message returned"""
        # Arrange
        activity = "Math Club"
        email = "not_enrolled@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_availability_increases_after_unregister(self, client, reset_activities):
        """Arrange: Check participant count before unregister
           Act: Unregister a student
           Assert: Participant count decreases by 1"""
        # Arrange
        activity = "Soccer Team"
        email = "liam@mergington.edu"
        
        response_before = client.get("/activities")
        count_before = len(response_before.json()[activity]["participants"])

        # Act
        client.post(f"/activities/{activity}/unregister?email={email}")
        response_after = client.get("/activities")
        count_after = len(response_after.json()[activity]["participants"])

        # Assert
        assert count_after == count_before - 1
