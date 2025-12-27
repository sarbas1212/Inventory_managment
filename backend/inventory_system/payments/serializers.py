from rest_framework import serializers
from decimal import Decimal
from .models import Payment
from invoices.models import Invoice
from django.db import models

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("invoice", "amount_paid", "payment_method")

    def validate(self, data):
        invoice = data["invoice"]
        amount = data["amount_paid"]

        # Total already paid
        total_paid = invoice.payments.aggregate(
            total=models.Sum("amount_paid")
        )["total"] or Decimal("0.00")

        outstanding = invoice.total_amount - total_paid

        if amount <= 0:
            raise serializers.ValidationError(
                "Payment amount must be greater than zero"
            )

        if amount > outstanding:
            raise serializers.ValidationError(
                "Payment exceeds outstanding invoice amount"
            )

        return data
