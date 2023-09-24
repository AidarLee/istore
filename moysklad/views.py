from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import json
import requests
# Create your views here.
from .models import Auth
from products.models import ProductSpecification
from webapp.models import Currency
import datetime
def auth(request):
    data = {
        'name': 'SAMSA',
        "attributes": [
            {
                "meta": {
                    "href": "https://online.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/3e7f2594-345b-11eb-0a80-03ad0002e45a",
                    "type": "attributemetadata",
                    "mediaType": "application/json"
                },
                "name": "color",
                "value": "White",
            }
        ],
        "group": {
            "meta": {
                "href": "https://online.moysklad.ru/api/remap/1.2/entity/group/55af0bc1-33b0-11eb-0a80-05520000277f",
                "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/group/metadata",
                "type": "group",
                "mediaType": "application/json"
            }
        },
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://online.moysklad.ru/api/remap/1.2/entity/product'
    r = requests.post(url, data=json.dumps(data), auth=(
        "admin@kaarov81", "6fa8fa798e"), headers=headers)

    return JsonResponse(r.json())




def check_connection(request, id):
    auth = Auth.objects.get(id=id)
    url = 'https://online.moysklad.ru/api/remap/1.2/security/token'
    r = requests.post(url, auth=(auth.email, auth.password))
    data = r.json()
    if "errors" in data:
        auth.error = data["errors"][0]["error"]
        auth.is_active = False
    else:
        auth.is_active = True
        auth.error = ""
    auth.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def get_products(request, id=None):
    if id:
        auth = Auth.objects.get(id=id)
    else:
        auth = Auth.objects.first()
    url = 'https://online.moysklad.ru/api/remap/1.2/entity/assortment'
    r = requests.get(url, auth=(auth.email, auth.password))
    data = r.json()
    # return JsonResponse(r.json())
    if "rows" in data:
        auth.is_active = True
        auth.error = ""
        specifications = ProductSpecification.objects.filter(
            code__isnull=False, is_active=True)
        specifications.update(is_valid=False)
        update_next_offset(data, auth, specifications)
    elif "errors" in data:
        auth.error = data["errors"][0]["error"]
        auth.is_active = False
    auth.pub_date = datetime.datetime.now()
    auth.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def update_next_offset(data, auth, specifications):
    update_products(data["rows"], auth, specifications)
    if "nextHref" in data["meta"]:
        r = requests.get(data["meta"]["nextHref"],
                         auth=(auth.email, auth.password))
        data = r.json()
        update_next_offset(data, auth, specifications)



def get_currencies(auth_moysklad):
    currency = Currency.objects.first()
    if currency:
        url = 'https://online.moysklad.ru/api/remap/1.2/entity/currency/{}'.format(currency.usd)
        resp = requests.get(url, auth=(auth_moysklad.email, auth_moysklad.password)).json()
        if resp:
            if "errors" in resp:
                currency.error = resp["errors"][0]["error"]
                currency.is_valid = False
            else:
                currency.error = ""
                currency.is_valid = True
            
            if currency.is_active and "rate" in resp:
                currency.exchange_rate = resp["rate"]
            currency.save()
    return currency


def update_products(products, auth, specifications):
    currency = get_currencies(auth)
    if currency:
        usd_currency = "https://online.moysklad.ru/api/remap/1.2/entity/currency/{}".format(
            currency.usd)
        for product in products:
            code_specification = specifications.filter(code=product["code"])
            for specification in code_specification:
                exchange = 1
                if product["salePrices"][0] and product["salePrices"][0]["currency"]["meta"]["href"] != usd_currency:
                    exchange = currency.exchange_rate
                specification.price = float(product["salePrices"][0]["value"]/100) / exchange
                specification.quantity = product["quantity"]
                specification.is_valid = True
                specification.save()

        
        
        
