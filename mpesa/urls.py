from django.urls import path
from .views import stk_push
from .callbacks import mpesa_callback

urlpatterns = [
    path("stkpush/", stk_push, name="stk_push"),
    path("callback/", mpesa_callback, name="mpesa_callback"),
]
