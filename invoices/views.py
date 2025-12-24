from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceCreateSerializer

class InvoiceCreateAPIView(CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceCreateSerializer
    permission_classes = [IsAuthenticated]