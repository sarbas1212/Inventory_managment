from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name