# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, ShippingAddress
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
# --- NEW DRF IMPORTS ---
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, OrderSerializer
# -------------------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/templates/registration/register.html', {'form': form})

# Helper function to consolidate cart data logic (UNCHANGED)
def cartData(request):
    """Fetches cart details for both logged-in and anonymous users (simplified for this task)."""
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
    return {'cartItems': cartItems, 'order': order, 'items': items}


# ==========================================================
# 🥇 DRF API VIEWSETS (For Frontend/Mobile App JSON Access)
# ==========================================================

# 1. Public Product API (Read-Only)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to list and retrieve products."""
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    # Overriding global permission: ANYONE can view products
    permission_classes = [AllowAny] 

# 2. Protected Order/Cart API
class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint for authenticated users to manage their carts/orders."""
    # Uses the global default: permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        """ Filters data to show only the current user's carts/orders. """
        if self.request.user.is_authenticated:
            # Filters the orders based on the token-authenticated user
            return Order.objects.filter(customer=self.request.user).order_by('-date_ordered')
        return Order.objects.none()

    def perform_create(self, serializer):
        """ Associates a new order with the authenticated user on creation. """
        serializer.save(customer=self.request.user)


# ==========================================================
# 🥈 TRADITIONAL DJANGO VIEWS (For Template Rendering/Standard Forms)
# ==========================================================

# 1. Product List Page (store.html)
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('store')

@login_required(login_url='login')
def store(request):
    data = cartData(request)
    products = Product.objects.all()
    context = {'products': products, 'cartItems': data['cartItems']}
    return render(request, 'store/store.html', context)


# 2. Product Detail Page (product_detail.html)
def view_product(request, slug):
    data = cartData(request)
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product, 'cartItems': data['cartItems']}
    return render(request, 'store/product_detail.html', context)



# 3. Cart Page (cart.html)
def cart(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/cart.html', context)


# 4. Checkout Page (checkout.html)
@login_required(login_url='login') 
def checkout(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/checkout.html', context)


# 5. AJAX Endpoint to Update Cart (Logic) - UNCHANGED
def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'User not logged in'}, status=401)
        
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    updated_cart_items = order.get_cart_items
    return JsonResponse({'message': 'Item updated successfully', 'cartItems': updated_cart_items}, safe=False)


# 6. Process Order (Checkout Logic) - UNCHANGED
@login_required(login_url='login')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    customer = request.user
    order = Order.objects.get(customer=customer, complete=False)

    # Save Shipping Information
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )
    
    # Mark Order as Complete
    order.complete = True
    order.transaction_id = transaction_id
    order.save()

    return JsonResponse('Payment complete!', safe=False)

# 7. Order History Page (Mandatory Bonus Feature) - UNCHANGED
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(customer=request.user, complete=True).order_by('-date_ordered')
    
    data = cartData(request)
    context = {'orders': orders, 'cartItems': data['cartItems']}
    return render(request, 'store/order_history.html', context)
