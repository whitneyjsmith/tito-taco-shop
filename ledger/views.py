from rest_framework.response import Response
from .tasks import *


def transaction(request):
    result = record_transaction(request.data)
    status = 200 if result[0] else 400
    return Response(
        status=status,
        data={'message': result[1]}
    )


def redeem(request):
    result = redeem_tacos(request.data)
    status = 200 if result[0] else 400
    return Response(
        status=status,
        data={'message': result[1]}
    )
