# -*- coding: utf-8 -*-
import asyncio
from telethon import functions, types
from telethon import TelegramClient, events
from telethon.tl.functions.channels import (GetFullChannelRequest,
                                            GetParticipantsRequest)
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
from telethon.tl.types import InputPeerChat
from telethon.network import ConnectionTcpAbridged
from .load_config import API_HASH, API_ID, SESSION_NAME, users_file_path
from telethon.tl.types import InputPeerUser
from typing import Union


class Bot(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash,
                 proxy=None):
        """
        Initializes the InteractiveTelegramClient.
        :param session_user_id: Name of the *.session file.
        :param api_id: Telegram's api_id acquired through my.telegram.org.
        :param api_hash: Telegram's api_hash.
        :param proxy: Optional proxy tuple/dictionary.
        """
        # The first step is to initialize the TelegramClient, as we are
        # subclassing it, we need to call super().__init__(). On a more
        # normal case you would want 'client = TelegramClient(...)'
        super().__init__(
            # These parameters should be passed always, session name and API
            session_user_id, api_id, api_hash,

            # You can optionally change the connection mode by passing a
            # type or an instance of it. This changes how the sent packets
            # look (low-level concept you normally shouldn't worry about).
            # Default is ConnectionTcpFull, smallest is ConnectionTcpAbridged.
            connection=ConnectionTcpAbridged,

            # If you're using a proxy, set it here.
            proxy=proxy
        )

    async def get_chat_users(self) -> list:
        """Returns a list of user IDs from chats"""
        dialog_users = list()
        async for dialog in self.iter_dialogs():
            if dialog.is_user:
                dialog_users.append(dialog.entity.id)
        return dialog_users

    async def get_contacts(self) -> list:
        """Returns a list of user IDs from contacts"""
        contact_users = list()
        users_request = await self(functions.contacts.GetContactsRequest(
            hash=0
        ))
        for user in users_request.users:
            contact_users.append(user.id)
        return contact_users

    async def get_customer_base(self) -> list:
        """Merges contacts and chats. Deletes duplicates"""
        customer_base = list()
        contacts = await self.get_contacts()
        chat_users = await self.get_chat_users()
        customer_base = list(set(contacts + chat_users))
        return customer_base

    async def write_base_to_file(self) -> str:
        """Writes user fresh user base to a users.txt file or returns an error"""
        try:
            base = await self.get_customer_base()
            with open(users_file_path, "w", encoding="utf-8") as file:
                for user in base:
                    file.write(str(user) + "\n")
            return "Successfully updated user base"
        except Exception as e:
            print(e)
            return str(e)

    async def send_messages(self, message) -> str:
        """Function to spam from users.txt base. Returns success message or error"""
        try:
            with open(users_file_path, "r", encoding="utf-8") as file:
                users_str = file.readlines()
                users_int = [int(i) for i in users_str]
            for user in users_int:
                await self.send_message(user, message)
                sleep(1)  # not to get banned for spamming
            return "Successfully sent messages"
        except Exception as e:
            print(e)
            return str(e)


async def controller(command, message=None) -> str:
    """Fucntion that controlls every call from bot. Returns success message or error
       :param command: command 1 updates database, command 2 starts spamming
    """
    client = Bot(SESSION_NAME, int(API_ID), API_HASH)

    try:
        await client.connect()
        # print("Connected")
        if command == 1:
            result_code = await client.write_base_to_file()

        if command == 2:
            result_code = await client.send_messages(message)
    except Exception as e:
        print(f"Error!\n{e}")
        await client.disconnect()
    await client.disconnect()
    # print("Disconnected")
    return result_code
