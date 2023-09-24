from source import settings
from products.models import Category, Product, Basket
from .models import AdditionalCategory, Footer, PopularSearch, Settings, MainPage, Category, Currency
from datetime import datetime
data = settings.FILES


def initial_variables(request):
    products_in_basket = []
    recommended_products = []
    products_price = 0
    products_converted_price = 0

    if 'user_token' in request.session:

        token = request.session['user_token']
        products_in_basket = Basket.objects.filter(user_token=token)

        for product in products_in_basket:
            products_price += product.get_product_price() * product.quantity
            products_converted_price += product.get_product_converted_price() * product.quantity
            recommended_products.append(product.product)

    popular_search = PopularSearch.objects.all()
    footer = Footer.objects.latest('pub_date')

    previous = request.META.get('HTTP_REFERER')

    settings = Settings.objects.latest('pub_date')

    notify = None

    category_images = Category.objects.first()
    additional_categoreis = AdditionalCategory.objects.filter(active=True)
    mac_category = additional_categoreis.filter(main_category="mac")
    accessory_category = additional_categoreis.filter(
        main_category="accessory")
    gadget_category = additional_categoreis.filter(main_category="gadgets")
    currency = Currency.objects.latest('created_at')

    if 'notify' in request.session:
        notify = request.session['notify']
        del request.session['notify']


    currentYear = datetime.now().year
    return {'js': data['js'], 'css': data['css'], 'popular_search': popular_search, 'notify':notify,
            'products_in_basket': products_in_basket, 'previous': previous,
            'products_price': products_price, 'products_converted_price': products_converted_price,
            'recommended_products': recommended_products, 'settings': settings, 'category_images': category_images, 'mac_category': mac_category,
            'accessory_category': accessory_category, 'gadget_category': gadget_category,
            'currency': currency, 'footer': footer, 'currentYear': currentYear}
