"""Tests for the unregister endpoints."""
import pytest


def test_unregister_existing_participant(client, reset_activities):
    """Test unregistering an existing participant."""
    response = client.post(
        "/activities/Chess%20Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the participant was actually removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_participant(client, reset_activities):
    """Test unregistering a participant who is not signed up."""
    response = client.post(
        "/activities/Chess%20Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_from_nonexistent_activity(client, reset_activities):
    """Test unregistering from a non-existent activity."""
    response = client.post(
        "/activities/Nonexistent%20Club/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_then_signup_again(client, reset_activities):
    """Test that a participant can sign up again after unregistering."""
    email = "michael@mergington.edu"
    
    # First unregister
    response = client.post(
        "/activities/Chess%20Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Then sign up again
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify they are signed up
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]


def test_unregister_multiple_participants(client, reset_activities):
    """Test unregistering multiple participants."""
    # Drama Club has marcus and lily
    response1 = client.post(
        "/activities/Drama%20Club/unregister",
        params={"email": "marcus@mergington.edu"}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        "/activities/Drama%20Club/unregister",
        params={"email": "lily@mergington.edu"}
    )
    assert response2.status_code == 200
    
    # Verify both are removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert len(activities["Drama Club"]["participants"]) == 0
