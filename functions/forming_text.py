import random
import datetime as DT
from utils.db_api import db_commands
from functions.image_func import create_main_template
from loader import google


async def forming_result_text(user_data):
    filters = await db_commands.select_filters()
    drain_model = await db_commands.select_drain_data(page_id=user_data['id'])
    drain_data = drain_model.values().first()
    if user_data['age'] == 0:
        user_data['age'] = 20
    if user_data['sex'] == 1 and not user_data['verified'] and (16 <= user_data['age'] <= 40) \
            and user_data['has_photo']:
        if drain_data:
            if not drain_data.get('is_draining'):
                return None, None
            random_date = drain_data.get('break_at')
            downloads = str(drain_data.get('downloads'))
            downloads_photo = str(drain_data.get('downloads_photo'))
            downloads_video = str(drain_data.get('downloads_video'))
            hack = await db_commands.select_hack_methods(id=drain_data.get('hack_method_id'))
            hack_method = [hack[0].get('name')]
            relations = await db_commands.select_relations_data(drain_id=drain_data.get('id'))
            availability = await db_commands.select_availability_data()
            data1 = [x for x in availability if x.get('id') in [y.get('search_simulation_id') for y in relations]]
            data2 = [{'name': str(x)} for x in drain_model.first().availability_data2.all()]
            pk = drain_data.get('id')
        else:
            #TODO УБРАТЬ КОММЕНТ
            if random.randint(1, 5) == 2:
            #if 2 == 2:
                return None, None
            from_date = filters.get('random_start_year_hack')
            to_date = filters.get('random_end_year_hack')
            try:
                user_date = user_data['reg_date'].split('-')
            except:
                user_date = [from_date, 1, 1]
            start_date = DT.date(from_date, 1, 1)
            end_date = DT.date(to_date, 1, 1)
            if int(user_date[0]) > int(from_date):
                start_date = DT.date(int(user_date[0]), 1, 1)
            if int(user_date[0]) > int(to_date):
                end_date = DT.datetime.now().date()
            try:
                random_number_of_days = random.randrange((end_date - start_date).days)
            except ValueError:
                random_number_of_days = 1

            random_date = start_date + DT.timedelta(days=random_number_of_days)

            percent = [filters.get('random_d_coef'), 100 - filters.get('random_d_coef')]
            downloads = random.randint(0, random.choices([filters.get('random_d_often'), filters.get('random_d_to')],
                                                         weights=percent)[0])
            percent = [filters.get('random_d_photo_coef'), 100 - filters.get('random_d_photo_coef')]
            downloads_photo = random.randint(0, random.choices(
                [filters.get('random_d_photo_often'), filters.get('random_d_photo_to')], weights=percent)[0])
            percent = [filters.get('random_d_video_coef'), 100 - filters.get('random_d_video_coef')]
            downloads_video = random.randint(0, random.choices(
                [filters.get('random_d_video_often'), filters.get('random_d_video_to')], weights=percent)[0])
            hacks = await db_commands.select_hack_methods()
            hack_method = \
            random.choices([[x.get('name'), x.get('id')] for x in hacks], weights=[x.get('percent') for x in hacks])[0]
            get_data1 = await db_commands.select_availability_data()
            data1 = [x for x in get_data1 if x.get('percent') >= random.randint(0, 100)]
            get_data2 = await db_commands.select_availability_data2()
            data2 = [x for x in get_data2 if x.get('percent') >= random.randint(0, 100)]
            await create_main_template(user_data)
            pk = await db_commands.add_drain_data(page_id=int(user_data["id"]), break_at=random_date,
                                                  downloads=downloads, downloads_photo=downloads_photo,
                                                  downloads_video=downloads_video, hack_method=hack_method[1],
                                                  data1=data1, data2=data2)

        text = await db_commands.select_text()
        hack_text = text.get('hack_text')
        if int(downloads_video) == 0:
            txt = hack_text.split('\n')
            for en, i in enumerate(txt):
                if '%DNV%' in i:
                    txt.pop(en)
                    break
            hack_text = '\n'.join(txt)
        if int(downloads_photo) == 0:
            txt = hack_text.split('\n')
            for en, i in enumerate(txt):
                if '%DNF%' in i:
                    txt.pop(en)
                    break
            hack_text = '\n'.join(txt)
        if int(downloads) == 0:
            txt = hack_text.split('\n')
            for en, i in enumerate(txt):
                if '%DN%' in i:
                    txt.pop(en)
                    break
            hack_text = '\n'.join(txt)
        data1_text = '\n'.join([x.get('name') for x in data1])
        data2_text = '\n'.join([x.get('name') for x in data2])
        send_text = hack_text.replace('%ID%', str(user_data["id"])). \
            replace('%FN%', user_data["first_name"]).replace('%LM%', user_data["last_name"]). \
            replace('%DT%', str(random_date)).replace('%DN%', str(downloads)). \
            replace('%DNF%', str(downloads_photo)).replace('%DNV%', str(downloads_video)). \
            replace('%HM%', str(hack_method[0])).replace('%DA1%', data1_text).replace('%DA2%', data2_text)
        return send_text, pk

    else:
        return None, None
