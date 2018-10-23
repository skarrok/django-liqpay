from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from liqpay import LiqPay

from . import settings
from .forms import CallbackForm
from .models import LiqPayOrder
from .signals import result_received


@csrf_exempt
@require_POST
def liqpay_callback(request):

    form = CallbackForm(request.POST or None)
    if not form.is_valid():
        return HttpResponse(status=400)

    data = form.cleaned_data['data']
    signature = form.cleaned_data['signature']

    liqpay = LiqPay(settings.PUBLIC_KEY, settings.PRIVATE_KEY)
    our_sign = liqpay.str_to_sign(settings.PRIVATE_KEY + data +
                                  settings.PRIVATE_KEY)

    if signature != our_sign:
        return HttpResponse(status=400)

    data = liqpay.decode_data_from_str(data)

    status = data['status']
    if status != 'success':
        return HttpResponse(status=400)

    try:
        order = LiqPayOrder.objects.get(order_id=data['order_id'])
    except LiqPayOrder.DoesNotExist:
        return HttpResponse(status=400)

    result_received.send(
        sender=order,
        order_id=order.id,
        amount=data['amount'],
        currency=data['currency'],
    )

    return HttpResponse('OK', status=200)
