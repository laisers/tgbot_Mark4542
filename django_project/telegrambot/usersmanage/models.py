from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator




############################ INLINES MODELS ############################
class SearchSimulation_true(models.Model):
    objects = models.Model
    name = models.CharField(max_length=4024, verbose_name=u'Текст')
    timing = models.IntegerField(default=2, verbose_name=u'Тайминг')
    search_simulation = models.ForeignKey('Filters', related_name="Simulation_True", on_delete=models.SET_NULL,
                                          blank=True, null=True)


class SearchSimulation_false(models.Model):
    objects = models.Model
    name = models.CharField(max_length=4024, verbose_name=u'Текст')
    timing = models.IntegerField(default=2, verbose_name=u'Тайминг')
    search_simulation = models.ForeignKey('Filters', related_name="Simulation_False", on_delete=models.SET_NULL,
                                          blank=True, null=True)


class HackMethods(models.Model):
    objects = models.Model
    name = models.CharField(max_length=4024, verbose_name=u'Текст')
    percent = models.IntegerField(default=0, verbose_name=u'Процент',
                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    search_simulation = models.ForeignKey('Filters', related_name="hack_methods", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class RelationsData(models.Model):
    objects = models.Model
    search_simulation = models.ForeignKey('AvailabilityData', related_name="RelationsData", verbose_name=u'Имитация',
                                          on_delete=models.CASCADE)
    drain = models.ForeignKey('DrainData', related_name="drain_id", on_delete=models.CASCADE, blank=True)
    link = models.CharField(max_length=4024, verbose_name=u'Ссылка', null=True, blank=True)


class AvailabilityData(models.Model):
    objects = models.Model
    name = models.CharField(max_length=4024, verbose_name=u'Текст')
    name_but = models.CharField(max_length=4024, verbose_name=u'Кнопка')
    percent = models.IntegerField(default=0, verbose_name=u'Процент',
                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    price = models.IntegerField(default=0, verbose_name=u'Цена')
    search_simulation = models.ForeignKey('Filters', related_name="availability_data", on_delete=models.CASCADE,
                                          blank=True)

    def __str__(self):
        return self.name


class AvailabilityDataTwo(models.Model):
    objects = models.Model
    name = models.CharField(max_length=4024, verbose_name=u'Текст')
    percent = models.IntegerField(default=0, verbose_name=u'Процент',
                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    search_simulation = models.ForeignKey('Filters', related_name="availability_data_two", on_delete=models.CASCADE,
                                          blank=True)

    def __str__(self):
        return self.name


class Links(models.Model):
    objects = models.Model
    method = models.ForeignKey(AvailabilityData, on_delete=models.PROTECT, verbose_name='Метод')
    links = models.FileField(upload_to='links', verbose_name='Коллаж')
    search_simulation = models.ForeignKey('Filters', related_name="link", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.links)





############################ MODELS ############################
class Users(models.Model):
    objects = models.Model
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name=u'ID пользователя Телеграм')
    username = models.CharField(max_length=100, verbose_name=u'Логин пользователя', null=True)
    firstname = models.CharField(max_length=100, verbose_name=u'Имя пользователя', null=True)
    created_at = models.DateTimeField(verbose_name=u'Дата регистрации', auto_now=True)
    invited_by = models.BigIntegerField(verbose_name=u'По приглашению', null=True, blank=True)
    ref_count = models.IntegerField(default=0, verbose_name=u'Кол-во рефералов')
    ref_link = models.IntegerField(default=0, verbose_name=u'Кол-во ссылок')
    balance = models.IntegerField(default=0, verbose_name=u'Баланс')
    subscribed = models.IntegerField(default=0, verbose_name=u'subscribed')
    last_search_link = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = u'Пользователи'
        verbose_name_plural = u'Пользователи'


class DrainData(models.Model):
    objects = models.Model
    page_id = models.BigIntegerField(unique=True, default=1, verbose_name=u'ID страницы VK')
    break_at = models.DateField(verbose_name=u'Дата взлома')
    downloads = models.IntegerField(default=0, verbose_name=u'Скачано')
    downloads_photo = models.IntegerField(default=0, verbose_name=u'Скачано Фото')
    downloads_video = models.IntegerField(default=0, verbose_name=u'Скачано Видео')
    hack_method = models.ForeignKey('HackMethods', on_delete=models.PROTECT, verbose_name=u'Метод взлома', null=True,
                                    blank=True)
    availability_data2 = models.ManyToManyField('AvailabilityDataTwo', verbose_name='Данные 2', blank=True)
    template = models.ImageField(upload_to='Files/Photos/Template', verbose_name='Шаблон пользователя', blank=True)
    is_draining = models.BooleanField(default=1, verbose_name=u'Есть слив')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = DrainData.objects.get(pk=self.pk)
            if old_self.template and self.template != old_self.template:
                old_self.template.delete(False)
        return super(DrainData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Данные сливов'
        verbose_name_plural = u'Данные сливов'

    def __str__(self):
        return str(self.page_id)


class Bot(models.Model):
    objects = models.Model
    token = models.CharField(max_length=100, verbose_name=u'Token')
    vk_token = models.CharField(max_length=250, verbose_name=u'Token VK')
    name = models.CharField(max_length=100, verbose_name=u'Bot Name')
    admins = models.CharField(max_length=1000, verbose_name=u'Админы', help_text='Через запятую без пробела')
    support_link = models.CharField(max_length=1000, verbose_name=u'Ссылка поддержки')
    damps_percentage = models.FileField(upload_to='Files/links/ref_link', verbose_name=u'Дампы рефералов')
    ref_min_widthdraw = models.IntegerField(default=500, verbose_name=u'Минималка на вывод')
    price_but1 = models.IntegerField(default=100, verbose_name=u'Цена кнопки 1')
    link_but1 = models.CharField(max_length=1000, verbose_name=u'Ссылка 1')
    price_but2 = models.IntegerField(default=100, verbose_name=u'Цена кнопки 2')
    link_but2 = models.CharField(max_length=1000, verbose_name=u'Ссылка 2')
    google_token = models.CharField(max_length=250, verbose_name=u'Google токен')


    class Meta:
        verbose_name = u'Настройки'
        verbose_name_plural = u'Настройки'

    def __str__(self):
        return 'Настройки'


class AllText(models.Model):
    objects = models.Model
    start_text = models.TextField(max_length=4024, verbose_name=u'Текст приветсвия',
                                  help_text=u'%LN% - Last Name | %FN% - First Name')
    search_text = models.TextField(max_length=4024, verbose_name=u'Найти сливы')
    start_photo = models.ImageField(upload_to='Files/Photos/', verbose_name='Картинка')
    hack_text = models.TextField(max_length=4024, verbose_name=u'Текст взлома',
                                 help_text='%ID%-ID | %FN%-FirstName | %LM%-LastName | %DT%-Date | '
                                           '%DN%-Downloads | %DNF%-Downl photo | %DNV%-Downl video | %HM%-Method | '
                                           '%DA%-Data | %DA2%-Data2')
    ref_text = models.TextField(max_length=4024, verbose_name=u'Рефка',
                                help_text=u'"Реф.Система" | %ref% | %bal% | %link% | %links%')


    ref_no_money_text = models.TextField(max_length=4024, verbose_name=u'Нет денег', help_text=u'%bal%')
    ref_widthdraw_text = models.TextField(max_length=4024, verbose_name=u'Вывод', help_text=u'%bal%')
    ref_well_widthdraw = models.TextField(max_length=4024, verbose_name=u'Заявка на вывод', help_text=u'%bal%')
    ref_admin_notification = models.TextField(max_length=4024, verbose_name=u'Уведомление админам',
                                              help_text=u'%UN% | %ID% | %bal% | %cred%')
    button1_text = models.TextField(max_length=4024, verbose_name=u'Кнопка 1', help_text=u'Текст при нажатии "1"')
    button1_pay_text = models.TextField(max_length=4024, verbose_name=u'', help_text=u'Текст после оплаты "1" ')
    button2_text = models.TextField(max_length=4024, verbose_name=u'Кнопка 2', help_text=u'Текст при нажатии "2"')
    button2_pay_text = models.TextField(max_length=4024, verbose_name=u'', help_text=u'Текст после оплаты "2" ')

    support_text = models.TextField(max_length=4024, verbose_name=u'Поддержка',
                                    help_text=u'Текст при нажатии "Поддержка"')
    set_download_text = models.TextField(max_length=4024, verbose_name=u'Скачать1')
    download_text = models.TextField(max_length=4024, verbose_name=u'Скачать', help_text=u'Текст при нажатии "Скачать"')
    method_text = models.TextField(max_length=4024, verbose_name=u'Способ', help_text=u'Выбор способа оплаты')
    pay_text = models.TextField(max_length=4024, verbose_name=u'Оплата', help_text=u'Текст оплаты')
    get_product_text = models.TextField(max_length=4024, verbose_name=u'Оплата', help_text=u'Текст после покупки')
    qiwi_waiting = models.TextField(max_length=20, verbose_name=u'WAITING', help_text=u'Ожидание оплаты')
    qiwi_paid = models.TextField(max_length=4024, verbose_name=u'PAID', help_text=u'Оплачено')
    qiwi_rejected = models.TextField(max_length=4024, verbose_name=u'REJECTED', help_text=u'Оплата отменена')

    but1 = models.CharField(max_length=30, verbose_name=u'Кнопка 1', help_text=u'Найти сливы')
    but2 = models.CharField(max_length=30, verbose_name=u'Кнопка 2', help_text=u'Поддержка')
    but3 = models.CharField(max_length=30, verbose_name=u'Кнопка 3', help_text='1')
    but4 = models.CharField(max_length=30, verbose_name=u'Кнопка 4', help_text='2')
    but5 = models.CharField(max_length=30, verbose_name=u'Кнопка 5', help_text=u'Реф')
    download_but = models.CharField(max_length=30, verbose_name=u'Кнопка 6', help_text=u'Скачать')
    select_pay_but = models.CharField(max_length=30, verbose_name=u'Кнопка 7', help_text=u'Способ оплаты')
    pay_but = models.CharField(max_length=30, verbose_name=u'Кнопка 8', help_text=u'Оплата')
    back_but = models.CharField(max_length=30, verbose_name=u'Кнопка 10', help_text=u'Отмена назад')
    go_to_pay_but = models.CharField(max_length=30, verbose_name=u'Кнопка 11', help_text=u'Перейти к оплате')
    check_pay_but = models.CharField(max_length=30, verbose_name=u'Кнопка 12', help_text=u'Проверка оплаты')
    cancel_pay_but = models.CharField(max_length=30, verbose_name=u'Кнопка 13', help_text=u'Отмена оплаты')
    get_product_but = models.CharField(max_length=30, verbose_name=u'Кнопка 14', help_text=u'Кнопка с ссылкой на товар')
    paid_qiwi_but = models.CharField(max_length=30, verbose_name=u'Кнопка 14', help_text=u'Кнопка скачать')
    but1_but = models.CharField(max_length=30, verbose_name=u'Кнопка 15', help_text=u'Кнопка с ссылкой 1')
    but2_but = models.CharField(max_length=30, verbose_name=u'Кнопка 16', help_text=u'Кнопка с ссылкой 2')
    button1_2_well_but = models.CharField(max_length=30, verbose_name=u'Кнопка 17',
                                          help_text=u'Кнопка после оплаты "1 и 2"')
    text_notification = models.TextField(max_length=4024, verbose_name=u'Рассылка',
                                         help_text=u'Стандартный текст уведомления. %LN% - Last Name |'
                                                   u' %FN% - First Name | %ID% - ID')

    class Meta:
        verbose_name = u'Текст'
        verbose_name_plural = u'Текст'


class Filters(models.Model):
    objects = models.Model
    random_d_to = models.IntegerField(default=0, verbose_name=u'Рандом скачек. ДО')
    random_d_often = models.IntegerField(default=0, verbose_name=u'Чаще')
    random_d_coef = models.IntegerField(default=0, verbose_name=u'Процент',
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])
    random_d_photo_to = models.IntegerField(default=0, verbose_name=u'Рандом на фото. ДО')
    random_d_photo_often = models.IntegerField(default=0, verbose_name=u'Чаще')
    random_d_photo_coef = models.IntegerField(default=0, verbose_name=u'Процент',
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    random_d_video_to = models.IntegerField(default=0, verbose_name=u'Рандом на фото. ДО')
    random_d_video_often = models.IntegerField(default=0, verbose_name=u'Чаще')
    random_d_video_coef = models.IntegerField(default=0, verbose_name=u'Процент',
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    random_start_year_hack = models.IntegerField(default=2006, verbose_name=u'Год взлома. От')
    random_end_year_hack = models.IntegerField(default=2014, verbose_name=u'До')

    class Meta:
        verbose_name = u'Фильтры'
        verbose_name_plural = u'Фильтр'


class Payment(models.Model):
    objects = models.Model
    STATUS = (('1', '✅'), ('0', '❌'))
    api_id = models.CharField(max_length=100, verbose_name=u'ApiID')
    api_key = models.CharField(max_length=100, verbose_name=u'ApiKey')
    secret_key = models.CharField(max_length=100, verbose_name=u'SecretKey')
    shop = models.CharField(max_length=10, verbose_name=u'shop')
    limit_day = models.IntegerField(default=0, verbose_name=u'Лимит в день')
    use_count_day = models.IntegerField(default=0, verbose_name=u'Сегодня')
    date_day = models.DateTimeField(auto_now=True)
    limit_month = models.IntegerField(default=0, verbose_name=u'Лимит в месяц')
    use_count_month = models.IntegerField(default=0, verbose_name=u'В этом месяце')
    date_month = models.DateTimeField(auto_now=True)
    use_count_all = models.IntegerField(default=0, verbose_name=u'Всего оплат')
    balance = models.CharField(default=0, max_length=100, verbose_name=u'Баланс')
    use_count = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS, default='1', verbose_name='Статус')

    class Meta:
        verbose_name = u'Платежка'
        verbose_name_plural = u'Платежка'

    def __str__(self):
        return self.shop


class Orders(models.Model):
    user_id = models.BigIntegerField(verbose_name=u'User ID')
    break_at = models.DateField(verbose_name=u'Время покупки', auto_now=True)
    bill_id = models.CharField(max_length=1000, verbose_name=u'Номер заказа')
    order_sum = models.IntegerField(default=0, verbose_name='Сумма')
    order_type = models.CharField(max_length=1000, verbose_name=u'Тип')
    buy_product = models.CharField(max_length=1000, verbose_name=u'Товар')
    link = models.CharField(max_length=1000)

    class Meta:
        verbose_name = u'Покупка'
        verbose_name_plural = u'Покупки'

    def __str__(self):
        return str(self.pk)

class Template(models.Model):
    template = models.ImageField(upload_to='Files/Photos/templates', verbose_name='Шаблон')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = Template.objects.get(pk=self.pk)
            if old_self.template and self.template != old_self.template:
                old_self.template.delete(False)
        return super(Template, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Шаблон'
        verbose_name_plural = u'Шаблоны'

    def __str__(self):
        return u'Шаблон'


class Templates(models.Model):
    objects = models.Model
    METHODS = (('1', 'Мини ава'), ('2', 'Ава'), ('3', 'Ава друга(Ж)'), ('4', 'Фото друга(Ж)'), ('5', 'Ава друга(М)'),
               ('6', 'Фото друга(М)'), ('7', 'Рандом фото'), ('8', 'ФИО'), ('9', 'ФИО друга(Ж)'),
               ('10', 'ФИО друга(М)'))
    method = models.CharField(max_length=2, choices=METHODS, default='1', verbose_name='Метод')
    coord_x1 = models.IntegerField(default=0, verbose_name='X1')
    coord_y1 = models.IntegerField(default=0, verbose_name='Y1')
    size = models.CharField(max_length=100, verbose_name='Размер', help_text='200 200', default='200 200')
    color = models.CharField(max_length=100, default='#000000', verbose_name='Цвет текста')

    template_name = models.ForeignKey(Template, related_name="Template_name", on_delete=models.CASCADE,
                                      blank=True, null=True)

    def save(self, *args, **kwargs):
        print('_______________')
        print(self.method)

        # if self.pk is not None:
        #     old_self = TemplateSetting.objects.get(pk=self.pk)
        #     if old_self.main_template and self.main_template != old_self.main_template:
        #         old_self.main_template.delete(False)
        #     if old_self.watermark and self.watermark != old_self.watermark:
        #         old_self.watermark.delete(False)
        # return super(TemplateSetting, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Настройка'
        verbose_name_plural = u'Настройки'

    def __str__(self):
        return u'Настройка'


class TemplateSetting(models.Model):
    objects = models.Model
    main_template = models.ImageField(upload_to='Photos', verbose_name='Коллаж')
    coord1 = models.CharField(default='51 215', max_length=30, verbose_name='XY 1',
                              help_text='Корды XY верхней левой точки')
    size1 = models.CharField(default='235 293', max_length=30, verbose_name='Размер 1', help_text='Размер фото')
    crop1 = models.BooleanField(default=False, verbose_name='Обрезка 1', help_text='Обрежет фото под размеры')
    coord2 = models.CharField(default='291 215', max_length=30, verbose_name='XY 2')
    size2 = models.CharField(default='235 293', max_length=30, verbose_name='Размер 2')
    crop2 = models.BooleanField(default=False, verbose_name='Обрезка 2')
    coord3 = models.CharField(default='291 513', max_length=30, verbose_name='XY 3')
    size3 = models.CharField(default='235 293', max_length=30, verbose_name='Размер 3')
    crop3 = models.BooleanField(default=False, verbose_name='Обрезка 3')
    coord4 = models.CharField(default='51 513', max_length=30, verbose_name='XY 4')
    size4 = models.CharField(default='235 293', max_length=30, verbose_name='Размер 4')
    crop4 = models.BooleanField(default=False, verbose_name='Обрезка')
    coord5 = models.CharField(default=0, max_length=30, verbose_name='XY 5')
    size5 = models.CharField(default=0, max_length=30, verbose_name='Размер 5')
    crop5 = models.BooleanField(default=False, verbose_name='Обрезка')
    coord6 = models.CharField(default=0, max_length=30, verbose_name='XY 6')
    size6 = models.CharField(default=0, max_length=30, verbose_name='Размер 6')
    crop6 = models.BooleanField(default=False, verbose_name='Обрезка')
    coord7 = models.CharField(default=0, max_length=30, verbose_name='XY 7')
    size7 = models.CharField(default=0, max_length=30, verbose_name='Размер 7')
    crop7 = models.BooleanField(default=False, verbose_name='Обрезка')
    coord8 = models.CharField(default=0, max_length=30, verbose_name='XY 8')
    size8 = models.CharField(default=0, max_length=30, verbose_name='Размер 8')
    crop8 = models.BooleanField(default=False, verbose_name='Обрезка')
    coord_name = models.CharField(default=0, max_length=30, verbose_name='XY ФИО')
    size_name = models.CharField(default=0, max_length=30, verbose_name='Размер ФИО')
    color_name = models.CharField(default=0, max_length=30, verbose_name='Цвет')
    coord_ava = models.CharField(default=0, max_length=30, verbose_name='XY ава')
    size_ava = models.CharField(default=0, max_length=30, verbose_name='Размер ава')
    watermark = models.ImageField(upload_to='Photos', verbose_name='Watermark')
    is_watermark = models.BooleanField(default=True, verbose_name='is watermark')
    coord_watermark = models.CharField(default=0, max_length=30, verbose_name='XY watermark')
    blur = models.IntegerField(default=10, verbose_name='Размытие')
    template_from = models.IntegerField(default=1, verbose_name='Шаблонов От', help_text='Кол-во шаблонов в коллаже')
    template_to = models.IntegerField(default=3, verbose_name='Шаблонов До')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = TemplateSetting.objects.get(pk=self.pk)
            if old_self.main_template and self.main_template != old_self.main_template:
                old_self.main_template.delete(False)
            if old_self.watermark and self.watermark != old_self.watermark:
                old_self.watermark.delete(False)
        return super(TemplateSetting, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Настройки шаблона'
        verbose_name_plural = u'Настройки шаблона'

    def __str__(self):
        return u'Настройки шаблона'


###################### DELETE PHOTOS ######################
@receiver(pre_delete, sender=Template)
def template_delete(sender, instance, **kwargs):
    instance.template.delete(False)


@receiver(pre_delete, sender=DrainData)
def drain_delete(sender, instance, **kwargs):
    instance.template.delete(False)


@receiver(pre_delete, sender=AllText)
def text_delete(sender, instance, **kwargs):
    instance.start_photo.delete(False)
