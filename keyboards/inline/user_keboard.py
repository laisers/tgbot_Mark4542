from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django_project.telegrambot.usersmanage.models import *

def referal_key(ref_link, link=False):
    keyboard = InlineKeyboardMarkup()
    if link:
        keyboard.add(InlineKeyboardButton("Скачать дамп", callback_data='get_ref_link'))
    keyboard.add(InlineKeyboardButton("Поделиться реферальной ссылкой", switch_inline_query=ref_link))
    return keyboard