from django.db import models
from django.core.files.storage import default_storage


class AttributeBase(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    value = models.CharField(max_length=75)
    internal_value = models.CharField(max_length=75)
    attribute_base = models.ForeignKey(AttributeBase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attribute_base.name} - {self.value}


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    attributes = models.ManyToManyField(Attribute, through='ProductAttributeStock')
    attribute_stock

    def __str__(self):
        return self.name


class ProductAttributeStock(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.product.name}:{self.attribute}:{self.stock}"


class Category(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.category


class Quote(models.Model):
    category = models.ManyToManyField(Category, null=True, blank=True)
    quote = models.CharField(max_length=1000)

    def __str__(self):
        return self.quote
