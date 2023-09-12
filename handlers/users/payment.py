from loader import dp
from aiogram.types import CallbackQuery
from keyboards.inline.search_result_keyboard import method_download_keyboard
from utils.db_api import db_commands
from keyboards.inline.payment_keyboard import method_pay_keyboard, pay_keyboard, paid_qiwi_keyboard
from functions.qiwi_func import creation_payment, QiwiP2PClient


@dp.callback_query_handler(text_startswith="download")
async def download(call: CallbackQuery):
    uid = call.data.split(':')[1]
    await call.message.edit_reply_markup(None)
    text = await db_commands.select_text()
    await call.message.delete()
    await call.message.answer(text.get('download_text'), reply_markup=method_download_keyboard(uid))


@dp.callback_query_handler(text_startswith="purchase")
async def purchase(call: CallbackQuery):
    user_data = call.data.split(':')
    get_data = await db_commands.select_availability_data(id=call.data.split(':')[1])
    text = await db_commands.select_text()
    method_text = text.get('method_text').replace('%sum%', str(get_data[0].get('price')))
    await call.message.edit_text(method_text, reply_markup=method_pay_keyboard(user_data[1], user_data[2]))


@dp.callback_query_handler(text_startswith="pay")
async def pay(call: CallbackQuery):
    user_data = call.data.split(':')
    get_data = await db_commands.select_availability_data(id=user_data[1])
    result = await creation_payment(get_data[0].get('price'))
    if not result:
        await call.message.answer('❌ Ошибка. Попробуйте позже')
        return
    text = await db_commands.select_text()
    pay_text = text.get('pay_text').replace('%sum%', str(get_data[0].get('price')))
    await call.message.edit_text(pay_text,
                                 reply_markup=pay_keyboard(user_data[1], user_data[2], result[0], result[1], result[2]))


@dp.callback_query_handler(text_startswith="check_pay")
async def check_pay(call: CallbackQuery):
    user_data = call.data.split(':')
    qiwi = (await db_commands.select_qiwi(id=int(user_data[3])))[0]
    text = await db_commands.select_text()
    async with QiwiP2PClient(secret_p2p=qiwi.get('p2p_token')) as p2p:
        status = await p2p.get_bill_status(user_data[2])
    if status == 'WAITING':
        await call.answer(text.get('qiwi_waiting'))
    elif status == 'PAID':
        availability = await db_commands.select_availability_data(id=user_data[4])
        price = availability[0].get('price')
        link = await db_commands.add_order(call.from_user.id, user_data, price)
        await call.message.edit_text(text.get('qiwi_paid'), reply_markup=paid_qiwi_keyboard(link))
        await db_commands.update_qiwi(int(user_data[3]), use_count_day=qiwi.get('use_count_day') + 1,
                                      use_count_month=qiwi.get('use_count_month') + 1,
                                      use_count_all=qiwi.get('use_count_all') + 1)
        # Обновление баланса реферала
        # user_info = await db_commands.select_user(user_id=call.from_user.id)
        # invited_by = user_info.get('invited_by')
        # if invited_by:
        #     percent = (await db_commands.select_setting()).get('referal_percentage')
        #     refer_info = await db_commands.select_user(user_id=invited_by)
        #     result = refer_info.get('balance') + int(price / 100 * percent)
        #     await db_commands.update_user(invited_by, balance=result)
    else:
        await call.message.delete()
        await call.message.answer(text.get('qiwi_rejected'))
