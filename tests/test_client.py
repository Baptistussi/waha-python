"""
Unit tests for WAHA Python client (async, httpx)
"""

import asyncio
import json

import httpx
import pytest

from waha_python import (
    WAHAAuthenticationError,
    WAHAClient,
    WAHAClientError,
    WAHANotFoundError,
    WAHARateLimitError,
    WAHAServerError,
)


def make_client(handler):
    """Build a WAHAClient backed by an httpx MockTransport."""
    client = WAHAClient(base_url="http://localhost:3000", api_key="test-key")
    client._client = httpx.AsyncClient(
        base_url=client.base_url,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Api-Key": "test-key",
        },
        timeout=httpx.Timeout(30.0),
        transport=httpx.MockTransport(handler),
    )
    return client


def run(coro):
    """Run an async coroutine to completion."""
    return asyncio.run(coro)


def test_client_initialization():
    """Test client initialization and module wiring."""
    client = WAHAClient(base_url="http://localhost:3000", api_key="test-key")
    assert client.base_url == "http://localhost:3000"
    assert client.api_key == "test-key"
    assert client.timeout == 30.0
    for attr in ("sessions", "messages", "chats", "contacts", "groups", "status", "channels"):
        assert hasattr(client, attr)


def test_api_key_header():
    """The API key must be sent as the X-Api-Key header."""
    captured = {}

    async def handler(request: httpx.Request):
        captured["header"] = request.headers.get("X-Api-Key")
        return httpx.Response(200, json={"ok": True})

    async def go():
        async with make_client(handler) as client:
            await client.get("/api/sessions")

    run(go())
    assert captured["header"] == "test-key"


def test_handle_json_response():
    """A 200 JSON response is returned as parsed data."""

    async def handler(request):
        return httpx.Response(200, json={"status": "WORKING"})

    async def go():
        async with make_client(handler) as client:
            return await client.get("/api/sessions/default")

    assert run(go()) == {"status": "WORKING"}


@pytest.mark.parametrize(
    "status,exc",
    [
        (401, WAHAAuthenticationError),
        (404, WAHANotFoundError),
        (429, WAHARateLimitError),
        (500, WAHAServerError),
    ],
)
def test_error_mapping(status, exc):
    """Error HTTP statuses map to their dedicated exceptions."""

    async def handler(request):
        return httpx.Response(status, json={"message": "boom"})

    async def go():
        async with make_client(handler) as client:
            await client.get("/api/sessions")

    with pytest.raises(exc):
        run(go())


def test_connection_error_maps_to_client_error():
    """A transport/connection failure raises WAHAClientError."""

    def handler(request):
        raise httpx.ConnectError("boom")

    async def go():
        async with make_client(handler) as client:
            await client.get("/api/sessions")

    with pytest.raises(WAHAClientError):
        run(go())


def test_send_text():
    """messages.send_text posts JSON to the sendText endpoint."""

    async def handler(request: httpx.Request):
        assert request.method == "POST"
        assert request.url.path == "/api/sendText"
        assert json.loads(request.content.decode()) == {
            "session": "default",
            "chatId": "1234567890@c.us",
            "text": "Hello!",
        }
        return httpx.Response(200, json={"id": "msg1"})

    async def go():
        async with make_client(handler) as client:
            return await client.messages.send_text("default", "1234567890@c.us", "Hello!")

    assert run(go()) == {"id": "msg1"}


def test_list_sessions():
    """sessions.list returns parsed session data."""

    async def handler(request: httpx.Request):
        assert request.method == "GET"
        assert request.url.path == "/api/sessions"
        return httpx.Response(200, json=[{"name": "default"}])

    async def go():
        async with make_client(handler) as client:
            return await client.sessions.list(all_sessions=True)

    assert run(go()) == [{"name": "default"}]


def test_context_manager_closes_client():
    """The async context manager closes the underlying httpx client."""

    async def handler(request):
        return httpx.Response(200, json={})

    async def go():
        client = make_client(handler)
        async with client:
            pass
        assert client._client.is_closed

    run(go())
