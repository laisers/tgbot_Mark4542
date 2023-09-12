from pathlib import Path
# from django.conf import settings
# import django
# settings.configure()
# django.setup()
# from django_project.telegrambot.Text.models import Bot
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
VK_TOKEN = env.str("VK_TOKEN")
SECRET_KEY = env.str("SECRET_KEY")

DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')


