from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
from ledger.tasks import redeem_tacos
from integration.clients.slack import Client as Slack
from integration.models import Team
from django.conf import settings


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
    print(f"REQUEST POST: {request.POST}")
    redeem_tacos({"user_id": request.user.unique_id, "product_name": product.name})
    team_obj = Team.objects.first()
    slack_client = Slack("T1DM32N0P", "Monumetric", "xoxb-251031683808-Cz0bVgRM4537MdPvsynKAQ6d")
    user = request.user
    slack_client.order_information(user.unique_id, settings.ORDER_CHANNEL, product.name)
    slack_client.receipt(user.unique_id, product.name, product.price, user.taco_bank_set.first().total_tacos)
    return render(request, 'products/checkout.html', context={'product': product})
