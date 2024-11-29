from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default=' Product')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
