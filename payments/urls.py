# payments/urls.py
from django.urls import path
from payments import views

urlpatterns = [
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
]
