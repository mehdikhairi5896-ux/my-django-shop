from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

STATUS_CHOICES = [
    ('pending', 'در انتظار بررسی'),
    ('processing', 'در حال آماده‌سازی'),
    ('shipped', 'ارسال شده'),
    ('delivered', 'تحویل شده'),
]

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def total_price(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.product.price * item.quantity
        return total

    def total_items(self):
        return sum(item.quantity for item in self.orderitem_set.all()) 

    def __str__(self):
        return f"سفارش {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

class OrderPayment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("success", "پرداخت موفق"),
        ("failed", "پرداخت ناموفق"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.PositiveIntegerField()

    authority = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    ref_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"سفارش {self.order.id} - {self.amount}"
