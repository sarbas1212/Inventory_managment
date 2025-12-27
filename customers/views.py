from django.shortcuts import render

# Create your views here.
from .models import Customer
from . serializers import CustomerSerializer
from rest_framework import authentication

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from common.pagination import CustomLimitOffsetPagination



class CustomerListAPIView(ListAPIView):
    permission_classes=[IsAuthenticated]
    pagination_class=CustomLimitOffsetPagination
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


   