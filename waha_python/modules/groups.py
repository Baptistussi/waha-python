"""
Groups module for WAHA Python client
"""

import builtins
from typing import Any

from ..base_module import BaseModule


class GroupsModule(BaseModule):
    """
    Module for managing WhatsApp groups
    """

    async def list(self, session: str) -> list[dict[str, Any]]:
        """
        Get all groups

        Args:
            session: Session name

        Returns:
            List of groups

        Example:
            .. code-block:: python

                groups = client.groups.list("default")
        """
        return await self.client.get(f"/api/{session}/groups")

    async def get_count(self, session: str) -> dict[str, Any]:
        """
        Get count of groups

        Args:
            session: Session name

        Returns:
            Count

        Example:
            .. code-block:: python

                count = client.groups.get_count("default")
        """
        return await self.client.get(f"/api/{session}/groups/count")

    async def get(self, session: str, group_id: str) -> dict[str, Any]:
        """
        Get a specific group

        Args:
            session: Session name
            group_id: Group ID

        Returns:
            Group data

        Example:
            .. code-block:: python

                group = client.groups.get("default", "1234567890@g.us")
        """
        return await self.request("GET", f"/api/{session}/groups/{group_id}")

    async def create(
        self, session: str, subject: str, participants: builtins.list[str] | None = None
    ) -> dict[str, Any]:
        """
        Create a new group

        Args:
            session: Session name
            subject: Group name
            participants: List of participant IDs (optional)

        Returns:
            Created group data

        Example:
            .. code-block:: python

                group = client.groups.create(
                    "default",
                    "My New Group",
                    participants=["1234567890@c.us"]
                )
        """
        data = {"subject": subject}
        if participants:
            data["participants"] = participants

        return await self.post(f"/api/{session}/groups", json_data=data)

    async def leave(self, session: str, group_id: str) -> dict[str, Any]:
        """
        Leave a group

        Args:
            session: Session name
            group_id: Group ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.leave("default", "1234567890@g.us")
        """
        return await self.post(f"/api/{session}/groups/{group_id}/leave")

    async def update_subject(
        self, session: str, group_id: str, subject: str
    ) -> dict[str, Any]:
        """
        Update group subject (name)

        Args:
            session: Session name
            group_id: Group ID
            subject: New subject

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.update_subject(
                    "default", "1234567890@g.us", "New Group Name"
                )
        """
        data = {"subject": subject}
        return await self.put(f"/api/{session}/groups/{group_id}/subject", json_data=data)

    async def update_description(
        self, session: str, group_id: str, description: str
    ) -> dict[str, Any]:
        """
        Update group description

        Args:
            session: Session name
            group_id: Group ID
            description: New description

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.update_description(
                    "default", "1234567890@g.us", "Group description"
                )
        """
        data = {"description": description}
        return await self.put(
            f"/api/{session}/groups/{group_id}/description", json_data=data
        )

    async def get_invite_code(self, session: str, group_id: str) -> dict[str, Any]:
        """
        Get group invite code

        Args:
            session: Session name
            group_id: Group ID

        Returns:
            Invite code

        Example:
            .. code-block:: python

                code = client.groups.get_invite_code("default", "1234567890@g.us")
        """
        return await self.client.get(f"/api/{session}/groups/{group_id}/invite-code")

    async def revoke_invite_code(self, session: str, group_id: str) -> dict[str, Any]:
        """
        Revoke group invite code

        Args:
            session: Session name
            group_id: Group ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.revoke_invite_code("default", "1234567890@g.us")
        """
        return await self.post(f"/api/{session}/groups/{group_id}/invite-code/revoke")

    async def get_picture(
        self, session: str, group_id: str, accept_json: bool = False
    ) -> Any:
        """
        Get group picture

        Args:
            session: Session name
            group_id: Group ID
            accept_json: If True, returns JSON with base64 data

        Returns:
            Picture data

        Example:
            .. code-block:: python

                picture = client.groups.get_picture("default", "1234567890@g.us")
        """
        endpoint = f"/api/{session}/groups/{group_id}/picture"

        if accept_json:
            headers = {"Accept": "application/json"}
            return await self.client.request("GET", endpoint, headers=headers)

        return await self.client.get(endpoint)

    async def get_participants(self, session: str, group_id: str) -> builtins.list[dict[str, Any]]:
        """
        Get group participants

        Args:
            session: Session name
            group_id: Group ID

        Returns:
            List of participants

        Example:
            .. code-block:: python

                participants = client.groups.get_participants("default", "1234567890@g.us")
        """
        return await self.client.get(f"/api/{session}/groups/{group_id}/participants")

    async def add_participants(
        self, session: str, group_id: str, participants: builtins.list[str]
    ) -> dict[str, Any]:
        """
        Add participants to a group

        Args:
            session: Session name
            group_id: Group ID
            participants: List of participant IDs

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.add_participants(
                    "default",
                    "1234567890@g.us",
                    ["9876543210@c.us"]
                )
        """
        data = {"participants": participants}
        return await self.post(
            f"/api/{session}/groups/{group_id}/participants/add", json_data=data
        )

    async def remove_participants(
        self, session: str, group_id: str, participants: builtins.list[str]
    ) -> dict[str, Any]:
        """
        Remove participants from a group

        Args:
            session: Session name
            group_id: Group ID
            participants: List of participant IDs

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.remove_participants(
                    "default",
                    "1234567890@g.us",
                    ["9876543210@c.us"]
                )
        """
        data = {"participants": participants}
        return await self.post(
            f"/api/{session}/groups/{group_id}/participants/remove", json_data=data
        )

    async def promote_admin(
        self, session: str, group_id: str, participants: builtins.list[str]
    ) -> dict[str, Any]:
        """
        Promote participants to admin

        Args:
            session: Session name
            group_id: Group ID
            participants: List of participant IDs

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.promote_admin(
                    "default",
                    "1234567890@g.us",
                    ["9876543210@c.us"]
                )
        """
        data = {"participants": participants}
        return await self.post(
            f"/api/{session}/groups/{group_id}/admin/promote", json_data=data
        )

    async def demote_admin(
        self, session: str, group_id: str, participants: builtins.list[str]
    ) -> dict[str, Any]:
        """
        Demote participants from admin

        Args:
            session: Session name
            group_id: Group ID
            participants: List of participant IDs

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.groups.demote_admin(
                    "default",
                    "1234567890@g.us",
                    ["9876543210@c.us"]
                )
        """
        data = {"participants": participants}
        return await self.post(
            f"/api/{session}/groups/{group_id}/admin/demote", json_data=data
        )

