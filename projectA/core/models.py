from django.db import models
from django.db.models.signals import post_save

from core.decorators import retail_notify_changes

# Create your models here.

@retail_notify_changes
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    sku = models.CharField(max_length=255)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} - R$ {self.price} - {self.store.name}"

@retail_notify_changes
class Store(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255)

    def __str__(self):
        return self.name


