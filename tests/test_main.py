from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
import uuid

client = TestClient(app)

# Global variables to store access token and asset_id
access_token = None
test_asset_id = "A1"
random_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

def test_signup():
    
    response = client.post("/users/signup", json={
        "e_name": "Test User",
        "e_id": "123",
        "e_email": random_email,
        "assets": [],
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login():
    global access_token
    response = client.post("/users/login", data={
        "username": random_email,
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    assert "access_token" in response.json()

def test_get_users_unauthorized():
    """Ensure unauthorized users cannot fetch the users list"""
    response = client.get("/users/users")
    assert response.status_code == 401  # Unauthorized

def test_get_all_users():
    """Fetch all users (should succeed with authentication)"""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/users", headers=headers)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of users
    assert len(response.json()) > 0  # At least one user should exist

def test_add_asset():
    """Add an asset to the authenticated user's account"""
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/assets/assets", json={
        "asset_id": test_asset_id,
        "asset_desc": "Laptop",
        "asset_type": "Electronics",
        "asset_expiry": "2026-01-01"
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["asset_id"] == test_asset_id

def test_get_assets():
    """Retrieve all assets for the authenticated user"""
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/assets/assets", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(asset["asset_id"] == test_asset_id for asset in response.json())  # Ensure test asset exists

def test_delete_asset():
    """Delete an asset and verify it's removed"""
    headers = {"Authorization": f"Bearer {access_token}"}

    # Send DELETE request
    response = client.delete(f"/assets/assets/{test_asset_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Asset deleted"

    # Verify asset is removed
    response = client.get("/assets/assets", headers=headers)
    assert response.status_code == 200
    assert not any(asset["asset_id"] == test_asset_id for asset in response.json())  # Ensure asset is gone
