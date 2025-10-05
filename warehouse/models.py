from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=0)  

    def clean(self):
        if self.stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")

    def __str__(self):
        return self.name