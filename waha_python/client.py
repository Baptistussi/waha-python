"""
Main WAHA Client implementation
"""

from typing import Any

import httpx

from .exceptions import (
    WAHAAuthenticationError,
    WAHAClientError,
    WAHANotFoundError,
    WAHARateLimitError,
    WAHAServerError,
)
from .modules.channels import ChannelsModule
from .modules.chats import ChatsModule
from .modules.contacts import ContactsModule
from .modules.groups import GroupsModule
from .modules.messages import MessagesModule
from .modules.profile import ProfileModule
from .modules.sessions import SessionsModule
from .modules.status import StatusModule


class WAHAClient:
    """
    WAHA (WhatsApp HTTP API) Python Client

    This is the main client class that provides a high-level async interface
    to interact with the WAHA server.

    Args:
        base_url: Base URL of the WAHA server (default: "http://localhost:3000")
        api_key: API key for authentication (optional)
        timeout: Request timeout in seconds (default: 30)

    Example:
        .. code-block:: python

            from waha_python import WAHAClient

            async with WAHAClient(
                base_url="http://localhost:3000",
                api_key="your-api-key-here"
            ) as client:
                # Send a text message
                result = await client.messages.send_text(
                    session="default",
                    chat_id="1234567890@c.us",
                    text="Hello, World!"
                )
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3000",
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the WAHA client

        Args:
            base_url: Base URL of the WAHA server
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout),
        )

        self.sessions = SessionsModule(self)
        self.messages = MessagesModule(self)
        self.chats = ChatsModule(self)
        self.contacts = ContactsModule(self)
        self.groups = GroupsModule(self)
        self.status = StatusModule(self)
        self.profile = ProfileModule(self)
        self.channels = ChannelsModule(self)

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Any:
        """
        Make a request to the WAHA API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/api/sessions")
            params: URL parameters
            json_data: JSON body data
            **kwargs: Additional arguments for httpx

        Returns:
            Response data

        Raises:
            WAHAAuthenticationError: If authentication fails
            WAHANotFoundError: If resource is not found
            WAHARateLimitError: If rate limit is exceeded
            WAHAServerError: If server returns an error
            WAHAClientError: For other errors
        """
        try:
            response = await self._client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json_data,
                **kwargs,
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise WAHAClientError(f"Request timeout: {e}") from e
        except httpx.ConnectError as e:
            raise WAHAClientError(f"Connection error: {e}") from e
        except httpx.HTTPError as e:
            raise WAHAClientError(f"Request failed: {e}") from e

    def _handle_response(self, response: httpx.Response) -> dict[str, Any] | Any:
        """
        Handle the HTTP response

        Args:
            response: HTTP response object

        Returns:
            Response data

        Raises:
            WAHAAuthenticationError: If authentication fails (401)
            WAHANotFoundError: If resource is not found (404)
            WAHARateLimitError: If rate limit is exceeded (429)
            WAHAServerError: If server returns an error (5xx)
        """
        if response.status_code == 401:
            raise WAHAAuthenticationError(
                "Authentication failed. Please check your API key."
            )
        elif response.status_code == 404:
            raise WAHANotFoundError(f"Resource not found: {response.url}")
        elif response.status_code == 429:
            raise WAHARateLimitError("Rate limit exceeded. Please try again later.")
        elif response.status_code >= 500:
            error_msg = self._error_message(response) or "Server error"
            raise WAHAServerError(f"{error_msg} (Status: {response.status_code})")

        if response.status_code in [200, 201, 204]:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            elif "image/" in content_type or "application/octet-stream" in content_type:
                return response.content
            else:
                return response.text

        if response.status_code >= 400:
            error_msg = self._error_message(response)
            if not error_msg:
                error_msg = response.text
            raise WAHAClientError(f"{error_msg} (Status: {response.status_code})")

        return response.text

    @staticmethod
    def _error_message(response: httpx.Response) -> str:
        """Best-effort extraction of an error message from a response body."""
        try:
            data = response.json()
        except ValueError:
            return ""
        if isinstance(data, dict) and data.get("message"):
            return data["message"]
        return ""

    async def get(
        self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any] | Any:
        """Make a GET request"""
        return await self.request("GET", endpoint, params=params, **kwargs)

    async def post(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Any:
        """Make a POST request"""
        return await self.request("POST", endpoint, json_data=json_data, **kwargs)

    async def put(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Any:
        """Make a PUT request"""
        return await self.request("PUT", endpoint, json_data=json_data, **kwargs)

    async def delete(
        self, endpoint: str, **kwargs: Any
    ) -> dict[str, Any] | Any:
        """Make a DELETE request"""
        return await self.request("DELETE", endpoint, **kwargs)

    async def close(self) -> None:
        """Close the client session"""
        await self._client.aclose()

    async def __aenter__(self) -> "WAHAClient":
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit"""
        await self.close()
