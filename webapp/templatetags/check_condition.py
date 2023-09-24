from django import template
from django.forms.models import model_to_dict
import json
register = template.Library()


@register.filter
def check_condition(value):
    for index, val in value:
        if index == 0:
            return True
    return False


@register.filter
def get_keys(value):
    data = list(value)
    if value:
        return data
    return []


@register.filter
def get_values(value):
    if value:
        return list(value.values())
    return []


@register.filter
def first_key_value(value):
    items = []
    for index, val in enumerate(value.values()):
        if not index:
            return val
    return items


@register.filter
def get_by_key(value, arg):
    return value[arg]


@register.filter
def get_enumerated(value):
    item = []
    if value:
        item = enumerate(value)
    return item


@register.filter
def hasnt_none_val(value):
    bool = True
    for val in value:
        if val == 'None':
            bool = False
            break
    return bool


@register.filter
def plus(value, arg):
    return value + arg


@register.filter
def jsonify(value):
    return json.dumps(value)


@register.filter
def unique_color(specifics):
    data = []
    for specific in specifics:
        if(specific.color_hex not in data):
            data.append(specific.color_hex)
    return data


@register.filter
def unique_capacity(specifics):
    data = []
    for specific in specifics:
        if(specific.capacity not in data):
            if specific.capacity:
                data.append(specific.capacity)
    return data


@register.filter
def unique_keyboard(specifics):
    data = []
    for specific in specifics:
        if(specific.keyboard not in data):
            if specific.keyboard:
                data.append(specific.keyboard)
    return data


@register.filter
def unique_caseSize(specifics):
    data = []
    for specific in specifics:
        if(specific.caseSize not in data):
            if specific.caseSize:
                data.append(specific.caseSize)
    return data


@register.filter
def unique_connectivity(specifics):
    data = []
    for specific in specifics:
        if(specific.connectivity not in data):
            if specific.connectivity:
                data.append(specific.connectivity)
    return data


@register.filter
def unique_ram(specifics):
    data = []
    for specific in specifics:
        if(specific.ram not in data):
            if specific.ram:
                data.append(specific.ram)
    return data

@register.filter
def unique_cpu(specifics):
    data = []
    for specific in specifics:
        if(specific.cpu not in data):
            if specific.cpu:
                data.append(specific.cpu)
    return data


@register.filter
def unique_edition(specifics):
    data = []
    for specific in specifics:
        if(specific.edition not in data):
            if specific.edition:
                data.append(specific.edition)
    return data


@register.filter
def unique_pattern(specifics):
    data = []
    for specific in specifics:
        if(specific.pattern not in data):
            if specific.pattern:
                data.append(specific.pattern)
    return data


@register.filter
def filter_by_category(value, arg):
    filtered = []
    for val in value:
        if val.category == arg:
            filtered.append(val)
    return filtered
