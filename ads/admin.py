from django.contrib import admin

from .models import Advertisement, Payment


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "city",
        "owner",
        "paid",
        "approved",
        "created_at",
    )

    search_fields = (
        "title",
        "city",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "advertisement",
        "user",
        "amount",
        "status",
        "authority",
        "ref_id",
        "created_at",
        "paid_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "advertisement__title",
        "user__username",
        "authority",
        "ref_id",
    )

    ordering = (
        "-created_at",
    )
