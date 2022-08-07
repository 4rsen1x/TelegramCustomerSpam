from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from .load_config import ADMIN_USER


class AuthMiddleware(BaseMiddleware):
    """Middleware which restricts use only for one user"""

    def __init__(self):
        self.admin_id = int(ADMIN_USER)
        super(AuthMiddleware, self).__init__()

    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return
        if user != self.admin_id:
            raise CancelHandler()
