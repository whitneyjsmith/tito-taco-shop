from django.contrib import admin

from .models import Product, Attribute, AttributeBase

admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(AttributeBase)
