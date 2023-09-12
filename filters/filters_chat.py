from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters import Filter

from aiogram import types


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return types.ChatType.PRIVATE == message.chat.type


class Is_Vk_Link(Filter):
    async def check(self, message: types.Message) -> bool:
        return message.text.startswith(tuple(['vk.com', 'https://vk.com', 'http://vk.com']))


class Is_Search(Filter):
    async def check(self, message: types.Message) -> bool:
        from utils.db_api import db_commands
        text = await db_commands.select_text()
        if message.text == text.get('but1'):
            return True
        return False


class Is_Ref(Filter):
    async def check(self, message: types.Message) -> bool:
        from utils.db_api import db_commands
        text = await db_commands.select_text()
        if message.text == text.get('but5'):
            return True
        return False


class Is_Support(Filter):
    async def check(self, message: types.Message) -> bool:
        from utils.db_api import db_commands
        text = await db_commands.select_text()
        if message.text == text.get('but2'):
            return True
        return False


class Is_Button1(Filter):
    async def check(self, message: types.Message) -> bool:
        from utils.db_api import db_commands
        text = await db_commands.select_text()
        if message.text == text.get('but3'):
            return True
        return False


class Is_Button2(Filter):
    async def check(self, message: types.Message) -> bool:
        from utils.db_api import db_commands
        text = await db_commands.select_text()
        if message.text == text.get('but4'):
            return True
        return False
