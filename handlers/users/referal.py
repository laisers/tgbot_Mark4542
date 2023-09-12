import asyncio

from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api import db_commands
from filters.filters_chat import Is_Ref
from states.widthraw_request import Widthdraw
from keyboards.inline.user_keboard import *
from aiogram.types import CallbackQuery
import random


@dp.message_handler(Is_Ref())
async def handle_referal(message: types.Message):
    user = await db_commands.select_user(user_id=message.from_user.id)
    link = False
    ref_link = f'https://t.me/{(await message.bot.me).username}?start={message.from_user.id}'

    text = (await db_commands.select_text()).get('ref_text'). \
        replace('%link%', ref_link).replace('%ref%', str(user.get("ref_count"))).replace('%bal%', str(user.get("balance"))).\
        replace('%links%', str(user.get("ref_link")))
    if user.get("ref_link"):
        link = True

    await message.answer(text, reply_markup=referal_key(ref_link, link))

@dp.callback_query_handler(text="get_ref_link")
async def handle_get_ref_link(call: CallbackQuery):
    await call.message.delete()
    setting = await db_commands.select_setting()
    user_id = call.from_user.id
    with open(setting.get('damps_percentage')) as f:
        link = random.choice(f.read().split('\n'))
    await call.message.answer(link)
    ref_user = await db_commands.select_user(user_id=user_id)
    await db_commands.update_user(user_id, ref_link=ref_user.get('ref_link') - 1)
    call.message.from_user.id = call.from_user.id
    await asyncio.sleep(1)
    await handle_referal(call.message)




@dp.message_handler(commands=['pay'])
async def widthdraw(message: types.Message, state: FSMContext):
    user_data = await db_commands.select_user(user_id=message.from_user.id)
    text = await db_commands.select_text()
    minimal = (await db_commands.select_setting()).get('ref_min_widthdraw')
    if user_data.get('balance') < minimal:
        await message.answer(text.get('ref_no_money_text').replace('%bal%', str(user_data.get("balance"))))
        return

    await message.answer(text.get('ref_widthdraw_text'))
    await state.update_data(balance=user_data.get('balance'))
    await Widthdraw.waiting_comment.set()


@dp.message_handler(state=Widthdraw.waiting_comment)
async def waiting_comment(message: types.Message, state: FSMContext):
    text = await db_commands.select_text()
    balance = (await state.get_data()).get('balance')
    await message.answer(text.get('ref_well_widthdraw'))
    await db_commands.update_user(message.from_user.id, balance=0)
    for admin in (await db_commands.select_setting()).get('admins').split(','):
        text_admin = text.get('ref_admin_notification').replace('%UN%', message.from_user.username). \
            replace('%ID%', str(message.from_user.id)).replace('%bal%', str(balance)).replace('%cred%', message.text)
        await bot.send_message(admin, text_admin)

    await state.finish()
