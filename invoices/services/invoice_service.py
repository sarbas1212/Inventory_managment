from django.db import transaction
from decimal import Decimal
from rest_framework.exceptions import ValidationError

from invoices.models import Invoice, InvoiceItem
import logging
logger = logging.getLogger("invoices")


class InvoiceService:

    @staticmethod
    def validate_stock(items):
        for item in items:
            product = item["product"]
            quantity = item["quantity"]

            if product.stock_quantity < quantity:
                raise ValidationError({
                    "stock": f"Insufficient stock for {product.name}"
                })

    @staticmethod
    @transaction.atomic
    def create_invoice(*, customer, items):
        logger.info(f"Creating invoice for customer {customer.id} with {len(items)} items")
        # ✅ VALIDATE FIRST
        InvoiceService.validate_stock(items)

        subtotal = Decimal("0.00")

        invoice = Invoice.objects.create(
            customer=customer,
            subtotal=Decimal("0.00"),
            tax_amount=Decimal("0.00"),
            total_amount=Decimal("0.00"),
        )

        for item in items:
            product = item["product"]
            quantity = item["quantity"]
            price = product.price
            total = price * quantity

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                price=price,
                total=total,
            )

            subtotal += total

        tax = subtotal * Decimal("0.18")
        total_amount = subtotal + tax

        invoice.subtotal = subtotal
        invoice.tax_amount = tax
        invoice.total_amount = total_amount
        invoice.save(update_fields=["subtotal", "tax_amount", "total_amount"])

        logger.info(f"Invoice {invoice.id} created successfully with total {invoice.total_amount}")
        return invoice
