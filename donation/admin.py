from django.contrib import admin
from django.db.models import Sum
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    
    list_display = (
    "id",
    "donor_name",
    "amount",
    "created_at",
)

    ordering = (
        "-created_at",
    )

    def changelist_view(self, request, extra_context=None):
        total = Donation.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0

        extra_context = extra_context or {}
        extra_context["total_donation"] = total

        return super().changelist_view(
            request,
            extra_context=extra_context
        )
