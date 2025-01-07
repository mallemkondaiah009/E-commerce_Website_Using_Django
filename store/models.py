from django.db import models
from django.db import models
#from .models import UserRegistration
from .product import Product

class UserRegistration(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

from django.db import models
#from .models import UserRegistration
from .product import Product

class Order(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} - {self.product.name}"





