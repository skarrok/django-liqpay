from django.urls import path
from . import views

app_name = 'djliqpay'

urlpatterns = [
    path('callback/', views.liqpay_callback, name='callback'),
]
