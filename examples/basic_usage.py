"""
Basic usage examples for WAHA Python client
"""

import asyncio

from waha_python import WAHAClient


async def example_send_message(client: WAHAClient) -> None:
    """Example: Send a simple text message"""
    result = await client.messages.send_text(
        session="default",
        chat_id="1234567890@c.us",
        text="Hello from WAHA Python! 👋",
    )
    print(f"Message sent: {result}")


async def example_create_session(client: WAHAClient) -> None:
    """Example: Create a new session with webhook"""
    session = await client.sessions.create(
        name="my_session",
        config={
            "webhooks": [
                {
                    "url": "https://your-webhook-url.com/webhook",
                    "events": ["message", "session.status"],
                }
            ]
        },
    )
    print(f"Session created: {session}")


async def example_get_qr(client: WAHAClient) -> None:
    """Example: Get QR code for authentication"""
    qr_data = await client.sessions.get_qr("default", accept_json=True)
    print(f"QR Code: {qr_data}")


async def example_list_chats(client: WAHAClient) -> None:
    """Example: List all chats"""
    chats = await client.chats.list("default")
    print(f"Total chats: {len(chats)}")
    for chat in chats[:5]:  # Print first 5 chats
        print(f"  - {chat.get('id', 'Unknown')}")


async def example_list_contacts(client: WAHAClient) -> None:
    """Example: List all contacts"""
    contacts = await client.contacts.list_all("default")
    print(f"Total contacts: {len(contacts)}")
    for contact in contacts[:5]:  # Print first 5 contacts
        print(f"  - {contact.get('name', 'Unknown')} ({contact.get('id', 'Unknown')})")


async def example_check_phone(client: WAHAClient) -> None:
    """Example: Check if a phone number exists in WhatsApp"""
    result = await client.contacts.check_exists("default", "1234567890")
    if result["numberExists"]:
        print(f"Phone exists! Chat ID: {result['chatId']}")
    else:
        print("Phone number not found in WhatsApp")


async def example_send_image(client: WAHAClient) -> None:
    """Example: Send an image"""
    result = await client.messages.send_image(
        session="default",
        chat_id="1234567890@c.us",
        file={
            "url": "https://github.com/devlikeapro/waha/raw/core/examples/dev.likeapro.jpg",
            "mimetype": "image/jpeg",
            "filename": "image.jpg",
        },
        caption="Check this out! 🖼️",
    )
    print(f"Image sent: {result}")


async def example_send_poll(client: WAHAClient) -> None:
    """Example: Send a poll"""
    result = await client.messages.send_poll(
        session="default",
        chat_id="1234567890@c.us",
        poll={
            "name": "How are you?",
            "options": ["Awesome!", "Good!", "Not bad!"],
            "multipleAnswers": False,
        },
    )
    print(f"Poll sent: {result}")


async def example_add_reaction(client: WAHAClient) -> None:
    """Example: Add reaction to a message"""
    result = await client.messages.add_reaction(
        session="default",
        message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA",
        reaction="👍",
    )
    print(f"Reaction added: {result}")


async def main() -> None:
    print("WAHA Python Basic Usage Examples")
    print("=" * 50)

    async with WAHAClient(
        base_url="http://localhost:3000",
        api_key="your-api-key-here",  # Optional if you don't use API key
    ) as client:
        # Uncomment the examples you want to run
        await example_send_message(client)
        # await example_create_session(client)
        # await example_get_qr(client)
        # await example_list_chats(client)
        # await example_list_contacts(client)
        # await example_check_phone(client)
        # await example_send_image(client)
        # await example_send_poll(client)
        # await example_add_reaction(client)

    print("\nDone! Uncomment examples in the code to try them.")


if __name__ == "__main__":
    asyncio.run(main())
