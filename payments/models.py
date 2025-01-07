from django.db import models

# Create your models here.
class Payment(models.Model):
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=256, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id