from django.db import models
from django.db.models import Sum
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
        return f'{self.attribute_base.name} - {self.value}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    attributes = models.ManyToManyField(Attribute, through='ProductAttributeStock')
    general_stock = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        stock_sum = self.attribute_stock.filter(attribute__attribute_base__name = 'Size', stock__gte = 1).aggregate(Sum('stock'))['stock__sum']
        return stock_sum if stock_sum else self.general_stock or 0


class ProductAttributeStock(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='product_stock')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_stock')
    stock = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.product.name}:{self.attribute}:{self.stock}"


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    used = models.IntegerField(default=0)
    usage_limit = models.IntegerField(blank=True, null=True, default=None)
    expiry_date = models.DateTimeField(blank=True, null=True)
    assigned_products = models.ManyToManyField(Product)
    assigned_attributes = models.ManyToManyField(AttributeBase)

    def __str__(self):
        return f'{self.code}: ({self.used}{"/"+self.usage_limit if self.usage_limit else ""})'


class Category(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.category


class Quote(models.Model):
    category = models.ManyToManyField(Category, null=True, blank=True)
    quote = models.CharField(max_length=1000)

    def __str__(self):
        return self.quote
