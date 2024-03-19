from django.contrib import admin
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse

from network.models import NetworkObject, Product


admin.site.register(Product)


@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    list_display = [f.name for f in NetworkObject._meta.fields] \
                   + ['supplier_link', 'products']
    readonly_fields = ('supplier_link',)
    list_filter = ('city',)
    search_fields = ('city',)
    actions = ['set_null_debt']

    @admin.action(description='Обнулить долг перед поставщиком '
                              'у выбранных объектов')
    def set_null_debt(self, request, queryset):
        queryset.update(debt=0)

    def supplier_link(self, obj):
        if obj.supplier:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse('admin:network_networkobject_change',
                        args=(obj.supplier.pk,)),
                obj.supplier)
            )
        else:
            return None

    supplier_link.allow_tags = True
    supplier_link.admin_order_field = 'supplier'
    supplier_link.short_description = 'ссылка на поставщика'

    def products(self, obj):
        if obj.supplier:
            return [product.product_name for product in obj.products]
        else:
            return None

    products.short_description = 'Товары поставщика'
