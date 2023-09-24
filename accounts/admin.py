from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('name', 'phone', 'email', 'address', 'preview', 'gender', 'birth_date')
    fields = ['name', 'phone', 'email', 'avatar', 'gender', 'password', 'birth_date']
    list_filter = ['birth_date']
    search_fields = ['phone', 'email', 'name']

    readonly_fields = ["preview"]

    def preview(self, obj):
        if (obj.avatar):
            return mark_safe(f'<img src="/media/{obj.avatar}" height="100">')
        else:
            return '-'

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        return qs.filter(is_superuser='')

    def save_model(self, request, obj, form, change):
        old = Profile.objects.get(pk=obj.pk)
        instance = form.save(commit=False)
        if form.cleaned_data['password'] != old.password:
            instance.password = make_password(form.cleaned_data['password'])
        instance.save()

    preview.short_description = "Аватар"


admin.site.register(Profile, ProfileAdmin)
