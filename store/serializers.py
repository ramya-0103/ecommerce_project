# store/serializers.py

from rest_framework import serializers
from .models import Product, Order, OrderItem
# Assuming your User model is the default Django one
from django.contrib.auth.models import User 

class ProductSerializer(serializers.ModelSerializer):
    imageURL = serializers.ReadOnlyField() 
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    get_total = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'get_total', 'date_added']

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True) 
    get_cart_total = serializers.ReadOnlyField()
    get_cart_items = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'date_ordered', 'complete', 'get_cart_total', 'get_cart_items', 'orderitem_set']
        read_only_fields = ['customer']