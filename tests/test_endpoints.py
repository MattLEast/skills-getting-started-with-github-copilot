"""Happy path tests for API endpoints using AAA pattern.

Arrange: Setup the test data and client.
Act: Execute the API call.
Assert: Verify the response and state.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, fresh_activities):
        """Verify GET /activities returns all activities with correct structure."""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == 3
        assert all(activity in data for activity in expected_activities)
        assert all("description" in data[activity] for activity in data)
        assert all("participants" in data[activity] for activity in data)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_adds_participant_to_activity(self, client, fresh_activities):
        """Verify signup successfully adds a participant to an activity."""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in fresh_activities[activity_name]["participants"]
        assert f"Signed up {email}" in data["message"]
    
    def test_signup_increments_participant_count(self, client, fresh_activities):
        """Verify participant count increases after signup."""
        # Arrange
        activity_name = "Gym Class"
        initial_count = len(fresh_activities[activity_name]["participants"])
        email = "sarah@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        final_count = len(fresh_activities[activity_name]["participants"])
        
        # Assert
        assert final_count == initial_count + 1


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_removes_participant_from_activity(self, client, fresh_activities):
        """Verify unregister successfully removes a participant."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert email not in fresh_activities[activity_name]["participants"]
        assert f"Unregistered {email}" in data["message"]
    
    def test_unregister_decrements_participant_count(self, client, fresh_activities):
        """Verify participant count decreases after unregister."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        final_count = len(fresh_activities[activity_name]["participants"])
        
        # Assert
        assert final_count == initial_count - 1
