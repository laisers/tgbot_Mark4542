from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api import db_commands
from filters.filters_chat import Is_Support, Is_Button1, Is_Button2
from keyboards.inline.support_keyboard import support_key, button1_key, button2_key
from states.widthraw_request import Widthdraw


@dp.message_handler(Is_Support())
async def support(message: types.Message):
    text = (await db_commands.select_text()).get('support_text')
    await message.answer(text, reply_markup=support_key())


@dp.message_handler(Is_Button1())
async def button1(message: types.Message):
    text = (await db_commands.select_text()).get('button1_text')
    await message.answer(text, reply_markup=button1_key())


@dp.message_handler(Is_Button2())
async def button1(message: types.Message):
    text = (await db_commands.select_text()).get('button2_text')
    await message.answer(text, reply_markup=button2_key())
