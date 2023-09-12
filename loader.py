from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from utils.db_api.postgres import Database
from functions.vk_parser import VKAPI
from functions import vk_parser, google_disk


db = Database()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
vkapi = vk_parser.VKAPI()
google = google_disk.AsyncGoogleDrive()


