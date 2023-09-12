from glQiwiApi import QiwiWallet, QiwiP2PClient
from datetime import datetime, timedelta


async def get_qiwi_balance(qiwi_token: str, phone_number: str):
    async with QiwiWallet(api_access_token=qiwi_token, phone_number=phone_number) as w:
        balance = await w.get_balance()
    return balance


async def check_valid_qiwi(qiwi_token: str):
    async with QiwiP2PClient(secret_p2p=qiwi_token) as p2p:
        await p2p.create_p2p_bill(amount=1, expire_at=datetime.now() + timedelta(hours=2))
    return
