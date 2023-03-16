from .models import *
from user.models import User
from datetime import date
from django.conf import settings
from products.models import *


def record_transaction(data):
    """
    Record taco transactions.
    """
    giver = data.get('giver_id')
    tacos_given_today = TacoLedger.objects.filter(giver=giver, timestamp__date=date.today().day).aggregate(Sum('amount'))
    transaction_amount = data.get('tacos')
    daily_limit = settings.TACO_DAILY_LIMIT
    if tacos_given_today >= daily_limit:
        return (False, 'Daily Limit reached')
    if tacos_given_today + transaction_amount > daily_limit:
        return (False, 'Not enough tacos to give')
    try:
        TacoLedger.objects.create(
            amount=transaction_amount,
            receiver=data.get('receiver_id'),
            giver=giver
        )
    except Exception as e:
        print(f'Error occurred in the Taco Ledger! {e}')
        return (False, 'Transaction Error')
    return (True, 'Transaction completed')


def purchase_item(item):
    """
    Call the chat integration.
    """
    pass


def redeem_tacos(data):
    """
    Redeem tacos by giving them to Tito.
    """
    user = User.objects.get(unique_id=data.get('user_id'))
    bank_account = TacoBank.objects.get(user=user)
    item = Product.objects.get(name=data.get('product_name'))
    if bank_account.total_tacos >= item.price:
        TacoLedger.objects.create(
            giver=data.get('user_id'),
            receiver=settings.SLACK_BOT_ID,
            amount=data.get('amount')
        )
        purchase_item(item)
        return (True, 'Transaction complete')
    return (False, 'Not enough tacos to buy item')

