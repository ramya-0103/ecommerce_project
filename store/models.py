# store/models.py
from django.db import models
from django.contrib.auth.models import User

# 1. Product Model (The item for sale)
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True) # Used for clean URLs

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        # Handles case where image might be missing
        try:
            url = self.image.url
        except:
            url = ''
        return url

# 2. Order/Cart Model (The transaction wrapper)
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) # False = Cart, True = Completed Order

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.filter(product__isnull=False)
        return sum(item.get_total for item in orderitems)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum(item.quantity for item in orderitems)

# 3. Order Item Model (A specific product within an order/cart)
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        if self.product:  # ensure product exists
            return self.product.price * self.quantity
        return 0


# 4. Shipping Address Model (Required for checkout)
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address