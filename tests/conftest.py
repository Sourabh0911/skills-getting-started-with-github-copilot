"""Pytest configuration and fixtures for API tests"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for testing"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to original state before each test"""
    # Store original state
    original_activities = {
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()
        }
        for key, value in activities.items()
    }
    
    yield
    
    # Restore original state after test
    for activity_name in activities:
        activities[activity_name]["participants"] = original_activities[activity_name]["participants"].copy()
