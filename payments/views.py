from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentCreateSerializer

class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]
