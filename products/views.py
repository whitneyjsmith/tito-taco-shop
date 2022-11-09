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
    redeem_tacos(request)
    team_obj = Team.objects.first()
    slack_client = Slack(team_obj.team_id, team_obj.name, team_obj.bot_user_id)
    user = request.user
    slack_client.order_information(user.unique_id, settings.ORDER_ID, product.name)
    slack_client.receipt(user.unique_id, product.name, product.price, user.taco_bank_set.first().total_tacos)
    return render(request, 'products/checkout.html', context={'product': product})
