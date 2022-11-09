from django.shortcuts import render
from products.models import Product
from django.http import HttpResponse
from pprint import pprint


def index(request):
    products = [{
        'id': p.id,
        'name': p.name,
        'image': p.image,
        'price': p.price,
        'description': p.description
    } for p in Product.objects.all()]
    step = 3 # max number of products in a row
    chunks = []
    for i in range(0, len(products), step):
        x = i
        chunks.append(products[x:x + step])
    pprint(request.user.is_authenticated)
    
    return render(request, 'products/base_index.html', context={'products': chunks, 'user': request.user})



