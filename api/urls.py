from django.urls import path

from api import views

app_name = "api"
urlpatterns = [
    path('checkPayments', views.check_payments, name='check_payments'),
    path('checkPaybox', views.check_paybox, name='check_paybox'),
]
