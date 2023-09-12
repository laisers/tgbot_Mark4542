import random

import vk_api
import datetime
import requests
from data.config import VK_TOKEN


# VK_TOKEN = 'vk1.a.-m46Yeo3RbuWnsbuUh8JEWlFwOodj7_Y3z4Gw9boRBMIdOiUe9ylOU6-lt736PI-pXKax427s0qZaxzrh_Lv2M-O5PmhFigS8xQCm0ZGG7Rs7mWl4HN3wHk4wFTSuGJLnUJn4MGaIvsr-8Wi-cXVQfQSiIhdpd7HJtsnabnetyFUIA0huZBXsD7tusqjvqhTC0taFktYQ7ybgVYZ3sSPpQ'
session = vk_api.VkApi(token=VK_TOKEN)
vk = session.get_api()


def get_user_data(user_id: str) -> dict:
    data = session.method('users.get', {'user_ids': user_id, 'fields': 'sex, photo_max, verified, bdate, has_photo'})
    data_dict = {'id': 0, 'first_name': '', 'last_name': '', 'sex': 0, 'photo': ''}
    data_dict['id'] = data[0]['id']
    data_dict['first_name'] = data[0]['first_name']
    data_dict['last_name'] = data[0]['last_name']
    data_dict['sex'] = data[0]['sex']
    data_dict['photo'] = data[0]['photo_max']
    data_dict['verified'] = data[0]['verified']
    data_dict['has_photo'] = data[0]['has_photo']
    req = requests.get(f'https://vk.com/foaf.php?id={data_dict["id"]}')
    data_dict['reg_date'] = req.text.split('created dc:date="')[1].split('"/>')[0].split('T')[0]
    try:
        data_dict['age'] = int(
            (datetime.date.today() - datetime.datetime.strptime(data[0]['bdate'], '%d.%m.%Y').date()).days / (365.2425))
    except:
        data_dict['age'] = 0
    return data_dict


def get_photo_friend(user_id: str, sex: int):
    try:
        data = session.method('friends.get', {'user_id': user_id, 'order': 'random', 'fields': 'sex, photo_max, verified, bdate, has_photo'})
        return_data = {}
        print(len(data['items']))
        print('______________________')
        for user in data['items']:
            try:
                if user['sex'] == sex and user['verified'] == 0 and user['has_photo'] == 1:
                    print(user)
                    return user
            except KeyError as e:
                continue
        if not return_data:
            print(return_data)
            raise
    except Exception as e:
        print(e)
        get_photo_friend('54128229', sex)



