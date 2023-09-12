from aiogram.dispatcher.filters.state import StatesGroup, State


class Widthdraw(StatesGroup):
    waiting_comment = State()
