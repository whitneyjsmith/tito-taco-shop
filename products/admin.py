from django.contrib import admin

from .models import Product, Attribute, AttributeBase, ProductAttributeStock


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttributeStock
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_vertical = ('attributes',)
    inlines = (ProductAttributeInline, )


admin.site.register(Attribute)
admin.site.register(AttributeBase)
