from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decimal import Decimal


class Product(models.Model):
    """
    Stores a single product entry.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Stores a single review entry related to :model:`auth.User`
    and :model:`item.Product`.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Review for {self.product.title} by {self.author.username}"


class Order(models.Model):
    """
    Stores an order for click and collect.
    """
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready', 'Ready for Collection'),
        ('collected', 'Collected'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

    def update_total(self):
        self.total = sum(item.subtotal for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    """
    Stores items within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in order {self.order.id}"

    @property
    def subtotal(self):
        return Decimal(self.price_at_order) * self.quantity


class Cart(models.Model):
    """
    Stores the current cart for a user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """
    Stores items in the cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in cart for {self.cart.user.username}"

    @property
    def subtotal(self):
        return Decimal(self.product.price) * self.quantity
