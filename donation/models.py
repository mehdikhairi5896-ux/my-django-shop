from django.db import models
from django.contrib.auth.models import User


class Donation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    donor_name = models.CharField(
    max_length=100,
    blank=True,
    verbose_name="نام کمک‌کننده"
)

    amount = models.PositiveIntegerField(
        verbose_name="مبلغ کمک"
    )

    description = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.amount} تومان"
