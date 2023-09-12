from glQiwiApi import QiwiP2PClient
from utils.db_api import db_commands
from datetime import datetime, timedelta
from loader import bot
from django.utils import timezone


async def creation_payment(price: int):
    result_qiwi = []
    admins = (await db_commands.select_setting()).get('admins').split(',')
    if not await db_commands.select_qiwi(status='1'):
        for admin in admins:
            await bot.send_message(admin, '❌ Все аккаунты QIWI имеют статус "❌"\nПроверьте валидность аккаунтов!')
        return []
    for qiwi in await db_commands.select_qiwi(status='1'):
        # Проверка дневного лимита
        if timezone.now().date() == qiwi['date_day'].date():
            print(qiwi['use_count_day'])
            print(qiwi['limit_day'])
            if qiwi['use_count_day'] >= qiwi['limit_day']:
                print('1')
                continue
        else:
            await db_commands.update_qiwi(qiwi['id'], date_day=timezone.now(), use_count_day=0)

        # Проверка месячного лимита
        if qiwi['date_month'].date() + timedelta(days=30) > timezone.now().date():
            if qiwi['use_count_month'] >= qiwi['limit_month']:
                print('2')
                continue
        else:
            await db_commands.update_qiwi(qiwi['id'], date_month=timezone.now(), use_count_month=0)
        result_qiwi.append(qiwi)

    if not result_qiwi:
        for admin in admins:
            await bot.send_message(admin, '❌ Все аккаунты QIWI исчерпали лимит\n'
                                          'Добавьте новый аккаунт или увеличьте лимит')
        return False
    setting = await db_commands.select_setting()
    print('___________________________________')
    print(result_qiwi)
    for qiwi in result_qiwi:
        try:
            async with QiwiP2PClient(secret_p2p=qiwi.get('p2p_token'), shim_server_url=setting.get('qiwi_refer')) as p2p:
                bill = await p2p.create_p2p_bill(amount=price, expire_at=datetime.now() + timedelta(hours=4))
                shim_url = p2p.create_shim_url(bill)
        except Exception as e:
            print(e)
            for admin in admins:
                await bot.send_message(admin, f"❌ {qiwi.get('number')}\n{e}")
            continue
        try:
            print(qiwi.get('id'))
            returned = [shim_url, bill.id, qiwi.get('id')]
        except UnboundLocalError:
            return []
        return returned
