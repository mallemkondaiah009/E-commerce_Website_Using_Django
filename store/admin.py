from django.contrib import admin
from .product import Product
from .category import Catogary
from .models import Order, UserRegistration

# Register your models here.
class Categoryinfo(admin.ModelAdmin):
    list_display=['name']

class Productinfo(admin.ModelAdmin):
    list_display=['name','category','price']


admin.site.register(Product,Productinfo)
admin.site.register(Catogary,Categoryinfo)

#userregistration
class UserRegistraionInfo(admin.ModelAdmin):
    list_display=['username','email','gender']
admin.site.register(UserRegistration,UserRegistraionInfo)


class OrderInfo(admin.ModelAdmin):
    list_display=['user','product','quantity','total_price','order_date']

admin.site.register(Order,OrderInfo)
