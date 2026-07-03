from httpx import AsyncClient


class TestAuth:
    async def test_login_success_admin(self, client: AsyncClient, admin_user):
        response = await client.post(
            "/api/v1/auth/login",
            json={"login": "admin", "password": "admin"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_success_user(self, client: AsyncClient, regular_user):
        response = await client.post(
            "/api/v1/auth/login",
            json={"login": "user", "password": "user"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    async def test_login_wrong_password(self, client: AsyncClient, admin_user):
        response = await client.post(
            "/api/v1/auth/login",
            json={"login": "admin", "password": "wrong"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    async def test_login_nonexistent_user(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/login",
            json={"login": "nobody", "password": "nobody"},
        )
        assert response.status_code == 401
