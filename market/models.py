from django.db import models
from django.contrib.auth.models import User


class MarketItem(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="market_items"
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.PositiveIntegerField()

    city = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="market/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class MarketOrder(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="market_orders"
    )

    item = models.ForeignKey(
        MarketItem,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    price = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    def __str__(self):
        return f"سفارش بازار {self.id}"
