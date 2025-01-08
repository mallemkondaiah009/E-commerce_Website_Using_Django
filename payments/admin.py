from django.contrib import admin
from .models import Payment

# Register your models here.
class PaymentInfo(admin.ModelAdmin):
    list_display = ['user','product_name','order_id', 'amount', 'status','created_at']    

admin.site.register(Payment, PaymentInfo)