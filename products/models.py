import datetime
import json

from django.db import models
from django.utils import timezone
from colorfield.fields import ColorField
from django.utils.safestring import mark_safe
from django.db.models import Q
from accounts.models import Profile
import webapp.models as webapp
from django.core.validators import FileExtensionValidator

capacity_name = [('mb', 'MB'), ('gb', 'GB'), ('tb', 'TB')]
categories = [('iphone', 'iPhone '), ('macBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'),
              ('apple-watch', 'Apple Watch'), ('gadgets', 'Гаджеты'), ('airpods', 'AirPods'),
              ('accessory', 'Аксеcсуары'), ('another', 'Разное')]

additional_categories = [('apple-tv', 'Apple TV '), ('cables', 'Кабели'), ('adapters', 'Переходники'),
                         ('protective-glass', 'Защитные стекла'), ('stylus', 'Стилусы'),
                         ('keyboards-and-mouse', 'Клавиатуры и мышки'), ('charging-device', 'Зарядные устройства'),
                         ('headphones-and-speakers', 'Наушники и колонки'), ('cases-and-bags', 'Чехлы и сумки'),
                         ('drones', 'Дроны'), ('stabilizers', 'Стабилизаторы'), ('camera', 'Камеры'),
                         ('garmin', 'Garmin'), ('vr-glasses', 'VR  очки'), ('graphic-tablets', 'Графические планшеты'),
                         ('another', 'Разное'), ('mac-16', 'MacBook Pro 16'), ('mac-13', 'MacBook Pro 13'),
                         ('mac-13-air', 'MacBook Air 13'), ('mac-12', 'MacBook Retina 12'), ('mac-mini', 'Mac mini'),
                         ('mac-pro', 'Mac Pro'), ('accessory_1', 'Доп Аксессуары 1'), ('accessory_2','Доп Аксессуары 2'), ('accessory_3', 'Доп Аксессуары 3'),
                         ('accessory_4', 'Доп Аксессуары 4'), ('accessory_5', 'Доп Аксессуары 5'), ('gadget_1', 'Доп Гаджеты 1'), ('gadget_2', 'Доп Гаджеты 2'),
                         ('gadget_3', 'Доп Гаджеты 3'), ('gadget_4', 'Доп Гаджеты 4'), ('gadget_5', 'Доп Гаджеты 5')]

categories_arr = {'iphone': 'iPhone ', 'macBook': 'MacBook', 'iPad': 'iPad', 'iMac': 'iMac',
                  'apple-watch': 'Apple Watch', 'gadgets': 'Гаджеты', 'accessory': 'Аксессуары', 'airpods': 'AirPods',
                  'tradeIn': 'Trade In',
                  'apple-tv': 'Apple TV ', 'cables': 'Кабели', 'adapters': 'Переходники',
                  'protective-glass': 'Защитные стекла', 'stylus': 'Стилусы',
                  'keyboards-and-mouse': 'Клавиатуры и мышки', 'charging-device': 'Зарядные устройства',
                  'headphones-and-speakers': 'Наушники и колонки', 'cases-and-bags': 'Чехлы и сумки',
                  'drones': 'Дроны', 'stabilizers': 'Стабилизаторы', 'camera': 'Камеры', 'garmin': 'Garmin',
                  'vr-glasses': 'VR  очки', 'graphic-tablets': 'Графические планшеты', 'another': 'Разное',
                  'mac-16': 'MacBook Pro 16', 'mac-13': 'MacBook Pro 13', 'mac-13-air': 'MacBook Air 13',
                  'mac-12': 'MacBook Retina 12', 'mac-mini': 'Mac mini', 'mac-pro': 'Mac Pro', 'accessory_1': 'Доп Аксессуары 1',
                  'accessory_2': 'Доп Аксессуары 2', 'accessory_3': 'Доп Аксессуары 3', 'accessory_4': 'Доп Аксессуары 4', 'accessory_5': 'Доп Аксессуары 5',
                  'gadget_1': 'Доп Гаджеты 1',
                  'gadget_2': 'Доп Гаджеты 2', 'gadget_3': 'Доп Гаджеты 3', 'gadget_4': 'Доп Гаджеты 4', 'gadget_5': 'Доп Гаджеты 5'
                  }


def convertCurrency(value):
    currency = webapp.Currency.objects.latest('created_at')
    return currency.get_converted_price(value)



class Product(models.Model):
    product_title = models.CharField('Название продукта', max_length=250)
    seo_desc = models.TextField('SEO описание', null=True, blank=True)
    product_description = models.TextField('Описание продукта', null=True, blank=True)
    slug_name = models.CharField('урл продукта', null=True, blank=True, max_length=250, unique=True)
    in_trade = models.BooleanField('tradeIn', default=False)
    pub_date = models.DateTimeField('дата поступления', default=timezone.now)
    product_category = models.CharField('Категория', null=True, max_length=20, choices=categories)
    additional_category = models.ForeignKey(
        'webapp.AdditionalCategory', null=True, blank=True, verbose_name='Подкатегория', related_name="add_category", on_delete=models.SET_NULL)
    description = models.TextField('Текст', null=True, blank=True)
    desc = models.TextField('Короткое описание', null=True, blank=True)
    active = models.BooleanField('Активный', default=True)
    order = models.IntegerField('Порядок', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)

    def __str__(self):
        return str(self.product_title)

    def get_specifcations(self):
        data = json.dumps(list(self.specification.values('id', 'price', 'color_hex', 'capacity', 'keyboard', 'caseSize', 'connectivity', 'ram', 'cpu', 'edition', 'pattern')))
        return data

    def get_url_name(self):
        if self.slug_name:
            return self.slug_name
        return self.id

    def min_price(self):
        min_price = 0
        value = self.specification.filter( ~Q(price=None)).values_list('price', flat=True)
        if value:
            min_price = min(value)
        return round(min_price,2)

    def calc_som_currency_min(self):
        min_price = 0
        value = self.specification.filter( ~Q(price=None)).values_list('price', flat=True)
        if value:
            min_price = convertCurrency(min(value))
        return int(min_price)

    def min_price_image(self):
        self.specification.all().order_by("price")[0]


    def get_image(self):
        image = ""
        specification = self.specification.all().order_by("price")[0]
        images = specification.image.all()
        if(images):
            image = images.first()
            image = '/media/' + str(image.image)
        return image

    def get_images_with_colors(self):
        images = list()
        for specification in self.specification.all():
            if specification.color_hex:
                for image in specification.image.all():
                    images.append([specification.color_hex, '/media/{}'.format(image.image)])
        return images
    
    def get_images_with_colors_unique(self):
        images = list()
        spec_list = []
        for specification in self.specification.all():
            if specification.color_hex:
                for image in specification.image.all():
                    if specification.color_hex.id not in spec_list:
                        spec_list.append(specification.color_hex.id)
                        images.append([specification.color_hex,
                                    '/media/{}'.format(image.image)])
        return images

    def get_images_to_compare(self):
        images = list()
        spec_list = []
        for specification in self.specification.all():
            if specification.color_hex:
                for image in specification.image.all():
                    if specification.color_hex.id not in spec_list:
                        spec_list.append(specification.color_hex.id)
                        images.append(
                            ['/media/{}'.format(specification.color_hex.img), '/media/{}'.format(image.image)])
        return images

    def get_colors(self):
        colors = self.specification.values_list('color_hex', flat=True)
        colors = Color.objects.filter(id__in=colors)
        return enumerate(colors)

    def get_capacities(self):
        capacities = self.specification.values_list('capacity', flat=True)
        capacities = Capacity.objects.filter(id__in=capacities)
        return enumerate(capacities)

    def get_additional_specific(self):
        specific = self.additional_spec.values_list('id', flat=True)
        specific = AdditionalSpecification.objects.filter(id__in=specific)
        return enumerate(specific)

    def get_main_specific(self):
        specific = self.main_spec.values_list('image', 'description')
        return enumerate(specific)

    def get_recommends(self):
        recommends = self.product_recommended.values_list('products_id', flat=True)
        recommends = Product.objects.filter(id__in=recommends)
        return enumerate(recommends)

    def get_recommends_custom(self):
        recommends = self.recommended.values_list('products_id', flat=True)
        recommends = Product.objects.filter(id__in=recommends)
        return enumerate(recommends)

    def get_modules(self):
        modules = self.module.all()
        result = {}
        if modules:
            for module in modules:
                if not module.name in result:
                    result[module.name] = {}
                    result[module.name]['products'] = []
                    result[module.name]['title'] = module.category_name

                result[module.name]['products'].append(
                    {'id': module.id, 'title': module.title, 'desc': module.description,
                     'price': module.price, 'converted': convertCurrency(module.price), 'name': module.name})
        return result

    def get_modules_for_loan(self):
        modules = self.module.all()
        result = {}
        if modules:
            filtered = modules

            if len(modules) > 1:
                filtered = modules[0]

            filtered = self.get_module_by_name(filtered.name)

            for key, module in enumerate(filtered):
                result[key] = []
                result[key].append([module.title, module.price, convertCurrency(module.price), module.id])
                for mod in modules:
                    if module.name != mod.name:
                        result[key].append([mod.title, mod.price, convertCurrency(mod.price), mod.id])
        return result

    def get_module_by_name(self, name):
        modules = self.module.filter(name=name)
        return modules

    def get_category_name(self):
        category = None

        if self.product_category:
            category = categories_arr[self.product_category]

        return category

    def get_additional_category_name(self):
        category = None

        if self.additional_category:
            category = self.additional_category.name

        return category

    def get_additional_category_link(self):
        category = None
        if self.additional_category:
            if self.product_category == 'accessory':
                category = '/catalog/accessory/' + self.additional_category.slug_name
            elif self.product_category == 'gadgets':
                category = '/catalog/gadgets/' + self.additional_category.slug_name
            elif self.product_category == 'tradeIn':
                category = '/catalog/tradeIn/' + self.additional_category.slug_name
            elif self.product_category == 'macBook':
                category = '/catalog/mac/' + self.additional_category.slug_name
        return category

    def get_category_link(self):
        category = None

        if self.product_category:
            category = self.product_category
        return category
    
    def all_specification_is_active(self):
        print(self.specitication.values_list('is_active', flat=True))
        return True


class Module(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='module')
    title = models.CharField('Название', null=True, blank=True, max_length=250)
    category_name = models.CharField('Название категории', null=True, blank=True, max_length=250)
    name = models.CharField('Уникальное слово', null=True, blank=True, max_length=250,
                            help_text="Нужно для того чтобы два модуля были взаимоисключаемые,слово должно быть без пробелов и на английском")
    description = models.TextField('Описание', null=True, blank=True)
    price = models.IntegerField('Цена', null=True, blank=True)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return str(self.title)

    def get_converted(self):
        return convertCurrency(self.price)




class Order(models.Model):
    user = models.ForeignKey(Profile, verbose_name='Пользователь', null=True, blank=True, on_delete=models.CASCADE,
                             related_name='users')
    delivery = models.CharField('Способ доставки', null=True, blank=True, max_length=200)
    address = models.CharField('Адрес', null=True, blank=True, max_length=200)
    country = models.CharField('Страна', null=True, blank=True, max_length=200)
    payment_option = models.CharField('Способ оплаты', null=True, blank=True, max_length=200)
    promo_name = models.CharField('Название промокода', null=True, blank=True, max_length=200)
    promo = models.IntegerField('Скидка по промокоду', null=True, blank=True)
    payment = models.FloatField('Оплачено', null=True, blank=True)
    need_pay = models.FloatField('Нужно оплатить', null=True, blank=True)
    formalized = models.BooleanField('Оформлен', default=False)
    comment = models.TextField('Комментраий', null=True, blank=True)
    created_at = models.DateTimeField('Дата заказа', default=timezone.now)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.promo)




class Color(models.Model):
    name = models.CharField('Название цвета', max_length=200)
    img = models.ImageField('Изображение', null=True, blank=True, upload_to='colors')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return str(self.name)


class Recommended(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_recommended')
    recommended = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='recommended')

    class Meta:
        verbose_name = 'Рекомендуемый'
        verbose_name_plural = 'Рекомендуемые'

    def __str__(self):
        return str(self.recommended)


class Keyboard(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)
    class Meta:
        verbose_name = 'Раскладка клавиатуры'
        verbose_name_plural = 'Раскладка клавиатуры'
    
    def __str__(self):
        return str(self.name)


class CaseSize(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)
    class Meta:
        verbose_name = 'Размер корпуса'
        verbose_name_plural = 'Размеры корпуса'

    def __str__(self):
        return str(self.name)


class Connectivity(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Возможность подключения'
        verbose_name_plural = 'Возможности подключения'

    def __str__(self):
        return str(self.name)


class RAM(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Оперативная память'
        verbose_name_plural = 'Оперативная память'

    def __str__(self):
        return str(self.name)

class CPU(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Процессор'
        verbose_name_plural = 'Процессор'

    def __str__(self):
        return str(self.name)


class Edition(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Pattern(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=200)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модель'

    def __str__(self):
        return str(self.name)
        
class ProductSpecification(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specification')
    capacity = models.ForeignKey('products.Capacity', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='product_capacity',
                                 verbose_name='ёмкость')
    
    color_hex = models.ForeignKey('products.Color', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='color_hex',
                              verbose_name='цвет')
    keyboard = models.ForeignKey('products.Keyboard', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='keyboard',
                                 verbose_name='Раскладка клавиатуры')
    caseSize = models.ForeignKey('products.CaseSize', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='caseSize',
                                 verbose_name='Размер корпуса')
    connectivity = models.ForeignKey('products.Connectivity', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='connectivity',
                                     verbose_name='Возможности подключения')

    ram = models.ForeignKey('products.RAM', null=True, blank=True, on_delete=models.SET_NULL,
                            related_name='ram',
                                 verbose_name='Оперативная память')
    
    cpu = models.ForeignKey('products.CPU', null=True, blank=True, on_delete=models.SET_NULL,
                            related_name='cpu',
                            verbose_name='Процессор')
    
    edition = models.ForeignKey('products.Edition', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='edition',
                                verbose_name='Edition')

    pattern = models.ForeignKey('products.Pattern', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='pattern',
                                verbose_name='Модель')
    quantity = models.IntegerField(
        'Колличество', null=True, blank=True, default=0)
    price = models.FloatField('Цена за штуку в $', null=True, blank=True, default=0)
    is_active = models.BooleanField('Сихронизировать', default=False)
    code = models.TextField('УКТ', null=True, blank=True)
    is_valid = models.BooleanField('Найден', default=False)

    class Meta:
        verbose_name = 'спецификацию'
        verbose_name_plural = 'Спецификации'

    def __str__(self):
        return str(self.products.product_title) + self.get_color_name()

    def get_image(self):
        if not self.image.all().count():
            return None
        return self.image.all()[0]

    def get_color_name(self):
        if (self.color_hex):
            return self.color_hex.name
        else: 
            return ""

    def convert_product_price(self):
        return convertCurrency(self.price)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True,
                              on_delete=models.CASCADE, related_name='ordered_products')
    product = models.ForeignKey(Product, verbose_name='Продукт', null=True, blank=True, on_delete=models.CASCADE,
                                related_name='in_order_products')
    color = models.CharField('Цвет', null=True, blank=True, max_length=50)
    specification = models.ForeignKey(
        ProductSpecification, null=True, blank=True, on_delete=models.SET_NULL, related_name='spec_order')
    capacity = models.CharField(
        'Ёмкость', null=True, blank=True, max_length=200)
    keyboard = models.CharField(
        'Раскладка клавиатуры', null=True, blank=True, max_length=256)
    caseSize = models.CharField(
        'Размер корпуса', null=True, blank=True, max_length=256)
    connectivity = models.CharField(
        'Возможности подключения', null=True, blank=True, max_length=256)
    ram = models.CharField('Оперативная память',
                           null=True, blank=True, max_length=256)
    cpu = models.CharField('Процессор', null=True, blank=True, max_length=256)
    edition = models.CharField(
        'Edition', null=True, blank=True, max_length=256)
    pattern = models.CharField('Модель', null=True, blank=True, max_length=256)
    quantity = models.IntegerField('Колличество', null=True, blank=True)
    comment = models.TextField('Комментарий', null=True, blank=True)
    price = models.IntegerField('Цена', null=True, blank=True)
    converted = models.IntegerField('Цена в сомах', null=True, blank=True)
    quantity = models.IntegerField('Колличество', null=True, blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_product_image(self):
        print("hererer")
        image = self.specification.get_image()
        return '/media/'+str(image)

    def get_product_title(self):
        title = self.product.product_title
        return title

    def get_product_id(self):
        title = self.product.id
        return title

    def get_product_price(self):
        return self.price

    def get_product_converted_price(self):
        return round(self.converted, 2)

class AdditionalSpecification(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_spec')
    specification = models.CharField('Свойство', null=True, blank=True, max_length=50)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'допольнительные свойство'
        verbose_name_plural = 'допольнительные свойства'

    def __str__(self):
        return str(self.specification)


class MainSpecification(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='main_spec')
    # image = models.ImageField('Изображение', null=True, blank=True, upload_to='specification')
    image = models.FileField('Изображение', null=True, blank=True, upload_to='specification', validators=[FileExtensionValidator(['webp','png', 'jpg', 'svg'])])

    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Основную характеристику'
        verbose_name_plural = 'Основные характеристики'

    def __str__(self):
        return str(self.description)


class Capacity(models.Model):
    capacity = models.IntegerField('Ёмкость')
    measure = models.CharField('Измерять в', null=True, max_length=20, choices=capacity_name)

    class Meta:
        verbose_name = 'ёмкость'
        verbose_name_plural = 'Ёмкости'

    def __str__(self):
        return str(self.capacity) + ' ' + str(self.measure)
    
    def get_name(self):
        return str(self.capacity) + ' ' + str(self.measure)


class Image(models.Model):
    specification = models.ForeignKey(ProductSpecification, on_delete=models.CASCADE, related_name='image', null=True, blank=True)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='products')

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'Изображении'

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    name = models.CharField('Название категории', max_length=200)
    slug_name = models.CharField('урл категории', null=True, blank=True, max_length=210, unique=True)
    products = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)


class Promocode(models.Model):
    name = models.CharField('Название промокода', max_length=200)
    code_word = models.CharField('Кодовое слово', null=True, blank=True, max_length=210, unique=True)
    percent = models.IntegerField('Процент', null=True, blank=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return str(self.name)


class Basket(models.Model):
    user_token = models.CharField(
        'Токен', null=True, blank=True, max_length=200)
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.CASCADE, related_name='products')
    specification = models.ForeignKey(
        ProductSpecification, null=True, blank=True, on_delete=models.SET_NULL, related_name='spec')
    color = models.CharField('Цвет', null=True, blank=True, max_length=200)
    capacity = models.CharField(
        'Ёмкость', null=True, blank=True, max_length=200)
    keyboard = models.CharField('Раскладка клавиатуры', null=True, blank=True, max_length=256)
    caseSize = models.CharField(
        'Размер корпуса', null=True, blank=True, max_length=256)
    connectivity = models.CharField(
        'Возможности подключения', null=True, blank=True, max_length=256)
    ram = models.CharField('Оперативная память', null=True, blank=True, max_length=256)
    cpu = models.CharField('Процессор', null=True, blank=True, max_length=256)
    edition = models.CharField('Edition', null=True, blank=True, max_length=256)
    pattern = models.CharField('Модель', null=True, blank=True, max_length=256)
    quantity = models.IntegerField('Колличество', null=True, blank=True)
    created_at = models.DateTimeField('дата поступления', default=timezone.now)
    comment = models.TextField('Комментарий', null=True, blank=True)

    def __str__(self):
        return str(self.capacity)

    def get_product_image(self):
        image = self.specification.get_image()
        return '/media/'+str(image)

    def get_product_title(self):
        title = self.product.product_title
        return title

    def get_product_id(self):
        id = self.product.id
        return id

    def get_product_price(self):
        price = self.specification.price
        return price

    def get_product_converted_price(self):
        price = self.specification.price
        price = convertCurrency(price)
        return round(price, 2)
