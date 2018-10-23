from copy import deepcopy

from django import forms
from django.urls import reverse
from liqpay import LiqPay

from . import constants, settings


def get_html_form(amount, order_id):
    liq = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    html = liq.cnb_form({
        'action': 'pay',
        'amount': str(amount),
        'currency': 'UAH',
        'order_id': str(order_id),
        'description': 'TODO: write description',
        'version': '3',
        'result_url': '',
        'sandbox': '',
        'server_url': '',
    })
    return html


class CallbackForm(forms.Form):
    data = forms.CharField(widget=forms.HiddenInput)
    signature = forms.CharField(widget=forms.HiddenInput)


class CheckoutForm(CallbackForm):
    method = 'POST'

    def __init__(self, params, *args, **kwargs):
        self.params = {} if params is None else deepcopy(params)
        self.liqpay = LiqPay(settings.PUBLIC_KEY, settings.PRIVATE_KEY)
        self.params.update(
            server_url=reverse('djliqpay-callback'),
            version=constants.API_VERSION,
            sandbox=str(
                int(bool(params.get('sandbox', settings.LIQPAY_SANDBOX)))),
        )
        initial = {
            'data': self.liqpay.cnb_data(self.params),
            'signature': self.liqpay.cnb_signature(self.params),
        }
        super().__init__(initial=initial, *args, **kwargs)
