"""Tests for the signup endpoints."""
import pytest


def test_signup_new_participant(client, reset_activities):
    """Test signing up a new participant for an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_duplicate_participant(client, reset_activities):
    """Test that duplicate signups are rejected."""
    # Michael is already in Chess Club
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup to a non-existent activity."""
    response = client.post(
        "/activities/Nonexistent%20Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_multiple_students(client, reset_activities):
    """Test that multiple different students can sign up."""
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    for email in emails:
        response = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200


def test_signup_response_includes_activity_name(client, reset_activities):
    """Test that signup response includes the activity name."""
    response = client.post(
        "/activities/Tennis%20Club/signup",
        params={"email": "tennis_player@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Tennis Club" in data["message"]
    assert "tennis_player@mergington.edu" in data["message"]
