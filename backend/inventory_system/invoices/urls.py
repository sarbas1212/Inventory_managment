from django.urls import path
from .views import InvoiceCreateAPIView, InvoiceListAPIView, InvoicePDFAPIView

urlpatterns = [
    path("create/", InvoiceCreateAPIView.as_view(), name="invoice-create"),
    path("<int:invoice_id>/pdf/", InvoicePDFAPIView.as_view(), name="invoice-pdf"),
    path("", InvoiceListAPIView.as_view(), name="invoice-list"),
]
