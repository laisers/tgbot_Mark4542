from aiogram import Dispatcher
from loguru import logger

from filters.filters_chat import IsPrivate, Is_Vk_Link



def setup(dp: Dispatcher):
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
    ]

    dp.filters_factory.bind(IsPrivate)
