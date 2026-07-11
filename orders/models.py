from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('done', 'تحویل داده شده'),
    ]
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='orders_app_orders'
)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
