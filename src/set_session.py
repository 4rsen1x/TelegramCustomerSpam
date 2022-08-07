import asyncio
import os
import sys
import time
from getpass import getpass

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.network import ConnectionTcpAbridged
from telethon.utils import get_display_name
from .load_config import API_HASH, API_ID, SESSION_NAME


def sprint(string, *args, **kwargs):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)


def print_title(title):
    """Helper function to print titles to the console more nicely"""
    sprint('\n')
    sprint('=={}=='.format('=' * len(title)))
    sprint('= {} ='.format(title))
    sprint('=={}=='.format('=' * len(title)))


def bytes_to_string(byte_count):
    """Converts a byte count to a string (in KB, MB...)"""
    suffix_index = 0
    while byte_count >= 1024:
        byte_count /= 1024
        suffix_index += 1

    return '{:.2f}{}'.format(
        byte_count, [' bytes', 'KB', 'MB', 'GB', 'TB'][suffix_index]
    )


async def async_input(prompt):
    """
    Python's ``input()`` is blocking, which means the event loop we set
    above can't be running while we're blocking there. This method will
    let the loop run while we wait for input.
    """
    print(prompt, end='', flush=True)
    return (await asyncio.get_running_loop().run_in_executor(None, sys.stdin.readline)).rstrip()


def get_env(name, message, cast=str):
    """Helper to get environment variables interactively"""
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


class InteractiveTelegramClient(TelegramClient):
    """Full featured Telegram client, meant to be used on an interactive
       session to see what Telethon is capable off -
       This client allows the user to perform some basic interaction with
       Telegram through Telethon, such as listing dialogs (open chats),
       talking to people, downloading media, and receiving updates.
    """

    def __init__(self, session_user_id, api_id, api_hash,
                 proxy=None):
        """
        Initializes the InteractiveTelegramClient.
        :param session_user_id: Name of the *.session file.
        :param api_id: Telegram's api_id acquired through my.telegram.org.
        :param api_hash: Telegram's api_hash.
        :param proxy: Optional proxy tuple/dictionary.
        """
        print_title('Initialization')

        print('Initializing interactive example...')

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

        # Store {message.id: message} map here so that we can download
        # media known the message ID, for every message having media.
        self.found_media = {}

    async def init(self):
        # Calling .connect() may raise a connection error False, so you need
        # to except those before continuing. Otherwise you may want to retry
        # as done here.
        print('Connecting to Telegram servers...')
        try:
            await self.connect()
        except IOError:
            # We handle IOError and not ConnectionError because
            # PySocks' errors do not subclass ConnectionError
            # (so this will work with and without proxies).
            print('Initial connection failed. Retrying...')
            await self.connect()

        # If the user hasn't called .sign_in() or .sign_up() yet, they won't
        # be authorized. The first thing you must do is authorize. Calling
        # .sign_in() should only be done once as the information is saved on
        # the *.session file so you don't need to enter the code every time.
        if not await self.is_user_authorized():
            print('First run. Sending code request...')
            user_phone = input('Enter your phone: ')
            await self.sign_in(user_phone)

            self_user = None
            while self_user is None:
                code = input('Enter the code you just received: ')
                try:
                    self_user = await self.sign_in(code=code)

                # Two-step verification may be enabled, and .sign_in will
                # raise this error. If that's the case ask for the password.
                # Note that getpass() may not work on PyCharm due to a bug,
                # if that's the case simply change it for input().
                except SessionPasswordNeededError:
                    pw = getpass('Two step verification is enabled. '
                                 'Please enter your password: ')

                    self_user = await self.sign_in(password=pw)
        await self.disconnect()


async def init_session():
    """Creates session file for telegram"""
    # SESSION_NAME = input("Enter the session name: ")
    # API_ID = input("Enter the API ID: ")
    # API_HASH = input("Enter the api hash: ")

    client = await InteractiveTelegramClient(SESSION_NAME, API_ID, API_HASH).init()

if __name__ == '__main__':
    asyncio.run(init_session())
