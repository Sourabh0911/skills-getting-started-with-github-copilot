"""Tests for GET /activities endpoint"""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""

    def test_get_activities_returns_all_activities(self, client):
        """Arrange: Activities exist in the database
           Act: Make GET request to /activities
           Assert: Response contains all activities"""
        # Arrange
        expected_activity_count = 9  # Based on app.py initial data

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count

    def test_get_activities_returns_correct_structure(self, client):
        """Arrange: Activities endpoint exists
           Act: Get activities response
           Assert: Each activity has required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_includes_participants(self, client):
        """Arrange: Activities have enrolled participants
           Act: Fetch activities
           Assert: Participants are included in response"""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        soccer_activity = activities.get("Soccer Team")
        assert soccer_activity is not None
        assert len(soccer_activity["participants"]) > 0
