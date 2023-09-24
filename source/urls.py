"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import handler404
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from webapp import views
from django.views.static import serve
handler404 = 'webapp.views.not_found'
handler503 = 'webapp.views.maintenance_mode'

urlpatterns = [
        path('', views.main, name='home'),
        path('_nested_admin/', include('nested_admin.urls')),
        path('grappelli/', include('grappelli.urls')),
        #path('social/', include('social_django.urls', namespace='social')),
        path('maintenance-mode/', include('maintenance_mode.urls')),
        path('log/', admin.site.urls),
        path('accounts/', include('accounts.urls')),
        path('catalog/', include('products.urls')),
        path('moysklad/', include('moysklad.urls')),
        path('api/', include('api.urls')),
        path('about-us', views.about_us, name='about_us'),
        path('contacts', views.contacts, name='contacts'),
        path('warranty', views.warranty, name='warranty'),
        path('whyUs', views.whyUs, name='whyUs'),
        path('loan', views.loan, name='loan'),
        path('create_loan', views.create_loan, name='create_loan'),
        path('purchase_on_credit', views.purchase_on_credit, name='purchase_on_credit'),
        path('add_on_credit', views.add_on_credit, name='add_on_credit'),
        path('getBankData', views.get_bank_data, name='get_bank_data'),
        # path('service', views.service, name='service'),
        # path('service/<str:category>', views.service, name='service'),
        path('articles', views.articles, name='articles'),
        path('article/<int:id>', views.article, name='article'),
        path('basket', views.basket, name='basket'),
        path('checkout', views.checkout, name='checkout'),
        path('compare', views.compare, name='compare'),
        path('toBasket', views.to_basket, name='to_basket'),
        path('callBack', views.call_back, name='call_back'),
        path('serviceCallBack', views.service_call_back, name='service_call_back'),
        path('removeFromBasket', views.remove_from_basket, name='remove_from_basket'),
        path('changeInBasket', views.change_in_basket, name='change_in_basket'),
        path('getServiceByCategory', views.get_service_by_category, name='get_service_by_category'),
        path('makeOrder', views.make_order, name='make_order'),
        path('removeReserve/<int:id>', views.remove_reserve, name='remove_reserve'),
        path('mainSearch', views.main_search, name='main_search'),
        path('promoSearch', views.promo_search, name='promo_search'),
        path('compareCategorySelect', views.compare_category_select, name='compare_category_select'),
        path('search', views.search, name='search'),
        path('search/<str:search>', views.search_with_value, name='search_with_value'),
        path('not_found', views.not_found, name='not_found'),
        path('saveImage', views.save_image, name='save_image'),
        path('addNewProduct', views.add_new_product, name='add_new_product'),
        path('success', views.success, name='success'),
        path('makeReserve', views.make_reserve, name='make_reserve'),
        path('checkPayment', views.check_payment, name='check_payment'),
        path('partnerGetPaymentStatus', views.partner_get_payment_status, name='partner_get_payment_status'),
        path('agreement', views.agreement, name='agreement'),
        path('privacy', views.privacy, name='privacy'),
        path('successPayment', views.success_payment, name='success_payment'),
        path('failurePayment', views.failure_payment, name='failure_payment'),
        path('parseCurrency', views.parse_currency, name='parse_currency'),
        path('tradeIn/<int:id>', views.tradeIn, name='tradeIn'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]
