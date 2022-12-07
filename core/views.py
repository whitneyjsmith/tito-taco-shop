from django.shortcuts import render
from products.models import Product
from django.http import HttpResponse
from pprint import pprint
from ledger.models import TacoBank


def bank_account(user):
    return TacoBank.objects.filter(user=user).first()


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
    
    account = bank_account(request.user)
    context = {
        'taco_balance': account.total_tacos,
        'products': chunks,
        'user': request.user
    }
    return render(request, 'products/base_index.html', context=context)
