# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Storefront pages
    path('', views.store, name="store"),
    path('product/<slug:slug>/', views.view_product, name="product_detail"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    
    # Order History Page (Bonus feature made mandatory)
    path('orders/', views.order_history, name="order_history"),

    # AJAX logic endpoint for updating cart (requires login)
    path('update_item/', views.updateItem, name="update_item"),
    
    # Logic to process the checkout form submission
    path('process_order/', views.processOrder, name="process_order"),
    path('register/', views.register, name='register'),
    
]