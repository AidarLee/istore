import datetime
import json

from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.forms import ModelForm
from products.models import Product, Order, ProductSpecification
from datetime import timedelta, datetime
from colorfield.fields import ColorField
from accounts.models import Profile

categories = [('iphone', 'iPhone '), ('macBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'),
              ('apple-watch', 'Apple Watch')]

main_page_categories = [('iphone', 'iPhone '), ('macBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'),
                        ('apple-watch', 'Apple Watch'), ('gadgets', 'Гаджеты'), ('airpods', 'AirPods'),
                        ('accessory', 'Акссесуары')]
additional_categories = [('mac', 'Mac'), ('gadgets', 'Гаджеты '), ('accessory', 'Аксессуары')]
passport_choices = [('1', 'ID паспорт'), ('2', 'Биометрический паспорт')]

salary_choices = [('1', 'Продленный действующий патент'), ('2', 'Справка о доходах')]
slider_choices = [('1', 'Главная'), ('2', 'Акционная')]
tradeIn = [(1, 1), (2, 2), (3, 3)]


def convertCurrency(value):
    currency = Currency.objects.latest('created_at')
    return currency.get_converted_price(value)


class Article(models.Model):
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='articles')
    title = models.CharField('Название статьи', max_length=250)
    secondary_title = models.CharField('Короткое описание', null=True, blank=True, max_length=250)
    description = models.TextField('Текст', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    active = models.BooleanField('Опубликовать', default=True)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return str(self.title)

    def get_image(self):
        image = self.image
        if image:
            image = '/media/' + str(image)
        return image


class Service(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=20)
    category = models.CharField('Категория', null=True, max_length=20, choices=categories)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return str(self.name)


class ServiceCallBack(models.Model):
    name = models.CharField('Имя', null=True, blank=True, max_length=20)
    phone = models.CharField('Телефон', null=True, max_length=25)
    category = models.CharField('Категория', null=True, max_length=100)
    product = models.CharField('Модель', null=True, max_length=100)
    reason = models.CharField('Причина', null=True, max_length=100)
    another = models.TextField('Другая причина', null=True, max_length=25)
    formalized = models.BooleanField('Расмотрен', default=False)
    created_at = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Форма заявки по сервису'
        verbose_name_plural = 'Форма заявки по сервисам'

    def __str__(self):
        return str(self.name)


class CallBack(models.Model):
    name = models.CharField('Имя', null=True, blank=True, max_length=20)
    phone = models.CharField('Телефон', null=True, max_length=25)
    topic = models.CharField('Тема', null=True, max_length=100)
    desc = models.TextField('Сообщение', null=True, max_length=25)
    formalized = models.BooleanField('Расмотрен', default=False)
    created_at = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return str(self.name)


class PopularSearch(models.Model):
    name = models.CharField('Имя', null=True, blank=True, max_length=20)
    created_at = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Популярный запрос'
        verbose_name_plural = 'Популярные запросы'

    def __str__(self):
        return str(self.name)


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y-%m-%d')
    created_at = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return str(self.docfile)


class Currency(models.Model):
    exchange_rate = models.FloatField('Курс', null=True, blank=True)
    is_active = models.BooleanField('Синхронизировать', default=False)
    time = models.TimeField('Промежуток обновление', default="00:30")
    created_at = models.DateTimeField('Дата', default=timezone.now)
    updated_at = models.DateTimeField('Обновлен', default=timezone.now)
    usd = models.CharField('USD id', null=True, blank=True, max_length=250)
    is_valid = models.BooleanField('Подключен', default=False)
    error = models.TextField('Ошибки', null=True, blank=True)

    class Meta:
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курс валют'

    def __str__(self):
        return str(self.exchange_rate)

    def get_converted_price(self, value):
        result = self.exchange_rate * value
        return int(round(result))


class Settings(models.Model):
    sms_url = models.CharField('Урл для смс', max_length=400)
    sms_login = models.CharField('Логин для смс', max_length=400)
    sms_pwd = models.CharField('Пароль для смс', max_length=400)
    sms_sender_id = models.CharField('Имя отправителя для смс', max_length=400)
    reserve_price = models.IntegerField('Сумма залога')
    reserve_text = models.TextField('Описание залога', null=True, blank=True)
    email = models.CharField('Email почта', max_length=400)
    contact_first = models.CharField('Контактный номер', null=True, blank=True, max_length=400)
    contact_second = models.CharField('Контактный номер 2', null=True, blank=True, max_length=400)
    address = models.CharField('Адрес', null=True, blank=True, max_length=400)
    schedule = models.CharField('Режим работы', max_length=400)
    loan_title = models.CharField('Текст покупки в кредит', max_length=400)
    loan_desc = models.TextField('Описание покупки в кредит')
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    instagram = models.CharField('Ссылка на instagram', max_length=400)
    facebook = models.CharField('Ссылка на facebook', max_length=400)
    youtube = models.CharField('Ссылка на YouTube', null=True, blank=True, max_length=400)
    title = models.CharField('Название сайта', null=True, blank=True, max_length=400)
    description = models.CharField('Описание сайта', max_length=400)
    class Meta:
        verbose_name = 'Настройка сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return str(self.sms_url)


class MainPage(models.Model):
    second_product_title = models.CharField('Название продукта', null=True, blank=True, max_length=400)
    second_product_desc = models.CharField('Описание', null=True, blank=True, max_length=400)
    second_product_img = models.ImageField('Изображение', null=True, blank=True, upload_to="main_page")
    second_product_img_mobile = models.ImageField('Мобильное изображение', null=True, blank=True, upload_to="main_page")
    second_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='second_product')

    fifth_block_title = models.CharField('Название пятого блока', null=True, blank=True, max_length=400)
    fifth_block_desc = models.CharField('Описание', null=True, blank=True, max_length=400)
    fifth_block_link = models.CharField('Сылка', null=True, blank=True, max_length=400)
    fifth_block_category = models.CharField('Категория', null=True, max_length=20, choices=main_page_categories)

    sixth_block_title = models.CharField('Название шестого блока', null=True, blank=True, max_length=400)
    sixth_block_desc = models.CharField('Описание', null=True, blank=True, max_length=400)
    sixth_block_link = models.CharField('Сылка', null=True, blank=True, max_length=400)
    sixth_block_category = models.CharField('Категория', null=True, max_length=20, choices=main_page_categories)

    seventh_block_title = models.CharField('Название седьмого блока', null=True, blank=True, max_length=400)
    seventh_block_desc = models.CharField('Описание', null=True, blank=True, max_length=400)
    seventh_block_link = models.CharField('Сылка', null=True, blank=True, max_length=400)
    seventh_block_img = models.FileField('Видео', upload_to='main_page', blank=True, null=True)

    first_service_title = models.CharField('Первый сервис', null=True, blank=True, max_length=400)
    first_service_desc = models.CharField('Описание', null=True, blank=True, max_length=400)
    first_service_link = models.CharField('Сылка', null=True, blank=True, max_length=400)
    first_service_img = models.ImageField('Изображение', null=True, blank=True, upload_to="main_page")

    second_service_title = models.CharField('Второй сервис', null=True, blank=True, max_length=400)
    second_service_desc = models.CharField('Описание', null=True, blank=True, max_length=400)
    second_service_link = models.CharField('Сылка', null=True, blank=True, max_length=400)
    second_service_img = models.ImageField('Изображение', null=True, blank=True, upload_to="main_page")

    news_title = models.CharField('Название новостей', null=True, blank=True, max_length=400)
    news_desc = models.CharField('Описание', null=True, blank=True, max_length=400)

    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'

    def __str__(self):
        return str(self.second_product_title)


class MainPageProducts(models.Model):
    page = models.ForeignKey(MainPage, null=True, blank=True, on_delete=models.CASCADE,
                             related_name='page_product')
    product_title = models.CharField('Название', max_length=400)
    product_desc = models.CharField('Описание', max_length=400)
    product_img = models.ImageField('Изображение', upload_to="main_page")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='main_page_product')
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return str(self.product_title)


class Bank(models.Model):
    title = models.CharField('Название', max_length=400)
    img = models.ImageField('Лого', upload_to="banks")
    desc = models.TextField('Необходимые документы')
    desc_for_office = models.TextField('Оформление кредита в нашем офисе')
    agreement = models.TextField('Пользовательское соглашение')
    start_price = models.IntegerField('Сумма от')
    end_price = models.IntegerField('Сумма до')
    guarantor = models.BooleanField('Поручитель', default=False)
    initial_fee = models.IntegerField('Первоначальный взнос')
    initial_fee_before = models.IntegerField('Первоначальный взнос после')
    start_period = models.IntegerField('Сроки кредитования от')
    end_period = models.IntegerField('Сроки кредитования до')
    term_of_consider = models.CharField('Сроки рассмотрения заявки', max_length=400)
    repayment = models.CharField('Погашение', max_length=400)
    online = models.BooleanField('Онлайн', default=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return str(self.title)

    def get_percents(self, w_json=True):
        percents = {}
        for percent in self.bank_percents.all():
            if percent.percent_before:
                percents[str(percent.percent_before)] = percent.percent
            else:
                percents['0'] = percent.percent

        if not percents:
            percents['0'] = 0
        if w_json:
            return json.dumps(percents)
        else:
            return percents

    def get_percent(self):
        percent = self.bank_percents.first()
        if percent:
            percent = percent.percent
        else:
            percent = 0
        return percent

    def get_all_sum_and_per_month(self, price, period, initial_fee):
        percent = 0
        for key, in_percent in self.get_percents(False).items():
            percent = in_percent
            if float(key) >= price:
                percent = in_percent
                break

        price -= initial_fee
        whole_price = price
        pl = percent/12/100
        period_val = period
        k = pl * pow(1+pl, period_val) / (pow(1+pl, period_val) - 1)
        per_month = k * price
        whole_interest = 0
        for i in range(0, period_val):
            interest = pl * whole_price
            whole_interest += interest
            whole_price -= per_month - interest

        per_month = round(per_month)
        price = round(price + whole_interest + initial_fee)

        if not per_month:
            per_month = 0
        if not price:
            price = 0
        return price, per_month


class BankPercents(models.Model):
    bank = models.ForeignKey(Bank, null=True, on_delete=models.CASCADE, related_name='bank_percents')
    percent = models.FloatField('Процент')
    percent_before = models.FloatField('Процент до достижение суммы', null=True, blank=True)

    class Meta:
        verbose_name = 'Процент банка'
        verbose_name_plural = 'Проценты банка'

    def __str__(self):
        return str(self.percent)


class PurchaseOnCredit(models.Model):
    name = models.CharField('ФИО', max_length=400)
    phone = models.CharField('Номер телефона', max_length=100)
    email = models.CharField('Email', max_length=100)
    passport = models.CharField('Паспортные данные', null=True, blank=True, max_length=20, choices=passport_choices)
    passport_front = models.ImageField('Лицевая сторона паспорта', upload_to="documents")
    passport_back = models.ImageField('Задняя сторона паспорта', upload_to="documents")
    place_of_residence = models.ImageField('Справка с места жительства', null=True, blank=True
                                           , upload_to="documents")
    salary = models.CharField('Справка о заработной плате', null=True, blank=True, max_length=20,
                              choices=passport_choices)
    salary_img = models.ImageField('Справка о заработной плате файл', upload_to="documents")
    bank = models.CharField('Банк', max_length=200, null=True, blank=True)
    whole_price = models.FloatField('Общая сумма', null=True, blank=True)
    per_month = models.FloatField('Оплата в месяц', null=True, blank=True)
    month = models.CharField('Срок кредита', max_length=100, null=True, blank=True)
    initial_fee = models.FloatField('Первоначальный взнос', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Покупка в кредит'
        verbose_name_plural = 'Покупки в кредит'

    def __str__(self):
        return str(self.name)


class PurchaseForm(ModelForm):
    class Meta:
        model = PurchaseOnCredit
        fields = '__all__'


class PurchaseOnCreditProducts(models.Model):
    credit = models.ForeignKey(PurchaseOnCredit, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='credit')
    credit_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='credit_product', verbose_name="Продукт")
    specification = models.ForeignKey(
        ProductSpecification, null=True, blank=True, on_delete=models.CASCADE, related_name='specification', verbose_name="Спецификация")
    price = models.FloatField('Цена устройства на момент оформление', null=True, blank=True)
    price_converted = models.FloatField('Цена устройства в сомах', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return str(self.price)


class Reserve(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='reserve')
    user = models.ForeignKey(Profile, verbose_name='Пользователь', null=True, blank=True, on_delete=models.CASCADE,
                             related_name='user_reserve')
    name = models.CharField('ФИО', max_length=200, null=True, blank=True)
    phone = models.CharField('Контактный номер', max_length=200, null=True, blank=True)
    color = models.CharField('Цвет', null=True, blank=True, max_length=25)
    specification = models.ForeignKey(
        ProductSpecification, null=True, blank=True, on_delete=models.SET_NULL, related_name='spec_reserve')
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
    capacity = models.CharField('Ёмкость', null=True, blank=True, max_length=25)
    payment = models.FloatField('Сумма брони', null=True, blank=True)
    reserve_price = models.FloatField('Цена брони', null=True, blank=True)
    price = models.FloatField('Цена устройства на момент брони', null=True, blank=True)
    price_converted = models.FloatField('Цена устройства в сомах', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    last_date = models.DateTimeField('Дата конца брони', default=datetime.now() + timedelta(days=10))

    class Meta:
        verbose_name = 'Брони'
        verbose_name_plural = 'Бронь'

    def __str__(self):
        return str(self.payment)

    def get_product_image(self):
        if self.specification:
            image = self.specification.get_image()
            return '/media/'+str(image)
        return ""
        
    def get_product_price(self):
        price = self.specification.price
        return price

    def get_product_converted_price(self):
        return convertCurrency(self.get_product_price())


class Transaction(models.Model):
    transaction_id = models.CharField(
        'Номер транзакции', max_length=200, null=True, blank=True)
    ip = models.CharField('IP клиента', max_length=200, null=True, blank=True)
    option = models.CharField('Оплата через', max_length=200, null=True, blank=True)
    reserve = models.ForeignKey(Reserve, null=True, blank=True, on_delete=models.SET_NULL, related_name='reserve')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name='purchase')
    to = models.CharField('Для оплаты в', max_length=200, null=True, blank=True)
    status = models.CharField('Статус', max_length=200, null=True, blank=True)
    payment = models.FloatField('Оплачено', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return str(self.ip)


class AboutUs(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    img = models.ImageField('Изображение', null=True, blank=True, upload_to="about_us_page")

    first_title = models.CharField('Заголовок первого блока', null=True, blank=True, max_length=600)
    first_desc = models.CharField('Описание', null=True, blank=True, max_length=600)
    first_img = models.ImageField('Изображение', null=True, blank=True, upload_to="about_us_page")

    second_title = models.CharField('Заголовок второго блока', null=True, blank=True, max_length=600)
    second_desc = models.CharField('Описание', null=True, blank=True, max_length=600)
    second_img = models.ImageField('Изображение', null=True, blank=True, upload_to="about_us_page")

    third_title = models.CharField('Заголовок третьего блока', null=True, blank=True, max_length=600)
    third_desc = models.CharField('Описание', null=True, blank=True, max_length=600)
    third_img = models.ImageField('Изображение', null=True, blank=True, upload_to="about_us_page")

    fourth_title = models.CharField('Заголовок четвертого блока', null=True, blank=True, max_length=600)
    fourth_desc = models.CharField('Описание', null=True, blank=True, max_length=600)
    fourth_img = models.ImageField('Изображение', null=True, blank=True, upload_to="about_us_page")

    shirt_title = models.CharField('Дополнительный заголовок', null=True, blank=True, max_length=600)
    description = models.TextField('Дополнительное описание', null=True, blank=True)

    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Страница о нас'
        verbose_name_plural = 'Страница о нас'

    def __str__(self):
        return str(self.title)


class Warranty(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    description = models.TextField('Контент', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Страница гарантии'
        verbose_name_plural = 'Страница гарантии'

    def __str__(self):
        return str(self.title)


class WhyUs(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    description = models.TextField('Контент', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Страница Почему iStore'
        verbose_name_plural = 'Страница Почему iStore'

    def __str__(self):
        return str(self.title)


class Contacts(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    desc = models.TextField('Описание', null=True, blank=True)
    contact = models.CharField(
        'Контакты', null=True, blank=True, max_length=600)
    form = models.CharField('Форма обратной связи', null=True, blank=True, max_length=600)
    phone = models.CharField('Номера', null=True, blank=True, max_length=600)
    email = models.CharField('Почта', null=True, blank=True, max_length=600)
    schedule = models.CharField('График', null=True, blank=True, max_length=600)
    socials = models.CharField('Соц сети', null=True, blank=True, max_length=600)
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return str(self.pub_date)

class Footer(models.Model):
    description = models.TextField('Контент', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Футер'
        verbose_name_plural = 'Футер'

    def __str__(self):
        return str(self.pub_date)

class TradeIn(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    description = models.TextField('Контент', null=True, blank=True)
    category = models.IntegerField('TradeIn', null=True, blank=True, choices=tradeIn)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Страница TradeIn'
        verbose_name_plural = 'Страница TradeIn'

    def __str__(self):
        return str(self.title)


class LoanPage(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    title_2 = models.CharField('Описание', null=True, blank=True, max_length=600)
    text_1 = models.CharField('Условия банка', null=True, blank=True, max_length=600)
    text_2 = models.CharField('Сумма', null=True, blank=True, max_length=600)
    text_3 = models.CharField('Поручитель', null=True, blank=True, max_length=600)
    text_4 = models.CharField('Поручителья нет', null=True, blank=True, max_length=600)
    text_5 = models.CharField('Поручителья есть', null=True, blank=True, max_length=600)
    text_6 = models.CharField('Первоначальный взнос', null=True, blank=True, max_length=600)
    text_7 = models.CharField('Сроки кредитования', null=True, blank=True, max_length=600)
    text_8 = models.CharField('Сроки рассмотрения заявки', null=True, blank=True, max_length=600)
    text_9 = models.CharField('Погашение', null=True, blank=True, max_length=600)
    text_10 = models.CharField('Рассчитать кредит', null=True, blank=True, max_length=600)
    text_11 = models.CharField('Цена устройство', null=True, blank=True, max_length=600)
    text_12 = models.CharField('Выбрать банк', null=True, blank=True, max_length=600)
    text_13 = models.CharField('Срок', null=True, blank=True, max_length=600)
    text_14 = models.CharField('Процент', null=True, blank=True, max_length=600)
    text_15 = models.CharField('Первоначальный взнос', null=True, blank=True, max_length=600)
    text_16 = models.CharField('Результаты расчета', null=True, blank=True, max_length=600)
    text_17 = models.CharField('Сумма кредита:', null=True, blank=True, max_length=600)
    text_18 = models.CharField('Первоначальный взнос:', null=True, blank=True, max_length=600)
    text_19 = models.CharField('Срок кредита:', null=True, blank=True, max_length=600)
    text_20 = models.CharField('Ежемесячный платеж:', null=True, blank=True, max_length=600)
    text_21 = models.CharField('Общая выплата:', null=True, blank=True, max_length=600)
    text_22 = models.CharField('Необходимые документы', null=True, blank=True, max_length=600)
    text_23 = models.CharField('Оформление кредита в нашем офисе', null=True, blank=True, max_length=600)
    text_24 = models.CharField('Выберите опцию', null=True, blank=True, max_length=600)
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Страница оформление в кредит'
        verbose_name_plural = 'Страница оформление в кредит'

    def __str__(self):
        return str(self.title)

class AdditionalCategory(models.Model):
    name = models.CharField('Название', null=True, blank=True, max_length=255)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to="category")
    slug_name = models.CharField(
        'Ссылка', null=True, blank=True, max_length=255, unique=True)
    main_category = models.CharField(
        'Категория', null=True, max_length=120, choices=additional_categories)
    active = models.BooleanField('Включить', default=False)
    
    class Meta:
        verbose_name = 'Доп Категорий'
        verbose_name_plural = 'Доп Категории'

    def __str__(self):
        return str(self.name)
        
class Category(models.Model):
    mac = models.ImageField('Mac изображение', null=True, blank=True, upload_to="category")
    mac_title = models.TextField('Mac название', null=True, blank=True)
    iphone = models.ImageField('iPhone изображение', null=True, blank=True, upload_to="category")
    iphone_title = models.TextField('iPhone название', null=True, blank=True)
    ipad = models.ImageField('iPad изображение', null=True, blank=True, upload_to="category")
    ipad_title = models.TextField('iPad название', null=True, blank=True)
    watch = models.ImageField('Watch изображение', null=True, blank=True, upload_to="category")
    watch_title = models.TextField('Watch название', null=True, blank=True)
    accessory = models.ImageField('Аксессуары изображение', null=True, blank=True, upload_to="category")
    accessory_title = models.TextField('Аксессуары название', null=True, blank=True)
    gadget = models.ImageField('Гаджеты изображение', null=True, blank=True, upload_to="category")
    gadget_title = models.TextField('Гаджеты название', null=True, blank=True)
    trade_iphone = models.ImageField('Trade - in iPhone изображение', null=True, blank=True, upload_to="category")
    trade_iphone_title = models.TextField('Trade - in iPhone название', null=True, blank=True)
    trade_ipad = models.ImageField('Trade - in iPad изображение', null=True, blank=True, upload_to="category")
    trade_ipad_title = models.TextField('Trade - in iPad название', null=True, blank=True)
    trade_mac = models.ImageField('Trade - in MacBook изображение', null=True, blank=True, upload_to="category")
    trade_mac_title = models.TextField('Trade - in MacBook название', null=True, blank=True)
    trade_watch = models.ImageField('Trade - in Apple Watch изображение', null=True, blank=True, upload_to="category")
    trade_watch_title = models.TextField('Trade - in Apple Watch название', null=True, blank=True)
    trade_another = models.ImageField('Trade - in Разное изображение', null=True, blank=True, upload_to="category")
    trade_another_title = models.TextField('Trade - in Разное название', null=True, blank=True)
    pub_date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Изображение Категории'
        verbose_name_plural = 'Изображение Категорий'

    def __str__(self):
        return str(self.pub_date)


class MainPageSlider(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    desktop_image = models.ImageField('Изображение для мобильных устройств', null=True, blank=True, upload_to="mainpageslider")
    mobile_image = models.ImageField(
        'Изображение', null=True, blank=True, upload_to="mainpageslider")
    link = models.CharField('Ссылка', null=True, blank=True, max_length=256)
    category = models.CharField('Категория', null=True, blank=True, max_length=30, choices=slider_choices)
    background = ColorField('Бэкграунд', default='#000000')
    pub_date = models.DateTimeField('Дата', default=timezone.now)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'

    def __str__(self):
        return str(self.title)


class Compare(models.Model):
    title = models.CharField('Название', null=True, blank=True, max_length=600)
    order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        verbose_name = 'Сравнение'
        verbose_name_plural = 'Сравнения'

    def __str__(self):
        return str(self.title)


class CompareProducts(models.Model):
    order = models.IntegerField('Порядок', null=True, blank=True)
    compare = models.ForeignKey(
        Compare, null=True, blank=True, on_delete=models.CASCADE, related_name='compare_product')
    product = models.ForeignKey(Product, verbose_name='Товар', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Сравнение'
        verbose_name_plural = 'Сравнения'

    def __str__(self):
        return str(self.order)
