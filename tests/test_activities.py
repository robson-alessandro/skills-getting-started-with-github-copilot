import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        # Arrange
        expected_activity_names = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball", "Tennis Club", "Art Studio", 
            "Drama Club", "Debate Team", "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(expected_activity_names)
        for name in expected_activity_names:
            assert name in data
    
    
    def test_get_activities_returns_activity_structure(self, client, reset_activities):
        # Arrange
        required_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert required_keys.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_participant_success(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_email in response.json()["message"]
    
    
    def test_signup_duplicate_participant_returns_error(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    
    def test_signup_to_nonexistent_activity_returns_404(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    
    def test_signup_updates_participant_count(self, client, reset_activities):
        # Arrange
        activity_name = "Tennis Club"
        new_email = "newplayer@mergington.edu"
        
        # Act - get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act - signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Act - get updated count
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count + 1
        assert new_email in updated_response.json()[activity_name]["participants"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_existing_participant_success(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
    
    
    def test_unregister_removes_participant_from_list(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        # Act - verify participant exists initially
        initial_response = client.get("/activities")
        assert email_to_remove in initial_response.json()[activity_name]["participants"]
        
        # Act - unregister
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Act - verify participant removed
        updated_response = client.get("/activities")
        
        # Assert
        assert email_to_remove not in updated_response.json()[activity_name]["participants"]
    
    
    def test_unregister_nonexistent_participant_returns_error(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        nonexistent_email = "notaparticipant@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": nonexistent_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]
    
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    
    def test_unregister_updates_participant_count(self, client, reset_activities):
        # Arrange
        activity_name = "Programming Class"
        email_to_remove = "emma@mergington.edu"
        
        # Act - get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act - unregister
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Act - get updated count
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count - 1
