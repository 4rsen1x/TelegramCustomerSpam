from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .load_config import BOT_KEY
from .tg_funcs import controller
from .menus import main_menu, confirmation_menu
from .states import StartSpam
from .utils import get_db_size
from .auth_middleware import AuthMiddleware

bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AuthMiddleware())


@dp.message_handler(commands="start")
async def greet(message: types.Message):
    """Greets user and opens main menu"""
    await message.reply("Hello!", reply_markup=main_menu())


@dp.message_handler(Text(equals="Refresh Customer Base"))
async def refresh_base(message: types.Message):
    """Refreshes database"""
    result_code = await controller(command=1)
    await message.answer(result_code)


@dp.message_handler(Text(equals="Send message"))
async def start_send(message: types.Message):
    """Starts the process of sending messages"""
    await message.answer("Send me the message")
    await StartSpam.waiting_for_message.set()


@dp.message_handler(state=StartSpam.waiting_for_message)
async def get_message(message: types.Message, state=FSMContext):
    """Receives message for spam"""
    spam_text = message.text
    await state.update_data(chosen_text=spam_text)
    await message.answer(
        f"Are you sure that you want to send message to your customer base with text: \n{spam_text}",
        reply_markup=confirmation_menu()
    )
    await StartSpam.waiting_for_confirmation.set()


@dp.message_handler(state=StartSpam.waiting_for_confirmation)
async def get_confirmation(message: types.Message, state=FSMContext):
    """Waits for confirmation and starts sending messages"""
    if message.text == "Cancel":
        await cmd_cancel(message, state)
    elif message.text == "Confirm":
        await message.answer("Starting to send messages", reply_markup=main_menu())
        data = await state.get_data()
        await state.finish()
        result_code = await controller(2, data.get("chosen_text"))
        await message.answer(result_code, reply_markup=main_menu())
    else:
        await message.answer("Please confirm using buttons below",
                             reply_markup=confirmation_menu())
        await StartSpam.waiting_for_confirmation.set()


@dp.message_handler(Text(equals="Base size"))
async def get_base_size(message: types.Message):
    """Returns user base size"""
    await message.answer(get_db_size())


@dp.message_handler(Text(equals="Cancel"), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Cancels any state"""
    await state.finish()
    await message.answer("Successfully canceled", reply_markup=main_menu())
