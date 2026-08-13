from django.shortcuts import render
from shop.models import Advertisement
from donation.models import Donation
from django.db.models import Sum

def home(request):
    ad = Advertisement.objects.first()

    donation_total = Donation.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    donations = Donation.objects.all().order_by("-id")[:10]

    return render(request, "index.html", {
    "donation_total": donation_total,
    "donations": donations,
})
