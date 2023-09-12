from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django_project.telegrambot.usersmanage.models import *



def download_keyboard(uid):
    text = AllText.objects.values().first().get('download_but')
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=text, callback_data=f"download:{uid}"))
    return markup


def method_download_keyboard(uid):
    markup = InlineKeyboardMarkup()
    text = AllText.objects.values().first()
    relations = RelationsData.objects.filter(drain_id=uid).values().all()
    availability = AvailabilityData.objects.values().all()
    for i in [x for x in availability if x.get('id') in [y.get('search_simulation_id') for y in relations]]:
        markup.row(InlineKeyboardButton(text=i.get('name_but'), callback_data=f"purchase:{i.get('id')}:{uid}"))

    markup.row(InlineKeyboardButton(text=text.get('cancel_pay_but'), callback_data=f'cancel_pay:{uid}'))
    return markup
