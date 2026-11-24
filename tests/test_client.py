import httpx
import pytest

from ai_project_skeleton.client import AsyncAPIClient
from ai_project_skeleton.config import Settings


def create_client(handler, max_retries=2):
    settings = Settings(
        base_url="https://test.example.com",
        max_retries=max_retries,
        retry_backoff_seconds=0,
    )
    transport = httpx.MockTransport(handler)
    return AsyncAPIClient(settings, transport=transport)


@pytest.mark.asyncio
async def test_successful_get_request():
    def handler(request):
        return httpx.Response(200, json={"message": "success"})

    async with create_client(handler) as client:
        response = await client.get("/test")

    assert response.status_code == 200
    assert response.json()["message"] == "success"


@pytest.mark.asyncio
async def test_retry_after_server_error():
    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1

        if attempts == 1:
            return httpx.Response(500)

        return httpx.Response(200, json={"message": "recovered"})

    async with create_client(handler) as client:
        response = await client.get("/test")

    assert response.status_code == 200
    assert attempts == 2


@pytest.mark.asyncio
async def test_retry_exhausted():
    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1
        return httpx.Response(500)

    async with create_client(handler, max_retries=2) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get("/test")

    assert attempts == 3


@pytest.mark.asyncio
async def test_client_does_not_retry_not_found():
    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1
        return httpx.Response(404)

    async with create_client(handler) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get("/missing")

    assert attempts == 1


@pytest.mark.asyncio
async def test_post_request():
    def handler(request):
        return httpx.Response(201, json={"created": True})

    async with create_client(handler) as client:
        response = await client.post("/items", json={"name": "demo"})

    assert response.status_code == 201
    assert response.json()["created"] is True


@pytest.mark.asyncio
async def test_api_key_is_added_to_headers():
    def handler(request):
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(200)

    settings = Settings(
        base_url="https://test.example.com",
        api_key="test-key",
        retry_backoff_seconds=0,
    )

    async with AsyncAPIClient(
        settings,
        transport=httpx.MockTransport(handler),
    ) as client:
        response = await client.get("/test")

    assert response.status_code == 200
