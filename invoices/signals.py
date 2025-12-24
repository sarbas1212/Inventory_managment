from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvoiceItem, Invoice

from customers.models import Customer
from products.models import Product

@receiver(post_save, sender=InvoiceItem)
def reduce_stock_on_invoice(sender, instance, created, **kwargs):
    if not created:
        return


    product = instance.product
    product.stock_quantity -= instance.quantity
    product.save()


@receiver(post_save, sender=Invoice)
def update_customer_balance(sender, instance, created, **kwargs):
    if not created:
        return

    customer = instance.customer
    customer.opening_balance += instance.total_amount
    customer.save()
