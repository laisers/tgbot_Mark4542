from loader import dp
from aiogram.types import CallbackQuery
from utils.db_api import db_commands
from keyboards.inline.payment_keyboard import buts_payment_keyboard, buts_paid_keyboard
from functions.qiwi_func import creation_payment, QiwiP2PClient


@dp.callback_query_handler(text_startswith="link_pay")
async def onepay(call: CallbackQuery):
    but = call.data.split(':')[1]
    setting = await db_commands.select_setting()

    result = await creation_payment(setting.get(f'price_but{but}'))
    if not result:
        await call.message.answer('❌ Ошибка. Попробуйте позже')
        return
    text = await db_commands.select_text()
    pay_text = text.get('pay_text').replace('%sum%', str(setting.get(f'price_but{but}')))
    await call.message.edit_text(pay_text, reply_markup=buts_payment_keyboard(*result, but))


@dp.callback_query_handler(text_startswith="one_pay")
async def onepay_check(call: CallbackQuery):
    user_data = call.data.split(':')
    but = user_data[3]
    qiwi = (await db_commands.select_qiwi(id=int(user_data[2])))[0]
    setting = await db_commands.select_setting()
    text = await db_commands.select_text()
    async with QiwiP2PClient(secret_p2p=qiwi.get('p2p_token')) as p2p:
        status = await p2p.get_bill_status(user_data[1])
    if status == 'WAITING':
        await call.answer(text.get('qiwi_waiting'))
    elif status == 'PAID':
        # TODO ЗАМЕНИТЬ
        # elif status == 'PAID':
        user_data = [None, user_data[1], user_data[2]]
        await db_commands.add_order(call.from_user.id, user_data, setting.get(f'price_but{but}'), but1=True)
        markup = buts_paid_keyboard(text.get('button1_2_well_but'), setting.get(f'link_but{but}'))
        await call.message.edit_text(text.get(f'button{but}_pay_text'), reply_markup=markup)
        await db_commands.update_qiwi(int(user_data[2]), use_count_day=qiwi.get('use_count_day') + 1,
                                      use_count_month=qiwi.get('use_count_month') + 1,
                                      use_count_all=qiwi.get('use_count_all') + 1)

    else:
        await call.message.delete()
        await call.message.answer(text.get('qiwi_rejected'))
