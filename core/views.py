from django.shortcuts import render
from products.models import Product
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from pprint import pprint
from ledger.models import TacoBank


def bank_account(user):
    return TacoBank.objects.get_or_create(user=user)[0]


def index(request):
    avail_products = Product.objects.annotate(attr_stock=Sum('attribute_stock__stock')).filter(Q(general_stock__gte = 1) | Q(attr_stock__gte = 1))
    if request.GET.get('include_out_of_stock'):
        avail_products = Product.objects.all()
    products = [{
        'id': p.id,
        'name': p.name,
        'image': p.image,
        'price': p.price,
        'description': p.description
    } for p in avail_products]
    step = 3  # max number of products in a row
    chunks = []
    for i in range(0, len(products), step):
        x = i
        chunks.append(products[x:x + step])

    if request.user.is_authenticated:
        account = bank_account(request.user)
        context = {
            'taco_balance': account.total_tacos if request.user.is_authenticated else 0,
            'products': chunks,
            'user': request.user
        }
    else:
        context = {
            'taco_balance': 0,
            'products': chunks,
            'user': request.user
        }
    return render(request, 'products/base_index.html', context=context)
