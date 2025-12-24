from django.urls import path
from .views import PaymentCreateAPIView

urlpatterns = [
    path("create/", PaymentCreateAPIView.as_view(), name="payment-create"),
]