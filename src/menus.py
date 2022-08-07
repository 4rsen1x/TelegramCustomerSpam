from aiogram import types


def main_menu() -> types.ReplyKeyboardMarkup:
    """Returns main menu keyboard"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Refresh Customer Base")
    button2 = types.KeyboardButton(text="Send message")
    button3 = types.KeyboardButton(text="Cancel")
    button4 = types.KeyboardButton(text="Base size")
    keyboard.add(button2, button4)
    keyboard.add(button1, button3)
    return keyboard


def confirmation_menu() -> types.ReplyKeyboardMarkup:
    """Returns confirmation menu keyboard"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Confirm")
    button2 = types.KeyboardButton(text="Cancel")
    keyboard.add(button1, button2)
    return keyboard
