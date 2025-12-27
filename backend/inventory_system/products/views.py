from django.shortcuts import render

# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from common.pagination import CustomLimitOffsetPagination

# Your app imports
from products.models import Product
from .serializers import ProductSerializer

class ProductListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    pagination_class=CustomLimitOffsetPagination
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
