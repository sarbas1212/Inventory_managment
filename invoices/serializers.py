from rest_framework import serializers
from customers.models import Customer
from products.models import Product
from .models import Invoice

class InvoiceItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)

class InvoiceCreateSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )
    items = InvoiceItemInputSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item required")
        return items




class InvoiceListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name')

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'customer_name', 'total_amount', 'created_at']
