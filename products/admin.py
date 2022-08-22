from django.contrib import admin

from .models import Product, Attribute, AttributeBase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_vertical = ('attributes',)


admin.site.register(Attribute)
admin.site.register(AttributeBase)
