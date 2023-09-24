from django import template
import json

register = template.Library()


@register.filter(name='range')
def make_range(start, end):
    return range(start, end + 1)


@register.filter(name='month_correct')
def month_correct(start):
    if start == 1 or start == 21: 
        return 'месяц'
    elif start < 5:
        return 'месяца'
    elif start < 21:
        return 'месяцев'
    else:
        return 'месяца'
@register.filter(name='add_percent')
def add_percent(value, arg):
    value += value * (arg / 100)
    return value


@register.filter(name='online_offline')
def online_offline(value):
    classes = ''
    if value:
        classes = 'online'
    else:
        classes = 'offline'
    return classes
