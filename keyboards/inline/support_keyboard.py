from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django_project.telegrambot.usersmanage.models import *


def support_key():
    link = Bot.objects.values().first().get('support_link')
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text='Написать', url=link))
    return markup


def button1_key():
    text = AllText.objects.values().first().get('but1_but')
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text, callback_data='link_pay:1'))
    return markup


def button2_key():
    text = AllText.objects.values().first().get('but2_but')
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text, callback_data='link_pay:2'))
    return markup
