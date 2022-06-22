from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images') # TODO: location of bucket for photos
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
