from django.contrib import admin
from .models import Auth
from django.utils.html import format_html
from django.urls import reverse
import requests
# Register your models here.

class AuthAdmin(admin.ModelAdmin):
    model = Auth
    list_display = ('email', 'password', 'is_active', 'pub_date',
                    'error', 'check_connection')
    fields = ['email', 'password']
    readonly_fields = ["is_active", "pub_date"]

    def save_model(self, request, obj, form, change):
        url = 'https://online.moysklad.ru/api/remap/1.2/security/token'
        r = requests.post(url, auth=(form.cleaned_data["email"], form.cleaned_data["password"]))
        data = r.json()
        if "errors" in data:
            obj.error = data["errors"][0]["error"]
            obj.is_active = False
        else:
            obj.is_active = True
            obj.error = ""
        super().save_model(request, obj, form, change)
    
    def check_connection(self, obj):
        return format_html(
            """<a class="grp-button" href="/moysklad/check_connection/{}">Запуск</a>
            <a class="grp-button" href="/moysklad/get_products/{}"  onclick="spinner()">Обновить</a>""".format(obj.id, obj.id)
        )
    check_connection.short_description = 'Проверить подключение'
    check_connection.allow_tags = True


admin.site.register(Auth, AuthAdmin)
