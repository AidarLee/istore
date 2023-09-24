import urllib.parse

from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect, HttpResponse
import json
from django.utils import translation
import requests
import socket
import ssl
import os
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_exempt
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
from django.core.mail import send_mail
from django.template.loader import render_to_string
import contextlib
import requests
import tempfile
import pycurl
from io import BytesIO
from urllib.parse import urlencode
from webapp.models import Transaction
from products.models import Order
from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404, redirect
send_message_to_mail = "info@istore.kg"
send_message_from_mail = "testingfor9999@gmail.com"

def make_payment(request):
    kicb = KICB()
    ip = kicb.get_client_ip()
    total_price = 2500
    currency = 417

    data = {
        'command': 'v',
        'client_ip_addr': ip,
        'msg_type': 'SMS',
        'amount': total_price * 100,
        'currency': currency,
        'lang': 'ru',
    }
    response = kicb.make_query(data)
    return HttpResponseRedirect(kicb.serverURL + '?trans_id=' + str(response[16:]))
    # json_resp = {
    #     "all": response,
    #     'cur': response[16:]
    # }
    # return JsonResponse(json_resp, safe=False)
class KICB():
    serverURL = 'https://ecomm.elpay.kg:2443/ecomm2/ClientHandler'
    merchantURL = 'https://ecomm.elpay.kg:3443/ecomm2/MerchantHandler'
    headers = {
        'Content-Type': 'application/json'
    }

    def get_client_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

    def make_query(self, data):
        b_obj = BytesIO()
        crl = pycurl.Curl()
        post = urllib.parse.urlencode(data)
        # Set URL value
        crl.setopt(crl.URL, self.merchantURL)

        # Write bytes that are utf-8 encoded
        crl.setopt(crl.WRITEFUNCTION, b_obj.write)
        crl.setopt(crl.VERBOSE, 1)
        crl.setopt(crl.SSLKEY, '/home/i/istorekg/istore.kg/public_html/tmp/ima.key')
        crl.setopt(crl.SSLCERT, '/home/i/istorekg/istore.kg/public_html/tmp/MCertResp.pem')
        crl.setopt(crl.SSLCERTPASSWD, 'XGD_2Odcaq8I1pdbry3G')

        crl.setopt(crl.SSL_VERIFYPEER, False)
        crl.setopt(crl.SSL_VERIFYHOST, False)

        crl.setopt(crl.HEADER, False)
        crl.setopt(crl.POST, 1)
        crl.setopt(crl.POSTFIELDS, post)

        # Perform a file transfer
        crl.perform()

        # End curl session
        crl.close()

        # Get the content stored in the BytesIO object (in byte characters)
        get_body = b_obj.getvalue()

        return get_body.decode('utf8')

    def check_payment(self, transaction, ip, delete_on="all"):
        data = {
            'command': 'c',
            'client_ip_addr': ip,
            'trans_id': transaction
        }
        response = self.make_query(data)
        status = ''
        if response:
            if 'OK' in response:
                status = 'success'
                trn = Transaction.objects.get(transaction_id=transaction)
                if trn and (delete_on == 'success' or delete_on == 'all'):
                    order = trn.order
                    trn.delete()
                    if order:
                        order.payment = order.need_pay
                        order.save()

            elif 'DECLINED' in response:
                status = 'fail'
            elif 'FAILED' in response:
                status = 'fail'
            elif 'TIMEOUT' in response:
                status = 'fail'

            if status == 'fail' and (delete_on == 'fail' or delete_on == 'all'):
                trn = Transaction.objects.get(transaction_id=transaction)
                if trn:
                    order = trn.order
                    trn.delete()
                    if order:
                        order.delete()

        return status

    def check_payment_response(self, transaction, ip, delete_on="all"):
        data = {
            'command': 'c',
            'client_ip_addr': ip,
            'trans_id': transaction
        }
        response = self.make_query(data)

        return response



def check_payment(self):
    trn = Transaction.objects.filter(option='kicb').latest('pub_date')
    kicb = KICB()
    data = {
        'command': 'c',
        'client_ip_addr':  trn.ip,
        'trans_id': trn.transaction_id
    }
    response = kicb.make_query(data)
    status = ''
    if response:
        if 'OK' in response:
            status = 'success'
        elif 'DECLINED' in response:
            status = 'fail'
        elif 'FAILED' in response:
            status = 'fail'
        elif 'TIMEOUT' in response:
            status = 'fail'

    json_resp = {
        "all": response,
        "status": status,
        "trn_id": trn.transaction_id
    }
    return JsonResponse(json_resp, safe=False)

@csrf_exempt
def check_payments(request):
    paybox = Paybox()
    transactions = Transaction.objects.filter(status=None)
    for transaction in transactions:
        paybox.check_transaction(transaction)
    return HttpResponse("checked")

def check_paybox(request):
    paybox = Paybox()    
    id = request.GET.get('pg_order_id')
    transaction = Transaction.objects.get(pk=id)
    resp = paybox.check_transaction(transaction)
    if resp:
        if transaction.reserve:
            msg_html = render_to_string(
                'mail/reserve_mail.html', {'reserve': transaction.reserve})
            send_mail(
                'Бронь с istore.kg',
                '',
                send_message_from_mail,
                [send_message_to_mail],
                fail_silently=True,
                html_message=msg_html
            )
        return redirect('/successPayment')
    else:
        return redirect('/failurePayment')

class Paybox():
    url = "https://api.paybox.money/init_payment.php"
    check_url = "https://api.paybox.money/get_status2.php"
    
    result_url = "https://istore.kg/api/checkPaybox"
    # result_url = "http://127.0.0.1:8000/api/checkPaybox"
    merchant_secret = "zVnXIm6VvbFusIiS"
    merchant_id = 541057

    def create_purchase_link(self, order, transaction):
        description = ""
        order_products = order.ordered_products.all()
        for order_product in order_products:
            description +=  order_product.product.product_title
        pg_salt = str(randint(100000, 1000000000))
        transaction.payment = order.need_pay
        transaction.save()
        paybox_data =  {
            'pg_amount': order.need_pay,
            'pg_description': description,
            'pg_failure_url': self.result_url,
            'pg_language': 'ru',
            'pg_merchant_id': self.merchant_id,
            'pg_order_id': transaction.id,
            'pg_salt': pg_salt,
            'pg_success_url': self.result_url,
        }
        signature = "init_payment.php;{};{};{};{};{};{};{};{};{}".format(
            order.need_pay, description, self.result_url, 'ru', self.merchant_id, transaction.id, pg_salt, self.result_url, self.merchant_secret)
        paybox_data['pg_sig'] = hashlib.md5(signature.encode('utf-8')).hexdigest()
        r = requests.post(self.url, data=paybox_data)
        xml = BeautifulSoup(r.content)
        if(xml.find('pg_status').get_text() == "ok"):
            return xml.find('pg_redirect_url').get_text()
        else:
            return None

    def check_transaction(self, transaction):
        pg_salt = str(randint(100000, 1000000000))
        paybox_data = {
            'pg_language': 'ru',
            'pg_merchant_id': self.merchant_id,
            'pg_order_id': transaction.id,
            'pg_salt': pg_salt,
        }
        signature = "get_status2.php;{};{};{};{};{}".format(
            'ru', self.merchant_id, transaction.id, pg_salt, self.merchant_secret)
        paybox_data['pg_sig'] = hashlib.md5(signature.encode('utf-8')).hexdigest()
        r = requests.post(self.check_url, data=paybox_data)
        xml = BeautifulSoup(r.content)
        transaction.status = xml.find('pg_transaction_status').get_text()
        
        if(transaction.status!='partial'):
            transaction.save()
        
        if(transaction.status == "ok"):
            if(transaction.to == "order"):
                transaction.order.payment = transaction.payment
                transaction.order.save()
            elif(transaction.to == "reserve"):
                transaction.reserve.payment = transaction.payment
                transaction.reserve.save()
            return True
        else:
            return False

    def create_reserve_link(self, reserve, transaction, payment_sum):
        pg_salt = str(randint(100000, 1000000000))
        description = reserve.product.product_title
        paybox_data = {
            'pg_amount': payment_sum,
            'pg_description': description,
            'pg_failure_url': self.result_url,
            'pg_language': 'ru',
            'pg_merchant_id': self.merchant_id,
            'pg_order_id': transaction.id,
            'pg_salt': pg_salt,
            'pg_success_url': self.result_url,
        }
        signature = "init_payment.php;{};{};{};{};{};{};{};{};{}".format(
            payment_sum, description, self.result_url, 'ru', self.merchant_id, transaction.id, pg_salt, self.result_url, self.merchant_secret)
        paybox_data['pg_sig'] = hashlib.md5(
            signature.encode('utf-8')).hexdigest()
        r = requests.post(self.url, data=paybox_data)
        xml = BeautifulSoup(r.content)
        if(xml.find('pg_status').get_text() == "ok"):
            return xml.find('pg_redirect_url').get_text()
        else:
            return None
