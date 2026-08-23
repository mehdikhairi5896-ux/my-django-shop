from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Advertisement(models.Model):
    DURATION_CHOICES = [
        (7, "۷ روز"),
        (30, "۳۰ روز"),
        (90, "۹۰ روز"),
    ]

    duration = models.IntegerField(
        choices=DURATION_CHOICES,
        default=30
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    city = models.CharField(max_length=100)

    image = models.ImageField(upload_to="ads/")

    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))

                buffer = BytesIO()

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img.save(
                    buffer,
                    format="JPEG",
                    quality=70
                )

                filename = self.image.name.split("/")[-1]
                self.image.name = filename

                self.image.save(
                    filename,
                    ContentFile(buffer.getvalue()),
                    save=False
                )

                super().save(update_fields=["image"])

    def get_price(self):
        return self.price

    def __str__(self):
        return self.title


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("success", "پرداخت موفق"),
        ("failed", "پرداخت ناموفق"),
    ]

    advertisement = models.ForeignKey(
        Advertisement,
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
        return f"{self.advertisement.title} - {self.amount}"
