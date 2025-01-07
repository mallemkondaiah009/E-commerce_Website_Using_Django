from django.shortcuts import render

# Create your views here.
# payments/views.py
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from store.product import Product


def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order = client.order.create({
        "amount": int(product.price * 100),  # Convert to paisa
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save payment in database
    payment = Payment(
        order_id=order['id'],
        amount=product.price,
        status='created'
    )
    payment.save()

    context = {
        "product": product,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": order['id'],
    }
    return render(request, "payments/checkout.html", context)


def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')

    try:
        payment = Payment.objects.get(order_id=order_id)
        payment.payment_id = payment_id
        payment.status = "success"
        payment.save()
        return render(request, "payments/success.html", {"payment": payment})
    except Payment.DoesNotExist:
        return render(request, "error.html", {"message": "Payment not found!"})
