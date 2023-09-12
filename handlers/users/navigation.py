from loader import dp, bot
from aiogram.types import CallbackQuery
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api import db_commands
from filters.filters_chat import Is_Ref
from states.widthraw_request import Widthdraw
from functions.qiwi_func import creation_payment, QiwiP2PClient
from keyboards.inline.search_result_keyboard import download_keyboard, method_download_keyboard


@dp.callback_query_handler(text="close")
async def cancel_pay(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(text_startswith="cancel_pay")
async def cancel_pay(call: CallbackQuery):
    try:
        qiwi = await db_commands.select_qiwi(id=call.data.split(':')[1])
        async with QiwiP2PClient(secret_p2p=qiwi[0].get('p2p_token')) as p2p:
            await p2p.reject_p2p_bill(call.data.split(':')[2])
    except:
        pass
    await call.answer('❌ Отмена')
    text = await db_commands.select_text()
    await call.message.delete()
    await call.message.answer(text.get('search_text'))


@dp.callback_query_handler(text_startswith="back")
async def cancel_purchase(call: CallbackQuery):
    uid = call.data.split(':')[1]
    await call.message.edit_reply_markup(None)
    text = await db_commands.select_text()
    await call.message.edit_text(text.get('download_text'), reply_markup=method_download_keyboard(uid))
