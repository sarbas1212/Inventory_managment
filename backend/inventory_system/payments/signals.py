from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def reduce_customer_balance_on_payment(sender, instance, created, **kwargs):
    if not created:
        return

    customer = instance.invoice.customer
    customer.opening_balance -= instance.amount_paid
    customer.save()
