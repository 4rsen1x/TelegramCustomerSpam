import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = Path(BASE_DIR / "config.env")
users_file_path = Path(BASE_DIR / "src/users.txt")

load_dotenv(dotenv_path=dotenv_path)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_KEY = os.getenv("BOT_KEY")
SESSION_NAME = os.getenv("SESSION_NAME")
ADMIN_USER = os.getenv("ADMIN_USER")
