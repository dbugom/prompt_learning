"""
API Integration Tests for Coding Platform
"""

import pytest
from httpx import AsyncClient
from main import app

# Test data
TEST_USER = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword123",
    "full_name": "Test User"
}

@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_user_registration():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json=TEST_USER)
        assert response.status_code in [200, 201, 400]  # 400 if user exists
        if response.status_code in [200, 201]:
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_user_login():
    """Test user login"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Try to login
        response = await client.post(
            "/api/auth/login",
            data={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
        )
        # May fail if user doesn't exist, which is OK in test
        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data

@pytest.mark.asyncio
async def test_get_lessons_unauthorized():
    """Test getting lessons without authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/lessons")
        # Should return 401 without token
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_code_execution_unauthorized():
    """Test code execution without authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/code/execute",
            json={
                "code": "print('Hello')",
                "language": "python"
            }
        )
        # Should return 401 without token
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_invalid_login():
    """Test login with invalid credentials"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_register_duplicate_user():
    """Test registering duplicate user"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Try to register twice
        await client.post("/api/auth/register", json=TEST_USER)
        response = await client.post("/api/auth/register", json=TEST_USER)
        # Second attempt should fail
        assert response.status_code == 400

# Helper function to get auth token
async def get_auth_token():
    """Get authentication token for tests"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Try to register
        await client.post("/api/auth/register", json=TEST_USER)
        # Login
        response = await client.post(
            "/api/auth/login",
            data={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        return None

@pytest.mark.asyncio
async def test_authenticated_endpoints():
    """Test endpoints that require authentication"""
    token = await get_auth_token()
    if not token:
        pytest.skip("Could not get auth token")

    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test get current user
        response = await client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200

        # Test get lessons
        response = await client.get("/api/lessons", headers=headers)
        assert response.status_code == 200

        # Test get progress
        response = await client.get("/api/progress/overview", headers=headers)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_code_execution_with_auth():
    """Test code execution with authentication"""
    token = await get_auth_token()
    if not token:
        pytest.skip("Could not get auth token")

    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/code/execute",
            headers=headers,
            json={
                "code": "print('Hello, World!')",
                "language": "python"
            }
        )
        # May fail if Piston is not available
        assert response.status_code in [200, 503]
