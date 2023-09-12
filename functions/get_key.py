import asyncio
from aioauth_client import OAuth2Client


async def get_google_drive_token():
    client = OAuth2Client(
        client_id="915183776259-pith5la687p9onhj98849ftsqcolukka.apps.googleusercontent.com",
        client_secret="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",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        authorize_params=None,
        access_token_url="https://oauth2.googleapis.com/token",
        access_token_params=None,
        redirect_uri=None,
        base_url=None,
    )

    # Получите URL для авторизации
    uri = client.get_authorize_url()
    print(f"Перейдите по следующей ссылке и авторизуйтесь: {uri}")

    # Пользователь вводит код, полученный после авторизации
    code = input("Введите код, который вы получили: ")

    # Получение токена доступа
    token = client.get_access_token(code)
    print(token)
    return token


asyncio.run(get_google_drive_token())
