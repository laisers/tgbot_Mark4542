import logging
import os
import django
from aiogram import executor
from data import config
import filters
from loader import dp, db, bot, vkapi, google


async def on_startup(dispatcher):
    # Уведомляет о запуске
    logging.info(f'Создаем подключение...')
    await db.create()
    logging.info(f'Подключение успешно!')
    logging.info(f'База загружена успешно!')
    logging.info(f'Подключение filters...')
    filters.setup(dp)
    setting = await db.get_setting()
    logging.info(f'Подключение к vk.com...')
    await vkapi.connect(setting[0].get('vk_token'))
    logging.info(f'Подключение к google.com...')
    google.set_token(setting[0].get('google_token'))
    me = await bot.me
    await db.create_table_setting(config.BOT_TOKEN, me.username)
    logging.info(f'Бот @{me.username} запущен...')


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()
    import handlers
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
