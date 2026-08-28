"""
Channels module for WAHA Python client
"""

import builtins
from typing import Any

from ..base_module import BaseModule


class ChannelsModule(BaseModule):
    """
    Module for managing WhatsApp Channels
    """

    async def list(self, session: str) -> list[dict[str, Any]]:
        """
        List all channels

        Args:
            session: Session name

        Returns:
            List of channels

        Example:
            .. code-block:: python

                channels = client.channels.list("default")
        """
        return await self.client.get(f"/api/{session}/channels")

    async def get(self, session: str, channel_id: str) -> dict[str, Any]:
        """
        Get a specific channel

        Args:
            session: Session name
            channel_id: Channel ID

        Returns:
            Channel data

        Example:
            .. code-block:: python

                channel = client.channels.get("default", "channel_id_here")
        """
        return await self.request("GET", f"/api/{session}/channels/{channel_id}")

    async def create(
        self, session: str, name: str, description: str | None = None
    ) -> dict[str, Any]:
        """
        Create a new channel

        Args:
            session: Session name
            name: Channel name
            description: Channel description (optional)

        Returns:
            Created channel data

        Example:
            .. code-block:: python

                channel = client.channels.create("default", "My Channel")
        """
        data: dict[str, Any] = {"name": name}
        if description:
            data["description"] = description

        return await self.post(f"/api/{session}/channels", json_data=data)

    async def delete(self, session: str, channel_id: str) -> dict[str, Any]:
        """
        Delete a channel

        Args:
            session: Session name
            channel_id: Channel ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.channels.delete("default", "channel_id_here")
        """
        return await self.request("DELETE", f"/api/{session}/channels/{channel_id}")

    async def get_messages(
        self, session: str, channel_id: str, limit: int | None = None
    ) -> builtins.list[dict[str, Any]]:
        """
        Get messages from a channel

        Args:
            session: Session name
            channel_id: Channel ID
            limit: Limit number of messages

        Returns:
            List of messages

        Example:
            .. code-block:: python

                messages = client.channels.get_messages("default", "channel_id_here")
        """
        params = {}
        if limit is not None:
            params["limit"] = limit

        return await self.client.get(
            f"/api/{session}/chats/{channel_id}/messages",
            params=params if params else None,
        )

