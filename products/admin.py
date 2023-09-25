from easy_select2 import select2_modelform, select2_modelform_meta, apply_select2
from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from django.utils.safestring import mark_safe
from nested_admin import NestedTabularInline
from .models import *
from django.utils.translation import gettext_lazy as _
from django import forms
import nested_admin
from .fields import MultipleFilesField
from .widgets import ClearableMultipleFilesInput

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImagesFieldForm(forms.Form):
    images = MultipleFileInput()
def make_formalized(Order, request, queryset):
    for query in queryset:
        if (query.formalized):
            query.formalized = False
        else:
            query.formalized = True
        query.save()


make_formalized.short_description = "Пометить как оформлен или не оформлен"


def make_active(Product, request, queryset):
    for query in queryset:
        if (query.active):
            query.active = False
        else:
            query.active = True
        query.save()


make_active.short_description = "Показать либо скрыть"


class ImageAdmin(nested_admin.NestedStackedInline):
    fields = [ 'image', 'preview']
    model = Image
    extra = 1
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="200">')

    def queryset(self):
        return Color.objects.all()


ProductSpecificationAdminForm = select2_modelform(
    ProductSpecification, attrs={'width': '200px'})
class ProductSpecificationAdmin(nested_admin.NestedStackedInline):
    form = ProductSpecificationAdminForm
    model = ProductSpecification
    extra = 1
    readonly_fields = ["is_valid"]
    inlines = [ImageAdmin]

    def queryset(self):
        return Capacity.objects.all()


class AdditionalSpecificationAdmin(NestedTabularInline):
    model = AdditionalSpecification
    extra = 0


RecommendedAdminForm = select2_modelform(Recommended, attrs={'width': '250px'})
class RecommendedAdmin(NestedTabularInline):
    form = RecommendedAdminForm
    model = Recommended
    extra = 1
    fk_name = "recommended"

    def queryset(self):
        return Product.objects.all()


KeyboardAdminForm = select2_modelform(Keyboard, attrs={'width': '200px'})
class KeyboardAdmin(admin.ModelAdmin):
    form = KeyboardAdminForm
    model = Keyboard
    extra = 1

CaseSizeAdminForm = select2_modelform(CaseSize, attrs={'width': '200px'})
class CaseSizeAdmin(admin.ModelAdmin):
    form = CaseSizeAdminForm
    model = CaseSize


ConnectivityAdminForm = select2_modelform(Connectivity, attrs={'width': '200px'})
class ConnectivityAdmin(admin.ModelAdmin):
    form = ConnectivityAdminForm
    model = Connectivity


RAMAdminForm = select2_modelform(RAM, attrs={'width': '200px'})
class RAMAdmin(admin.ModelAdmin):
    form = RAMAdminForm
    model = RAM


CPUAdminForm = select2_modelform(CPU, attrs={'width': '200px'})
class CPUAdmin(admin.ModelAdmin):
    form = CPUAdminForm
    model = CPU


EditionAdminForm = select2_modelform(Edition, attrs={'width': '200px'})
class EditionAdmin(admin.ModelAdmin):
    form = EditionAdminForm
    model = Edition

PatternAdminForm = select2_modelform(Pattern, attrs={'width': '200px'})
class PatternAdmin(admin.ModelAdmin):
    form = PatternAdminForm
    model = Pattern


class MainSpecificationAdmin(NestedTabularInline):
    model = MainSpecification
    extra = 1


class ModuleAdmin(NestedTabularInline):
    model = Module
    extra = 0


class SpecificationListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Спецификации')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'productSpecifiation'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('with', _('Товары с синхронизацией')),
            ('without', _('Товары без синхронизации')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'with':
            return queryset.exclude(specification__is_active=False)
        if self.value() == 'without':
            return queryset.exclude(specification__is_active=True)


ProductAdminForm = select2_modelform(Product, attrs={'width': '200px'})
class ProductAdmin(nested_admin.NestedModelAdmin):
    form = ProductAdminForm
    change_list_template = 'admin/products/product/change_list.html'
    list_display = (
        'title', 'product_category', 'pub_date', 'price', 'quantity', 'capacity', 'color','active','order')
    readonly_fields = ['title', 'short_desc', 'price', 'quantity', 'capacity', 'color' ]
    inlines = [MainSpecificationAdmin, ProductSpecificationAdmin, AdditionalSpecificationAdmin,
               RecommendedAdmin]
    list_filter = ['pub_date', 'product_category',
                   SpecificationListFilter, 'in_trade']
    search_fields = ['product_title']
    actions = [make_active]

    class Media:
        css = {
            'all': ("css/admin.css",)
        }

        js = ("js/admin.js",)

    def title(self, obj):
        name = obj.product_title
        if len(name) > 30:
            return name[:30] + '...'
        else:
            return name

    def short_desc(self, obj):
        name = obj.product_description
        if name:
            if len(name) > 30:
                return name[:30] + '...'
            else:
                return name

        return name

    def price(self, obj):
        prices = ''
        for specific in obj.specification.all():
            if (prices):
                prices = prices + ',' + str(specific.price)
            else:
                prices = prices + str(specific.price)

        return prices

    def quantity(self, obj):
        quantities = ''
        for specific in obj.specification.all():
            if (quantities):
                quantities = quantities + ',' + str(specific.quantity)
            else:
                quantities = quantities + str(specific.quantity)

        return quantities

    def capacity(self, obj):
        capacities = ''
        for specific in obj.specification.all():
            if (specific.capacity):
                if (capacities):
                    capacities = capacities + ',' + str(specific.capacity)
                else:
                    capacities = capacities + str(specific.capacity)

        return capacities

    def color(self, obj):
        prices = ''
        for specific in obj.specification.all():
            if specific.color_hex:
                if (prices):
                    prices = prices + ',' + str(specific.color_hex)
                else:
                    prices = prices + str(specific.color_hex)

        return prices

    title.short_description = "Название"
    short_desc.short_description = "Короткое описание"
    price.short_description = "Цены"
    quantity.short_description = "Колличество"
    capacity.short_description = "Ёмкость"
    color.short_description = "Цвет"


class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_word', 'percent')
    model = Promocode


OrderProductAdminForm = select2_modelform(
    OrderProduct, attrs={'width': '200px'})
class OrderProductAdmin(admin.TabularInline):
    form = OrderProductAdminForm
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('phone','delivery', 'address', 'payment_option', 'payment', 'formalized', 'promo_name', 'promo', 'created_at')
    model = Order
    # readonly_fields = ["phone"]
    inlines = [OrderProductAdmin]
    actions = [make_formalized]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'phone')
        return self.readonly_fields

    # def user_name(self, obj):
    #     return obj.user.name

    def phone(self, obj):
        return obj.user.phone

    # user_name.short_description = "Пользователь"
    phone.short_description = "Телефон"


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'img')
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Capacity)
admin.site.register(Keyboard, KeyboardAdmin)
admin.site.register(CaseSize, CaseSizeAdmin)
admin.site.register(Connectivity, ConnectivityAdmin)
admin.site.register(RAM, RAMAdmin)
admin.site.register(CPU, CPUAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Promocode, PromocodeAdmin)
admin.site.register(Order, OrderAdmin)
