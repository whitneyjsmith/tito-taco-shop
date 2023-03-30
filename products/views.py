from django.shortcuts import render
from django.http import HttpResponse

from ledger.models import TacoBank
from products.models import Product
from ledger.tasks import redeem_tacos, TacoBank
from integration.clients.slack import Client as Slack
from integration.models import Team
from django.conf import settings
from django.contrib import messages


def product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    context = {'product': product, 'user': request.user,
               'day_limit': settings.MAX_PURCHASES_PER_DAY}
    if request.user.is_authenticated:
        account = TacoBank.objects.filter(user=request.user).first()
        context['taco_balance'] = account.total_tacos
        context['purchases_today'] = account.total_purchases_today
        context['display_spend_warning'] = context['day_limit'] is not None and account.total_purchases_today >= context['day_limit']
    else:
        context['taco_balance'] = context['day_limit'] = context['display_spend_warning'] = 0
    return render(request, 'products/base_product.html', context)


def get_image(request, product_id, filename):
    print(f"GETTING IMAGE: {filename}")
    product = Product.objects.get(id=product_id)
    image_data = product.image.open()
    return HttpResponse(image_data, content_type="image/gif")


def checkout(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    context = {'product': product,
               'user': request.user,
               'day_limit': settings.MAX_PURCHASES_PER_DAY}
    if request.user.is_authenticated:
        account = TacoBank.objects.filter(user=request.user).first()
        context['taco_balance'] = account.total_tacos
        context['purchases_today'] = account.total_purchases_today
        context['display_spend_warning'] = context['day_limit'] is not None and account.total_purchases_today >= context['day_limit']
    else:
        context['taco_balance'] = context['day_limit'] = context['display_spend_warning'] = 0
    return render(request, 'products/checkout.html',
                  context=context)


def checkout_button(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    slack_client = Slack(settings.TEAM_ID, settings.TEAM_NAME, settings.SLACK_BOT_TOKEN)
    user = request.user
    taco_bank = TacoBank.objects.filter(user=user)
    total_tacos = taco_bank.first().total_tacos
    if total_tacos >= product.price:
        redeem_tacos({"user_id": request.user.unique_id, "product_name": product.name, "amount": product.price})
        slack_client.order_information(user.unique_id, settings.ORDER_CHANNEL, product.name)
        slack_client.receipt(user.unique_id, product.name, product.price, total_tacos)
    else:
        messages.error(request, "Insufficient taco balance.")
        return render(request, 'products/checkout.html', context={'product': product})
    return render(request, 'products/base_index.html', context={'product': product})
