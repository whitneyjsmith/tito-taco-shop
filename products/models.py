from django.db import models
from django.core.files.storage import default_storage


class AttributeBase(models.Model):
    name = models.CharField(max_length=75)


class Attribute(models.Model):
    value = models.CharField(max_length=75)
    internal_value = models.CharField(max_length=75)
    attribute_base = models.ForeignKey(AttributeBase, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    attributes = models.ManyToManyField(Attribute) # perhaps get rid of this?
    attribute_bases = models.ManyToManyField(AttributeBase)
