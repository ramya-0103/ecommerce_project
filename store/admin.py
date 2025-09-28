# store/admin.py
from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)