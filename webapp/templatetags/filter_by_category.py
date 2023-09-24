from django import template

register = template.Library()

@register.filter
def filter_by_category(value, arg):
    filtered = []
    for val in value:
        if val.category == arg:
            filtered.append(val)
    return filtered
@register.filter
def product_by_category(value, arg):
    filtered = []
    for val in value:
        if val.product_category == arg:
            filtered.append(val)
    return filtered

@register.filter
def get_specific_elements(value, arg):
    filtered = []
    if value:
        filtered = value[0:arg]
    return filtered
