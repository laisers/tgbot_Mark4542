import os.path
import random
import asyncio
import datetime
import requests
from vkbottle import API


class VKAPI:
    def __init__(self):
        self.session = None

    async def connect(self, token):
        self.session = API(token)

    async def get_user_data(self, user_id: str) -> dict:
        data = await self.session.users.get([user_id], ['sex, photo_max, verified, bdate, has_photo'])
        data = data[0].dict()
        data_dict = {'id': data['id'], 'first_name': data['first_name'], 'last_name': data['last_name'],
                     'sex': data['sex'],
                     'photo': data['photo_max'], 'verified': data['verified'], 'has_photo': data['has_photo']}
        req = requests.get(f'https://vk.com/foaf.php?id={data_dict["id"]}')
        try:
            data_dict['reg_date'] = req.text.split('created dc:date="')[1].split('"/>')[0].split('T')[0]
            data_dict['age'] = int(
                (datetime.date.today() - datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()).days / (
                    365.2425))
        except:
            data_dict['age'] = 0
        return data_dict

    async def get_info_friend(self, user_id: int, sex: int):
        try:
            data = await self.session.friends.get(user_id, order='random',
                                                  fields=['sex, photo_max, verified, has_photo'])
            data = data.dict()
            return_data = {}
            for user in data['items']:
                try:
                    if user['sex'] == sex and user['verified'] == 0 and user['has_photo'] == 1 and user['photo_max']:
                        return user
                except KeyError:
                    await asyncio.sleep(0.5)
                    continue
            if not return_data:
                raise
        except Exception as e:
            if sex == 1:
                path = 'Files/Photos/templates/Add_photos/Male'
            else:
                path = 'Files/Photos/templates/Add_photos/Female'
            photo = random.choice(os.listdir(path))
            name = photo.replace('.jpg', '').split(' ')
            return {'first_name': name[0], 'last_name': name[1], 'photo_max': os.path.join(path, photo)}

#
# async def get_user_data(user_id: str) -> dict:
#     data = await session.users.get([user_id], ['sex, photo_max, verified, bdate, has_photo'])
#     data = data[0].dict()
#     data_dict = {'id': data['id'], 'first_name': data['first_name'], 'last_name': data['last_name'], 'sex': data['sex'],
#                  'photo': data['photo_max'], 'verified': data['verified'], 'has_photo': data['has_photo']}
#     req = requests.get(f'https://vk.com/foaf.php?id={data_dict["id"]}')
#     try:
#         data_dict['reg_date'] = req.text.split('created dc:date="')[1].split('"/>')[0].split('T')[0]
#         data_dict['age'] = int(
#             (datetime.date.today() - datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()).days / (365.2425))
#     except:
#         data_dict['age'] = 0
#     return data_dict
#
#
# async def get_info_friend(user_id: int, sex: int):
#     try:
#         data = await session.friends.get(user_id, order='random', fields=['sex, photo_max, verified, has_photo'])
#         data = data.dict()
#         return_data = {}
#         for user in data['items']:
#             try:
#                 if user['sex'] == sex and user['verified'] == 0 and user['has_photo'] == 1 and user['photo_max']:
#                     return user
#             except KeyError:
#                 await asyncio.sleep(0.5)
#                 continue
#         if not return_data:
#             raise
#     except Exception as e:
#         if sex == 1:
#             path = 'Files/Photos/templates/Add_photos/Male'
#         else:
#             path = 'Files/Photos/templates/Add_photos/Female'
#         photo = random.choice(os.listdir(path))
#         name = photo.replace('.jpg', '').split(' ')
#         return {'first_name': name[0], 'last_name': name[1], 'photo_max': os.path.join(path, photo)}
