import threading
import time

from .models import Bot, DrainData, RelationsData, Filters, HackMethods, AvailabilityData, AvailabilityDataTwo, Links
from django.shortcuts import render, redirect
from .forms import BulkUploadForm
import requests, random
from datetime import datetime, timedelta
import datetime, json
import vk_api


class VKHelper:
    def __init__(self):
        setting = Bot.objects.values().first()
        self.session = vk_api.VkApi(token=setting.get('vk_token'))

    def get_user_data(self, user_id: str) -> dict:
        data = \
            self.session.method("users.get", {"user_ids": user_id, "fields": "sex,photo_max,verified,bdate,has_photo"})[
                0]
        data_dict = {'id': data['id'], 'first_name': data['first_name'], 'last_name': data['last_name'],
                     'sex': data['sex'], 'photo': data['photo_max'], 'verified': data['verified'],
                     'has_photo': data['has_photo']}
        req = requests.get(f'https://vk.com/foaf.php?id={data_dict["id"]}')
        try:
            data_dict['reg_date'] = req.text.split('created dc:date="')[1].split('"/>')[0].split('T')[0]
            data_dict['age'] = int(
                (datetime.date.today() - datetime.strptime(data['bdate'], '%d.%m.%Y').date()).days / 365.2425)
        except:
            data_dict['age'] = 0
        return data_dict


def random_date():
    start = datetime(2000, 1, 1)
    end = datetime.now()
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def bulk_upload_view(request):
    if request.method == 'POST':
        vk = VKHelper()

        form = BulkUploadForm(request.POST)
        if form.is_valid():
            lines = form.cleaned_data['data'].split('\n')
            for line in lines:
                datas = line.split(' | ')
                page_id = datas[0].split('/id')[-1]
                links = datas[1:]
                user_data = vk.get_user_data(page_id)

                filters = Filters.objects.values().first()
                drain_model = DrainData.objects.filter(page_id=user_data['id'])
                drain_data = drain_model.values().first()
                if user_data['age'] == 0:
                    user_data['age'] = 20

                from_date = filters.get('random_start_year_hack')
                to_date = filters.get('random_end_year_hack')
                try:
                    user_date = user_data['reg_date'].split('-')
                except:
                    user_date = [from_date, 1, 1]
                start_date = datetime.date(from_date, 1, 1)
                end_date = datetime.date(to_date, 1, 1)
                if int(user_date[0]) > int(from_date):
                    start_date = datetime.date(int(user_date[0]), 1, 1)
                if int(user_date[0]) > int(to_date):
                    end_date = datetime.datetime.now().date()
                try:
                    random_number_of_days = random.randrange((end_date - start_date).days)
                except ValueError:
                    random_number_of_days = 1

                random_date = start_date + timedelta(days=random_number_of_days)

                percent = [filters.get('random_d_coef'), 100 - filters.get('random_d_coef')]
                downloads = random.randint(0,
                                           random.choices([filters.get('random_d_often'), filters.get('random_d_to')],
                                                          weights=percent)[0])
                percent = [filters.get('random_d_photo_coef'), 100 - filters.get('random_d_photo_coef')]
                downloads_photo = random.randint(0, random.choices(
                    [filters.get('random_d_photo_often'), filters.get('random_d_photo_to')], weights=percent)[0])
                percent = [filters.get('random_d_video_coef'), 100 - filters.get('random_d_video_coef')]
                downloads_video = random.randint(0, random.choices(
                    [filters.get('random_d_video_often'), filters.get('random_d_video_to')], weights=percent)[0])

                hacks = HackMethods.objects.values().all()
                print(hacks)

                hack_method = random.choices([[x.get('name'), x.get('id')] for x in hacks],
                                             weights=[x.get('percent') for x in hacks])[0]
                get_data1 = AvailabilityData.objects.filter().values().all()
                data1 = [x for x in get_data1 if x.get('percent') >= random.randint(0, 100)]
                get_data2 = AvailabilityDataTwo.objects.filter().values().all()
                data2 = [x for x in get_data2 if x.get('percent') >= random.randint(0, 100)]
                print(hack_method[1])

                hack_method = HackMethods.objects.filter(pk=hack_method[1]).first()
                template = f'Files/Photos/Drain/Template/template_{page_id}.jpg'
                model = DrainData.objects.create(page_id=int(user_data["id"]), break_at=random_date,
                                                 downloads=downloads, downloads_photo=downloads_photo,
                                                 downloads_video=downloads_video, hack_method=hack_method,
                                                 template=template)  # Создание строки
                for i in data1:
                    availability = AvailabilityData.objects.filter(pk=i.get('id'))
                    links = Links.objects.filter(method_id=availability.values().first().get('id')).values().first()
                    if links:
                        with open('django_project/telegrambot/Files/' + links.get('links'), encoding='utf-8') as f:
                            links = random.choices(f.read().split('\n'))[0]
                    RelationsData.objects.create(drain=model, search_simulation=availability.first(), link=links)

                model.availability_data2.set([x.get('id') for x in data2])

                # drain_data = DrainData(
                #     page_id=int(user_data["id"]), break_at=random_date,
                #     downloads=downloads, downloads_photo=downloads_photo,
                #     downloads_video=downloads_video, hack_method=hack_method[1],
                #     data1=data1, data2=data2
                # )
                # drain_data.save()
                #
                # relation_data = RelationsData(
                #     drain=drain_data,
                #     link=relation_link.strip(),
                #     # ... добавьте остальные поля
                # )
                # relation_data.save()

            return redirect('/admin/usersmanage/draindata/')  # перенаправление после успешной загрузки

    else:
        form = BulkUploadForm()

    return render(request, 'admin/broadcast_message.html', {'form': form})


########################### Уведомление ###########################
# Отправка пользователям сообщение об появлении новых фоток
def startNotification(users_info, broadcast_message_text):
    result = DoNotif(users_info, broadcast_message_text)
    return result


def DoNotif(users_info: list, text: str):
    send = 0
    error = 0
    for user_info in users_info:
        user_id = user_info[0]
        inf = user_info[1]
        text = text.replace('%FN%', inf.get('first_name')).replace('%LN%', inf.get('first_name')). \
            replace('%ID%', str(inf.get("id")))

        setting = Bot.objects.values().first()

        reply_markup = {
            "inline_keyboard": [
                [{"text": "Приобрести 💳", "callback_data": "button_clicked"}]
            ]
        }

        r = requests.post(f"https://api.telegram.org/bot{setting.get('token')}/sendMessage", data={
            "chat_id": user_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": json.dumps(reply_markup)
        })
        if r.status_code == 200:
            send += 1
        else:
            error += 1
    return f'Рассылка уведомлений закончена.\nОтправлено: {send}\nОшибок: {error}'


########################### Рассылка ###########################
# Отправка пользователям текст
def startSpam(user_ids, broadcast_message_text):
    result = doSpam(user_ids, broadcast_message_text)
    return result


def doSpam(user_ids, broadcast_message_text):
    setting = Bot.objects.values().first()
    send = 0
    error = 0
    for user in user_ids:
        r = requests.post(f"https://api.telegram.org/bot{setting.get('token')}/sendMessage", data={
            "chat_id": user,
            "text": broadcast_message_text,
            "parse_mode": "HTML"
        })
        if r.status_code == 200:
            send += 1
        else:
            error += 1
    return f'Рассылка закончена.\nОтправлено: {send}\nОшибок: {error}'

# TODO УДАЛИТЬ КОММЕНТ
# def send_notification(user_id, text):
#     setting = Bot.objects.values().first()
#     r = requests.post(f"https://api.telegram.org/bot{setting.get('token')}/sendMessage", data={
#         "chat_id": user_id,
#         "text": text,
#         "parse_mode": "HTML"
#     })
#     if r.status_code != 200:
#         raise Exception("post_text error")
