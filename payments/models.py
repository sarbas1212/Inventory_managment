from django.db import models

from invoices.models import Invoice

class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="payments", on_delete=models.CASCADE
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.amount_paid} for {self.invoice.invoice_number}"  