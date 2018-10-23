from django.dispatch import Signal

result_received = Signal(providing_args=[
    'order_id',
    'amount',
    'currency',
])
