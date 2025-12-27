from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .services.invoice_service import InvoiceService
from .models import Invoice
from .serializers import InvoiceCreateSerializer,InvoiceListSerializer
from io import BytesIO
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
from common.responses import success_response
from common.models import AuditLog

class InvoiceCreateAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsAdmin | IsStaff]

    def post(self, request):
        serializer = InvoiceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = InvoiceService.create_invoice(
            customer=serializer.validated_data["customer"],
            items=serializer.validated_data["items"],
        )

        AuditLog.objects.create(
            user=request.user,
            action="Created Invoice",
            model_name="Invoice",
            object_id=invoice.id,
            extra_data={
                "items_count": len(serializer.validated_data["items"]),
                "total_amount": str(invoice.total_amount)
            }
        )

        return success_response(
            message="Invoice created successfully",
            data={"invoice_id": invoice.id},
            status_code=201,
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

        file_dir = os.path.join("invoices", "pdfs")
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, f"Invoice_{invoice.invoice_number}.pdf")

        generate_invoice_pdf(invoice, file_path)

        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=f"Invoice_{invoice.invoice_number}.pdf")
