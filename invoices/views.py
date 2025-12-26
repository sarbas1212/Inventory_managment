from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceCreateSerializer

import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .utils import generate_invoice_pdf

class InvoiceCreateAPIView(CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceCreateSerializer
    permission_classes = [IsAuthenticated]





class InvoicePDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise Http404("Invoice not found")

        pdf_dir = os.path.join(settings.BASE_DIR, "media", "invoices")
        os.makedirs(pdf_dir, exist_ok=True)

        file_path = os.path.join(
            pdf_dir, f"invoice_{invoice.invoice_number}.pdf"
        )

        generate_invoice_pdf(invoice, file_path)

        return FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf",
            filename=f"invoice_{invoice.invoice_number}.pdf",
        )
