from django.db import models


class LiqPayOrder(models.Model):

    created = models.DateTimeField(auto_now=True)
    order_id = models.CharField(unique=True, editable=False, max_length=255)

    def __str__(self):
        return 'LiqPay payment (orderId: {})'.format(self.order_id)
