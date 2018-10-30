import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from liqpay import LiqPay

from . import settings
from .forms import CallbackForm
from .models import LiqPayOrder
from .signals import result_received

logger = logging.getLogger('liqpay')


@csrf_exempt
@require_POST
def liqpay_callback(request):

    form = CallbackForm(request.POST or None)
    if not form.is_valid():
        logger.info('Invalid callback form, POST: {}'.format(request.POST))
        return HttpResponse(status=400)

    data = form.cleaned_data['data']
    signature = form.cleaned_data['signature']

    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    our_sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data +
                                  settings.LIQPAY_PRIVATE_KEY)

    if signature != our_sign:
        logger.info('Invalid signature: our {}!={}'.format(
            our_sign, signature))
        return HttpResponse(status=400)

    data = liqpay.decode_data_from_str(data)

    status = data.get('status')
    if status not in ('success', 'sandbox'):
        logger.info('Status: {} {} {} {}'.format(status, data.get('err_code'),
                                                 data.get('err_description'),
                                                 data))
        return HttpResponse(status=400)

    try:
        order = LiqPayOrder.objects.get(order_id=data['order_id'])
    except LiqPayOrder.DoesNotExist:
        logger.info('Wrong order_id: {}'.format(data['order_id']))
        return HttpResponse(status=400)

    logger.info('Payment status={}: id={} amount={} {}'.format(
        status,
        order.id,
        data['amount'],
        data['currency']
    ))

    result_received.send(
        sender=order,
        order_id=order.id,
        amount=data['amount'],
        currency=data['currency'],
    )

    return HttpResponse('OK', status=200)
