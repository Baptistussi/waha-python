"""
Base module class for WAHA Python client
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import WAHAClient


class BaseModule:
    """
    Base class for all WAHA modules

    Provides common functionality for sub-modules
    """

    def __init__(self, client: "WAHAClient"):
        """
        Initialize the module

        Args:
            client: WAHA client instance
        """
        self.client = client

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Any:
        """Proxy method to client request"""
        return await self.client.request(
            method, endpoint, params=params, json_data=json_data, **kwargs
        )

    async def get(
        self, *args: Any, **kwargs: Any
    ) -> dict[str, Any] | Any:
        """Proxy method to client get"""
        return await self.client.get(*args, **kwargs)

    async def post(
        self, *args: Any, **kwargs: Any
    ) -> dict[str, Any] | Any:
        """Proxy method to client post"""
        return await self.client.post(*args, **kwargs)

    async def put(
        self, *args: Any, **kwargs: Any
    ) -> dict[str, Any] | Any:
        """Proxy method to client put"""
        return await self.client.put(*args, **kwargs)

    async def delete(
        self, *args: Any, **kwargs: Any
    ) -> dict[str, Any] | Any:
        """Proxy method to client delete"""
        return await self.client.delete(*args, **kwargs)
