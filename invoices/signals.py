from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvoiceItem, Invoice

from customers.models import Customer
from products.models import Product
from django.db.models import F
from common.models import AuditLog

@receiver(post_save, sender=InvoiceItem)
def reduce_stock_on_invoice(sender, instance, created, **kwargs):
    if not created:
        return

    Product.objects.filter(id=instance.product.id).update(
        stock_quantity=F("stock_quantity") - instance.quantity
    )
    
    AuditLog.objects.create(
        user=None,  # or pass request.user via threadlocal if needed
        action="Stock Reduced",
        model_name="Product",
        object_id=instance.product.id,
        extra_data={"quantity_reduced": instance.quantity}
    )


@receiver(post_save, sender=Invoice)
def update_customer_balance(sender, instance, created, **kwargs):
    if not created:
        return

    Customer.objects.filter(id=instance.customer.id).update(
        opening_balance=F("opening_balance") + instance.total_amount
    )