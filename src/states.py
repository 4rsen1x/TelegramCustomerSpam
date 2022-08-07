from aiogram.dispatcher.filters.state import State, StatesGroup


class StartSpam(StatesGroup):
    """Describes the order in which operations
    are performed when spamming starts"""
    waiting_for_message = State()
    waiting_for_confirmation = State()
