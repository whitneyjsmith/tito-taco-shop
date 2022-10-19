from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product


def product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    return render(request, 'products/base_product.html', {'product': product})


def get_image(request, product_id, filename):
    print(f"GETTING IMAGE: {filename}")
    product = Product.objects.get(id=product_id)
    image_data = product.image.open()
    return HttpResponse(image_data, content_type="image/gif")


def checkout(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    return render(request, 'products/checkout.html', context={'product': product})