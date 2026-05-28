import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_requests_within_limit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for _ in range(5):
            r = await client.get("/", headers={"X-API-Key": "test-user-1"})
            assert r.status_code == 200

@pytest.mark.asyncio
async def test_rate_limit_exceeded():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for _ in range(10):
            await client.get("/", headers={"X-API-Key": "test-user-burst"})
        r = await client.get("/", headers={"X-API-Key": "test-user-burst"})
        assert r.status_code == 429
        assert r.json()["error"] == "Rate limit exceeded"

@pytest.mark.asyncio
async def test_different_clients_independent():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for _ in range(10):
            await client.get("/", headers={"X-API-Key": "heavy-user"})
        # a different client should still be allowed
        r = await client.get("/", headers={"X-API-Key": "new-user"})
        assert r.status_code == 200

@pytest.mark.asyncio
async def test_rate_limit_headers_present():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/", headers={"X-API-Key": "header-test"})
        assert "X-RateLimit-Remaining" in r.headers