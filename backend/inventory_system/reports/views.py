from django.shortcuts import render

# Create your views here.
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from invoices.models import Invoice
from customers.models import Customer
from products.models import Product
from common.permissions import IsAdmin, IsStaff
from common.pagination import CustomLimitOffsetPagination

class SalesReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsStaff]
    def get(self, request):
        report = (
            Invoice.objects
            .values("created_at__date")
            .annotate(total_sales=Sum("total_amount"))
            .order_by("created_at__date")
        )

        return Response(report)


class OutstandingReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsStaff]

    def get(self, request):
        customers = (
            Customer.objects
            .filter(opening_balance__gt=0)
            .values("id", "name", "opening_balance")
            .order_by("-opening_balance")
        )

        return Response(customers)
    

class StockReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsStaff]

    def get(self, request):
        threshold = int(request.GET.get("threshold", 5))

        products = (
            Product.objects
            .filter(stock_quantity__lte=threshold)
            .values("id", "name", "stock_quantity")
            .order_by("stock_quantity")
        )

        return Response(products)