from django.db import transaction
from decimal import Decimal

from invoices.models import Invoice, InvoiceItem
from products.models import Product
from customers.models import Customer

class InvoiceService:

    @staticmethod
    @transaction.atomic
    def create_invoice(*, customer, items):
        subtotal = Decimal("0.00")

        invoice = Invoice.objects.create(
            customer=customer,
            subtotal=Decimal("0.00"),
            tax_amount=Decimal("0.00"),
            total_amount=Decimal("0.00"),
        )

        for item in items:
            product = item["product"]  # ✅ FIX HERE

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

        return invoice