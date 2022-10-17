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


def checkout(request):
    #TODO: need to get user id
    products = [{
        'id': p.id,
        'name': p.name,
        'image': p.image,
        'price': p.price,
        'description': p.description
    } for p in Product.objects.all()]
    step = 3  # max number of products in a row
    chunks = []
    for i in range(0, len(products), step):
        x = i
        chunks.append(products[x:x + step])

    return render(request, 'products/checkout.html', context={'products': chunks})