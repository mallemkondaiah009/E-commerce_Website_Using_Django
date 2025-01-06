from http import client
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .product import Product
from .models import UserRegistration
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserRegistration  # Your custom user model
from django.contrib.auth.hashers import check_password  # For password validation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import UserRegistration
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import UserRegistration




def home(request):
    # Get the search query from the URL parameter (if it exists)
    query = request.GET.get('query', '').strip()  # Default to empty string if no query
    if query:
        # Filter products by name, using case-insensitive matching
        products = Product.objects.filter(name__icontains=query)
    else:
        # If no query, show all products
        products = Product.objects.all()

    # Pass the products and query to the template
    return render(request, 'store/home.html', {'products': products, 'query': query})




def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Input validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "store/register.html")

        if UserRegistration.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "store/register.html")

        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "store/register.html")

        # Creating the user
        try:
            user = UserRegistration.objects.create(
                username=username,
                email=email,
                gender=gender,
                password=make_password(password),
            )
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")  # Redirect to login page
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {e}")
            return render(request, "store/register.html")

    return render(request, "store/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Fetch user from the database
        try:
            user = UserRegistration.objects.get(username=username)
        except UserRegistration.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, "store/login.html")

        # Validate password
        if not check_password(password, user.password):
            messages.error(request, "Invalid username or password.")
            return render(request, "store/login.html")

        # Set user session (or redirect to a dashboard/homepage)
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        messages.success(request, f"Welcome, {user.username}!")
        return redirect("home")  # Replace "home" with the name of your home page URL

    return render(request, "store/login.html")


def logout_view(request):
    if 'user_id' in request.session:
        request.session.flush()  # Clears the session data
    return redirect('login')  # Redirect to login page after logout



def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)  # Fetch the full product object
        total_price += float(item['price']) * item['quantity']
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': float(item['price']) * item['quantity'],
            'image': product.image.url  # Include image URL
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product  # Import your Product model

@csrf_exempt  # Temporarily disable CSRF for testing (use proper CSRF handling in production)
def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Retrieve the cart from the session, or initialize it if not present
        cart = request.session.get('cart', {})

        # Get the product from the database
        product = get_object_or_404(Product, id=product_id)

        # If the product is already in the cart, increase its quantity
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            # Add the product to the cart, including the image URL
            cart[str(product_id)] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
                'image': product.image.url if product.image else '',  # Add the image URL here
            }

        # Save the cart back to the session
        request.session['cart'] = cart

        # Return a JSON response indicating success
        return JsonResponse({
            'status': 'success',
            'message': 'Product added to cart!',
            'cart': cart,  # Optionally return the updated cart data
        })
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method.',
        }, status=400)



def remove_from_cart(request, item_id):
    # Assuming you have a Cart model or session-based cart logic
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart successfully.")
    else:
        messages.error(request, "Item not found in cart.")
    return redirect('cart')  # Redirect to the cart page


def checkout(request, product_id):
    product = Product.objects.get(id=product_id)  # Fetch product from the database
    return render(request, 'store/checkout.html', {'product': product})


from django.shortcuts import render, redirect, get_object_or_404
from .product import Product
from .models import UserRegistration,Order

def confirm_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Get quantity from POST data, default to 1
        product = get_object_or_404(Product, id=product_id)
        
        # Assuming you have the currently logged-in user in the session
        user_id = request.session.get('user_id')  # Replace with your authentication logic
        user = get_object_or_404(UserRegistration, id=user_id)

        # Calculate total price
        total_price = product.price * quantity

        # Save order in the database
        order = Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        order.save()

        # Render success page
        return render(request, 'store/order_success.html', {'product': product, 'order': order})
    
    return redirect('home')  # Redirect to the home page for non-POST requests


def profile(request):
    if 'username' in request.session:
        user = get_object_or_404(UserRegistration, username=request.session['username'])
        orders = Order.objects.filter(user=user)  # Fetch orders for the logged-in user
        return render(request, 'store/profile.html', {'user': user, 'orders': orders})
    else:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')




def forgot_pass_view(request):
    return render(request, 'store/forgot_password.html')

