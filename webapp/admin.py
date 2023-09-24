import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from moysklad.models import Auth
import requests
from django.utils.html import format_html
from easy_select2 import select2_modelform

# Register your models here.

def make_formalized_service(ServiceCallBack, request, queryset):
    for query in queryset:
        if (query.formalized):
            query.formalized = False
        else:
            query.formalized = True
        query.save()


def make_formalized_callback(CallBack, request, queryset):
    for query in queryset:
        if (query.formalized):
            query.formalized = False
        else:
            query.formalized = True
        query.save()


make_formalized_service.short_description = "Пометить как расмотрено или не расмотрено"
make_formalized_callback.short_description = "Пометить как расмотрено или не расмотрено"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'secondary_title', 'desc', 'pub_date', 'preview', 'active', 'order')
    model = Article
    readonly_fields = ["preview", "desc"]

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" height="auto" width="150">')
        else:
            return mark_safe(f'<img src="" height="auto" width="150">')

    def desc(self, obj):
        return mark_safe(obj.description)

    desc.short_description = "Текст"
    preview.short_description = "Изображение"

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'pub_date', 'order')
    list_filter = ['pub_date', 'category']
    model = Service


class ServiceCallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'category', 'product', 'reason', 'another', 'formalized', 'created_at')
    model = ServiceCallBack
    actions = [make_formalized_service]


class CallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'topic', 'desc', 'formalized', 'created_at')
    model = CallBack
    actions = [make_formalized_callback]


class PopularSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    model = PopularSearch




class DocumentAdmin(admin.ModelAdmin):
    list_display = ('preview', 'created_at')
    model = Document
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.docfile.url}" height="auto" width="150">')

    preview.short_description = 'Превью'


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('exchange_rate', 'is_active', 'is_valid',
                    'error', 'created_at', 'usd', 'check_connection')
    fields = ['exchange_rate', 'is_active', 'time', 'usd']
    model = Currency


    def save_model(self, request, obj, form, change):
        auth_moysklad = Auth.objects.first()
        if auth_moysklad:
            url = 'https://online.moysklad.ru/api/remap/1.2/entity/currency/{}'.format(form.cleaned_data["usd"])
            resp = requests.get(url, auth=(auth_moysklad.email, auth_moysklad.password)).json()
            if resp:
                if "errors" in resp:
                    obj.error = resp["errors"][0]["error"]
                    obj.is_valid = False
                else:
                    obj.error = ""
                    obj.is_valid = True
                    if form.cleaned_data["is_active"]:
                        obj.exchange_rate = resp["rate"]
                    
        super().save_model(request, obj, form, change)

    def check_connection(self, obj):
        return format_html(
            "<a class='grp-button'  onclick='spinner()'>Обновить товары</a>"
        )
    check_connection.short_description = 'Проверить подключение'
    check_connection.allow_tags = True
    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'sms_url', 'sms_login', 'sms_pwd', 'sms_sender_id', 'reserve_price', 'contact_first',
        'contact_second',
        'address', 'schedule', 'email', 'instagram', 'facebook', 'youtube', 'pub_date')
    fields = ['title', 'description', 'sms_url', 'sms_login', 'sms_pwd', 'sms_sender_id', 'reserve_price',
              'reserve_text', 'contact_first', 'contact_second', 'address', 'schedule', 'loan_title', 'loan_desc',
              'email', 'instagram', 'facebook', 'youtube', 'pub_date']
    model = Settings


MainPageProductsAdminForm = select2_modelform(MainPageProducts, attrs={'width': '250px'})
class MainPageProductsAdmin(admin.TabularInline):
    form = MainPageProductsAdminForm
    model = MainPageProducts


MainPageAdminForm = select2_modelform(MainPage, attrs={'width': '250px'})
class MainPageAdmin(admin.ModelAdmin):
    form = MainPageAdminForm
    list_display = (
        'second_product_title', 'second_product_desc', 'fifth_block_title', 'fifth_block_desc', 'fifth_block_link')
    model = MainPage
    inlines = [MainPageProductsAdmin]


CompareProductsAdminForm = select2_modelform(CompareProducts, attrs={'width': '300px'})
class CompareProductsAdmin(admin.TabularInline):
    form = CompareProductsAdminForm
    extra = 1
    fields = ['product', 'order']
    model = CompareProducts
    
class CompareAdmin(admin.ModelAdmin):
    model = Compare
    inlines = [CompareProductsAdmin]

class BankPercentAdmin(admin.TabularInline):
    model = BankPercents
    extra = 1


class BankAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'preview', 'desc', 'pub_date', 'order')
    model = Bank
    inlines = [BankPercentAdmin]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.img.url}" height="auto" width="150">')

    preview.short_description = 'Лого'

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class PurchaseOnCreditProductsAdmin(admin.TabularInline):
    model = PurchaseOnCreditProducts
    extra = 0


class PurchaseOnCreditAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'email', 'passport', 'passport_front', 'passport_back', 'place_of_residence', 'salary',
        'salary_img', 'pub_date')
    model = PurchaseOnCredit
    inlines = [PurchaseOnCreditProductsAdmin]


ReserveAdminForm = select2_modelform(Reserve, attrs={'width': '200px'})
class ReserveAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'product_name', 'color', 'capacity', 'payment', 'price', 'price_converted',
        'pub_date', 'last_date')
    # fields = ['name', 'phone', 'product', 'color', 'capacity', 'payment', 'price', 'price_converted', 'module',
    #           'pub_date', 'last_date']
    form = ReserveAdminForm
    model = Reserve


    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'phone')
        return self.readonly_fields

    def product_name(self, obj):
        if obj.product:
            return obj.product.product_title
        else:
            return None

    product_name.short_description = 'Продукт'


class AboutUsAdmin(admin.ModelAdmin):
    model = AboutUs

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class LoanPageAdmin(admin.ModelAdmin):
    model = LoanPage


class CategoryAdmin(admin.ModelAdmin):
    model = Category


class MainPageSliderAdmin(admin.ModelAdmin):
    model = MainPageSlider
    list_display = ('title', 'category', 'background', 'order')
    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class WarrantyAdmin(admin.ModelAdmin):
    model = Warranty

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class WhyUsAdmin(admin.ModelAdmin):
    model = WhyUs

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class FooterAdmin(admin.ModelAdmin):
    model = Footer

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class TradeInAdmin(admin.ModelAdmin):
    model = TradeIn

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    

class ContactsAdmin(admin.ModelAdmin):
    model = Contacts

class AdditionalCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'image', 'main_category', 'active')
    model = AdditionalCategory

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCallBack, ServiceCallBackAdmin)
admin.site.register(CallBack, CallBackAdmin)
admin.site.register(PopularSearch, PopularSearchAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(MainPage, MainPageAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(PurchaseOnCredit, PurchaseOnCreditAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(LoanPage, LoanPageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MainPageSlider, MainPageSliderAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(WhyUs, WhyUsAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(TradeIn, TradeInAdmin)
admin.site.register(Compare, CompareAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(AdditionalCategory, AdditionalCategoryAdmin)
