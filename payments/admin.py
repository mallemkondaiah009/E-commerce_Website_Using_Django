from django.contrib import admin
from .models import Payment

# Register your models here.
class PaymentInfo(admin.ModelAdmin):
    list_display = ['order_id', 'amount', 'status']    

admin.site.register(Payment, PaymentInfo)