from asgiref.sync import sync_to_async
from django_project.telegrambot.usersmanage.models import *
import random


@sync_to_async
def add_user(telegram_id, username, firstname, invited_by):
    return Users(user_id=int(telegram_id), username=username, firstname=firstname, invited_by=invited_by).save()


@sync_to_async
def select_user(**kwarg):
    return Users.objects.filter(**kwarg).values().first()


@sync_to_async
def update_user(telegram_id, **kwargs):
    return Users.objects.filter(user_id=telegram_id).update(**kwargs)


@sync_to_async
def select_setting():
    return Bot.objects.values().first()


@sync_to_async
def select_text():
    return AllText.objects.values().first()


@sync_to_async
def select_qiwi(**kwargs):
    return Payment.objects.filter(**kwargs).values().all().order_by('pk')


@sync_to_async
def update_qiwi(qid, **kwargs):
    return Payment.objects.filter(id=qid).update(**kwargs)


@sync_to_async
def select_filters():
    return Filters.objects.values().first()


@sync_to_async
def select_simulation(simulation):
    if simulation:
        return SearchSimulation_true.objects.values().all()
    else:
        return SearchSimulation_false.objects.values().all()


@sync_to_async
def select_drain_data(**kwarg):
    return DrainData.objects.filter(**kwarg)


@sync_to_async
def select_drain_data_values(**kwarg):
    return DrainData.objects.filter(**kwarg).values().first()


@sync_to_async
def update_drain_data(page_id, **kwargs):
    return DrainData.objects.filter(page_id=page_id).update(**kwargs)


@sync_to_async
def add_drain_data(**kwargs):
    hm = HackMethods.objects.filter(pk=kwargs.get('hack_method')).first()
    create = kwargs.copy()
    create['hack_method'] = hm
    create['template'] = f'Files/Photos/Drain/Template/template_{kwargs["page_id"]}.jpg'
    del create['data1'], create['data2']
    model = DrainData.objects.create(**create)  # Создание строки
    for i in kwargs.get('data1'):
        availability = AvailabilityData.objects.filter(pk=i.get('id'))
        links = Links.objects.filter(method_id=availability.values().first().get('id')).values().first()
        if links:
            with open('django_project/telegrambot/Files/' + links.get('links'), encoding='utf-8') as f:
                links = random.choices(f.read().split('\n'))[0]
        RelationsData.objects.create(drain=model, search_simulation=availability.first(), link=links)

    model.availability_data2.set([x.get('id') for x in kwargs.get('data2')])
    return model.pk


@sync_to_async
def add_order(user_id, user_data, price, but1=False, but2=False):
    if but1:
        Orders(user_id=user_id, bill_id=user_data[2], buy_product='Кнопка 1', order_sum=price).save()
        return
    if but2:
        Orders(user_id=user_id, bill_id=user_data[2], buy_product='Кнопка 2', order_sum=price).save()
        return
    relation = RelationsData.objects.filter(search_simulation_id=user_data[4], drain_id=user_data[1]).values().first()
    avai = AvailabilityData.objects.filter(pk=user_data[4]).values().first().get('name')
    drain_data = DrainData.objects.filter(id=user_data[1]).values().first().get('page_id')
    Orders(user_id=user_id, buy_product=drain_data, order_type=avai, bill_id=user_data[2],
           link=relation.get('link'), order_sum=price).save()
    return relation.get('link')


@sync_to_async
def select_relations_data(**kwarg):
    return RelationsData.objects.filter(**kwarg).values().all()


@sync_to_async
def select_hack_methods(**kwarg):
    return HackMethods.objects.filter(**kwarg).values().all()


@sync_to_async
def select_availability_data(**kwarg):
    return AvailabilityData.objects.filter(**kwarg).values().all()


@sync_to_async
def select_links(**kwarg):
    return Links.objects.filter(**kwarg).values().first()


@sync_to_async
def select_availability_data2(**kwarg):
    return AvailabilityDataTwo.objects.filter(**kwarg).values().all()


@sync_to_async
def select_template(**kwarg):
    return Template.objects.filter(**kwarg).values().all()


@sync_to_async
def select_templates(**kwarg):
    return Templates.objects.filter(**kwarg).values().all()


@sync_to_async
def select_setting_template(**kwarg):
    return TemplateSetting.objects.filter(**kwarg).values().first()
