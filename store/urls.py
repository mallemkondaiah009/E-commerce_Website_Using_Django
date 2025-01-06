from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('profile/',views.profile,name='profile'),
    path('forgot_password/',views.forgot_pass_view,name='forgot_password'),
    path('', RedirectView.as_view(url='/home/', permanent=True), name='root'),

]

