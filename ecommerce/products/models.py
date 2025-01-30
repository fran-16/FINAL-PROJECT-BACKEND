from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="General")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.URLField(null=True, blank=True)  # Permitir nulo y vacío para imagen
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
