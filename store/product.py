from django.db import models
from .category import Catogary

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Catogary,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='img')
    desc=models.TextField()
    price=models.IntegerField()

    def __str__(self):
        return self.name