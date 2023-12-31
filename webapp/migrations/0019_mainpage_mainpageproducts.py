# Generated by Django 3.1.1 on 2020-10-12 17:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_auto_20201012_1429'),
        ('webapp', '0018_auto_20201012_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_product_title', models.CharField(max_length=400, verbose_name='Название главного продукта')),
                ('main_product_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('main_product_img', models.ImageField(upload_to='main_page', verbose_name='Изображение')),
                ('main_product_img_mobile', models.ImageField(upload_to='main_page', verbose_name='Мобильное изображение')),
                ('sale_product_title', models.CharField(max_length=400, verbose_name='Название акционого продукт')),
                ('sale_product_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('sale_product_img', models.ImageField(upload_to='main_page', verbose_name='Изображение')),
                ('sale_product_img_mobile', models.ImageField(upload_to='main_page', verbose_name='Мобильное изображение')),
                ('second_product_title', models.CharField(max_length=400, verbose_name='Название продукта')),
                ('second_product_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('second_product_img', models.ImageField(upload_to='main_page', verbose_name='Изображение')),
                ('second_product_img_mobile', models.ImageField(upload_to='main_page', verbose_name='Мобильное изображение')),
                ('fifth_block_title', models.CharField(max_length=400, verbose_name='Название пятого блока')),
                ('fifth_block_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('fifth_block_link', models.CharField(max_length=400, verbose_name='Сылка')),
                ('fifth_block_category', models.CharField(choices=[('iphone', 'iPhone '), ('macBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'), ('apple-watch', 'Apple Watch')], max_length=20, null=True, verbose_name='Категория')),
                ('sixth_block_title', models.CharField(max_length=400, verbose_name='Название шестого блока')),
                ('sixth_block_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('sixth_block_link', models.CharField(max_length=400, verbose_name='Сылка')),
                ('sixth_block_category', models.CharField(choices=[('iphone', 'iPhone '), ('macBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'), ('apple-watch', 'Apple Watch')], max_length=20, null=True, verbose_name='Категория')),
                ('seventh_block_title', models.CharField(max_length=400, verbose_name='Название седьмого блока')),
                ('seventh_block_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('seventh_block_link', models.CharField(max_length=400, verbose_name='Сылка')),
                ('first_service_title', models.CharField(max_length=400, verbose_name='Первый сервис')),
                ('first_service_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('first_service_link', models.CharField(max_length=400, verbose_name='Сылка')),
                ('first_service_img', models.ImageField(upload_to='main_page', verbose_name='Изображение')),
                ('second_service_title', models.CharField(max_length=400, verbose_name='Второй сервис')),
                ('second_service_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('second_service_link', models.CharField(max_length=400, verbose_name='Сылка')),
                ('second_service_img', models.ImageField(upload_to='main_page', verbose_name='Изображение')),
                ('news_title', models.CharField(max_length=400, verbose_name='Второй сервис')),
                ('news_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_product', to='products.product')),
                ('sale_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_product', to='products.product')),
                ('second_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_product', to='products.product')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главная страница',
            },
        ),
        migrations.CreateModel(
            name='MainPageProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=400, verbose_name='Название')),
                ('product_desc', models.CharField(max_length=400, verbose_name='Описание')),
                ('product_img', models.ImageField(upload_to='main_page', verbose_name='Изображение')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_product', to='webapp.mainpage')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_page_product', to='products.product')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
