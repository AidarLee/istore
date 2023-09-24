from django import forms
from .models import Code
from .models import Profile
import datetime


class VerifyForm(forms.Form):
    name = forms.CharField(label='', min_length=2, max_length=50,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'id': "nameField",
                                      'placeholder': 'Имя'}))
    password = forms.CharField(label='', min_length=8, max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'id': "passwordField", 'placeholder': 'Пароль'}),
                               required=False)
    code = forms.CharField(label='', max_length=4,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'id': "verifyCode", 'placeholder': 'Введите код'}))

    phone = forms.CharField(label='', min_length=7, max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'id': "phoneNumber",
                                       'placeholder': 'Контактный телефон'}))
                                       

    class Meta:
        model = Code
        fields = ['phone', 'code', 'name', 'password']


class ForgetForm(forms.Form):
    code = forms.CharField(label='', max_length=4,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'id': "verifyCode", 'placeholder': 'Введите код'}))

    phone = forms.CharField(label='', min_length=7, max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control forget', 'id': "phoneNumber",
                                       'placeholder': 'Контактный телефон'}))

    class Meta:
        model = Code
        fields = ['phone', 'code']


class LoginForm(forms.Form):
    phone = forms.CharField(label='', min_length=7, max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'id': "phoneNumber",
                                       'placeholder': 'Контактный телефон или email'}))

    password = forms.CharField(label='', max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'id': "passwordField", 'placeholder': 'Пароль'}))

    class Meta:
        model = Code
        fields = ['phone', 'password']


class EditForm(forms.Form):
    gender_choices = [('Мужской', 'мужской'), ('Женский', 'женский')]

    name = forms.CharField(label='', min_length=2, max_length=50,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'id': "edit_name",
                                      'placeholder': 'ФИО'}))

    phone = forms.CharField(label='', min_length=7, max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'id': "edit_phone",
                                       'placeholder': 'Контактный телефон', 'required': 'true'}))
    address = forms.CharField(label='', max_length=30,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'id': "edit_address",
                                         'placeholder': 'Введите адрес'}))
    email = forms.EmailField(label='', min_length=7, max_length=50,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'id': "edit_email",
                                        'placeholder': 'Email', 'required': 'true'}))
    birth_date = forms.DateField(label='Дата рождения', initial=datetime.datetime.now(),
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control return-none', 'id': "edit_date",
                                            'placeholder': ''}))
    gender = forms.ChoiceField(label='Пол', choices=gender_choices,
                               widget=forms.RadioSelect(attrs={'class': 'radio-btn'}), initial='Мужской')

    password = forms.CharField(label='', max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'id': "passwordField", 'placeholder': 'Пароль', 'autocomplete':'off'}),
                               required=False)

    def save(self, request):
        user = Profile.objects.get(id=request.user.id)
        user.name = request.POST['name']
        user.email = request.POST['email']
        if 'birth_date' in request.POST:
            if request.POST['birth_date']:
                user.birth_date = request.POST['birth_date']
        user.gender = request.POST['gender']
        user.phone = request.POST['phone']
        if 'address' in request.POST:
            user.address = request.POST['address']
        if request.POST['password']:
            user.set_password(request.POST['password'])
        user.save()
        return user

    class Meta:
        model = Profile
        fields = ['name', 'phone', 'email', 'address',
                  'birth_date', 'gender', 'phone']
        required = ['phone']
        widgets = {
            'birth_date': forms.DateInput(format=('%m/%d/%Y'),
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['address'].required = False
        self.fields['email'].required = False
        self.fields['birth_date'].required = False
