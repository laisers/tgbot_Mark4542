from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django_project.telegrambot.usersmanage.models import *


def method_pay_keyboard(uid, pid):
    text = AllText.objects.values().first()
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text.get('select_pay_but'), callback_data=f"pay:{uid}:{pid}"))
    markup.row(InlineKeyboardButton(text=text.get('back_but'), callback_data=f"back:{pid}"),
               InlineKeyboardButton(text=text.get('cancel_pay_but'), callback_data=f"cancel_pay:{uid}:{uid}"))
    return markup


def pay_keyboard(avai, uid, link, bill_id, token_id):
    text = AllText.objects.values().first()
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text.get('go_to_pay_but'), url=link))
    markup.row(InlineKeyboardButton(text=text.get('check_pay_but'),
                                    callback_data=f"check_pay:{uid}:{bill_id}:{token_id}:{avai}"))
    markup.row(InlineKeyboardButton(text=text.get('cancel_pay_but'), callback_data=f"cancel_pay:{token_id}:{bill_id}"))
    return markup


def paid_qiwi_keyboard(link):
    text = AllText.objects.values().first()
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text.get('paid_qiwi_but'), url=link))
    return markup


def buts_payment_keyboard(link, bill_id, token_id, but):
    text = AllText.objects.values().first()
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text.get('go_to_pay_but'), url=link))
    markup.row(InlineKeyboardButton(text=text.get('check_pay_but'), callback_data=f"one_pay:{bill_id}:{token_id}:{but}"))
    markup.row(InlineKeyboardButton(text=text.get('cancel_pay_but'), callback_data=f"cancel_pay"))
    return markup

def buts_paid_keyboard(text, link):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text, url=link))
    return markup