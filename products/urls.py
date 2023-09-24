from django.urls import path

from . import views

app_name = "catalog"
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<slug:slug>', views.product, name='product'),
    path('getProduct', views.get_product, name='get_product'),
    path('getProductPrice', views.get_product_price, name='get_product_price'),
    path('for-loan', views.for_loan, name='for_loan'),
    path('<str:category>', views.products, name='products'),
    path('accessory/<str:category>', views.accessory, name='accessory'),
    path('gadgets/<str:category>', views.gadgets, name='gadgets'),
    path('tradeIn/<str:category>', views.tradeIn, name='tradeIn'),
    path('mac/<str:category>', views.mac, name='mac'),
    path('sortFromCatalog', views.sort_from_catalog, name='sort_from_catalog'),
]
