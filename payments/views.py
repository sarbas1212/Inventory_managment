from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentCreateSerializer,PaymentListSerializer
from common.permissions import IsAdmin, IsStaff
from common.pagination import CustomLimitOffsetPagination

class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsStaff]



class PaymentListAPIView(ListAPIView):
    queryset=Payment.objects.all()
    serializer_class=PaymentListSerializer
    permission_classes=[IsAuthenticated]
    pagination_class=CustomLimitOffsetPagination
