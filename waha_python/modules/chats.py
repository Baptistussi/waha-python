"""
Chats module for WAHA Python client
"""

import builtins
from typing import Any

from ..base_module import BaseModule


class ChatsModule(BaseModule):
    """
    Module for managing WhatsApp chats
    """

    async def list(
        self,
        session: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all chats

        Args:
            session: Session name
            limit: Limit number of results
            offset: Skip number of results

        Returns:
            List of chats

        Example:
            .. code-block:: python

                chats = client.chats.list("default")
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return await self.get(f"/api/{session}/chats", params=params if params else None)

    async def get_overview(self, session: str) -> dict[str, Any]:
        """
        Get chats overview

        Args:
            session: Session name

        Returns:
            Chats overview

        Example:
            .. code-block:: python

                overview = client.chats.get_overview("default")
        """
        return await self.get(f"/api/{session}/chats/overview")

    async def get_picture(
        self, session: str, chat_id: str, accept_json: bool = False
    ) -> Any:
        """
        Get chat picture

        Args:
            session: Session name
            chat_id: Chat ID
            accept_json: If True, returns JSON with base64 data

        Returns:
            Picture data

        Example:
            .. code-block:: python

                picture = client.chats.get_picture("default", "1234567890@c.us")
        """
        endpoint = f"/api/{session}/chats/{chat_id}/picture"

        if accept_json:
            headers = {"Accept": "application/json"}
            return await self.client.request("GET", endpoint, headers=headers)

        return await self.get(endpoint)

    async def unread(self, session: str, chat_id: str) -> dict[str, Any]:
        """
        Mark chat as unread

        Args:
            session: Session name
            chat_id: Chat ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.chats.unread("default", "1234567890@c.us")
        """
        return await self.post(f"/api/{session}/chats/{chat_id}/unread")

    async def archive(self, session: str, chat_id: str) -> dict[str, Any]:
        """
        Archive a chat

        Args:
            session: Session name
            chat_id: Chat ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.chats.archive("default", "1234567890@c.us")
        """
        return await self.post(f"/api/{session}/chats/{chat_id}/archive")

    async def unarchive(self, session: str, chat_id: str) -> dict[str, Any]:
        """
        Unarchive a chat

        Args:
            session: Session name
            chat_id: Chat ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.chats.unarchive("default", "1234567890@c.us")
        """
        return await self.post(f"/api/{session}/chats/{chat_id}/unarchive")

    async def delete(self, session: str, chat_id: str) -> dict[str, Any]:
        """
        Delete a chat

        Args:
            session: Session name
            chat_id: Chat ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.chats.delete("default", "1234567890@c.us")
        """
        return await self.request("DELETE", f"/api/{session}/chats/{chat_id}")

    async def read_messages(
        self,
        session: str,
        chat_id: str,
        message_ids: builtins.list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Read messages in a chat

        Args:
            session: Session name
            chat_id: Chat ID
            message_ids: Optional list of message IDs to read

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.chats.read_messages("default", "1234567890@c.us")
        """
        data: dict[str, Any] = {}
        if message_ids:
            data["messageIds"] = message_ids

        return await self.post(
            f"/api/{session}/chats/{chat_id}/messages/read", json_data=data
        )

    async def get_messages(
        self,
        session: str,
        chat_id: str,
        limit: int | None = None,
        download_media: bool = False,
    ) -> builtins.list[dict[str, Any]]:
        """
        Get messages from a chat

        Args:
            session: Session name
            chat_id: Chat ID
            limit: Limit number of messages
            download_media: Download media files

        Returns:
            List of messages

        Example:
            .. code-block:: python

                messages = client.chats.get_messages("default", "1234567890@c.us", limit=100)
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if download_media:
            params["downloadMedia"] = True

        return await self.get(
            f"/api/{session}/chats/{chat_id}/messages",
            params=params if params else None,
        )

    async def get_message(
        self, session: str, chat_id: str, message_id: str, download_media: bool = False
    ) -> dict[str, Any]:
        """
        Get a specific message by ID

        Args:
            session: Session name
            chat_id: Chat ID
            message_id: Message ID
            download_media: Download media file

        Returns:
            Message data

        Example:
            .. code-block:: python

                message = client.chats.get_message(
                    "default",
                    "1234567890@c.us",
                    "false_1234567890@c.us_AAAAAAAAAAAAAAAAAA"
                )
        """
        params = {}
        if download_media:
            params["downloadMedia"] = True

        return await self.get(
            f"/api/{session}/chats/{chat_id}/messages/{message_id}",
            params=params if params else None,
        )

