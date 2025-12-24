from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from customers.models import Customer
from products.models import Product
from .models import Invoice, InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ("product", "quantity")

class InvoiceCreateSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ("customer", "items")

    def validate(self, data):
        customer = data["customer"]
        items = data["items"]

        total_amount = Decimal("0.00")

        for item in items:
            product = item["product"]
            qty = item["quantity"]

            # ✔ Stock availability check
            if product.stock_quantity < qty:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}"
                )

            line_total = product.price * qty
            tax = (line_total * product.tax_percentage) / 100
            total_amount += line_total + tax

        # ✔ Credit limit check
        if customer.opening_balance + total_amount > customer.credit_limit:
            raise serializers.ValidationError(
                "Customer credit limit exceeded"
            )

        return data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        customer = validated_data["customer"]

        subtotal = Decimal("0.00")
        tax_amount = Decimal("0.00")

        # ✔ Calculate totals
        for item in items_data:
            product = item["product"]
            qty = item["quantity"]

            line_total = product.price * qty
            tax = (line_total * product.tax_percentage) / 100

            subtotal += line_total
            tax_amount += tax

        total_amount = subtotal + tax_amount

        # ✔ Create invoice (NO side-effects)
        invoice = Invoice.objects.create(
            customer=customer,
            invoice_number=f"INV-{Invoice.objects.count() + 1}",
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
        )

        # ✔ Create invoice items (signals will handle stock & balance)
        for item in items_data:
            product = item["product"]
            qty = item["quantity"]

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=product.price,
                total=product.price * qty,
            )

        return invoice

