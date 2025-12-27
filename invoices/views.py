from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .services.invoice_service import InvoiceService
from .models import Invoice
from .serializers import InvoiceCreateSerializer,InvoiceListSerializer

import os
from rest_framework.response import Response
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .utils import generate_invoice_pdf
from common.permissions import IsAdmin, IsStaff
from common.pagination import CustomLimitOffsetPagination

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

class InvoiceCreateAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsAdmin | IsStaff]

    def post(self, request):
        serializer = InvoiceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = InvoiceService.create_invoice(
            customer=serializer.validated_data["customer"],
            items=serializer.validated_data["items"],
        )

        return Response(
            {
                "message": "Invoice created successfully",
                "invoice_id": invoice.id,
                "total": invoice.total_amount,
            },
            status=201,
        )

class InvoiceListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomLimitOffsetPagination
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['customer__id', 'created_at']
    search_fields = ['invoice_number', 'customer__name']

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
