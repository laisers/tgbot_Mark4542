from aiogram import types
from utils.db_api import db_commands


async def menu_buts():
    text = await db_commands.select_text()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton(text.get('but1')))
    keyboard.row(types.KeyboardButton(text.get('but2')), types.KeyboardButton(text.get('but3')))
    keyboard.row(types.KeyboardButton(text.get('but4')), types.KeyboardButton(text.get('but5')))
    return keyboard