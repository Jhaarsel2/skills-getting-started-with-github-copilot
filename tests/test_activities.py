"""Tests for the activities endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_get_activities(client, reset_activities):
    """Test fetching all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check that we have activities
    assert len(data) > 0
    
    # Check that Chess Club exists
    assert "Chess Club" in data
    
    # Check the structure of an activity
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess


def test_get_activities_chess_club_details(client, reset_activities):
    """Test that Chess Club has expected details."""
    response = client.get("/activities")
    data = response.json()
    chess = data["Chess Club"]
    
    assert chess["max_participants"] == 12
    assert "michael@mergington.edu" in chess["participants"]
    assert "daniel@mergington.edu" in chess["participants"]


def test_root_redirect(client):
    """Test that root endpoint redirects to static page."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
