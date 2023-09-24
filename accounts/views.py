import urllib

import requests
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .forms import VerifyForm, ForgetForm, LoginForm, EditForm
from .models import Profile, Code
from products.models import Order
from webapp.models import Settings, Reserve
import google.oauth2.credentials
import google_auth_oauthlib.flow
from source.settings import BASE_DIR
import random
import string
import datetime
from datetime import timedelta
import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from pyfacebook import GraphAPI
from django.db.models import Q
import jwt
import json


send_message_to_mail = "info@istore.kg"
# send_message_to_mail = "kaarov8@gmail.com"
send_message_from_mail = "testingfor9999@gmail.com"
link  = "https://istore.kg"
def verify_code(phone, code):
    if Code.objects.filter(phone=phone, code=code).exists():
        return True
    return False


def create_user(name, phone, password):
    user = Profile()
    user.password = make_password(password)
    user.name = name
    user.phone = phone
    user.save()
    return user


def get_user(phone):
    user = Profile.objects.get(Q(email=phone) | Q(phone=phone))
    return user


def user_exists(phone):
    user = Profile.objects.filter(Q(email=phone) | Q(phone=phone)).count()

    if user:
        return True
    else:
        return False


# Create your views here.
def login_user(request):
    context = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        phone = request.POST['phone']
        password = request.POST['password']
        if form.is_valid():
            if user_exists(phone):
                user = get_user(phone)
                if check_password(password, user.password):
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    if user.is_staff:
                        return HttpResponseRedirect('/catalog')
                    return HttpResponseRedirect('profile')
                else:
                    context = True
            else:
                context = True
    else:
        form = LoginForm()
    return render(request, 'auth/login.html',
                  {'form': form, 'has_error': context})

# Create your views here.
def login_google(request):
    context = False
    if request.method == 'GET':
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            str(BASE_DIR) + '/accounts/client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email'])
        flow.redirect_uri = link + '/accounts/login_google_resp'
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            prompt='select_account',
            include_granted_scopes='true')
        return redirect(authorization_url)
    else:
        form = LoginForm()
    return render(request, 'auth/login.html',
                  {'form': form, 'has_error': context})


def login_google_resp(request):
    params = {
        'code': request.GET.get('code'),
        'redirect_uri': link+ "/accounts/login_google_resp",
        'client_id': '1095023957265-l2rtcccmeckvfdlqi45p0g2ne3logptv.apps.googleusercontent.com',
        'client_secret': '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',
        'grant_type': 'authorization_code'
    }

    url = "https://oauth2.googleapis.com/token"
    r = requests.post(url=url, params=params)
    r_dictionary = r.json()
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    params = {
        'id_token': r_dictionary['id_token']
    }
    
    r = requests.get(url=url, params=params)
    profile = r.json()
    try:
        user = Profile.objects.get(email=profile['email'])
    except:
        user = Profile()
        letters = string.ascii_lowercase
        rand_passwd = ''.join(random.choice(letters) for i in range(8))
        user.password = make_password(rand_passwd)
        user.name = profile['name']
        user.email = profile['email']
        user.save()
        msg_html = render_to_string(
            'mail/new_user.html', {'email': user.email, 'password': rand_passwd})
        send_mail(
            'Добро пожаловать в iStore',
            '',
            send_message_from_mail,
            [send_message_to_mail],
            fail_silently=True,
            html_message=msg_html
        )
    if user:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponseRedirect('profile')


# Create your views here.
def login_facebook(request):
    api = GraphAPI(app_id="1579664409045076",
                   app_secret="29163012b1f144c9435c189d71a82ffb", oauth_flow=True)
    # api.exchange_user_access_token(response="url redirected")
    url = api.get_authorization_url(redirect_uri=link+"/accounts/login_facebook_resp", scope="email")
    return redirect(url[0])


def login_facebook_resp(request):
    url = "https://graph.facebook.com/v12.0/oauth/access_token"
    params = {
        'client_id': '1579664409045076',
        'client_secret': '29163012b1f144c9435c189d71a82ffb',
        'redirect_uri': link+"/accounts/login_facebook_resp",
        'code': request.GET.get('code'),
    }
    r = requests.get(url=url, params=params)
    profile = r.json()
    try:
        params = {
            'fields': 'id,name,email',
            'access_token': profile['access_token'],
        }
        url = "https://graph.facebook.com/me"
        r = requests.get(url=url, params=params)
        user_id = r.json()
        email = ""
        if 'email' in user_id:
            email = user_id['email']
        try:
            user = Profile.objects.get(
                Q(email=email) | Q(fb_id=user_id['id']))
        except:
            user = Profile()
            letters = string.ascii_lowercase
            rand_passwd = ''.join(random.choice(letters) for i in range(8))
            user.password = make_password(rand_passwd)
            user.name = user_id['name']
            user.email = email
            user.fb_id = user_id['id']
            user.save()
            if getattr(user_id, 'email', None):
                msg_html = render_to_string(
                    'mail/new_user.html', {'email': user.email, 'password': rand_passwd})
                send_mail(
                    'Добро пожаловать в iStore',
                    '',
                    send_message_from_mail,
                    [send_message_to_mail],
                    fail_silently=True,
                    html_message=msg_html
                )
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('profile')
    except:
        return HttpResponseRedirect('login')


@csrf_exempt
def login_apple_resp(request):
    # f = open(str(BASE_DIR) + '/accounts/client_secret.txt', "a")
    user_req = {
        "email":"",
        "name": {
            "first_name":"",
            "last_name": "",
        }
    }
    if 'user' in request.POST:
        user_req = json.loads(request.POST.get('user'))
    if 'name' not in user_req and 'first_name' not in user_req['name']:
        user_req['name'] = {
            "first_name": "",
            "last_name": "",
        }
    id_token = request.POST.get('id_token')
    if  user_req['email'] == "":
        decode = jwt.decode(id_token, options={"verify_signature": False})
        user_req['email'] = decode['email']
    try:
        user = Profile.objects.get(email=user_req['email'])
    except:
        user = Profile()
        letters = string.ascii_lowercase
        rand_passwd = ''.join(random.choice(letters) for i in range(8))
        user.password = make_password(rand_passwd)
        user.name = user_req['name']['first_name'] + \
            user_req['name']['last_name']
        user.email = user_req['email']
        user.save()
        if user.email:
            msg_html = render_to_string(
                'mail/new_user.html', {'email': user.email, 'password': rand_passwd})
            send_mail(
                'Добро пожаловать в iStore',
                '',
                send_message_from_mail,
                [send_message_to_mail],
                fail_silently=True,
                html_message=msg_html
            )
    if user:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('profile')
    return HttpResponseRedirect('login')

def logout_user(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        name = request.POST['name']
        password = request.POST['password']
        phone = request.POST['phone']
        code = request.POST['code']
        if phone:
            phone = phone.replace('+', '')
        if form.is_valid() and verify_code(phone, code):
            Code.objects.filter(phone=phone).delete()
            user = create_user(name, phone, str(password))
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session['new_user_password'] = password
            return HttpResponseRedirect('edit')
    else:
        form = VerifyForm()
    
    return render(request, 'auth/register.html', {'form': form})

def forget_modal(request):
    phone_or_email = request.POST['phone']
    password = request.POST['password']
    code = request.POST['code']
    if verify_code(phone_or_email, code):
        Code.objects.filter(phone=phone_or_email, code=code).delete()
        user = get_user(phone_or_email)
        if user:
            user.set_password(password)
            user.save()
            login(request, user)
    return HttpResponseRedirect('/checkout')

def forget(request):
    if request.method == 'POST':
        form = ForgetForm(request.POST)
        phone_or_email = request.POST['phone']
        code = request.POST['code']
        if form.is_valid() and verify_code(phone_or_email, code):
            Code.objects.filter(phone=phone_or_email, code=code).delete()
            user = Profile.objects.get(
                Q(email=phone_or_email) | Q(phone=phone_or_email))
            login(request, user)
            return HttpResponseRedirect('profile')

    else:
        form = ForgetForm()
    return render(request, 'auth/forget.html', {'form': form})


def edit(request):
    user = request.user
    print(datetime.datetime.now(), "bogatyi", user.gender or "Мужской")
    form = EditForm(
        initial={'name': user.name, 'phone': user.phone, 'address': user.address, 'email': user.email, 'birth_date': user.birth_date or datetime.datetime.now(),
                    'gender': user.gender or "Мужской"}, use_required_attribute=False)
    return render(request, 'auth/edit.html', {'form': form})

def edit_profile(request):
    form = EditForm(request.POST, use_required_attribute=False)
    if form.is_valid():
        user = form.save(request)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('accounts:profile')
    return redirect('accounts:edit')


@login_required(login_url='/accounts/login/')
def profile(request):
    from django.urls import get_resolver
    reserved = []
    ordered = []
    new_password = None
    if request.user.is_authenticated:
        user = request.user
        for order in Order.objects.filter(user_id=user.id, formalized=True):
            for product in order.ordered_products.all():
                ordered.append({'id': product.id, 'image': product.get_product_image(), 'name': product.product.product_title,
                            'created_at': order.created_at})
    
        reserved = Reserve.objects.filter(user_id=user.id, payment__isnull=False)
    if 'new_user_password' in request.session:
        new_password = request.session['new_user_password']
        del request.session['new_user_password']

    return render(request, 'auth/profile.html',
                  {'ordered': ordered, 'reserved': reserved, 'new_password': new_password})


def set_code(request):
    phone_or_email = request.POST['phone']
    forget = request.POST['forget']
    num = random.randint(1000, 10000)
    if Profile.objects.filter(Q(email=phone_or_email) | Q(phone=phone_or_email)).count() and forget == '0':
        json = {
            'status': 'phone_exist',
        }
    elif not Profile.objects.filter(Q(email=phone_or_email) | Q(phone=phone_or_email)).count() and forget == '1':
        json = {
            'status': 'phone_not_exist',
        }
    else:
        just_created = 0
        now = datetime.datetime.now().replace(tzinfo=None)
        if Code.objects.filter(phone=phone_or_email).count():
            code = Code.objects.get(phone=phone_or_email)
        else:
            code = Code(phone=phone_or_email, code=num)
            code.save()
            just_created = 1
        created_at = (code.created_at + timedelta(minutes=1)).replace(tzinfo=None)
        minutes_diff = (created_at - now).total_seconds()
        minutes_diff = max(0, int(minutes_diff))
        if not minutes_diff or just_created:
            code.code = num
            code.created_at = now
            code.save()
            settings = Settings.objects.latest('pub_date')
            if "@" in phone_or_email:
                msg_html = render_to_string(
                    'mail/reset_password.html', { 'code': code.code})
                send_mail('Восстановление пароля в istore.kg', '',
                    send_message_from_mail,
                    [phone_or_email],
                    fail_silently=True,
                    html_message=msg_html
                )
            elif settings:
                URL = settings.sms_url
                login = settings.sms_login
                pwd = settings.sms_pwd
                id = random.randint(10000, 10000000)
                sender = settings.sms_sender_id
                XML = """<?xml version='1.0' encoding='UTF-8'?>
                  <message>
                  <login>{}</login>
                  <pwd>{}</pwd>
                  <id>{}</id>
                  <sender>{}</sender>
                  <text>Ваш код:{}</text>
                  <phones>
                  <phone>{}</phone>
                  </phones>
                  </message> """.format(login, pwd, id, sender, code.code, phone_or_email)
                r = requests.post(URL, data=XML.encode('utf-8'))
        json = {
            'status': 'success',
            'minutes': minutes_diff
        }

    return JsonResponse(json)


def check_code(request):
    phone = request.POST['phone']
    num = request.POST['code']
    json = {
        'status': 'success',
    }
    print(phone, num)
    if not Code.objects.filter(phone=phone, code=num).count():
        json['status'] = 'fail'

    return JsonResponse(json)


def get_code_time(request):
    phone = request.POST['phone']
    now = datetime.datetime.now().replace(tzinfo=None)
    minutes_diff = 0
    if Code.objects.filter(phone=phone).count():
        code = Code.objects.get(phone=phone)
        created_at = (code.created_at + timedelta(minutes=1)).replace(tzinfo=None)
        minutes_diff = (created_at - now).total_seconds()
        minutes_diff = max(0, int(minutes_diff))

    json = {
        'status': 'success',
        'minutes': minutes_diff
    }

    return JsonResponse(json)


def save_avatar(request):
    new_ava = Profile.objects.get(pk=request.user.pk)
    new_ava.avatar.delete()
    new_ava.avatar = request.FILES['avatar']
    new_ava.save()
    return HttpResponseRedirect('profile')


def remove_avatar(request):
    new_ava = Profile.objects.get(pk=request.user.pk)
    new_ava.avatar.delete()
    return HttpResponseRedirect('profile')
