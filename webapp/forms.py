from django import forms
from .models import PurchaseOnCredit
import datetime


class PurchaseForm(forms.ModelForm):
    passport_choices = [('1', 'ID паспорт'), ('2', 'Биометрический паспорт')]
    salary_choices = [('1', 'Продленный действующий патент'), ('2', 'Справка о доходах')]

    name = forms.CharField(label='Имя*', min_length=1, max_length=50,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control mt-0', 'id': "name"}))
    second_name = forms.CharField(label='Введите адрес', max_length=30,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control mt-0', 'id': "second_name"}))

    phone = forms.CharField(label='Номер телефона *', min_length=7, max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control mt-0', 'id': "phone"}))

    email = forms.EmailField(label='Email*', min_length=7, max_length=50,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control mt-0', 'id': "email"}))
    passport = forms.ChoiceField(label='Паспортные данные', choices=passport_choices,
                                 widget=forms.RadioSelect(attrs={'class': 'radio-btn remove-por'}))

    passport_front = forms.FileField(label='',
                                     widget=forms.FileInput(
                                         attrs={'class': 'form-control', 'accept': 'image/*', 'id': "passport_front",
                                                'placeholder': 'Прикрепить файл'}))

    passport_back = forms.FileField(label='',
                                    widget=forms.FileInput(
                                        attrs={'class': 'form-control', "accept": "image/*", 'id': "passport_back",
                                               'placeholder': 'Прикрепить файл'}))

    place_of_residence = forms.FileField(label='',
                                         widget=forms.FileInput(
                                             attrs={'class': 'form-control', "accept": "image/*",
                                                    'id': "place_of_residence", 'placeholder': 'Прикрепить файл'}))

    salary = forms.ChoiceField(label='Справка о заработной плате', choices=salary_choices,
                               widget=forms.Select(attrs={'class': 'form-control loan mt-0'}))

    salary_img = forms.FileField(label='', widget=forms.FileInput(
        attrs={'class': 'form-control', "accept": "image/*", 'id': "salary_img", 'placeholder': 'Прикрепить файл'}))

    class Meta:
        model = PurchaseOnCredit
        fields = ["name", 'phone', 'email', 'passport', 'passport_front', 'passport_back',
                  'salary', 'salary_img']

    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['place_of_residence'].required = False
        self.fields['email'].required = False
