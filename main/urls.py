from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),    
    path("payment/", order_payment, name="payment"),
    path("success/", callback, name="callback"),
]
