from django.contrib import admin
from django.http import HttpResponseRedirect
from django.db.models import QuerySet
from django.shortcuts import render
from django.core import validators
from .views import startSpam, startNotification
from django.contrib import messages
from .forms import BroadcastForm, BulkUploadForm
from .models import *
import asyncio
from ..management.functions import qiwi_check





@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "created_at", "balance")
    search_fields = ('user_id', 'username', 'firstname')
    list_editable = ("balance",)
    #exclude = ('last_search_link',)

    actions = ('broadcast',)

    def broadcast(self, request, queryset):
        if 'apply_broadcast' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]
            # получить результат от doSpam
            message_result = startSpam([u.user_id for u in queryset], broadcast_message_text)
            self.message_user(request, message_result, level=messages.SUCCESS)  # использовать результат в качестве сообщения
            return HttpResponseRedirect(request.get_full_path())
        elif 'apply_notification' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]
            if 'default' in broadcast_message_text.lower():
                broadcast_message_text = AllText.objects.values().first().get('text_notification')
            messages_result = startNotification([[u.user_id, u.last_search_link] for u in queryset if u.last_search_link], broadcast_message_text)

            #print(users_info)
        form = BroadcastForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        return render(request, 'admin/broadcast_message.html', {'form': form, 'users_count': len([u.user_id for u in queryset])})

    broadcast.short_description = u"Рассылка"

    def has_add_permission(self, request):
        return False


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("name", 'admins', 'support_link', 'damps_percentage', 'ref_min_widthdraw',)
    list_editable = ('admins', 'support_link', 'damps_percentage', 'ref_min_widthdraw')
    readonly_fields = ('name', 'hide_token')
    exclude = ('token',)

    def hide_token(self, obj):
        return f'{obj.token[:20]}...{obj.token[-15:]}'

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    hide_token.short_description = "Токен"


class RelationsDataAdmin(admin.TabularInline):
    verbose_name = 'Данные'
    verbose_name_plural = 'Данные'
    model = RelationsData
    extra = 0


@admin.register(DrainData)
class DrainDataAdmin(admin.ModelAdmin):
    list_display = (
        'page_id', 'break_at', 'downloads', 'downloads_photo', 'downloads_video', 'hack_method', 'is_draining')
    search_fields = ('page_id',)
    list_editable = ('downloads', 'downloads_photo', 'downloads_video', 'hack_method', 'is_draining',)
    exclude = ('factor',)
    inlines = [RelationsDataAdmin]


class SearchSimulationInline_true(admin.TabularInline):
    verbose_name = 'Имитацию'
    verbose_name_plural = 'Имитация True'
    model = SearchSimulation_true
    ordering = ['id']
    extra = 0


class SearchSimulationInline_false(admin.TabularInline):
    verbose_name = 'Имитацию'
    verbose_name_plural = 'Имитация False'
    model = SearchSimulation_false
    extra = 0


class HackMethodsInline(admin.TabularInline):
    verbose_name = 'Метод'
    verbose_name_plural = 'Методы взлома'
    model = HackMethods
    extra = 0


class AvailabilityDataInline(admin.TabularInline):
    verbose_name = 'Данные'
    verbose_name_plural = 'Данные'
    model = AvailabilityData
    extra = 0


class AvailabilityDataTwoInline(admin.TabularInline):
    verbose_name = 'Данные 2'
    verbose_name_plural = 'Данные 2'
    model = AvailabilityDataTwo
    extra = 0


class LinkInline(admin.TabularInline):
    verbose_name = 'Ссылка'
    verbose_name_plural = 'Ссылки'
    model = Links
    extra = 0


class TemplatesInline(admin.TabularInline):
    verbose_name = 'Настройка'
    verbose_name_plural = 'Настройки'
    model = Templates
    extra = 0


@admin.register(Filters)
class FiltersAdmin(admin.ModelAdmin):
    list_display = ('case_name',)

    inlines = [SearchSimulationInline_true, SearchSimulationInline_false, HackMethodsInline, AvailabilityDataInline,
               AvailabilityDataTwoInline, LinkInline]

    filters = (('random_d_to', 'random_d_often', 'random_d_coef'),
               ('random_d_photo_to', 'random_d_photo_often', 'random_d_photo_coef'),
               ('random_d_video_to', 'random_d_video_often', 'random_d_video_coef'),
               ('random_start_year_hack', 'random_end_year_hack'))

    fieldsets = (
        ("Фильтры", {"fields": filters}),
    )
    jazzmin_section_order = ("Фильтры")

    def case_name(self, obj):
        return 'Настройка фильтров'

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AllText)
class UserAdmin(admin.ModelAdmin):
    list_display = ('case_name',)
    text = ('start_text', 'search_text', 'start_photo', 'hack_text', 'set_download_text', 'download_text',
            'support_text', 'text_notification', ('button1_text', 'button1_pay_text'), ('button2_text', 'button2_pay_text'))
    buttons = (('but1', 'but2', 'but3'), ('but4', 'but5', 'download_but'),
               ('select_pay_but', 'pay_but', 'back_but'), ('go_to_pay_but', 'check_pay_but', 'cancel_pay_but'),
               ('paid_qiwi_but', 'but1_but', 'but2_but'), 'button1_2_well_but')
    referal = ('ref_text', 'ref_no_money_text', 'ref_widthdraw_text', 'ref_well_widthdraw',
               'ref_admin_notification')
    payment = ('method_text', 'pay_text', 'qiwi_waiting', 'qiwi_paid', 'qiwi_rejected')

    fieldsets = (
        ("Кнопки", {"fields": buttons}),
        ("Текст", {"fields": text}),
        ("Реф. Текст", {"fields": referal}),
        ("Оплата", {"fields": payment}),
    )
    jazzmin_section_order = ("Текст", "Кнопки")

    def case_name(self, obj):
        return 'Настроить текст'

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    inlines = [TemplatesInline, ]


@admin.register(TemplateSetting)
class TemplateSettingAdmin(admin.ModelAdmin):
    main = (
        'main_template', ('coord1', 'size1', 'crop1'), ('coord2', 'size2', 'crop2'),
        ('coord3', 'size3', 'crop3'), ('coord4', 'size4', 'crop4'), ('coord5', 'size5', 'crop5'),
        ('coord6', 'size6', 'crop6'), ('coord7', 'size7', 'crop7'), ('coord8', 'size8', 'crop8'),
        ('coord_name', 'size_name', 'color_name'), ('coord_ava', 'size_ava'))
    add = ('watermark', ('coord_watermark', 'is_watermark'), ('template_from', 'template_to'), 'blur')

    fieldsets = (
        ("Коллаж", {"fields": main}),
        ("Дополнительно", {"fields": add}),
    )
    jazzmin_section_order = ("Коллаж",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("shop", 'use_count_all', 'balance', 'status')
    readonly_fields = ('use_count_all', 'balance', 'use_count_day', 'use_count_month')
    exclude = ('use_count_all',)
    text = ('api_id', 'api_key', 'secret_key', 'shop', ('limit_day', 'limit_month'),
            'use_count_day', 'use_count_month', 'use_count_all', 'balance', 'status')
    fieldsets = (("Настройки", {"fields": text}),)

    actions = ('update_qiwi',)

    def has_delete_permission(self, request, obj=None):
        return False



    # def save_model(self, request, obj, form, change):
    #     obj.save()
        # try:
        #     balance = asyncio.run(qiwi_check.get_qiwi_balance(str(obj.token), str(obj.number)))
        #     print(balance)
        #     asyncio.run(qiwi_check.check_valid_qiwi(obj.p2p_token))
        #     obj.balance = f'{balance.amount} ({balance.currency.name})'
        #     obj.save()
        # except Exception as e:
        #     obj.status = '0'
        #     obj.save()
        #     self.message_user(request, f'Ошибка: {e}', level=messages.ERROR)

    # def update_qiwi(self, request, queryset: QuerySet):
    #     for qiwi in queryset:
    #         try:
    #             balance = asyncio.run(qiwi_check.get_qiwi_balance(qiwi.token, qiwi.number))
    #             qiwi.balance = f'{balance.amount} ({balance.currency.name})'
    #             qiwi.save()
    #             asyncio.run(qiwi_check.check_valid_qiwi(qiwi.p2p_token))
    #             qiwi.status = '1'
    #             qiwi.save()
    #             self.message_user(request, f'{qiwi.number}: Обновлен!', level=messages.SUCCESS)
    #         except Exception as e:
    #             self.message_user(request, f'{qiwi.number}: Ошибка: {e}', level=messages.ERROR)
    #             qiwi.status = '0'
    #             qiwi.save()
    #             continue


from django.utils.html import format_html


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("user_id", "break_at", "buy_product", "order_sum", "show_link",)
    readonly_fields = ("user_id", "break_at", "bill_id", "order_sum", "order_type", "buy_product", "show_link")
    exclude = ('link',)

    def show_link(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)

    show_link.short_description = "Ссылка"
