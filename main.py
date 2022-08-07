from src.bot import bot, dp
from aiogram import executor
from pathlib import Path
from src.load_config import SESSION_NAME
from src.set_session import init_session
import asyncio

loop = asyncio.get_event_loop()


async def check_session():
    if Path(f"{SESSION_NAME}.session").is_file():
        print("Session file exists starting bot")
    else:
        print("Session file doesn't exist")
        await init_session()


def start_bot():
    executor.start_polling(dp, skip_updates=True)


def main():
    loop.create_task(check_session())
    loop.create_task(start_bot())
    loop.run_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit()
