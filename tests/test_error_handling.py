"""Error handling and edge case tests using AAA pattern.

Tests for validation, error responses, and data integrity.
"""

import pytest


class TestSignupErrors:
    """Tests for error cases in signup endpoint."""
    
    def test_signup_nonexistent_activity_returns_404(self, client, fresh_activities):
        """Verify signup to non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_email_returns_400(self, client, fresh_activities):
        """Verify duplicate signup returns 400 error."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_preserves_existing_participants(self, client, fresh_activities):
        """Verify new signup doesn't remove existing participants."""
        # Arrange
        activity_name = "Programming Class"
        existing_email = "emma@mergington.edu"
        new_email = "alex@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        participants = fresh_activities[activity_name]["participants"]
        
        # Assert
        assert existing_email in participants
        assert new_email in participants


class TestUnregisterErrors:
    """Tests for error cases in unregister endpoint."""
    
    def test_unregister_nonexistent_activity_returns_404(self, client, fresh_activities):
        """Verify unregister from non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in data["detail"]
    
    def test_unregister_not_signed_up_returns_400(self, client, fresh_activities):
        """Verify unregister of non-participant returns 400 error."""
        # Arrange
        activity_name = "Gym Class"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_preserves_other_participants(self, client, fresh_activities):
        """Verify unregister only removes the specified participant."""
        # Arrange - sign up multiple people
        activity_name = "Gym Class"
        email1 = "user1@mergington.edu"
        email2 = "user2@mergington.edu"
        
        client.post(f"/activities/{activity_name}/signup", params={"email": email1})
        client.post(f"/activities/{activity_name}/signup", params={"email": email2})
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email1}
        )
        participants = fresh_activities[activity_name]["participants"]
        
        # Assert
        assert email1 not in participants
        assert email2 in participants
