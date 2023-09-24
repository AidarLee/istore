import os
from datetime import timedelta
from django.utils import timezone

from wsgiref.util import FileWrapper

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from django.core import serializers
from bs4 import BeautifulSoup

from api.views import KICB, Paybox
from products.models import Product, Basket, Order, Promocode, Color, OrderProduct, Module, ProductSpecification
from accounts.models import Profile
from .models import Article, Compare, Contacts, Service, ServiceCallBack, CallBack, Document, MainPage, Bank, PurchaseOnCredit, \
    PurchaseOnCreditProducts, Reserve, Settings, Transaction, AboutUs, MainPageSlider, Currency, LoanPage, Warranty, \
    WhyUs, TradeIn
from .forms import PurchaseForm
import uuid
import random
import requests
import string
import json
from maintenance_mode.decorators import force_maintenance_mode_off, force_maintenance_mode_on
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import urllib.parse
import mimetypes
from django.core.mail import send_mail
from django.db.models import F

categories = {'iphone': 'iPhone ', 'macBook': 'MacBook', 'iPad': 'iPad', 'iMac': 'iMac',
              'apple-watch': 'Apple Watch', 'gadgets': 'Гаджеты', 'accessory': 'Акссесуары', 'tradeIn': 'Trade In'}

send_message_to_mail = "info@istore.kg"
# send_message_to_mail = "kaarov8@gmail.com"
send_message_from_mail = "testingfor9999@gmail.com"
def main(request):
    articles = Article.objects.filter(active=True)
    products = Product.objects.filter(in_trade=False, active=True).order_by(
        F('order').desc(nulls_last=True))
    main_page = MainPage.objects.latest(F('order').desc(nulls_last=True))
    main_page_slider = MainPageSlider.objects.filter(
        category=1).order_by(F('order').desc(nulls_last=True))
    sales_slider = MainPageSlider.objects.filter(
        category=2).order_by(F('order').desc(nulls_last=True))

    return render(request, 'index.html', {'articles': articles, 'products': products, 'main_page': main_page
                                          , 'main_page_slider': main_page_slider, 'sales_slider': sales_slider})


def about_us(request):
    about = AboutUs.objects.first()

    return render(request, 'about_us.html', {'about': about})


def warranty(request):
    warranty = Warranty.objects.first()

    return render(request, 'warranty.html', {'warranty': warranty})


def whyUs(request):
    whyus = WhyUs.objects.first()

    return render(request, 'whyus.html', {'whyus': whyus})


def contacts(request):
    contacts = Contacts.objects.first()
    return render(request, 'contacts.html', {'contacts': contacts})


def service(request, category='iphone'):
    services = Service.objects.filter(category=category).order_by(
        F('order').desc(nulls_last=True))
    return render(request, 'service.html',
                  {'services': services, 'category': category, 'category_name': categories[category]})


def articles(request):
    articles = Article.objects.filter(active=True).order_by(
        F('order').desc(nulls_last=True))
    return render(request, 'articles.html', {'articles': articles})


def article(request, id):
    article = get_object_or_404(Article, pk=id)

    return render(request, 'article.html', {'article': article})


def basket(request):
    return render(request, 'basket.html')


def loan(request):
    banks = Bank.objects.all()
    text_arr = LoanPage.objects.first()
    bank = banks.filter(online=True).latest('order')
    products = []
    ids = request.GET.get('id', '').split(',')
    specs = request.GET.get('spec', '').split(',')
    if ids[0] != "":
        for i in range(len(ids)):
            product = get_object_or_404(Product, pk=ids[i])
            specific = product.specification.get(pk=specs[i])
            products.append({'product': product, 'specific': specific})
            
    elif 'loan_products' in request.session:
        loan_products = request.session['loan_products']
        for loan in loan_products:
            product = get_object_or_404(Product, pk=loan['id'])
            specific = product.specification.get(pk=loan['spec'])
            products.append(
                {'product': product, 'specific': specific})
    return render(request, 'loan.html', {'banks': banks, 'bank': bank, 'text_arr': text_arr, 'products': products})


def create_loan(request):
    if request.POST:
        id = request.POST['product_id']
        spec = request.POST['product_spec']
        request.session['loan_products'] = [{'id': id, 'spec': spec}]
        json = {'status': 'success'}

        return JsonResponse(json)
    else:
        banks = Bank.objects.all()
        if 'loan_products' in request.session:
            loan = request.session['loan_products']
            product = get_object_or_404(Product, pk=loan['id'])
            spec = loan['spec']
            specific = product.specification.get(pk=spec)

            return render(request, 'create_loan.html', {'banks': banks, 'product': product, 'specific': specific})
        else:
            return HttpResponseRedirect('profile')


def purchase_on_credit(request):
    if request.POST:
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            bank = request.session['bank']
            all_sum = request.session['all_sum']
            period = request.session['period']
            per_month = request.session['per_month']
            initial_fee = request.session['initial_fee']
            obj = form.save()
            obj.bank = bank
            obj.whole_price = all_sum
            obj.per_month = per_month
            obj.month = period
            obj.initial_fee = initial_fee
            obj.save()

            if 'final_products' in request.session:
                for product in request.session['final_products']:
                    name = ''
                    spec = PurchaseOnCreditProducts(credit=obj, credit_product_id=product['id'], specification_id=product['spec'],
                                                    price=product['price'], price_converted=product['converted'],
                                                    )
                    spec.save(force_insert=True)
            products_in_credit = []
            for spec in request.session['final_products']:
                prod = ProductSpecification.objects.get(id=spec['spec'])
                products_in_credit.append(prod)
            
            msg_html = render_to_string(
                'mail/credit_mail.html', {'name': obj.name, 'phone': obj.phone, 'bank': bank, 'all_sum': all_sum, 'per_month': per_month, 'period': period, 'initial_fee': initial_fee, 'products': products_in_credit})
            send_mail(
                'Заявка на кредит с istore.kg',
                '',
                send_message_from_mail,
                [send_message_to_mail],
                fail_silently=True,
                html_message=msg_html
            )
            return HttpResponseRedirect('success')
    else:
        form = PurchaseForm()
    if 'loan_products' in request.session:
        bank = get_object_or_404(Bank, pk=request.session['bank'])
        period = int(request.session['period'])
        loan = request.session['loan_products']
        initial_fee = float(request.session['initial_fee'])
        all_sum = 0
        per_month = 0
        products = []

        for product_in in loan:
            product = get_object_or_404(Product, pk=product_in['id'])
            specific = product.specification.get(pk=product_in['spec'])
            name = str(product.product_title) + ',' + specific.get_color_name()

            converted = specific.convert_product_price()
            all_sum += converted
            products.append(
                {'id': product.id, 'spec': product_in['spec'], 'name': name, 'price': specific.price,
                 'converted': converted})
        
        all_sum, per_month = bank.get_all_sum_and_per_month(all_sum, period, initial_fee)

        request.session['final_products'] = products
        request.session['all_sum'] = all_sum
        request.session['per_month'] = per_month
        request.session['bank'] = bank.title
        request.session['period'] = period

        return render(request, 'purchase_on_credit.html',
                      {'bank': bank, 'period': period, 'products': products, 'form': form, 'all_sum': all_sum,
                       'per_month': per_month})
    else:
        return HttpResponseRedirect('index')


def add_on_credit(request):
    import json
    if request.POST:
        products = request.POST['products']
        bank = request.POST['bank']
        period = request.POST['period']
        initial_fee = request.POST['initial_fee']
        final = []
        for product in json.loads(products):
            final.append({'id': product['id'], 'spec': product['spec']})
        request.session['loan_products'] = final
        request.session['bank'] = bank
        request.session['period'] = period
        request.session['initial_fee'] = initial_fee
        return HttpResponseRedirect('purchase_on_credit')


def to_basket(request):
    if 'user_token' in request.session:
        token = request.session['user_token']
    else:
        token = uuid.uuid1(random.randint(0, 281474976710655))
        request.session['user_token'] = token.__str__()

    if request.POST:
        id = request.POST['product_id']
        spec = None

        if request.POST['specification'] != 'undefined':
            spec = request.POST['specification']
        
        spec = ProductSpecification.objects.get(pk=spec)

        basket = Basket.objects.create(user_token=token, product_id=id, quantity=1, color=spec.color_hex.name, capacity=spec.capacity, 
                                       keyboard=spec.keyboard, caseSize=spec.caseSize, connectivity=spec.connectivity, ram=spec.ram, cpu=spec.cpu, edition=spec.edition, pattern=spec.pattern, specification=spec)
        product = Product.objects.get(id=id)
        price = product.min_price()
        converted = product.calc_som_currency_min()

        json_resp = {'status': 'success',
                'product': {'unique': basket.id, 'id': product.id, 'product_title': product.product_title,
                            'image': basket.get_product_image(), 'price': price, 'converted': converted,
                            'comment': ''}}

        return JsonResponse(json_resp)


def get_service_by_category(request):
    if request.POST:
        category = request.POST['category']
        services = Service.objects.filter(category=category)
        final = []
        for service in services:
            final.append({'id': service.id, 'name': service.name})
        json = {'status': 'success', 'category': categories[category], 'services': final}

        return JsonResponse(json)


def service_call_back(request):
    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        another = request.POST['another']
        reason = request.POST['reason']
        product = request.POST['product']
        category = request.POST['category']
        msg_html = render_to_string(
            'mail/service_call_back.html', {'name': name, 'phone': phone, 'reason': reason, 'another': another, 'product': product, 'category': category})
        send_mail(
            'Заявка на ремонт с istore.kg',
            '',
            send_message_from_mail,
            [send_message_to_mail],
            fail_silently=True,
            html_message=msg_html
        )
        ServiceCallBack.objects.create(name=name, phone=phone, another=another, reason=reason, product=product,
                                       category=category)

        json = {'status': 'success'}

        return JsonResponse(json)


def call_back(request):
    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        topic = request.POST['topic']
        desc = request.POST['desc']
        msg_html = render_to_string(
            'mail/call_back.html', {'name': name, 'phone': phone, 'topic': topic, 'desc': desc})
        send_mail(
            'Заявка на обратный звонок с istore.kg',
            '',
            send_message_from_mail,
            [send_message_to_mail],
            fail_silently=True,
            html_message=msg_html
        )
        CallBack.objects.create(name=name, phone=phone, topic=topic, desc=desc)

        json = {'status': 'success'}

        return JsonResponse(json)


def change_in_basket(request):
    id = request.POST['basket_id']
    quantity = request.POST['quantity']
    comment = request.POST['comment']

    if request.POST:
        product_in_basket = Basket.objects.get(id=id)
        product_in_basket.quantity = quantity
        product_in_basket.comment = comment
        product_in_basket.save()
        json = {'status': 'success'}

        return JsonResponse(json)


def remove_from_basket(request):
    if request.POST:
        id = request.POST['basket_id']
        Basket.objects.filter(id=id).delete()
        json = {'status': 'success'}
        return JsonResponse(json)


def checkout(request):
    token = ""
    if "user_token" in request.session:
        token = request.session['user_token']
    product_in_basket = Basket.objects.filter(user_token=token)
    final_price = 0
    final_converted_price = 0

    for product in product_in_basket:
        final_price += product.get_product_price() * product.quantity
        final_converted_price += product.get_product_converted_price() * product.quantity

    return render(request, 'checkout.html',
                  {'final_price': final_price, 'final_converted_price': final_converted_price})


def compare(request):
    category = ''
    product_first = 0
    product_second = 0
    product_third = 0

    if 'category' in request.GET:
        category = request.GET['category']

    if 'product_first' in request.GET and request.GET['product_first'] != "null":
        product_first = request.GET['product_first']

    if 'product_second' in request.GET and request.GET['product_second'] != "null":
        product_second = request.GET['product_second']

    if 'product_third' in request.GET and request.GET['product_second'] != "null":
        product_third = request.GET['product_third']
    compare = Compare.objects.order_by(F('order').desc(nulls_last=True))
    
    selected_compare = Compare.objects.filter(title=category).first()
    
    if(not selected_compare):
        selected_compare = compare[0]
    products = selected_compare.compare_product.all().order_by(
        F('order').desc(nulls_last=True))
    
    if product_first == 0:
        product_first = products[0].product.id

    if product_second == 0:
        if len(products) > 1:
            product_second = products[1].product.id
        else:
            product_second = products[0].product.id

    if product_third == 0:
        if len(products) > 2:
            product_third = products[2].product.id
        else:
            product_third = products[0].product.id

    return render(request, 'compare.html',
                  {'products': products, 'product_first': product_first, 'product_second': product_second,
                   'product_third': product_third, 'compare': compare, 'category': category})


def create_user(phone, name, second_name, email):
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(10))
    user = Profile()
    user.name = str(second_name)+' '+str(name)
    user.email = email
    user.password = make_password(password)
    user.phone = phone
    user.save()
    return user


def make_order(request):
    delivery = request.POST['delivery']
    address = request.POST['address']
    country = request.POST['country']
    payment = request.POST['payment']
    promo = request.POST['promo']
    comment = request.POST['comment']
    auth = request.POST['auth']
    json_resp = {'status': 'success'}

    if not request.user.is_authenticated:
        if auth == 'true':
            name = request.POST['name']
            second_name = request.POST['second_name']
            email = request.POST['email']
            phone = request.POST['phone']
            user = Profile.objects.filter(phone=phone).count()
            if user:
                json_resp['status'] = 'phone_exist'
                return JsonResponse(json_resp)
            user = create_user(phone, name, second_name, email)
            login(request, user)

        else:
            auth_phone = request.POST['auth_phone']
            password = request.POST['password']
            user = Profile.objects.get(phone=auth_phone)
            if not user:
                json_resp['status'] = 'user_not_found'
                return JsonResponse(json_resp)

            if check_password(password, user.password):
                login(request, user)
            else:
                json_resp['status'] = 'password_not_match'
                return JsonResponse(json_resp)
    elif not request.user.phone:
        phone = request.POST['phone']
        user_exist = Profile.objects.filter(phone=phone).count()
        if user_exist:
            json_resp['status'] = 'phone_exist'
            return JsonResponse(json_resp)
        
        user = Profile.objects.get(id=request.user.id)
        user.phone = phone
        user.save()
    else:
        user = request.user
    token = request.session['user_token']

    product_in_basket = Basket.objects.filter(user_token=token)
    promo_name = ''
    promo_percent = 0
    promocode = Promocode.objects.filter(code_word=promo)
    if promocode:
        promo_name = promocode[0].name
        promo_percent = promocode[0].percent
    order = Order(user=user, promo_name=promo_name, promo=promo_percent, delivery=delivery, address=address,
                  country=country, payment_option=payment, comment=comment)
    order.save()
    total_price = 0
    for product in product_in_basket:
        order_product = OrderProduct(order=order, product=product.product, color=product.color,
                                     quantity=product.quantity,
                                     capacity=product.capacity, price=product.get_product_price(),
                                     converted=product.get_product_converted_price(), comment=product.comment,
                                     keyboard=product.keyboard, caseSize=product.caseSize, connectivity=product.connectivity, ram=product.ram, cpu=product.cpu, edition=product.edition, pattern=product.pattern, specification=product.specification)
        order_product.save(force_insert=True)
        total_price += product.get_product_converted_price()
        product.delete()

    if country == 'Казахстан':
        total_price += 1000

    order.need_pay = total_price
    order.save()
    if payment == "paybox":
        trn = Transaction(option='paybox', order=order, to='order')
        trn.save()
        paybox = Paybox()
        resp = paybox.create_purchase_link(order, trn)
        if(resp != None):
            json_resp = {'status': 'success', 'url': resp}
        else:
            json_resp = {'status': 'failure', 'url': '/catalog'}
    else:
        request.session['notify'] = 'success'
        json_resp = {'status': 'success', 'url': '/accounts/profile'}
    msg_html = render_to_string('mail/order_mail.html', {
        'name': order.user.name, 'phone': order.user.phone, 'products': order.ordered_products.all(),  'country': order.country, 
        'address': order.address, 'delivery': order.delivery, 'payment_option': order.payment_option, 'promo_name': order.promo_name, 
        'promo': order.promo, 'payment': order.payment, 'comment': order.comment, 'created': order.created_at})
    print(order.ordered_products.all())
    send_mail(
        'Заказ с istore.kg',
        '',
        send_message_from_mail,
        [send_message_to_mail],
        fail_silently=True,
        html_message=msg_html
    )
    return JsonResponse(json_resp, safe=False)


def remove_reserve(request, id):
    Reserve.objects.filter(id=id).delete()
    return redirect('/accounts/profile')


def compare_category_select(request):
    category = request.POST['category']
    compare = Compare.objects.filter(title=category).order_by(
        F('order').desc(nulls_last=True)).first()
    compare_products = compare.compare_product.all().order_by(
        F('order').desc(nulls_last=True))
    final = []
    for compare_product in compare_products:
        final.append({'id': compare_product.product.id,
                     'name': compare_product.product.product_title})
    json = {'status': 'success', 'products': final}

    return JsonResponse(json)


def main_search(request):
    search = request.POST['search']
    final = []
    final_article = []

    if search:
        search = urllib.parse.unquote(search)
        
        products = Product.objects.filter(Q(product_title__icontains=search) | Q(product_description__icontains=search), active=True)
        for product in products:
            final.append({'id': product.id, 'name': product.product_title, 'desc': product.product_description,
                          'image': product.get_image()})
        articles = Article.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        for article in articles:
            final_article.append({'id': article.id, 'title': article.title, 'desc': article.secondary_title})
    json = {'status': 'success', 'products': final, 'articles': final_article}

    return JsonResponse(json)


def promo_search(request):
    search = request.POST['codeword']
    json = {'status': 'fail'}
    if search:
        promo = Promocode.objects.filter(code_word=search)
        if promo:
            promo = promo[0]
            json['status'] = 'success'
            json['promo'] = promo.name
            json['percent'] = promo.percent

    return JsonResponse(json)


def search(request):
    return render(request, 'search.html')


def search_with_value(request, search):
    search = search.replace('%20', ' ')
    search = urllib.parse.unquote(search)
    products = products = Product.objects.filter(Q(product_title__icontains=search) | Q(
        product_description__icontains=search), active=True)
    articles = Article.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
    count = products.count() + articles.count()
    return render(request, 'search.html',
                  {'products': products, 'articles': articles, 'search': search, 'count': count})


def not_found(request, exception=None):
    return render(request, 'exceptions/404.html')


def maintenance_mode(request, exception=None):
    return render(request, 'exceptions/503.html')


def save_image(request):
    newdoc = Document(docfile=request.FILES['file'])
    newdoc.save()
    json = {'location': '/media/' + newdoc.__str__()}

    return JsonResponse(json)


def add_new_product(request):
    if request.POST:
        final = []
        search = request.POST['search']
        products = Product.objects.filter(Q(product_title__icontains=search) | Q(
            product_description__icontains=search), active=True)

        if len(products) > 3:
            products = products[:3]

        for product in products:
            for specific in product.specification.filter(~Q(quantity=0)).all():
                name = str(product.product_title) + ',' + str(specific.get_color_name())
                final.append(
                    {'id': product.id, 'spec': specific.id,
                        'price': specific.price, 'price_converted': specific.convert_product_price(),
                        'name': name})

        json_resp = {'status': 'success', 'products': final}
        return JsonResponse(json_resp)


def get_bank_data(request):
    final = {}
    if request.POST:
        id = request.POST['id']
        bank = get_object_or_404(Bank, pk=id)
        final = {
            'title': bank.title,
            'desc': bank.desc,
            'desc_for_office': bank.desc_for_office,
            'logo': bank.img.url,
            'start': bank.start_period,
            'end': bank.end_period,
            'price': bank.start_price,
            'end_price': bank.end_price,
            'guarantor': bank.guarantor,
            'initial_fee': bank.initial_fee,
            'initial_fee_before': bank.initial_fee_before,
            'percent': bank.get_percent(),
            'percents': bank.get_percents(),
            'repayment': bank.repayment,
            'term': bank.term_of_consider
        }
    json = {'status': 'success', 'bank': final}
    return JsonResponse(json)


def success(request):
    return render(request, 'success.html')


@force_maintenance_mode_off
@csrf_exempt
def check_payment(request):
    json_data = json.loads(request.body)
    json_resp = {"Response": {"ErrorCode": "0", "ErrorMsg": "Failure"}}
    if json_data['PartnerPaymentResult']['PaymentStatus'] == 'A':
        trn = Transaction.objects.filter(transaction_id=json_data['PartnerPaymentResult']['PartnerTrnID'])
        if trn:
            if len(trn) > 0:
                trn = trn[0]
            if trn.to == 'reserve':
                reserve = trn.reserve
                if reserve:
                    reserve.payment = reserve.reserve_price
                    reserve.save()
            else:
                order = trn.order
                if order:
                    order.payment = order.need_pay
                    order.save()
            trn.delete()
            json_resp['Response']['ErrorMsg'] = 'Success'
            json_resp['Response']['ErrorCode'] = "0"
        else:
            json_resp['Response']['ErrorMsg'] = 'Not_found'
            json_resp['Response']['ErrorCode'] = "0"

    return JsonResponse(json_resp)


@force_maintenance_mode_off
def partner_get_payment_status(request):
    transactions = Transaction.objects.all()
    json_resp = {"Response": {"ErrorCode": "0", "ErrorMsg": "Not_found"}}
    kicb = KICB()
    for trn in transactions:
        if trn.option == 'kicb':
            data = {
                'command': 'c',
                'client_ip_addr': trn.ip,
                'trans_id': trn.transaction_id
            }
            kicb.check_payment(data, trn.transaction_id, trn.ip)
        else:
            input = {
                "PartnerGetPaymentStatus": {
                    "CultureInfo": 'ru-RU',
                    "MSISDN": '0902000037',
                    "PartnerTrnID": trn.transaction_id,
                    "Password": '2ac9cb7dc02b3c0083eb70898e549b63',
                }
            }

            elsom = ElsomController()
            elsom = elsom.checkPaymentStatus(input)


            if elsom["Response"]["Result"]:
                json_resp = {"Response": {"ErrorCode": "0", "ErrorMsg": "Success"}}
                if elsom["Response"]["Result"]["PaymentStatus"] == 'A':
                    if trn.to == 'reserve':
                        reserve = trn.reserve
                        if reserve:
                            reserve.payment = reserve.reserve_price
                            reserve.save()
                            msg_html = render_to_string(
                                'mail/reserve_mail.html', {'name': reserve.name, 'phone': reserve.phone, 'product': reserve.product, 'color': reserve.color, 'capacity': reserve.capacity, 'module': reserve.module})
                            send_mail(
                                'Бронь с istore.kg',
                                '',
                                send_message_from_mail,
                                [send_message_to_mail],
                                fail_silently=True,
                                html_message=msg_html
                            )
                    else:
                        order = trn.order
                        if order:
                            order.payment = order.need_pay
                            order.save()
                            if order.user:
                                msg_html = render_to_string('mail/order_mail.html', {'name': order.user.name, 'phone': order.user.phone, 'products': order.ordered_products.all(), 
                                                            'country': order.country, 'address': order.address, 'delivery': order.delivery, 'payment_option': order.payment_option,
                                                                                     'promo_name': order.promo_name, 'promo': order.promo, 'payment': order.payment, 'created': order.created_at, 'comment': order.comment, })
                                send_mail(
                                    'Заказ с istore.kg',
                                    '',
                                    send_message_from_mail,
                                    [send_message_to_mail],
                                    fail_silently=True,
                                    html_message=msg_html
                                )
                    trn.delete()
                elif elsom["Response"]["Result"]["PaymentStatus"] != '1':
                    if trn.to == 'reserve':
                        reserve = trn.reserve
                        if reserve:
                            reserve.payment = reserve.reserve_price
                            reserve.delete()
                    else:
                        order = trn.order
                        if order:
                            order.payment = order.need_pay
                            order.delete()
                    trn.delete()

    return JsonResponse(json_resp)

def get_attr(obj, name):
    el = ""
    if(obj):
        obj = obj.__dict__
        el = obj[name]
    return el

def make_reserve(request):
    settings = Settings.objects.latest('pub_date')

    id = request.POST['product_id']
    spec = request.POST['specification']
    name = request.POST['client_name']
    phone = request.POST['client_phone']
    product = get_object_or_404(Product, pk=id)

    spec = ProductSpecification.objects.get(pk=spec)
    capacity = getattr(spec, "capacity")
    if(capacity):
        capacity = capacity.get_name()
    user = None
    if request.user.is_authenticated:
        user = request.user
    reserve = Reserve(user=user, product=product, name=name, phone=phone, color=get_attr(spec.color_hex, "name"), capacity=capacity, keyboard=get_attr(getattr(spec, "keyboard"), "name"), caseSize=get_attr(getattr(spec, "caseSize"), "name"), connectivity=get_attr(getattr(spec, "connectivity"), "name"), ram=get_attr(getattr(spec, "ram"), "name"), cpu=get_attr(getattr(spec, "cpu"), "name"), edition=get_attr(getattr(spec, "edition"), "name"), pattern=get_attr(getattr(spec, "pattern"), "name"), specification=spec,
                      reserve_price=settings.reserve_price)
    reserve.save()
    reserve.price = reserve.get_product_price()
    reserve.price_converted = reserve.get_product_converted_price()
    reserve.save()
    trn = Transaction(option="paybox", reserve=reserve,
                      to='reserve', payment=settings.reserve_price)
    trn.save()
    paybox = Paybox()
    resp = paybox.create_reserve_link(reserve, trn, settings.reserve_price)
    if(resp):
        return HttpResponseRedirect(resp)

    return redirect('/failurePayment')
    


def agreement(request):
    file = '/static/docs/terms_of_use_istore_kg.pdf'
    return HttpResponseRedirect(file)


def privacy(request):
    file = '/static/docs/privacy_policy.pdf'
    return HttpResponseRedirect(file)


class ElsomController():
    api_url = 'https://mbgwt.elsom.kg:10680/JsonWebServer'
    api_url_check = 'https://mbgwt.elsom.kg:10690/MerchantAPI'

    output_result = list()

    def iaUnit(self, ParentInput):
        data = {
            'IA_Init': {
                'MSISDN': ParentInput['MSISDN'],
                'PmSISDN': ParentInput['PmSISDN'],
                'PartnerCode': ParentInput['PartnerCode'],
                'Amount': ParentInput['Amount'],
                'PartnerTrnID': ParentInput['PartnerTrnID'],
                'ChequeNo': ParentInput['ChequeNo'],
                'CashierNo': ParentInput['CashierNo'],
                'CultureInfo': ParentInput['CultureInfo'],
                'Password': ParentInput['Password'],
                'UDF': ParentInput['UDF'],
            }
        }
        get_data = self.callAPI('POST', self.api_url, json.dumps(data))
        return get_data

    def checkPaymentStatus(self, data):
        get_data = self.callAPI('POST', self.api_url_check, json.dumps(data))
        return get_data

    def callAPI(self, method, url, data):
        r = requests.post(url, data=data)
        return r.json()

    def get(self, second):
        return self

@csrf_exempt
def success_payment(request):
    return render(request, 'kicb_success.html')
    # kicb = KICB()
    # ip = kicb.get_client_ip()
    # if request.POST:
    #     transaction = Transaction.objects.get(transaction_id=request.POST['trans_id'])
    #     if transaction:
    #         status = kicb.check_payment(transaction.transaction_id, ip, 'success')
    #         # json_resp = {'status': status}
    #         # return JsonResponse(json_resp, safe=False)
    #         if status == 'success':
    #             return render(request, 'kicb_success.html')
    #         elif status == 'fail':
    #             return failure_payment(request)
@csrf_exempt
def failure_payment(request):
    return render(request, 'kicb_failure.html')
    # kicb = KICB()
    # ip = kicb.get_client_ip()
    # if request.POST:
    #     transaction = Transaction.objects.get(transaction_id=request.POST['trans_id'])
    #     if transaction:
    #         status = kicb.check_payment(transaction.transaction_id, ip, 'fail')
    #         if status == 'success':
    #             return success_payment(request)
    #         elif status == 'fail':
    #             return render(request, 'kicb_failure.html')

    # return HttpResponseRedirect('/')


def parse_currency(request):
    curr = Currency.objects.first()
    now = curr.updated_at
    interval = curr.time
    last_time = (now + timedelta(minutes=interval.minute, hours=interval.hour)).replace(tzinfo=None)
    json = {'status': 'success'}

    if last_time <= timezone.now():
        url = "https://en.kicb.net/welcome/"
        session = requests.Session()
        page = session.get(url, verify=True)
        soup = BeautifulSoup(page.text, 'html.parser')
        currency = soup.find('div', {'id': 'curency'}).find('div', {'class': 'con'}).find_all('div',
                                                                                              {'class': 'cur_line'})

        if len(currency) > 1:
            currency = currency[1].find('div', {'class': 'data3'})
            curr.exchange_rate = currency.text
            curr.updated_at = timezone.now()
            curr.save()
        return JsonResponse(json)
    else:
        json['status'] = 'false'
        return JsonResponse(json)

    return None


def tradeIn(request, id):
    tradeIn = TradeIn.objects.filter(category=id).latest('order')
    return render(request, 'tradeIn.html', {'tradeIn': tradeIn})
