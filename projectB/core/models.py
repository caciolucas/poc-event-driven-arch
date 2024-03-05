from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    sku = models.CharField(max_length=255)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} - R$ {self.price} - {self.store.name}"

class Store(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255)

    def __str__(self):
        return self.name