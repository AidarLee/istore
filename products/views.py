from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Recommended, ProductSpecification
from webapp.models import Currency, AdditionalCategory
from django.forms.models import model_to_dict
from django.db.models import F
import requests
import os
import json

categories = {'iphone': 'iPhone ', 'macBook': 'MacBook', 'iPad': 'iPad', 'iMac': 'iMac',
              'apple-watch': 'Apple Watch', 'gadgets': 'Гаджеты', 'accessory': 'Аксессуары', 'airpods': 'AirPods',
              'tradeIn': 'Trade In', 'another': 'Разное'}

additional_categories = {'apple-tv': 'Apple TV ', 'cables': 'Кабели', 'adapters': 'Переходники',
                         'protective-glass': 'Защитные стекла', 'stylus': 'Стилусы',
                         'keyboards-and-mouse': 'Клавиатуры и мышки', 'charging-device': 'Зарядные устройства',
                         'headphones-and-speakers': 'Наушники и колонки', 'cases-and-bags': 'Чехлы и сумки',
                         'drones': 'Дроны', 'stabilizers': 'Стабилизаторы', 'camera': 'Камеры', 'garmin': 'Garmin',
                         'vr-glasses': 'VR  очки', 'graphic-tablets': 'Графические планшеты', 'another': 'Разное',
                         'mac-16': 'MacBook Pro 16', 'mac-13': 'MacBook Pro 13', 'mac-13-air': 'MacBook Air 13',
                         'mac-12': 'MacBook Retina 12', 'mac-mini': 'Mac mini', 'mac-pro': 'Mac Pro', 'accessory_1': 'Доп Аксессуары 1',
                         'accessory_2': 'Доп Аксессуары 2', 'accessory_3': 'Доп Аксессуары 3', 'accessory_4': 'Доп Аксессуары 4', 'accessory_5': 'Доп Аксессуары 5',
                         'gadget_1': 'Доп Гаджеты 1', 'gadget_2': 'Доп Гаджеты 2', 'gadget_3': 'Доп Гаджеты 3', 'gadget_4': 'Доп Гаджеты 4', 'gadget_5': 'Доп Гаджеты 5'}

def index(request):
    return render(request, 'catalog.html')


def product(request, slug):
    if slug.isnumeric():
        product = Product.objects.get(id=slug)
    else:
        product = Product.objects.get(slug_name=slug)
    price = 0
    converted = 0
    specification = {}
    recommends = []
    for recommend in Recommended.objects.filter(products_id=product.id):
        recommends.append(recommend.recommended)
    data = {}
    for index, specific in enumerate(product.specification.filter(~Q(price=None))):
        capacity = specific.__str__()
        if not index:
            price = specific.price
            converted = specific.convert_product_price()

        if not capacity in specification:
            specification[capacity] = {}
        data[str(specific.id)] = model_to_dict(specific)
        data[str(specific.id)]['secondary_price'] = specific.convert_product_price()
        data[str(specific.id)]['images'] = list(
            specific.image.values_list('image', flat=True))
        
    return render(request, 'product.html',
                  {'product': product, 'recommends': recommends, 'specification': specification,
                   'price': price, 'converted': converted, 'data': json.dumps(data)})


def get_product(request):
    if request.POST:
        id = request.POST['product']
        product = Product.objects.get(id=id)
        specifics = list()
        images = list()
        final = []
        if product:
            for index, specific in product.get_additional_specific():
                specifics.append({'title': specific.specification, 'desc': specific.description})
            for index, image in product.get_images_to_compare():
                images.append({'color': index, 'image': image})
            final = {'id': product.id, 'image': product.get_images_to_compare()}

        json = {'status': 'success', 'product': final, 'specific': specifics, 'images': images}
        return JsonResponse(json)


def get_product_price(request):
    if request.POST:
        id = request.POST['id']
        color = request.POST['color']
        capacity = request.POST['capacity'].split()
        product = Product.objects.get(id=id)
        if request.POST['capacity'] != "None":
            main_price = product.specification.filter(color_hex__color=color, capacity__capacity=capacity[0],
                                                      capacity__measure=capacity[1])
        else:
            main_price = product.specification.filter(color_hex__color=color)
        if len(main_price) == 0:
            main_price = main_price
        else:
            main_price = main_price[0]

        quantity = main_price.quantity
        currency = Currency.objects.latest('created_at')
        secondary_price = currency.get_converted_price(main_price.price)

        json = {'status': 'success', 'main_price': main_price.price, 'secondary_price': secondary_price,'quantity':quantity}
        return JsonResponse(json)


def products(request, category):
    tradeIn = None
    tradeInLink = "another"
    if category == 'tradeIn':
        products = []
    elif category == 'accessory':
        products = []
    elif category == 'gadgets':
        products = []
    elif category == 'macBook':
        tradeInLink = "macBook"
        categories[category] = 'Mac'
        products = []
        products_in_trade = Product.objects.filter(
            product_category=category, in_trade=True, active=True).values_list('id', flat=True)
        specification = ProductSpecification.objects.filter(
            products_id__in=products_in_trade).order_by('price')
        if specification:
            specification = specification[0]
            tradeIn = Product.objects.filter(id=specification.products_id, active=True)

            if tradeIn:
                tradeIn = tradeIn[0]
    elif category == 'iMac':
        tradeInLink = "macBook"
        products = Product.objects.filter(
            product_category="iMac", in_trade=False, active=True).order_by(F('order').desc(nulls_last=True))
        products_in_trade = Product.objects.filter(
            product_category="macBook", in_trade=True, active=True).values_list('id', flat=True)
        specification = ProductSpecification.objects.filter(
            products_id__in=products_in_trade).order_by('price')
        if specification:
            specification = specification[0]
            tradeIn = Product.objects.filter(
                id=specification.products_id, active=True)

            if tradeIn:
                tradeIn = tradeIn[0]
    else:
        tradeInLink = category
        products = Product.objects.filter(product_category=category, in_trade=False, active=True).order_by(F('order').desc(nulls_last=True))
        products_in_trade = Product.objects.filter(product_category=category, in_trade=True, active=True).values_list('id', flat=True)
        specification = ProductSpecification.objects.filter(products_id__in=products_in_trade).order_by('price')
        if specification:
            specification = specification[0]
            tradeIn = Product.objects.filter(id=specification.products_id, active=True)

            if tradeIn:
                tradeIn = tradeIn[0]
    return render(request, 'products.html',
                  {'products': products, 'category': category, 'category_name': categories[category],
                   'tradeIn': tradeIn, 'tradeInLink': tradeInLink})


def accessory(request, category):
    tradeIn = None
    category = AdditionalCategory.objects.filter(slug_name=category).first()
    products = Product.objects.filter(product_category="accessory", additional_category=category.id,
                                      in_trade=False, active=True).order_by(F('order').desc(nulls_last=True))
    products_in_trade = Product.objects.filter(additional_category=category.id, in_trade=True, active=True).values_list(
        'id',
        flat=True)
    specification = ProductSpecification.objects.filter(products_id__in=products_in_trade).order_by('price')
    if specification:
        specification = specification[0]
        tradeIn = Product.objects.filter(id=specification.products_id, active=True)
        if tradeIn:
            tradeIn = tradeIn[0]
    additional = {
        'name': 'Аксессуары',
        'link': '/catalog/accessory',
    }
    tradeInLink = "another"
    return render(request, 'products.html',
                  {'products': products, 'category': category, 'category_name': category.name,
                   'additional': additional, 'tradeIn': tradeIn, 'tradeInLink': tradeInLink
                   })


def gadgets(request, category):
    tradeIn = None
    category = AdditionalCategory.objects.filter(slug_name=category).first()
    products = Product.objects.filter(
        product_category="gadgets",  additional_category=category.id, in_trade=False, active=True).order_by(F('order').desc(nulls_last=True))
    products_in_trade = Product.objects.filter(additional_category=category.id, in_trade=True, active=True).values_list(
        'id',
        flat=True)
    specification = ProductSpecification.objects.filter(products_id__in=products_in_trade).order_by('price')
    if specification:
        specification = specification[0]
        tradeIn = Product.objects.filter(id=specification.products_id, active=True)
        if tradeIn:
            tradeIn = tradeIn[0]
    additional = {
        'name': 'Гаджеты',
        'link': '/catalog/gadgets',
    }
    return render(request, 'products.html',
                  {'products': products, 'category': category, 'category_name': category.name,
                   'additional': additional, 'tradeIn': tradeIn
                   })


def tradeIn(request, category):
    products = Product.objects.filter(product_category=category, in_trade=True, active=True).order_by(
        F('order').desc(nulls_last=True))

    additional = {
        'name': 'Trade In',
        'link': '/catalog/tradeIn',
    }
    return render(request, 'products.html',
                  {'products': products, 'category': category, 'category_name': categories[category],
                   'additional': additional
                   })


def mac(request, category):
    tradeIn = None
    category = AdditionalCategory.objects.filter(slug_name=category).first()
    products = Product.objects.filter(
        additional_category=category.id, in_trade=False, active=True).order_by(F('order').desc(nulls_last=True))
    products_in_trade = Product.objects.filter(additional_category=category.id, in_trade=True, active=True).values_list('id',
                                                                                                                  flat=True)
    specification = ProductSpecification.objects.filter(products_id__in=products_in_trade).order_by('price')
    if specification:
        specification = specification[0]
        tradeIn = Product.objects.filter(id=specification.products_id, active=True)
        if tradeIn:
            tradeIn = tradeIn[0]
    additional = {
        'name': 'Mac',
        'link': '/catalog/macBook',
    }
    return render(request, 'products.html',
                  {'products': products, 'category': category, 'category_name': category.name,
                   'additional': additional, 'tradeIn': tradeIn
                   })


def sort_from_catalog(request):
    if request.POST:
        category = request.POST['category']
        val = request.POST['val']
        products = Product.objects.filter(product_category=category, active=True)

        final = []
        for product in products:
            final.append({'id': product.id, 'name': product.product_title, 'image': product.get_image(),
                          'price': product.min_price(), 'converted_price': product.calc_som_currency_min()})
        json = {'status': 'success', 'products': final}

        return JsonResponse(json)


def for_loan(request):
    return render(request, 'loan.html')

