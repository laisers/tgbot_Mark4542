import asyncio
import json
import aiohttp
from PIL import Image, ImageDraw
from io import BytesIO

#915183776259-iue7ojrebegqif68k344eeubfl7t45mi.apps.googleusercontent.com
#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
token = 'ya29.a0AfB_byCDUeEtAnkBgsWg6yLvL4IUy5Uu3L_HpQBxp0Jwfd00m1sTEnVvgTXZMWzpgjW9oxQqV51qMzAxd-OzfxE9zXUR95quaZU7nYd2yR07dSayCVpT6kRIqJA1_opAshC7hjYxu5HtxDs9Bgt1omG8mBXCe85uIAaCgYKAQMSARISFQGOcNnCnxikUkICwegoijPg35BdKA0169'


class AsyncGoogleDrive:
    BASE_URL = "https://www.googleapis.com/drive/v3"

    def __init__(self):
        self.token = None

    def set_token(self, value):
        self.token = value

    async def upload_file_from_memory(self, img: Image.Image, folder_id="1iftq01HUAwb2oxYOKFPNobkQTcrU09qR", file_name=''):
        # Преобразование изображения Pillow в байтовый поток
        byte_stream = BytesIO()
        img.save(byte_stream, format="PNG")
        byte_stream.seek(0)

        # Создание метаданных файла
        metadata = {
            "name": file_name,
            "parents": [folder_id]
        }

        headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json; charset=UTF-8'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.BASE_URL}/files',
                                    headers=headers,
                                    data=json.dumps(metadata)) as response:
                res_data = await response.json()
                file_id = res_data['id']

                # Загрузка тела файла
                headers['Content-Type'] = 'media'
                async with session.patch(f'{self.BASE_URL}/files/{file_id}',
                                         headers=headers,
                                         data=byte_stream) as upload_response:
                    upload_data = await upload_response.json()
                    return upload_data


    async def upload_file(self, file_path: str, folder_id="1iftq01HUAwb2oxYOKFPNobkQTcrU09qR", file_name: str = None):
        # Если имя файла не указано, используется имя исходного файла
        file_name = file_name or file_path.split('/')[-1]

        # 1. Создание метаданных файла
        metadata = {
            "name": file_name,
            "parents": [folder_id]
        }

        headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json; charset=UTF-8'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.BASE_URL}/files',
                                    headers=headers,
                                    data=json.dumps(metadata)) as response:

                res_data = await response.json()
                print(res_data)
                file_id = res_data['id']

                # 2. Загрузка тела файла
                headers['Content-Type'] = 'media'
                async with session.patch(f'{self.BASE_URL}/files/{file_id}',
                                         headers=headers,
                                         data=open(file_path, 'rb')) as upload_response:
                    upload_data = await upload_response.json()
                    return upload_data


    async def get_files(self, folder_id: str):
        # Запрашивайте список файлов из Google Drive
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f"Bearer {self.token}"
            }
            params = {
                'q': f"'{folder_id}' in parents"
            }
            async with session.get('https://www.googleapis.com/drive/v3/files', headers=headers,
                                   params=params) as response:
                data = await response.json()
                print(await self.get_file(str(data['files'][0]['id'])))
                # for i in [file for file in data['files']]:
                #     print(i)
                #     print('______________________________')

    async def get_file(self, file_id: str) -> bytes:
        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        async with aiohttp.ClientSession() as session:
            # Получение метаданных файла
            metadata_response = await session.get(f"{self.BASE_URL}/files/{file_id}", headers=headers)
            metadata = await metadata_response.json()

            mime_type = metadata.get("mimeType")
            if "image" not in mime_type:
                raise ValueError("The requested file is not an image")

            # Получение содержимого файла
            download_url = f"{self.BASE_URL}/files/{file_id}?alt=media"
            print(download_url)
            # async with session.get(download_url, headers=headers) as response:
            #     result = await response.read()
            #     return result


path = r"C:\Users\User\PycharmProjects\tgbot_Mark4542\django_project\telegrambot\Files\Photos\Drain\Template\template_1214962.jpg"
x = AsyncGoogleDrive(token)
#asyncio.run(x.get_files('1iftq01HUAwb2oxYOKFPNobkQTcrU09qR'))
asyncio.run(x.upload_file(path, '1iftq01HUAwb2oxYOKFPNobkQTcrU09qR'))