from django.urls import path
from .views import PaymentCreateAPIView,PaymentListAPIView

urlpatterns = [
    path("create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("", PaymentListAPIView.as_view(), name="payment-list"),
]