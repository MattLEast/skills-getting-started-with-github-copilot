"""Pytest configuration and shared fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """Provide fresh activities data for each test to ensure isolation.
    
    Uses monkeypatch to replace the module-level activities dict with test data.
    """
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }
    
    # Replace the module-level activities with test data
    monkeypatch.setitem(activities, "Chess Club", test_activities["Chess Club"])
    monkeypatch.setitem(activities, "Programming Class", test_activities["Programming Class"])
    monkeypatch.setitem(activities, "Gym Class", test_activities["Gym Class"])
    
    # Clear any extra activities
    for key in list(activities.keys()):
        if key not in test_activities:
            monkeypatch.delitem(activities, key)
    
    return activities
