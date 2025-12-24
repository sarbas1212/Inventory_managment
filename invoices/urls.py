from django.urls import path
from .views import InvoiceCreateAPIView

urlpatterns = [
    path("create/", InvoiceCreateAPIView.as_view(), name="invoice-create"),
]
