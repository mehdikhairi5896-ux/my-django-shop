from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Donation
from .forms import DonationForm
from django.db.models import Sum

def donation_home(request):

    if request.method == "POST":
        form = DonationForm(request.POST)

        if form.is_valid():
            donation = form.save(commit=False)

            if request.user.is_authenticated:
                donation.user = request.user

            donation.save()

            return redirect("home")

    else:
        form = DonationForm()


    total = Donation.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0


    return render(
    request,
    "donation/home.html",
    {
        "total": intcomma(total),
        "form": form,
    }

    )

def donation_total_api(request):
    total = Donation.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return JsonResponse({
        "total": total
    })
