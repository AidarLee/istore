from django import template
from products.models import Color
register = template.Library()

additional_categories = {'Доп Аксессуары 1':'accessory_1_title', 'Доп Аксессуары 2':'accessory_2_title', 'Доп Аксессуары 3':'accessory_3_title', 'Доп Аксессуары 4':'accessory_4_title', 'Доп Аксессуары 5':'accessory_5_title', 'Доп Гаджеты 1':'gadget_1_title',
                         'Доп Гаджеты 2':'gadget_2_title', 'Доп Гаджеты 3':'gadget_3_title', 'Доп Гаджеты 4':'gadget_4_title', 'Доп Гаджеты 5':'gadget_5_title'}
@register.filter
def get_color_name(value):
    return value.name


@register.filter
def get_category_name(value, categories):
    if categories:
        categories = categories.__dict__
        if value in additional_categories:
            value = categories[additional_categories[value]]
    return value
