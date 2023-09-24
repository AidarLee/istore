from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from uuid import uuid4
from django.db.models import Q

gender_choices = [('Мужской', 'мужской'), ('Женский', 'женский')]


class ProfileManager(BaseUserManager):
    def create_user(self, username=None, email=None, phone=None, password=None):
        try:
            user = Profile.objects.get(email=username)
            print("suseris", user.email)
        except:
            user = Profile()
            user.email = email
            user.phone = phone
            user.set_password(password)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.is_admin = False
            user.save()
        return user

    def create_superuser(self, phone, password):
        user = Profile()
        user.phone = phone
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.save()

    def get_by_natural_key(self, phone):
        return self.get(phone=phone)


class Profile(AbstractBaseUser, models.Model):
    objects = ProfileManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    name = models.CharField('ФИО', null=True, blank=True, max_length=50)
    email = models.EmailField(
        'Email', null=True, unique=True, blank=True, max_length=100)
    password = models.CharField('Пароль', null=True, blank=True, max_length=250, help_text="Пароль зашифрован, его можно только изменить")
    avatar = models.ImageField('Аватар', null=True, blank=True, upload_to='user_pics')
    phone = models.CharField('Телефон', unique=True, null=True, blank=True, max_length=20, default=None)
    address = models.CharField('Адрес', null=True, blank=True, max_length=30)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', null=True, blank=True, max_length=20, choices=gender_choices)
    vf_code = models.CharField(null=True, blank=True, max_length=20)
    fb_id = models.CharField(null=True, blank=True, max_length=120)
    is_active = models.BooleanField(null=True, blank=True)
    is_superuser = models.BooleanField(null=True, blank=True)
    is_staff = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.phone or self.name

    

    def authenticate(self, username, password):
        print("hererererere", username)
        try:
            user = Profile.objects.get(
                Q(email=username) | Q(phone=username))
        except:
            return None
        return user if user.check_password(password) else None

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        return False

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    def set_password(self, password):
        self.password = make_password(password)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Code(models.Model):
    phone = models.CharField(null=True, blank=True, max_length=20)
    code = models.CharField(null=True, blank=True, max_length=20)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = 'Временный код'
        verbose_name_plural = 'Временные коды'


class Address(models.Model):
    place = models.CharField(null=True, blank=True, max_length=100)
    user = models.OneToOneField(Profile, related_name="user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
